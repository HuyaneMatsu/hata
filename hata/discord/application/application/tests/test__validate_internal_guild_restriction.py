import vampytest

from ..fields import validate_internal_guild_restriction
from ..preinstanced import ApplicationInternalGuildRestriction


def _iter_options__passing():
    yield None, ApplicationInternalGuildRestriction.none
    yield ApplicationInternalGuildRestriction.restricted, ApplicationInternalGuildRestriction.restricted
    yield ApplicationInternalGuildRestriction.restricted.value, ApplicationInternalGuildRestriction.restricted


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_internal_guild_restriction(input_value):
    """
    Tests whether ``validate_internal_guild_restriction`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationInternalGuildRestriction``
    
    Raises
    ------
    TypeError
    """
    output = validate_internal_guild_restriction(input_value)
    vampytest.assert_instance(output, ApplicationInternalGuildRestriction)
    return output
