import vampytest

from ..constants import MIN_LENGTH_DEFAULT
from ..fields import parse_min_length


def _iter_options():
    yield (
        {},
        MIN_LENGTH_DEFAULT,
    )
    
    yield (
        {
            'min_length': None,
        },
        MIN_LENGTH_DEFAULT,
    )
    
    yield (
        {
            'min_length': 10,
        },
        10,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_min_length(input_data):
    """
    Tests whether ``parse_min_length`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_min_length(input_data)
    vampytest.assert_instance(output, int)
    return output
