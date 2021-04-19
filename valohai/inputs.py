from typing import IO, Iterable, Iterator, Optional

from valohai.internals.download_type import DownloadType

from .internals import vfs
from .internals.input_info import load_input_info


class Input:
    def __init__(self, name: str) -> None:
        self.name = str(name)

    def paths(
        self,
        default: Optional[Iterable[str]] = None,
        process_archives: bool = True,
        force_download: bool = False,
    ) -> Iterator[str]:
        """Get paths to all files for a given input name.

        Returns a list of file system paths for an input.
        If the input is not found in the cache, it is downloaded automatically.

        See streams() or path() for alternatives.

        :param default: Default fallback paths.
        :param process_archives: When facing an archive file, is it unpacked to several paths or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: List of file system paths for all the files for this input.
        """

        found_file = False
        for file in self._get_input_vfs(
            process_archives=process_archives, force_download=force_download
        ).files:
            if isinstance(file, vfs.FileInContainer):
                yield file.open_concrete(delete=False).name
                found_file = True
            elif isinstance(file, vfs.FileOnDisk):
                yield file.path
                found_file = True

        if not found_file:
            if default is None:
                default = []
            yield from default

    def path(
        self,
        default: Optional[str] = None,
        process_archives: bool = True,
        force_download: bool = False,
    ) -> Optional[str]:
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
        input_paths = self.paths(
            process_archives=process_archives, force_download=force_download
        )
        return next(input_paths, default)

    def streams(
        self, process_archives: bool = True, force_download: bool = False
    ) -> Iterator[IO]:
        """Get file streams to all files for a given input name.

        Returns an Iterable for all the file IO streams for an input.

        If the file(s) are not found in the cache, they are downloaded automatically.

        See stream() or paths() for an alternative.

        :param process_archives: When facing an archive file, is it unpacked or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: Iterable for all the IO streams of files for this input.
        """
        for file in self._get_input_vfs(
            process_archives=process_archives, force_download=force_download
        ).files:
            yield file.open()

    def stream(
        self, process_archives: bool = True, force_download: bool = False
    ) -> Optional[IO]:
        """Get a stream for to a file for a given input name.

        Returns an IO stream to a file for this input.
        If the input contains multiple files, only the stream to the first one is returned.
        If the file(s) are not found in the cache, they are downloaded automatically.

        See path() or streams() for an alternative.

        :param process_archives: When facing an archive file, is it unpacked or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: IO stream to a file for this input.
        """

        streams = self.streams(
            process_archives=process_archives, force_download=force_download
        )
        return next(streams, None)

    def _get_input_vfs(
        self, process_archives: bool = True, force_download: bool = False
    ) -> vfs.VFS:
        v = vfs.VFS()
        ii = load_input_info(
            self.name,
            download=DownloadType.ALWAYS if force_download else DownloadType.OPTIONAL,
        )
        if ii:
            for file_info in ii.files:
                assert file_info.path
                vfs.add_disk_file(
                    v,
                    name=file_info.name,
                    path=file_info.path,
                    process_archives=process_archives,
                )
        return v


inputs = Input
