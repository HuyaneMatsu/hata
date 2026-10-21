import vampytest

from ..fields import put_status
from ..preinstanced import GuildJoinRequestStatus


def _iter_options():
    yield (
        GuildJoinRequestStatus.started,
        False,
        {
            'application_status': GuildJoinRequestStatus.started.value,
        },
    )
    
    yield (
        GuildJoinRequestStatus.started,
        True,
        {
            'application_status': GuildJoinRequestStatus.started.value,
        },
    )
    
    yield (
        GuildJoinRequestStatus.pending,
        False,
        {
            'application_status': GuildJoinRequestStatus.pending.value,
        },
    )
    
    yield (
        GuildJoinRequestStatus.pending,
        True,
        {
            'application_status': GuildJoinRequestStatus.pending.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_status(input_value, defaults):
    return put_status(input_value, {}, defaults)
