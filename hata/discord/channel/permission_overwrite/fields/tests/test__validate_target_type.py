import vampytest

from ...preinstanced import PermissionOverwriteTargetType

from ..target_type import validate_target_type


def _iter_options():
    yield None, PermissionOverwriteTargetType.role # This is not `.unknown` because the default value is `0`!
    yield PermissionOverwriteTargetType.user, PermissionOverwriteTargetType.user
    yield PermissionOverwriteTargetType.user.value, PermissionOverwriteTargetType.user


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_target_type__passing(input_value):
    """
    Tests whether ``validate_target_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``PermissionOverwriteTargetType``
    """
    output = validate_target_type(input_value)
    vampytest.assert_instance(output, PermissionOverwriteTargetType)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_target_type__type_error(input_value):
    """
    Tests whether ``validate_target_type`` works as intended.
    
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
