import vampytest

from ..constants import INTENSITY_MIN
from ..fields import parse_intensity


def _iter_options():
    yield (
        {},
        INTENSITY_MIN,
    )
    
    yield (
        {
            'base_mix': INTENSITY_MIN,
        },
        INTENSITY_MIN,
    )
    
    yield (
        {
            'base_mix': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_intensity(input_data):
    """
    Tests whether ``parse_intensity`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_intensity(input_data)
    vampytest.assert_instance(output, int)
    return output
