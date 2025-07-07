import vampytest

from ..fields import validate_target_type
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def _iter_options__passing():
    yield None, ApplicationCommandPermissionOverwriteTargetType.none
    yield ApplicationCommandPermissionOverwriteTargetType.user, ApplicationCommandPermissionOverwriteTargetType.user
    yield ApplicationCommandPermissionOverwriteTargetType.user.value, ApplicationCommandPermissionOverwriteTargetType.user


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
    output : ``ApplicationCommandPermissionOverwriteTargetType``
    
    Raises
    ------
    TypeError
    """
    output = validate_target_type(input_value)
    vampytest.assert_instance(output, ApplicationCommandPermissionOverwriteTargetType)
    return output
