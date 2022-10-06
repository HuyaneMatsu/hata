import vampytest

from ....role import Role
from ....user import User

from ...permission import Permission

from ..permission_overwrite import PermissionOverwrite
from ..preinstanced import PermissionOverwriteTargetType


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


def test__PermissionOverwrite__copy():
    """
    Tests whether ``PermissionOverwrite.copy`` works as intended.
    """
    target_id = 202210050007
    target_type = PermissionOverwriteTargetType.user
    allow = 10
    deny = 8
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    copy = permission_overwrite.copy()
    vampytest.assert_instance(copy, PermissionOverwrite)
    vampytest.assert_is_not(copy, permission_overwrite)
    
    vampytest.assert_eq(copy.target_id, target_id)
    vampytest.assert_is(copy.target_type, target_type)
    vampytest.assert_instance(copy.allow, Permission)
    vampytest.assert_eq(copy.allow, allow)
    vampytest.assert_instance(copy.allow, Permission)
    vampytest.assert_eq(copy.deny, deny)


def test__PermissionOverwrite__copy_with__0():
    """
    Tests whether ``PermissionOverwrite.copy_with` works as intended.
    
    Case: no parameters.
    """
    target_id = 202210050007
    target_type = PermissionOverwriteTargetType.user
    allow = 10
    deny = 8
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    copy = permission_overwrite.copy_with()
    vampytest.assert_instance(copy, PermissionOverwrite)
    vampytest.assert_is_not(copy, permission_overwrite)
    
    vampytest.assert_eq(copy.target_id, target_id)
    vampytest.assert_is(copy.target_type, target_type)
    vampytest.assert_instance(copy.allow, Permission)
    vampytest.assert_eq(copy.allow, allow)
    vampytest.assert_instance(copy.allow, Permission)
    vampytest.assert_eq(copy.deny, deny)


def test__PermissionOverwrite__copy_with__1():
    """
    Tests whether `PermissionOverwrite.copy_with` works as intended.
    
    Case: with parameters.
    """
    target_id = 202210050008
    target_type = PermissionOverwriteTargetType.user
    allow = 10
    deny = 8
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    for field_name, field_value, expected_overwrite in (
        (
            'target_id',
            202210050009,
            PermissionOverwrite(
                202210050009,
                target_type = target_type,
                allow = allow,
                deny = deny,
            ),
        ), (
            'target_type',
            PermissionOverwriteTargetType.role,
            PermissionOverwrite(
                target_id,
                target_type = PermissionOverwriteTargetType.role,
                allow = allow,
                deny = deny,
            ),
        ), (
            'target',
            Role.precreate(202210050010),
            PermissionOverwrite(
                202210050010,
                target_type = PermissionOverwriteTargetType.role,
                allow = allow,
                deny = deny,
            ),
        ), (
            'target',
            202210050011,
            PermissionOverwrite(
                202210050011,
                target_type = PermissionOverwriteTargetType.user,
                allow = allow,
                deny = deny,
            ),
        ), (
            'allow',
            13,
            PermissionOverwrite(
                target_id,
                target_type = target_type,
                allow = 13,
                deny = deny,
            ),
        ), (
            'deny',
            14,
            PermissionOverwrite(
                target_id,
                target_type = target_type,
                allow = allow,
                deny = 14,
            ),
        ),
    ):
        copy = permission_overwrite.copy_with(**{field_name: field_value})
        vampytest.assert_instance(copy, PermissionOverwrite)
        vampytest.assert_eq(copy, expected_overwrite)
