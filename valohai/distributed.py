import json
import warnings
from typing import List, Optional

from valohai import paths
from valohai.internals.distributed_config import DistributedConfig, Member


class Distributed:
    """
    Distributed toolkit accessed through `valohai.distributed`.
    """

    _config: Optional[DistributedConfig] = None

    def is_distributed_task(self) -> bool:
        # not a property to mimic `is_running_in_valohai`
        try:
            return bool(self.config.group_name)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        except Exception as exc:
            warnings.warn(f"Failed to parse distributed config: {exc}")
            return False

    @property
    def group_name(self) -> str:
        return self.config.group_name

    @property
    def member_id(self) -> str:
        return self.config.member_id

    @property
    def rank(self) -> Optional[int]:
        return self.me().rank

    @property
    def required_count(self) -> int:
        return self.config.required_count

    def members(self) -> List[Member]:
        return self.config.members

    def member(self, member_id: str) -> Member:
        for member in self.members():
            if member.member_id == member_id:
                return member
        raise RuntimeError(f"No member with id {member_id}")

    def me(self) -> Member:
        return self.member(member_id=self.config.member_id)

    def master(self) -> Member:
        for member in self.members():
            if member.is_master:
                return member
        raise RuntimeError("No master member found")

    @property
    def config(self) -> DistributedConfig:
        if not self._config:
            with open(self._get_config_path()) as json_file:
                json_data = json.load(json_file)
            self._config = DistributedConfig.from_json_data(json_data)
        return self._config

    def _get_config_path(self) -> str:
        return paths.get_distributed_config_path()

    def flush_state(self) -> None:
        self._config = None
