import vampytest

from .. import Permission, PermissionOverwrite, PermissionOverwriteTargetType


def test__PermissionOverwrite__from_data():
    """
    Tests whether `PermissionOverwrite.from_data` works as intended.
    """
    target_id = 202209130007
    target_type = PermissionOverwriteTargetType.user
    allow = 8
    deny = 12
    
    permission_overwrite = PermissionOverwrite.from_data({
        'id': str(target_id),
        'type': target_type.value,
        'allow': str(allow),
        'deny': str(deny),
    })
    
    vampytest.assert_instance(permission_overwrite.target_id, int)
    vampytest.assert_instance(permission_overwrite.target_type, PermissionOverwriteTargetType)
    vampytest.assert_instance(permission_overwrite.allow, Permission)
    vampytest.assert_instance(permission_overwrite.deny, Permission)
    
    vampytest.assert_eq(permission_overwrite.target_id, target_id)
    vampytest.assert_is(permission_overwrite.target_type, target_type)
    vampytest.assert_eq(permission_overwrite.allow, allow)
    vampytest.assert_eq(permission_overwrite.deny, deny)


def test__PermissionOverwrite__to_data():
    """
    Tests whether ``PermissionOverwrite.to_data`` works as intended.
    """
    target_id = 202209140000
    target_type = PermissionOverwriteTargetType.user
    allow = 8
    deny = 12
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    data = permission_overwrite.to_data()
    
    vampytest.assert_in('type', data)
    vampytest.assert_in('allow', data)
    vampytest.assert_in('deny', data)

    vampytest.assert_eq(data['type'], target_type.value)
    vampytest.assert_eq(data['allow'], str(allow))
    vampytest.assert_eq(data['deny'], str(deny))


def test__PermissionOverwrite__to_data__include_internals():
    """
    Tests whether `PermissionOverwrite.to_data(include_internal = True)` works as intended.
    """
    target_id = 202209140001
    target_type = PermissionOverwriteTargetType.user
    allow = 8
    deny = 12
    
    permission_overwrite = PermissionOverwrite(target_id, target_type = target_type, allow = allow, deny = deny)
    
    data = permission_overwrite.to_data(include_internals = True)
    
    vampytest.assert_in('id', data)
    vampytest.assert_in('type', data)
    vampytest.assert_in('allow', data)
    vampytest.assert_in('deny', data)

    vampytest.assert_eq(data['id'], str(target_id))
    vampytest.assert_eq(data['type'], target_type.value)
    vampytest.assert_eq(data['allow'], str(allow))
    vampytest.assert_eq(data['deny'], str(deny))
