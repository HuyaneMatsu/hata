import vampytest

from ..fields import put_type
from ..preinstanced import InviteType


def _iter_options():
    yield InviteType.friend, False, {'type': InviteType.friend.value}
    yield InviteType.friend, True, {'type': InviteType.friend.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``InviteType``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
