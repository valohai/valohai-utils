import glob

from valohai.internals.files import set_file_read_only, get_glob_pattern


def live_upload(source: str):
    for file_path in glob.glob(get_glob_pattern(source)):
        set_file_read_only(file_path)
