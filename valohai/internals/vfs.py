import hashlib
import os
import re
import shutil
import tempfile
from contextlib import ExitStack
from tarfile import TarFile, TarInfo
from typing import IO, TYPE_CHECKING, List, Optional, Union
from zipfile import ZipFile, ZipInfo

if TYPE_CHECKING:
    DirEntry = os.DirEntry[str]


class File:
    parent_file: Optional["File"] = None

    def open(self) -> IO[bytes]:
        raise NotImplementedError("...")

    def read(self) -> bytes:
        with self.open() as f:
            return f.read()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"

    @property
    def name(self) -> str:
        raise NotImplementedError("...")

    @property
    def extension(self) -> str:
        return os.path.splitext(self.name)[1]


class FileOnDisk(File):
    _name: str
    path: str
    dir_entry: Optional["DirEntry"]

    def __init__(
        self, name: str, path: str, dir_entry: Optional["DirEntry"] = None
    ) -> None:
        self._name = name
        self.path = path
        self.dir_entry = dir_entry

    def open(self) -> IO[bytes]:
        return open(self.path, "rb")  # noqa: SIM115

    @property
    def name(self) -> str:
        return self._name

    @property
    def container_temp_root(self) -> str:
        path_hash = hashlib.sha1(self.path.encode("utf-8")).hexdigest()
        return os.path.join(tempfile.gettempdir(), f"vh-vfs-{path_hash}")


class FileInContainer(File):
    parent_file: FileOnDisk
    _concrete_path: Optional[str] = None

    def open_concrete(self, delete: bool = True) -> IO[bytes]:
        if self._concrete_path and os.path.isfile(self._concrete_path):
            return open(self._concrete_path, "rb")  # noqa: SIM115

        file_path = os.path.join(
            self.parent_file.container_temp_root, self.path_in_container
        )
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        tf = open(file_path, "wb")  # noqa: SIM115
        self.extract(tf)
        tf.seek(0)
        self._concrete_path = tf.name
        return tempfile._TemporaryFileWrapper(tf, tf.name, delete=delete)  # type: ignore

    def extract(self, destination: Union[str, IO[bytes]]) -> None:
        if isinstance(destination, str):
            destination = open(destination, "wb")  # noqa: SIM115
            should_close = True
        else:
            should_close = False
        try:
            self._do_extract(destination)
        finally:
            if should_close:
                destination.close()

    def _do_extract(self, destination: IO[bytes]) -> None:
        # if a file has a better idea how to write itself into an IO, this is the place
        with self.open() as f:
            shutil.copyfileobj(f, destination)

    @property
    def path_in_container(self) -> str:
        raise NotImplementedError(
            "FileInContainer subclass must implement path_in_container"
        )


class FileInZip(FileInContainer):
    zipfile: ZipFile
    zipinfo: ZipInfo

    def __init__(
        self, parent_file: FileOnDisk, zipfile: ZipFile, zipinfo: ZipInfo
    ) -> None:
        self.parent_file = parent_file
        self.zipfile = zipfile
        self.zipinfo = zipinfo

    def open(self) -> IO[bytes]:
        return self.zipfile.open(self.zipinfo, "r")

    @property
    def name(self) -> str:
        return os.path.join(
            os.path.dirname(self.parent_file.name), self.path_in_container
        )

    @property
    def path(self) -> str:
        return os.path.join(
            os.path.dirname(self.parent_file.path), self.path_in_container
        )

    @property
    def path_in_container(self) -> str:
        return self.zipinfo.filename


class FileInTar(FileInContainer):
    tarfile: TarFile
    tarinfo: TarInfo

    def __init__(
        self, parent_file: FileOnDisk, tarfile: TarFile, tarinfo: TarInfo
    ) -> None:
        self.parent_file = parent_file
        self.tarfile = tarfile
        self.tarinfo = tarinfo

    def open(self) -> IO[bytes]:
        fp = self.tarfile.extractfile(self.tarinfo)
        if not fp:
            raise ValueError(f"extractfile() returned None for {self.tarinfo}")
        return fp

    @property
    def name(self) -> str:
        return os.path.join(
            os.path.dirname(self.parent_file.name), self.path_in_container
        )

    @property
    def path_in_container(self) -> str:
        return self.tarinfo.path


def find_files_in_zip(vr: "VFS", df: FileOnDisk) -> None:
    zf = ZipFile(df.path)
    df.zipfile = zf  # type: ignore
    vr.exit_stack.callback(zf.close)
    vr.files.extend(
        [
            FileInZip(parent_file=df, zipfile=zf, zipinfo=zinfo)
            for zinfo in zf.infolist()
            if not zinfo.is_dir()
        ]
    )


def find_files_in_tar(vr: "VFS", df: FileOnDisk) -> None:
    tf = TarFile.open(df.path)
    df.tarfile = tf  # type: ignore
    vr.exit_stack.callback(tf.close)
    vr.files.extend(
        [
            FileInTar(parent_file=df, tarfile=tf, tarinfo=tinfo)
            for tinfo in tf.getmembers()
            if tinfo.isreg()
        ]
    )


class VFS:
    files: List[File]

    def __init__(self) -> None:
        self.files = []
        self.exit_stack = ExitStack()

    def __enter__(self) -> "VFS":
        return self

    def __exit__(self, *exc_details) -> None:  # type: ignore[no-untyped-def]
        self.exit_stack.__exit__(*exc_details)

    def filter(self, path: str) -> List[File]:
        pattern = re.compile(
            path.replace("**", "*").replace("*", ".*")
        )  # support for both * and ** notation
        return [f for f in self.files if re.match(pattern, f.name)]


def add_disk_file(
    vfs: VFS,
    name: str,
    path: str,
    dir_entry: Optional["DirEntry"] = None,
    process_archives: bool = False,
) -> None:
    disk_file = FileOnDisk(name=name, path=path, dir_entry=dir_entry)
    if process_archives:
        extension = disk_file.extension.lower()
        if extension == ".zip":
            find_files_in_zip(vfs, disk_file)
            return
        elif extension in (".tar", ".tar.gz", ".tar.bz2", ".tar.xz"):
            find_files_in_tar(vfs, disk_file)
            return
    vfs.files.append(disk_file)


def find_files(vfs: VFS, root: str, *, process_archives: bool) -> None:
    dent: "DirEntry"

    def _walk(path: str) -> None:
        for dent in os.scandir(path):
            if dent.is_dir():
                _walk(dent.path)
                continue
            if not dent.is_file():
                continue
            add_disk_file(
                vfs,
                name=os.path.relpath(dent.path, root),
                path=dent.path,
                dir_entry=dent,
                process_archives=process_archives,
            )

    _walk(root)
