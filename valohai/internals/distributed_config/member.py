from typing import Any, Dict, List, Optional


class Member:
    def __init__(
        self,
        *,
        announce_time: str,
        identity: str,
        job_id: str,
        member_id: str,
        exposed_ports: Dict[str, str],
        local_ips: List[str],
        public_ips: List[str],
        rank: Optional[int] = None,
    ):
        self.announce_time = announce_time
        self.identity = identity
        self.job_id = job_id
        self.member_id = member_id
        self.exposed_ports = exposed_ports
        self.local_ips = local_ips
        self.public_ips = public_ips
        self.rank = rank  # populated by `DistributedConfig.from_json_data()`

    @property
    def is_master(self) -> bool:
        return self.rank == 0

    @property
    def primary_local_ip(self) -> str:
        try:
            return self.local_ips[0]
        except IndexError as ie:
            raise RuntimeError(
                "There are no local IPs in the distributed worker network configuration"
            ) from ie

    @property
    def primary_public_ip(self) -> str:
        try:
            return self.public_ips[0]
        except IndexError as ie:
            raise RuntimeError(
                "There are no public IPs in the distributed worker network configuration"
            ) from ie

    @classmethod
    def from_json_data(cls, json_data: Dict[str, Any]) -> "Member":
        return cls(
            announce_time=json_data["announce_time"],
            identity=json_data["identity"],
            job_id=json_data["job_id"],
            member_id=json_data["member_id"],
            exposed_ports=json_data["network"]["exposed_ports"],
            local_ips=json_data["network"]["local_ips"],
            public_ips=json_data["network"]["public_ips"],
        )
