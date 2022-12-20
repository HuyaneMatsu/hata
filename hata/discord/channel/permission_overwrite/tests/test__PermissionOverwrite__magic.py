import vampytest

from .. import PermissionOverwrite, PermissionOverwriteTargetType


def test__PermissionOverwrite__hash():
    """
    Tests whether ``PermissionOverwrite.__hash__` works as intended.
    """
    target_id = 202209140004
    target_type = PermissionOverwriteTargetType.user
    allow = 8
    deny = 12
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    vampytest.assert_instance(hash(permission_overwrite), int)


def test__PermissionOverwrite__repr():
    """
    Tests whether ``PermissionOverwrite.__repr__` works as intended.
    """
    target_id = 202209140005
    target_type = PermissionOverwriteTargetType.user
    allow = 8
    deny = 12
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    vampytest.assert_instance(repr(permission_overwrite), str)


def test__PermissionOverwrite__eq():
    """
    Tests whether ``PermissionOverwrite.__eq__`` works as intended.
    """
    target_id = 202209140010
    target_type = PermissionOverwriteTargetType.user
    allow = 8
    deny = 12
    
    fields = {
        'target_id': target_id,
        'target_type': target_type,
        'allow': allow,
        'deny': deny,
    }
    
    permission_overwrite = PermissionOverwrite(**fields)
    
    vampytest.assert_eq(permission_overwrite, permission_overwrite)
    
    for field_name, field_value in (
        ('target_id', 202209140011),
        ('target_type', PermissionOverwriteTargetType.role),
        ('allow', 69),
        ('deny', 69),
    ):
        test_permission_overwrite = PermissionOverwrite(**{**fields, field_name: field_value})
        
        vampytest.assert_ne(permission_overwrite, test_permission_overwrite)


def test__PermissionOverwrite__sort():
    permission_overwrite_1 = PermissionOverwrite(
        target_id = 202209140012, target_type = PermissionOverwriteTargetType.user,
    )
    permission_overwrite_2 = PermissionOverwrite(
        target_id = 202209140013, target_type = PermissionOverwriteTargetType.role,
    )
    permission_overwrite_3 = PermissionOverwrite(
        target_id = 202209140014, target_type = PermissionOverwriteTargetType.user,
    )
    permission_overwrite_4 = PermissionOverwrite(
        target_id = 202209140015, target_type = PermissionOverwriteTargetType.role,
    )
    
    expected_order = [
        permission_overwrite_1,
        permission_overwrite_3,
        permission_overwrite_2,
        permission_overwrite_4,
    ]
    
    listed = [
        permission_overwrite_1,
        permission_overwrite_2,
        permission_overwrite_3,
        permission_overwrite_4,
    ]
    
    listed.sort()
    
    vampytest.assert_eq(expected_order, listed)
