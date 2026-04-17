import vampytest

from ..fields import parse_type
from ..preinstanced import ActivityType


def _iter_options():
    yield {}, ActivityType.playing
    yield {'type': ActivityType.competing.value}, ActivityType.competing


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
    output : ``ActivityType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ActivityType)
    return output
