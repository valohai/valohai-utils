import glob

from valohai.internals.files import get_glob_pattern, set_file_read_only


def live_upload(source: str):
    for file_path in glob.glob(get_glob_pattern(source)):
        set_file_read_only(file_path)
