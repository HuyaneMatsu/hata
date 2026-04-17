import vampytest

from ..shared_constants import CUSTOM_ID_LENGTH_MAX
from ..shared_fields import validate_custom_id


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'a', 'a'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (CUSTOM_ID_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_custom_id(input_value):
    """
    Tests whether `validate_custom_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_custom_id(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
