import vampytest

from ..fields import validate_visibility
from ..preinstanced import ConnectionVisibility


def _iter_options__passing():
    yield None, ConnectionVisibility.user_only
    yield ConnectionVisibility.everyone, ConnectionVisibility.everyone
    yield ConnectionVisibility.everyone.value, ConnectionVisibility.everyone


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_visibility(input_value):
    """
    Tests whether `validate_visibility` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``ConnectionVisibility``
    
    Raises
    ------
    TypeError
    """
    output = validate_visibility(input_value)
    vampytest.assert_instance(output, ConnectionVisibility)
    return output
