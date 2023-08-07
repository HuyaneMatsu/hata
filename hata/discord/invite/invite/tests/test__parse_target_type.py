import vampytest

from ..fields import parse_target_type
from ..preinstanced import InviteTargetType


def _iter_options():
    yield {}, InviteTargetType.none
    yield {'target_type': None}, InviteTargetType.none
    yield {'target_type': InviteTargetType.stream.value}, InviteTargetType.stream


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_target_type(input_data):
    """
    Tests whether ``parse_target_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the target type from.
    
    Returns
    -------
    output : ``InviteTargetType``
    """
    output = parse_target_type(input_data)
    vampytest.assert_instance(output, InviteTargetType)
    return output
