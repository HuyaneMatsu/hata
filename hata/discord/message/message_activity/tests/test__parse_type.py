import vampytest

from ..fields import parse_type
from ..preinstanced import MessageActivityType


def _iter_options():
    yield {}, MessageActivityType.none
    yield {'type': MessageActivityType.join.value}, MessageActivityType.join


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
    output : ``MessageActivityType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, MessageActivityType)
    return output
