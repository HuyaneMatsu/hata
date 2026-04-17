import vampytest

from ..fields import parse_status
from ..preinstanced import GuildJoinRequestStatus


def _iter_options():
    yield (
        {},
        GuildJoinRequestStatus.started,
    )
    yield (
        {
            'application_status': None,
        },
        GuildJoinRequestStatus.started,
    )
    
    yield (
        {
            'application_status': GuildJoinRequestStatus.pending.value,
        },
        GuildJoinRequestStatus.pending,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_status(input_data):
    """
    Tests whether ``parse_status`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
        
    Returns
    -------
    output : ``GuildJoinRequestStatus``
    """
    output = parse_status(input_data)
    vampytest.assert_instance(output, GuildJoinRequestStatus)
    return output
