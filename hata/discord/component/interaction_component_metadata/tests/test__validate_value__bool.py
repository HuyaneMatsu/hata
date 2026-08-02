import vampytest

from ..fields import validate_value__bool


def _iter_options__passing():
    yield None, None
    yield '', None
    yield '\000', '\000'
    yield '\001', '\001'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_value__bool(input_value):
    """
    Validates whether ``validate_value__bool`` works as intended.
    
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
    output = validate_value__bool(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
