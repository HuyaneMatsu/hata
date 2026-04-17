import vampytest

from ....application_command import ApplicationCommandTargetType

from ..fields import validate_target_type


def _iter_options__passing():
    yield None, ApplicationCommandTargetType.none
    yield ApplicationCommandTargetType.user, ApplicationCommandTargetType.user
    yield ApplicationCommandTargetType.user.value, ApplicationCommandTargetType.user


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_target_type(input_value):
    """
    Validates whether ``validate_target_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``ApplicationCommandTargetType``
    
    Raises
    ------
    TypeError
    """
    output = validate_target_type(input_value)
    vampytest.assert_instance(output, ApplicationCommandTargetType)
    return output
