from typing import IO, Iterable, List, Optional

from valohai.internals.download_type import DownloadType
from .internals import vfs
from .internals.input_info import InputInfo


def inputs(name: str):
    return Input(name)


class Input:
    def __init__(self, name: str):
        self.name = name

    def paths(self, default: Optional[List[str]] = None, process_archives: bool = True, force_download: bool = False) -> Optional[List[str]]:
        """Get paths to all files for a given input name.

        Returns a list of file system paths for an input.
        If the input is not found in the cache, it is downloaded automatically.

        See streams() or path() for alternatives.

        :param default: Default fallback paths.
        :param process_archives: When facing an archive file, is it unpacked to several paths or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: List of file system paths for all the files for this input.
        """
        if default is None:
            default = []

        for file in self._get_input_vfs(process_archives=process_archives, force_download=force_download).files:
            if isinstance(file, vfs.FileInContainer):
                yield file.open_concrete(delete=False).name
            elif isinstance(file, vfs.FileOnDisk):
                yield file.path

        return default

    def path(self, default: Optional[str] = None, process_archives: bool = True, force_download: bool = False) -> Optional[str]:
        """Get path to a file for a given input name.

        Returns a file system path for an input.
        If the input contains multiple files, only the first one is returned.
        If the input is not found in the cache, it is downloaded automatically.

        See stream() or paths() for an alternative.

        :param process_archives: When facing an archive file, is it unpacked or returned as is
        :param default: Default fallback path.
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: File system path to a file for this input.
        """
        input_paths = self.paths(process_archives=process_archives, force_download=force_download)
        if input_paths:
            try:
                return next(input_paths)
            except StopIteration:
                return default
        return default

    def streams(self, process_archives: bool = True, force_download: bool = False) -> Iterable[IO]:
        """Get file streams to all files for a given input name.

        Returns an Iterable for all the file IO streams for an input.

        If the file(s) are not found in the cache, they are downloaded automatically.

        See stream() or paths() for an alternative.

        :param process_archives: When facing an archive file, is it unpacked or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: Iterable for all the IO streams of files for this input.
        """
        for file in self._get_input_vfs(process_archives=process_archives, force_download=force_download).files:
            yield file.open()
        return []

    def stream(self, process_archives: bool = True, force_download: bool = False) -> Optional[IO]:
        """Get file streams to a file for a given input name.

        Returns an IO stream to a file for this input.
        If the input contains multiple files, only the stream to the first one is returned.
        If the file(s) are not found in the cache, they are downloaded automatically.

        See path() or streams() for an alternative.

        :param process_archives: When facing an archive file, is it unpacked or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: IO stream to a file for this input.
        """

        streams = self.streams(process_archives=process_archives, force_download=force_download)
        if streams:
            try:
                return next(streams)
            except StopIteration:
                return None

    def _get_input_vfs(self, process_archives: bool = True, force_download: bool = False) -> vfs.VFS:
        v = vfs.VFS()
        ii = InputInfo.load(self.name, download=DownloadType.ALWAYS if force_download else DownloadType.OPTIONAL)
        if ii:
            for file_info in ii.files:
                vfs.add_disk_file(
                    v,
                    name=file_info.name,
                    path=file_info.path,
                    process_archives=process_archives,
                )
        return v
