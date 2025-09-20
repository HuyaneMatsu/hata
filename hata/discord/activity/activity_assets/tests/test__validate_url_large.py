import vampytest

from ..fields import validate_url_large


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'aa', 'aa'


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_url_large(input_value):
    """
    Tests whether `validate_url_large` works as intended.
    
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
    """
    output = validate_url_large(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
