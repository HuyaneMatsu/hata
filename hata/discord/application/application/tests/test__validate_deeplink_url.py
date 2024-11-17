import vampytest

from ..fields import validate_deeplink_url


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'https://orindance.party/', 'https://orindance.party/'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_deeplink_url(input_value):
    """
    Tests whether `validate_deeplink_url` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test with.
    
    Returns
    -------
    output : `None | str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_deeplink_url(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
