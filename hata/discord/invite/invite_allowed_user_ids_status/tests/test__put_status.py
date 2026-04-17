import vampytest

from ..fields import put_status
from ..preinstanced import InviteAllowedUserIdsStatusStatus


def _iter_options():
    yield (
        InviteAllowedUserIdsStatusStatus.none,
        False,
        {
            'status': InviteAllowedUserIdsStatusStatus.none.value,
        },
    )
    
    yield (
        InviteAllowedUserIdsStatusStatus.none,
        True,
        {
            'status': InviteAllowedUserIdsStatusStatus.none.value,
        },
    )
    
    yield (
        InviteAllowedUserIdsStatusStatus.failed,
        False,
        {
            'status': InviteAllowedUserIdsStatusStatus.failed.value,
        },
    )
    
    yield (
        InviteAllowedUserIdsStatusStatus.failed,
        True,
        {
            'status': InviteAllowedUserIdsStatusStatus.failed.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_status(input_value, defaults):
    """
    Tests whether ``put_status`` is working as intended.
    
    Parameters
    ----------
    input_value : ``InviteAllowedUserIdsStatusStatus``
        Value to serialise.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_status(input_value, {}, defaults)
