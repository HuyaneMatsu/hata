import vampytest

from ....role import Role

from ..audit_log_role import AuditLogRole

from .test__AuditLogRole__constructor import _assert_fields_set


def test__AuditLogRole__copy():
    """
    Tests whether ``AuditLogRole.copy`` works as intended.
    """
    role_id = 202308300007
    name = 'Red'
    
    audit_log_role = AuditLogRole(
        role_id = role_id,
        name = name,
    )
    
    copy = audit_log_role.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, audit_log_role)
    vampytest.assert_not_is(copy, audit_log_role)


def test__AuditLogRole__copy_with__0():
    """
    Tests whether ``AuditLogRole.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    role_id = 202308300008
    name = 'Red'
    
    audit_log_role = AuditLogRole(
        role_id = role_id,
        name = name,
    )
    
    copy = audit_log_role.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, audit_log_role)
    vampytest.assert_not_is(copy, audit_log_role)


def test__AuditLogRole__copy_with__1():
    """
    Tests whether ``AuditLogRole.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_role_id = 202308300009
    old_name = 'Red'
    
    new_role_id = 202308300010
    new_name = 'Angel'
    
    
    audit_log_role = AuditLogRole(
        role_id = old_role_id,
        name = old_name,
    )
    
    copy = audit_log_role.copy_with(
        role_id = new_role_id,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_not_is(copy, audit_log_role)

    vampytest.assert_eq(copy.id, new_role_id)
    vampytest.assert_eq(copy.name, new_name)


def test__AuditLogRole__entity():
    """
    Tests whether ``AuditLogRole.entity`` works as intended.
    """
    role_id = 202308300011
    name = 'Red'
    
    audit_log_role = AuditLogRole(
        role_id = role_id,
        name = name,
    )
    
    role = audit_log_role.entity
    
    vampytest.assert_instance(role, Role)
    vampytest.assert_eq(role.id, role_id)
    vampytest.assert_eq(role.name, name)


def test__AuditLogRole__entity__caching():
    """
    Tests whether ``AuditLogRole.entity`` works as intended.
    
    Case: Check entity caching.
    """
    role_id = 202308300012
    name = 'Red'
    
    audit_log_role = AuditLogRole(
        role_id = role_id,
        name = name,
    )
    
    role = audit_log_role.entity
    test_role = audit_log_role.entity
    
    vampytest.assert_is(role, test_role)
