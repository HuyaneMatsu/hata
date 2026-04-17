import vampytest

from ....role import Role
from ....user import User

from ..fields import validate_target
from ..preinstanced import PermissionOverwriteTargetType


def _iter_options():
    user = User.precreate(202210050000)
    role = Role.precreate(202210050001)
    target_id = 202210050002
    
    yield user, (user.id, PermissionOverwriteTargetType.user)
    yield role, (role.id, PermissionOverwriteTargetType.role)
    yield target_id, (target_id, PermissionOverwriteTargetType.unknown)
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_target__passing(input_value):
    """
    Tests whether ``validate_target`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `(int, PermissionOverwriteTargetType)`
    """
    return validate_target(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with('afraid')
def test__validate_target__type_error(input_value):
    """
    Tests whether ``validate_target`` works as intended.
    
    Case: ``TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_target(input_value)
