import vampytest

from ....role import Role
from ....user import User

from ..permission_overwrite import PermissionOverwrite
from ..preinstanced import PermissionOverwriteTargetType


def test__PermissionOverwrite__target():
    """
    Tests whether ``PermissionOverwrite.target`` works as intended.
    """
    for target_id, target_type, expected_output_type in (
        (202209140002, PermissionOverwriteTargetType.user, User),
        (202209140003, PermissionOverwriteTargetType.role, Role),
    ):
        permission_overwrite = PermissionOverwrite(target_id, target_type = target_type)
        
        target = permission_overwrite.target
        vampytest.assert_instance(target, expected_output_type)
        vampytest.assert_eq(target.id, target_id)


def test__PermissionOverwrite__keys():
    """
    Tests whether ``PermissionOverwrite.keys`` works as intended.
    """
    target_id = 202209140006
    target_type = PermissionOverwriteTargetType.user
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type)
    
    keys = [*permission_overwrite.keys()]
    
    vampytest.assert_true(keys)
    
    for key in keys:
        vampytest.assert_instance(key, str)


def test__PermissionOverwrite__values__0():
    """
    Tests whether ``PermissionOverwrite.values`` works as intended.
    
    Case: no permissions.
    """
    target_id = 202209140007
    target_type = PermissionOverwriteTargetType.user
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type)
    
    values = [*permission_overwrite.values()]
    
    vampytest.assert_true(values)
    
    for value in values:
        vampytest.assert_instance(value, int)
        vampytest.assert_eq(value, 0)
        

def test__PermissionOverwrite__values__1():
    """
    Tests whether ``PermissionOverwrite.values`` works as intended.
    
    Case: mixed.
    """
    target_id = 202209140008
    target_type = PermissionOverwriteTargetType.user
    allow = 55555
    deny = 66666
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    values = [*permission_overwrite.values()]
    vampytest.assert_in(+1, values)
    vampytest.assert_in(-1, values)


def test__PermissionOverwrite__items():
    """
    Tests whether ``PermissionOverwrite.items`` works as intended.
    """
    target_id = 202209140009
    target_type = PermissionOverwriteTargetType.user
    allow = 55555
    deny = 66666
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    items = [*permission_overwrite.items()]
    
    vampytest.assert_true(items)
    
    for key_value_pair, item in zip(zip(permission_overwrite.keys(), permission_overwrite.values()), items):
        vampytest.assert_eq(key_value_pair, item)
