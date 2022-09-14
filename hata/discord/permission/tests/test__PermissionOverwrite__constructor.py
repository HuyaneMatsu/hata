import vampytest

from ...role import Role
from ...user import User

from .. import Permission, PermissionOverwrite, PermissionOverwriteTargetType


def test__PermissionOverwrite__new__0():
    """
    Tests whether ``PermissionOverwrite`` works as intended.
    
    Case: default.
    """
    target_id = 202209130001
    target_type = PermissionOverwriteTargetType.user
    allow = 10
    deny = 8
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    vampytest.assert_eq(permission_overwrite.target_id, target_id)
    vampytest.assert_is(permission_overwrite.target_type, target_type)
    vampytest.assert_instance(permission_overwrite.allow, Permission)
    vampytest.assert_eq(permission_overwrite.allow, allow)
    vampytest.assert_instance(permission_overwrite.allow, Permission)
    vampytest.assert_eq(permission_overwrite.deny, deny)


def test__PermissionOverwrite__new__1():
    """
    Tests whether ``PermissionOverwrite`` works as intended.
    
    Case: target-type auto detect.
    """
    user_id = 202209130002
    role_id = 202209130003
    
    for target, expected_target_id, expected_target_type in (
        (User.precreate(user_id), user_id, PermissionOverwriteTargetType.user),
        (Role.precreate(role_id), role_id, PermissionOverwriteTargetType.role),
    ):
        permission_overwrite = PermissionOverwrite(target)
        
        vampytest.assert_eq(permission_overwrite.target_id, expected_target_id)
        vampytest.assert_is(permission_overwrite.target_type, expected_target_type)


def test__PermissionOverwrite__new__2():
    """
    Tests whether ``PermissionOverwrite`` works as intended.
    
    Case: allow - deny wrong type.
    """
    target_id = 202209130004
    target_type = PermissionOverwriteTargetType.user
    
    for field_name in ('allow', 'deny'):
        with vampytest.assert_raises(TypeError):
            PermissionOverwrite(**{'target_id': target_id, 'target_type': target_type, field_name: 12.6})


def test__PermissionOverwrite__new__3():
    """
    Tests whether ``PermissionOverwrite`` works as intended.
    
    Case: unknown target type.
    """
    target_id = 202209130005
    
    with vampytest.assert_raises(ValueError):
        PermissionOverwrite(target_id)


def test__PermissionOverwrite__new__4():
    """
    Tests whether ``PermissionOverwrite`` works as intended.
    
    Case: different target type.
    """
    role = Role.precreate(202209130006)
    target_type = PermissionOverwriteTargetType.user
    
    with vampytest.assert_raises(ValueError):
        PermissionOverwrite(role, target_type = target_type)
