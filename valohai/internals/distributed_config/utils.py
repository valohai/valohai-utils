from typing import TYPE_CHECKING, Dict, Iterable, Union

if TYPE_CHECKING:
    from valohai.internals.distributed_config import Member


def rank_members(members: Iterable["Member"]) -> None:
    """Add ranks to members in-place."""
    mapping = compute_member_id_ranks([m.member_id for m in members])
    for m in members:
        m.rank = mapping[m.member_id]


def compute_member_id_ranks(member_ids: Iterable[str]) -> Dict[str, int]:
    """Given member ids, return member id to rank mapping."""
    id_to_sortable: Dict[str, Union[str, int]]
    try:
        id_to_sortable = {member_id: int(member_id) for member_id in member_ids}
    except ValueError:
        # if we fail to parse all member ids as an integer, just sort as string
        id_to_sortable = {member_id: member_id for member_id in member_ids}
    return {
        member_id: index
        for index, (member_id, sort_value) in enumerate(
            sorted(id_to_sortable.items(), key=lambda kv: kv[1])
        )
    }
