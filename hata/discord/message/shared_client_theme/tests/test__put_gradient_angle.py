import vampytest

from ..constants import GRADIENT_ANGLE_MIN
from ..fields import put_gradient_angle


def _iter_options():
    yield (
        GRADIENT_ANGLE_MIN,
        False,
        {
            'gradient_angle': GRADIENT_ANGLE_MIN,
        },
    )
    
    yield (
        GRADIENT_ANGLE_MIN,
        True,
        {
            'gradient_angle': GRADIENT_ANGLE_MIN,
        },
    )
    
    yield (
        1,
        False,
        {
            'gradient_angle': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'gradient_angle': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_gradient_angle(input_value, defaults):
    """
    Tests whether ``put_gradient_angle`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_gradient_angle(input_value, {}, defaults)
