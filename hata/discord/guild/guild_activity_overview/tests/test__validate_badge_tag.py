import vampytest

from ..constants import BADGE_TAG_LENGTH_MAX, BADGE_TAG_LENGTH_MIN
from ..fields import validate_badge_tag


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'a' * BADGE_TAG_LENGTH_MIN, 'a' * BADGE_TAG_LENGTH_MIN


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (BADGE_TAG_LENGTH_MIN - 1)
    yield 'a' * (BADGE_TAG_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_badge_tag(input_value):
    """
    Tests whether `validate_badge_tag` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_badge_tag(input_value)
    vampytest.assert_instance(output, str)
    return output
