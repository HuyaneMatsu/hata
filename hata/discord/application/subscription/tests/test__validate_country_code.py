import vampytest

from ..fields import validate_country_code


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'AA', 'AA'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'A'
    yield 'AAA'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_country_code(input_value):
    """
    Tests whether `validate_country_code` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_country_code(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
