import vampytest

from ...guild_join_request import GuildJoinRequestStatus

from ..fields import put_status


def _iter_options():
    yield (
        GuildJoinRequestStatus.started,
        False,
        {
            'status': GuildJoinRequestStatus.started.value,
        },
    )
    
    yield (
        GuildJoinRequestStatus.started,
        True,
        {
            'status': GuildJoinRequestStatus.started.value,
        },
    )
    
    yield (
        GuildJoinRequestStatus.pending,
        False,
        {
            'status': GuildJoinRequestStatus.pending.value,
        },
    )
    
    yield (
        GuildJoinRequestStatus.pending,
        True,
        {
            'status': GuildJoinRequestStatus.pending.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_status(input_value, defaults):
    return put_status(input_value, {}, defaults)
