from typing import Any, Dict, List

from valohai.internals.distributed_config.member import Member
from valohai.internals.distributed_config.utils import rank_members


class DistributedConfig:
    def __init__(
        self,
        *,
        group_name: str,
        member_id: str,
        required_count: int,
        members: List[Member],
    ):
        self.group_name = group_name
        self.member_id = member_id
        self.required_count = required_count
        self.members = members

    @classmethod
    def from_json_data(cls, json_data: Dict[str, Any]) -> "DistributedConfig":
        members = [Member.from_json_data(m) for m in json_data["members"]]
        rank_members(members)
        return cls(
            group_name=json_data["config"]["group_name"],
            member_id=json_data["config"]["member_id"],
            required_count=json_data["config"]["required_count"],
            members=members,
        )
