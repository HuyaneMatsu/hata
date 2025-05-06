import vampytest

from ..constants import MAX_LENGTH_DEFAULT
from ..fields import parse_max_length


def _iter_options():
    yield (
        {},
        MAX_LENGTH_DEFAULT,
    )
    
    yield (
        {
            'max_length': None,
        },
        MAX_LENGTH_DEFAULT,
    )
    
    yield (
        {
            'max_length': 10,
        },
        10,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_max_length(input_data):
    """
    Tests whether ``parse_max_length`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_max_length(input_data)
    vampytest.assert_instance(output, int)
    return output
