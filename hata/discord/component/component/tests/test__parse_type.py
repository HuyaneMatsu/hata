import vampytest

from ..fields import parse_type
from ..preinstanced import ComponentType


def _iter_options():
    yield {}, ComponentType.none
    yield {'type': ComponentType.button.value}, ComponentType.button


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
    output : ``ComponentType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ComponentType)
    return output
