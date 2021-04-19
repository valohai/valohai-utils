import contextlib
import io
import os
import shutil
import tarfile
import threading
import zipfile
from mimetypes import guess_type
from typing import IO, Union

# A short and likely incomplete list of file extensions that are likely not to
# compress well or at all.
INCOMPRESSIBLE_SUFFIXES = {
    "avi",
    "bz2",
    "flac",
    "gif",
    "gz",
    "jpeg",
    "jpg",
    "mkv",
    "mp3",
    "mp4",
    "mpg",
    "npz",
    "ogg",
    "png",
    "rar",
    "tgz",
    "xz",
    "zip",
}


def guess_compressible(name: str) -> bool:
    """
    Guess whether a file with the given name is compressible.
    """
    suffix = os.path.splitext(name)[-1].lower()

    if suffix in INCOMPRESSIBLE_SUFFIXES:
        return False

    type, encoding = guess_type(name, strict=False)
    if encoding:  # Likely a compression
        return False

    if type and "compressed" in type:  # The mime type already says it's compressed
        return False

    return True  # Okay, give it a shot!


class BaseArchive:
    """
    Base class for writable archives with an unified signature for adding files.
    """

    def put(self, archive_name, source: Union[str, IO]):
        raise NotImplementedError("...")


class ZipArchive(BaseArchive, zipfile.ZipFile):
    _lock: threading.RLock  # This is actually defined in ZipFile...

    def __init__(self, file: str, mode: str = "r", *, compresslevel: int = 1) -> None:
        # Only Python 3.7+ has the compresslevel kwarg here
        super().__init__(file, mode, compression=zipfile.ZIP_STORED)
        self.compresslevel = compresslevel

    def writestream(
        self,
        arcname: str,
        data: Union[str, bytes, IO[bytes]],
        compress_type: int,
        compresslevel: int,
    ) -> None:
        # Like `writestr`, but also supports a stream (and doesn't support directories).
        zinfo = zipfile.ZipInfo(filename=arcname)
        zinfo.compress_type = compress_type
        if hasattr(zinfo, "_compresslevel"):  # only has an effect on Py3.7+
            zinfo._compresslevel = compresslevel  # type: ignore
        zinfo.external_attr = 0o600 << 16  # ?rw-------
        # this trusts `open` to fixup file_size.
        with self._lock, self.open(zinfo, mode="w") as dest:
            if isinstance(data, str):
                dest.write(data.encode("utf-8"))
            elif isinstance(data, bytes):
                dest.write(data)
            else:
                shutil.copyfileobj(data, dest, 524288)
        assert zinfo.file_size

    def put(self, archive_name: str, source: Union[str, IO]) -> None:
        compress_type = (
            zipfile.ZIP_DEFLATED
            if guess_compressible(archive_name)
            else zipfile.ZIP_STORED
        )
        with contextlib.ExitStack() as es:
            # Python 3.6's `zipfile` does not have `.compresslevel`,
            # so let's just always use our `writestream` instead...
            if isinstance(source, str):
                source = open(source, "rb")  # noqa: SIM115
                es.enter_context(source)
            self.writestream(
                arcname=archive_name,
                data=source,
                compress_type=compress_type,
                compresslevel=self.compresslevel,
            )


class TarArchive(BaseArchive, tarfile.TarFile):
    def put(self, archive_name: str, source: Union[str, IO]) -> None:
        with contextlib.ExitStack() as es:
            if isinstance(source, str):
                size = os.stat(source).st_size
                stream = open(source, "rb")  # noqa: SIM115
                es.callback(stream.close)
            else:
                # for TAR files we need to know the size of the data beforehand :(
                stream = io.BytesIO(source.read())
                size = len(stream.getbuffer())
            tarinfo = self.tarinfo()
            tarinfo.name = archive_name
            tarinfo.size = size
            self.addfile(tarinfo, stream)


def open_archive(path: str) -> BaseArchive:
    if path.endswith(".zip"):
        return ZipArchive(path, "w")
    elif path.endswith(".tar"):
        return TarArchive.open(path, "w")  # type: ignore
    elif path.endswith(".tgz") or path.endswith(".tar.gz"):
        return TarArchive.open(path, "w:gz")  # type: ignore

    raise ValueError(f"Unrecognized compression format for {path}")
