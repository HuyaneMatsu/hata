import vampytest

from ..constants import VALUE_LENGTH_MAX
from ..fields import validate_value


def _iter_options__passing():
    yield None, None
    yield 'a', 'a'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (VALUE_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_value(input_value):
    """
    Validates whether ``validate_value`` works as intended.
    
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
    output = validate_value(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
