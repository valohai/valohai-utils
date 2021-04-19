import glob
import os
import tempfile
from typing import Union

from valohai.internals.compression import open_archive
from valohai.internals.files import (
    expand_globs,
    get_canonical_extension,
    get_glob_pattern,
    set_file_read_only,
)
from valohai.paths import get_outputs_path


class Output:
    def __init__(self, name: str = "") -> None:
        self.name = str(name)

    def path(self, filename: str, makedirs: bool = True) -> str:
        """Absolute path of an output file

        Compress files into a temporary file, which is then copied to the target path.
        Optionally removes original files and live uploads the package.

        Returns the absolute path to the created package.

        :param filename: Name of the file. Can also include sub path (example: myfolder/hello.txt)
        :param makedirs: Auto-create folders if they do not exist.

        """
        path = get_outputs_path()

        # To guard against absolute paths in the output name.
        # If the absolute path is in the outputs dir, the path will be made relative.
        # If it is some other absolute path, an exception is raised.
        if os.path.isabs(self.name):
            if self.name.startswith(path):
                self.name = os.path.relpath(self.name, path)
            else:
                raise ValueError(
                    f"Absolute path used, when relative expected ({self.name})"
                )

        if self.name:
            path = os.path.join(path, self.name)

        path = os.path.join(path, filename)

        if makedirs:
            os.makedirs(os.path.dirname(path), exist_ok=True)

        return path

    def live_upload(self, filename: str) -> None:
        for file_path in glob.glob(get_glob_pattern(self.path(filename))):
            set_file_read_only(file_path)

    def compress(
        self,
        source: Union[str, list],
        filename: str,
        live_upload: bool = False,
        remove_originals: bool = True,
    ) -> str:
        """Compress output files as single package.

        Compress files into a temporary file, which is then copied to the target path.
        Optionally removes original files and live uploads the package.

        Returns the absolute path to the created package.

        :param source: List of things to compress. Supports wildcard(s) and directory name(s). (examples: "folder", "folder/*.jpg")
        :param filename: Name of the compressed file. Suffix is used to determine compression type ("example.zip")
        :param live_upload: Sets the result file read-only to allow live upload in cloud executions
        :param remove_originals: Are the original files removed after packaging

        """
        target_path = self.path(filename)
        files_to_compress = expand_globs(source, preprocessor=self.path)
        common_prefix = os.path.commonprefix(list(files_to_compress))

        # We can't use `delete=True` since we need to replace the file later, and moving
        # the `os.replace()` call within the block if it has delete=True means there'll be an
        # exception trying to unlink the name that has been already `replace`d out...

        suffix = get_canonical_extension(filename)
        tmp_file = tempfile.NamedTemporaryFile(
            dir=os.path.dirname(target_path), suffix=suffix, delete=False
        )
        with tmp_file, open_archive(tmp_file.name) as archive:  # type: ignore
            compressed_paths = []
            for file_path in files_to_compress:
                arc_path = os.path.relpath(file_path, common_prefix)
                archive.put(arc_path, file_path)
                compressed_paths.append(file_path)

        os.replace(tmp_file.name, target_path)
        if live_upload:
            set_file_read_only(target_path)

        if remove_originals:
            for file_path in compressed_paths:
                os.remove(file_path)

        return target_path


outputs = Output
