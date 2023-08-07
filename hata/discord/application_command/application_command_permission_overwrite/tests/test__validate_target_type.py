import vampytest

from ..fields import validate_target_type
from ..preinstanced import ApplicationCommandPermissionOverwriteTargetType


def _iter_options():
    yield None, ApplicationCommandPermissionOverwriteTargetType.none
    yield ApplicationCommandPermissionOverwriteTargetType.user, ApplicationCommandPermissionOverwriteTargetType.user
    yield ApplicationCommandPermissionOverwriteTargetType.user.value, ApplicationCommandPermissionOverwriteTargetType.user


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_target_type__passing(input_value):
    """
    Validates whether ``validate_target_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``ApplicationCommandPermissionOverwriteTargetType``
    """
    output = validate_target_type(input_value)
    vampytest.assert_instance(output, ApplicationCommandPermissionOverwriteTargetType)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_target_type__type_error(input_value):
    """
    Validates whether ``validate_target_type`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_target_type(input_value)
