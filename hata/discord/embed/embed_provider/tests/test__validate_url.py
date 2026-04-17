import vampytest

from ..constants import URL_LENGTH_MAX
from ..fields import validate_url


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'https://orindance.party/', 'https://orindance.party/'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a'
    
    url = 'https://orindance.party/'
    yield url + 'a' * (URL_LENGTH_MAX - len(url) + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_url(input_value):
    """
    Tests whether `validate_url` works as intended.
    
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
    return validate_url(input_value)
