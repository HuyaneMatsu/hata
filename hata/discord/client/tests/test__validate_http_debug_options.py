import vampytest

from ..fields import validate_http_debug_options


def _iter_options__passing():
    debug_option_0 = 'youkai'
    debug_option_1 = 'girl'
    
    yield None, None
    yield debug_option_0, {debug_option_0}
    yield [], None
    yield [debug_option_0], {debug_option_0}
    yield [debug_option_0, debug_option_1], {debug_option_0, debug_option_1}


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_http_debug_options(input_value):
    """
    Tests whether `validate_http_debug_options` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | set<str>`
        The validated value.
    
    Raises
    ------
    TypeError
    """
    return validate_http_debug_options(input_value)
