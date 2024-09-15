import vampytest

from ..constants import AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
from ..fields import validate_mention_limit


def _iter_options__passing():
    yield None, AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
    yield 0, 0
    yield 1, 1


def _iter_options__type_error():
    yield 12.6
    yield '12'


def _iter_options__value_error():
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_mention_limit(input_value):
    """
    Tests whether `validate_mention_limit` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_mention_limit(input_value)
    vampytest.assert_instance(output, int)
    return output
