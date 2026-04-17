import vampytest

from ..fields import parse_type
from ..preinstanced import InviteType


def _iter_options():
    yield {}, InviteType.guild
    yield {'type': InviteType.friend.value}, InviteType.friend


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``InviteType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, InviteType)
    return output
