import vampytest

from ..fields import parse_hang_type
from ..preinstanced import HangType


def _iter_options():
    yield {}, HangType.none
    yield {'state': None}, HangType.none
    yield {'state':HangType.none.value}, HangType.none
    yield {'state': HangType.gaming.value}, HangType.gaming


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_hang_type(input_data):
    """
    Tests whether ``parse_hang_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``HangType``
    """
    output = parse_hang_type(input_data)
    vampytest.assert_instance(output, HangType)
    return output
