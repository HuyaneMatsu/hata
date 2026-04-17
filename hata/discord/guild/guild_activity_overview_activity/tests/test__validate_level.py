import vampytest

from ..fields import validate_level
from ..preinstanced import GuildActivityOverviewActivityLevel


def _iter_options__passing():
    yield None, GuildActivityOverviewActivityLevel.none
    yield GuildActivityOverviewActivityLevel.any_previous.value, GuildActivityOverviewActivityLevel.any_previous
    yield GuildActivityOverviewActivityLevel.any_previous, GuildActivityOverviewActivityLevel.any_previous


def _iter_options__type_error():
    yield ''

def _iter_option__value_error():
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_option__value_error()).raising(ValueError))
def test__validate_level(input_value):
    """
    Validates whether ``validate_level`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``GuildActivityOverviewActivityLevel``
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = validate_level(input_value)
    vampytest.assert_instance(output, GuildActivityOverviewActivityLevel)
    return output
