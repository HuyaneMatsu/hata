import vampytest

from ..shared_fields import validate_default


def _iter_options__passing():
    yield None, False
    yield False, False
    yield True, True


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_default(input_value):
    """
    Tests whether `validate_default` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `bool`
    
    Raises
    ------
    TypeError
    """
    output = validate_default(input_value)
    vampytest.assert_instance(output, bool)
    return output
