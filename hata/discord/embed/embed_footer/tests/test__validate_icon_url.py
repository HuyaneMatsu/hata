import vampytest

from ..constants import ICON_URL_LENGTH_MAX
from ..fields import validate_icon_url


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'https://orindance.party/', 'https://orindance.party/'
    yield 'attachment://orin.png', 'attachment://orin.png'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    icon_url = 'https://orindance.party/'
    yield icon_url + 'a' * (ICON_URL_LENGTH_MAX - len(icon_url) + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_icon_url(input_value):
    """
    Tests whether `validate_icon_url` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `None | str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_icon_url(input_value)
