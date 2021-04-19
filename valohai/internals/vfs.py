import os
import shutil
import tempfile
from contextlib import ExitStack
from tarfile import TarFile, TarInfo
from typing import IO, List, Optional, Union
from zipfile import ZipFile, ZipInfo


class File:
    parent_file: Optional["File"] = None

    def open(self) -> IO[bytes]:
        raise NotImplementedError("...")

    def read(self) -> bytes:
        with self.open() as f:
            return f.read()

    def __repr__(self):
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
    dir_entry: Optional[os.DirEntry]

    def __init__(
        self, name: str, path: str, dir_entry: Optional[os.DirEntry] = None
    ) -> None:
        self._name = name
        self.path = path
        self.dir_entry = dir_entry

    def open(self) -> IO[bytes]:
        return open(self.path, "rb")  # noqa: SIM115

    @property
    def name(self) -> str:
        return self._name


class FileInContainer(File):
    _concrete_path: Optional[str] = None

    def open_concrete(self, delete: bool = True) -> IO[bytes]:
        if self._concrete_path and os.path.isfile(self._concrete_path):
            return open(self._concrete_path, "rb")  # noqa: SIM115
        tf = tempfile.NamedTemporaryFile(suffix=self.extension, delete=delete)
        self.extract(tf)
        tf.seek(0)
        self._concrete_path = tf.name
        return tf

    def extract(self, destination: Union[str, IO]) -> None:
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

    def _do_extract(self, destination: IO) -> None:
        # if a file has a better idea how to write itself into an IO, this is the place
        with self.open() as f:
            shutil.copyfileobj(f, destination)


class FileInZip(FileInContainer):
    parent_file: FileOnDisk
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
            os.path.dirname(self.parent_file.name), self.zipinfo.filename
        )

    @property
    def path(self) -> str:
        return os.path.join(
            os.path.dirname(self.parent_file.path), self.zipinfo.filename
        )


class FileInTar(FileInContainer):
    parent_file: FileOnDisk
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
        return os.path.join(os.path.dirname(self.parent_file.name), self.tarinfo.path)


def find_files_in_zip(vr: "VFS", df: FileOnDisk) -> None:
    zf = ZipFile(df.path)
    df.zipfile = zf  # type: ignore
    vr.exit_stack.callback(zf.close)
    vr.files.extend(
        [
            FileInZip(parent_file=df, zipfile=zf, zipinfo=zinfo)
            for zinfo in zf.infolist()
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

    def __exit__(self, *exc_details) -> None:
        self.exit_stack.__exit__(*exc_details)


def add_disk_file(
    vfs: VFS,
    name: str,
    path: str,
    dir_entry: Optional[os.DirEntry] = None,
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
    dent: os.DirEntry

    def _walk(path):
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
