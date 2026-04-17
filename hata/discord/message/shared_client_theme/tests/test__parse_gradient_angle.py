import vampytest

from ..constants import GRADIENT_ANGLE_MIN
from ..fields import parse_gradient_angle


def _iter_options():
    yield (
        {},
        GRADIENT_ANGLE_MIN,
    )
    
    yield (
        {
            'gradient_angle': GRADIENT_ANGLE_MIN,
        },
        GRADIENT_ANGLE_MIN,
    )
    
    yield (
        {
            'gradient_angle': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_gradient_angle(input_data):
    """
    Tests whether ``parse_gradient_angle`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_gradient_angle(input_data)
    vampytest.assert_instance(output, int)
    return output
