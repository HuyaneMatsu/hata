import vampytest

from ..fields import parse_type
from ..preinstanced import ConnectionType


def _iter_options():
    yield {}, ConnectionType.none
    yield {'type': ConnectionType.github.value}, ConnectionType.github


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
    output : ``ConnectionType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ConnectionType)
    return output
