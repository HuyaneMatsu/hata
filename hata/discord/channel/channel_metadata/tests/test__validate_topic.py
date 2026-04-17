import vampytest

from ..constants import TOPIC_LENGTH_MAX
from ..fields import validate_topic


def _iter_options():
    yield None, None
    yield '', None
    yield 'a', 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_topic__passing(input_value):
    """
    Tests whether `validate_topic` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None`, `str`
    """
    return validate_topic(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_topic__type_error(input_value):
    """
    Tests whether `validate_topic` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_topic(input_value)



@vampytest.raising(ValueError)
@vampytest.call_with('a' * (TOPIC_LENGTH_MAX + 1))
def test__validate_topic__value_error(input_value):
    """
    Tests whether `validate_topic` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    ValueError
    """
    validate_topic(input_value)
