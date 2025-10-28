import vampytest

from ..constants import INTENSITY_MIN
from ..fields import put_intensity


def _iter_options():
    yield (
        INTENSITY_MIN,
        False,
        {
            'base_mix': INTENSITY_MIN,
        },
    )
    
    yield (
        INTENSITY_MIN,
        True,
        {
            'base_mix': INTENSITY_MIN,
        },
    )
    
    yield (
        1,
        False,
        {
            'base_mix': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'base_mix': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_intensity(input_value, defaults):
    """
    Tests whether ``put_intensity`` works as intended.
    
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
    return put_intensity(input_value, {}, defaults)
