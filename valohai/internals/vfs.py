import io
import os
import shutil
import tempfile
from contextlib import ExitStack
from tarfile import TarFile, TarInfo
from typing import IO, Optional, Union
from zipfile import ZipFile, ZipInfo


class File:
    parent_file: Optional["File"] = None

    def open(self) -> io.BufferedReader:
        raise NotImplementedError("...")

    def read(self):
        with self.open() as f:
            return f.read()

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.name}>'

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

    def __init__(self, name, path, dir_entry=None):
        self._name = name
        self.path = path
        self.dir_entry = dir_entry

    def open(self):
        return open(self.path, "rb")

    @property
    def name(self) -> str:
        return self._name


class FileInContainer(File):
    _concrete_path: Optional[str] = None

    def open_concrete(self, delete=True):
        if self._concrete_path and os.path.isfile(self._concrete_path):
            return open(self._concrete_path)
        tf = tempfile.NamedTemporaryFile(suffix=self.extension, delete=delete)
        self.extract(tf)
        tf.seek(0)
        self._concrete_path = tf.name
        return tf

    def extract(self, destination: Union[str, IO]):
        if isinstance(destination, str):
            destination = open(destination, "wb")
            should_close = True
        else:
            should_close = False
        try:
            self._do_extract(destination)
        finally:
            if should_close:
                destination.close()

    def _do_extract(self, destination: IO):
        # if a file has a better idea how to write itself into an IO, this is the place
        with self.open() as f:
            shutil.copyfileobj(f, destination)


class FileInZip(FileInContainer):
    zipfile: ZipFile
    zipinfo: ZipInfo

    def __init__(self, parent_file, zipfile, zipinfo):
        self.parent_file = parent_file
        self.zipfile = zipfile
        self.zipinfo = zipinfo

    def open(self):
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
    tarfile: TarFile
    tarinfo: TarInfo

    def __init__(self, parent_file, tarfile, tarinfo):
        self.parent_file = parent_file
        self.tarfile = tarfile
        self.tarinfo = tarinfo

    def open(self):
        return self.tarfile.extractfile(self.tarinfo)

    @property
    def name(self) -> str:
        return os.path.join(os.path.dirname(self.parent_file.name), self.tarinfo.path)


def find_files_in_zip(vr: "VFS", df: FileOnDisk) -> None:
    df.zipfile = zf = ZipFile(df.path)
    vr.exit_stack.callback(zf.close)
    vr.files.extend(
        [
            FileInZip(parent_file=df, zipfile=zf, zipinfo=zinfo)
            for zinfo in zf.infolist()
        ]
    )


def find_files_in_tar(vr: "VFS", df: FileOnDisk) -> None:
    df.tarfile = tf = TarFile.open(df.path)
    vr.exit_stack.callback(tf.close)
    vr.files.extend(
        [
            FileInTar(parent_file=df, tarfile=tf, tarinfo=tinfo)
            for tinfo in tf.getmembers()
            if tinfo.isreg()
        ]
    )


class VFS:
    def __init__(self):
        self.files = []
        self.exit_stack = ExitStack()

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.exit_stack.__exit__(*exc_details)


def add_disk_file(
    vfs: VFS,
    name: str,
    path: str,
    dir_entry: Optional[os.DirEntry] = None,
    process_archives=False,
):
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


def find_files(vfs: VFS, root: str, *, process_archives: bool):
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
