import vampytest

from ..constants import SLOP_DEFAULT
from ..fields import parse_slop


def _iter_options():
    yield (
        {},
        SLOP_DEFAULT,
    )
    
    yield (
        {
            'slop': None,
        },
        SLOP_DEFAULT,
    )
    
    yield (
        {
            'slop': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_slop(input_data):
    """
    Tests whether ``parse_slop`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the slop from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_slop(input_data)
    vampytest.assert_instance(output, int)
    return output
