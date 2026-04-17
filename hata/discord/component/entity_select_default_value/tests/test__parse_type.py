import vampytest

from ..fields import parse_type
from ..preinstanced import EntitySelectDefaultValueType


def _iter_options():
    yield {}, EntitySelectDefaultValueType.none
    yield {'type': EntitySelectDefaultValueType.role.value}, EntitySelectDefaultValueType.role


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
    output : ``EntitySelectDefaultValueType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, EntitySelectDefaultValueType)
    return output
