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
    """
    Tests whether ``put_status`` is working as intended.
    
    Parameters
    ----------
    input_value : ``GuildJoinRequestStatus``
        Value to serialise.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_status(input_value, {}, defaults)
