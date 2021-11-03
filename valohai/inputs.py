from typing import IO, Iterable, Iterator, List, Optional, Union

from valohai.internals import vfs
from valohai.internals.download_type import DownloadType
from valohai.internals.inputs import get_input_vfs
from valohai.paths import get_inputs_path


class Input:
    def __init__(
        self, name: str, default: Optional[Union[str, List[str]]] = None
    ) -> None:
        self.name = str(name)
        self.default = default

    def paths(
        self,
        path_filter: Optional[str] = None,
        default: Optional[Iterable[str]] = None,
        process_archives: bool = True,
        force_download: bool = False,
    ) -> Iterator[str]:
        """Get paths to all files for a given input name.

        Returns a list of file system paths for an input.
        If the input is not found in the cache, it is downloaded automatically.

        See streams() or path() for alternatives.

        :param path_filter: Filter the results with wildcards. For example: "myfile.txt" or "myfolder/*.txt".
        :param default: Default fallback paths.
        :param process_archives: When facing an archive file, is it unpacked to several paths or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: List of file system paths for all the files for this input.
        """

        fs = get_input_vfs(
            name=self.name,
            process_archives=process_archives,
            download_type=(
                DownloadType.ALWAYS if force_download else DownloadType.OPTIONAL
            ),
        )
        files = fs.filter(path_filter) if path_filter else fs.files

        found_file = False
        for file in files:
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
        path_filter: Optional[str] = None,
        default: Optional[str] = None,
        process_archives: bool = True,
        force_download: bool = False,
    ) -> Optional[str]:
        """Get path to a file for a given input name.

        Returns a file system path for an input.
        If the input contains multiple files, only the first one is returned.
        If the input is not found in the cache, it is downloaded automatically.

        See stream() or paths() for an alternative.

        :param path_filter: Filter the results with wildcards. For example: "myfile.txt" or "myfolder/*.txt".
        :param process_archives: When facing an archive file, is it unpacked or returned as is
        :param default: Default fallback path.
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: File system path to a file for this input.
        """
        input_paths = self.paths(
            path_filter=path_filter,
            process_archives=process_archives,
            force_download=force_download,
        )
        return next(input_paths, default)

    def streams(
        self,
        path_filter: Optional[str] = None,
        process_archives: bool = True,
        force_download: bool = False,
    ) -> Iterator[IO[bytes]]:
        """Get file streams to all files for a given input name.

        Returns an Iterable for all the file IO streams for an input.

        If the file(s) are not found in the cache, they are downloaded automatically.

        See stream() or paths() for an alternative.

        :param path_filter: Filter the results with wildcards. For example: "myfile.txt" or "myfolder/*.txt".
        :param process_archives: When facing an archive file, is it unpacked or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: Iterable for all the IO streams of files for this input.
        """

        fs = get_input_vfs(
            name=self.name,
            process_archives=process_archives,
            download_type=DownloadType.ALWAYS
            if force_download
            else DownloadType.OPTIONAL,
        )
        files = fs.filter(path_filter) if path_filter else fs.files

        for file in files:
            yield file.open()

    def stream(
        self,
        path_filter: Optional[str] = None,
        process_archives: bool = True,
        force_download: bool = False,
    ) -> Optional[IO[bytes]]:
        """Get a stream for to a file for a given input name.

        Returns an IO stream to a file for this input.
        If the input contains multiple files, only the stream to the first one is returned.
        If the file(s) are not found in the cache, they are downloaded automatically.

        See path() or streams() for an alternative.

        :param path_filter: Filter the results with wildcards. For example: "myfile.txt" or "myfolder/*.txt".
        :param process_archives: When facing an archive file, is it unpacked or returned as is
        :param force_download: Force re-download of file(s) even when they are cached already.
        :return: IO stream to a file for this input.
        """

        streams = self.streams(
            path_filter=path_filter,
            process_archives=process_archives,
            force_download=force_download,
        )
        return next(streams, None)

    def dir_path(
        self,
    ) -> str:
        return get_inputs_path(self.name)


inputs = Input
