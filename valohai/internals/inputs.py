from typing import Optional

from valohai.internals import global_state, vfs
from valohai.internals.download_type import DownloadType
from valohai.internals.global_state_loader import load_global_state_if_necessary
from valohai.internals.input_info import InputInfo


def get_input_vfs(
    name: str,
    process_archives: bool = True,
    download_type: DownloadType = DownloadType.OPTIONAL,
) -> vfs.VFS:
    v = vfs.VFS()
    ii = get_input_info(name)
    if ii:
        ii.download_if_necessary(name, download_type)
        for file_info in ii.files:
            assert file_info.path
            vfs.add_disk_file(
                v,
                name=file_info.name,
                path=file_info.path,
                process_archives=process_archives,
            )

    return v


def get_input_info(name: str) -> Optional[InputInfo]:
    load_global_state_if_necessary()
    return global_state.inputs.get(name, None)
