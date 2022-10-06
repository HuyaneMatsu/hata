import vampytest

from .....role import Role
from .....user import User

from ...preinstanced import PermissionOverwriteTargetType

from ..target import validate_target


def test__validate_target__0():
    """
    Tests whether ``validate_target`` works as intended.
    
    Case: passing.
    """
    user = User.precreate(202210050000)
    role = Role.precreate(202210050001)
    target_id = 202210050002
    
    for input_value, expected_output in (
        (user, (user.id, PermissionOverwriteTargetType.user)),
        (role, (role.id, PermissionOverwriteTargetType.role)),
        (target_id, (target_id, PermissionOverwriteTargetType.unknown)),
    ):
        output = validate_target(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_target__1():
    """
    Tests whether ``validate_target`` works as intended.
    
    Case: ``TypeError`.
    """
    for input_value in (
        'afraid',
    ):
        with vampytest.assert_raises(TypeError):
            validate_target(input_value)
