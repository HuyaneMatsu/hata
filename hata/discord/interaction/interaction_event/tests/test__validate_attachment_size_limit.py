import vampytest

from ....guild.guild.guild_boost_perks import LEVEL_0, LEVEL_MAX
from ..fields import validate_attachment_size_limit


def _iter_options__passing():
    yield None, LEVEL_0.attachment_size_limit
    yield LEVEL_0.attachment_size_limit, LEVEL_0.attachment_size_limit
    yield 12800000, 12800000


def _iter_options__type_error():
    yield ''

def _iter_option__value_error():
    yield LEVEL_0.attachment_size_limit - 1
    yield LEVEL_MAX.attachment_size_limit + 1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_option__value_error()).raising(ValueError))
def test__validate_attachment_size_limit(input_value):
    """
    Validates whether ``validate_attachment_size_limit`` works as intended.
    
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
    output = validate_attachment_size_limit(input_value)
    vampytest.assert_instance(output, int)
    return output
