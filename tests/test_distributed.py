import json

import pytest

import valohai
from valohai.internals.distributed_config import Member
from valohai.internals.distributed_config.utils import compute_member_id_ranks

# all _valid_ test distributed configurations for different use-cases
configs = {
    "exposed_ports": "exposed-ports.json",
    "is-master": "is-master.json",
    "is-not-master": "is-not-master.json",
    "network-host": "network-host.json",
    "no-public-ips": "no-public-ips.json",
}


@pytest.mark.parametrize("use_distributed_config", configs.values(), indirect=True)
def test_parsing_basic_values(use_distributed_config):
    assert valohai.distributed.is_distributed_task()
    assert valohai.distributed.group_name.startswith("task-")
    assert valohai.distributed.member_id in ["0", "1", "2"]
    assert valohai.distributed.rank in [0, 1, 2]
    assert isinstance(valohai.distributed.required_count, int)
    assert isinstance(valohai.distributed.me(), Member)
    assert len(valohai.distributed.members()) > 0
    for member in valohai.distributed.members():
        assert isinstance(member, Member)
        assert isinstance(member.rank, int)
        assert isinstance(member.exposed_ports, dict)
        assert all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in member.exposed_ports.items()
        )
        assert all(isinstance(li, str) for li in member.local_ips)
        assert all(isinstance(pi, str) for pi in member.public_ips)


@pytest.mark.parametrize(
    "use_distributed_config", ["I do not exist.json"], indirect=True
)
def test_using_missing_file(use_distributed_config):
    assert not valohai.distributed.is_distributed_task()
    with pytest.raises(FileNotFoundError):
        assert valohai.distributed.group_name


@pytest.mark.parametrize("use_distributed_config", ["malformed.json"], indirect=True)
def test_using_malformed_file(use_distributed_config):
    assert not valohai.distributed.is_distributed_task()
    with pytest.raises(json.decoder.JSONDecodeError):
        assert valohai.distributed.group_name


@pytest.mark.parametrize("use_distributed_config", configs.values(), indirect=True)
def test_getting_member_by_id(use_distributed_config):
    expected_self = valohai.distributed.member(valohai.distributed.me().member_id)
    assert expected_self.member_id == valohai.distributed.me().member_id
    assert expected_self.identity == valohai.distributed.me().identity
    assert expected_self.job_id == valohai.distributed.me().job_id


@pytest.mark.parametrize(
    "use_distributed_config", [configs["is-master"]], indirect=True
)
def test_unable_to_find_member_by_id(use_distributed_config):
    with pytest.raises(Exception) as e:
        valohai.distributed.member("1234")
    assert "no member" in str(e).lower()


@pytest.mark.parametrize(
    "use_distributed_config", [configs["is-master"]], indirect=True
)
def test_checking_master_as_master(use_distributed_config):
    master = valohai.distributed.master()
    assert valohai.distributed.me().member_id == master.member_id
    assert valohai.distributed.member_id == master.member_id
    assert master.is_master
    assert valohai.distributed.me().is_master


@pytest.mark.parametrize(
    "use_distributed_config", [configs["is-not-master"]], indirect=True
)
def test_checking_master_as_non_master(use_distributed_config):
    master = valohai.distributed.master()
    assert valohai.distributed.me().member_id != master.member_id
    assert valohai.distributed.member_id != master.member_id
    assert master.is_master
    assert not valohai.distributed.me().is_master


@pytest.mark.parametrize("use_distributed_config", configs.values(), indirect=True)
def test_getting_master_primary_local_ip(use_distributed_config):
    assert valohai.distributed.master().primary_local_ip


@pytest.mark.parametrize(
    "use_distributed_config", [configs["network-host"]], indirect=True
)
def test_getting_master_primary_public_ip(use_distributed_config):
    assert valohai.distributed.master().primary_public_ip


@pytest.mark.parametrize(
    "use_distributed_config", [configs["no-public-ips"]], indirect=True
)
def test_failing_to_get_master_primary_public_ip(use_distributed_config):
    with pytest.raises(Exception) as e:
        assert valohai.distributed.master().primary_public_ip
    assert "no public ips" in str(e).lower()


@pytest.mark.parametrize(
    "ids_and_ranking",
    [
        (["0", "1", "2"], {"0": 0, "1": 1, "2": 2}),
        (["2", "0", "1"], {"0": 0, "1": 1, "2": 2}),  # integers out-of-order is fine
        (
            ["30", "100", "2000"],
            {"30": 0, "100": 1, "2000": 2},
        ),  # integers don't map 1:1 to ranking
        (
            ["abc", "ghj", "def"],
            {"abc": 0, "def": 1, "ghj": 2},
        ),  # member ids are non-integer
        (["10", "2", "x"], {"10": 0, "2": 1, "x": 2}),  # mixed type will string sort
    ],
)
def test_ranking_member_ids(ids_and_ranking):
    member_ids, ranking = ids_and_ranking
    assert compute_member_id_ranks(member_ids) == ranking
