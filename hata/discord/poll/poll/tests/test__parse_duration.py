import vampytest

from ..constants import DURATION_DEFAULT
from ..fields import parse_duration


def _iter_options():
    yield {}, DURATION_DEFAULT
    yield {'duration': None}, DURATION_DEFAULT
    yield {'duration': 1}, 3600


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_duration(input_data):
    """
    Tests whether ``parse_duration`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_duration(input_data)
    vampytest.assert_instance(output, int)
    return output
