import vampytest

from ..fields import parse_type
from ..preinstanced import EntitlementType


def _iter_options():
    yield {}, EntitlementType.none
    yield {'type': EntitlementType.purchase.value}, EntitlementType.purchase


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
    output : ``EntitlementType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, EntitlementType)
    return output
