import vampytest

from ..constants import TEXT_LENGTH_MAX
from ..fields import validate_text


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'a', 'a'
    yield 1, '1'


def _iter_options__value_error():
    yield 'a' * (TEXT_LENGTH_MAX + 1)
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_text(input_value):
    """
    Tests whether `validate_text` works as intended.
    
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
    output = validate_text(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
