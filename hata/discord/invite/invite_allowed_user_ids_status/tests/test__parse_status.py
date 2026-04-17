import vampytest

from ..fields import parse_status
from ..preinstanced import InviteAllowedUserIdsStatusStatus


def _iter_options():
    yield (
        {},
        InviteAllowedUserIdsStatusStatus.none,
    )
    
    yield (
        {
            'status': None,
        },
        InviteAllowedUserIdsStatusStatus.none,
    )
    
    yield (
        {
            'status': InviteAllowedUserIdsStatusStatus.completed.value,
        },
        InviteAllowedUserIdsStatusStatus.completed,
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
    output : ``InviteAllowedUserIdsStatusStatus``
    """
    output = parse_status(input_data)
    vampytest.assert_instance(output, InviteAllowedUserIdsStatusStatus)
    return output
