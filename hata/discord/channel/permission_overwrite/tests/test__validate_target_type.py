import vampytest

from ..fields import validate_target_type
from ..preinstanced import PermissionOverwriteTargetType


def _iter_options__passing():
    yield None, PermissionOverwriteTargetType.role # This is not `.unknown` because the default value is `0`!
    yield PermissionOverwriteTargetType.user, PermissionOverwriteTargetType.user
    yield PermissionOverwriteTargetType.user.value, PermissionOverwriteTargetType.user


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
    output : ``PermissionOverwriteTargetType``
    
    Raises
    ------
    TypeError
    """
    output = validate_target_type(input_value)
    vampytest.assert_instance(output, PermissionOverwriteTargetType)
    return output
