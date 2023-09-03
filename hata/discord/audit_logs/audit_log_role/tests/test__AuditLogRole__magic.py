import vampytest

from ..audit_log_role import AuditLogRole


def test__AuditLogRole__repr():
    """
    Tests whether ``AuditLogRole.__repr__`` works as intended.
    """
    role_id = 202308300003
    name = 'Red'
    
    
    audit_log_role = AuditLogRole(
        role_id = role_id,
        name = name,
    )
    
    vampytest.assert_instance(repr(audit_log_role), str)


def test__AuditLogRole__hash():
    """
    Tests whether ``AuditLogRole.__hash__`` works as intended.
    """
    role_id = 202308300004
    name = 'Red'
    
    audit_log_role = AuditLogRole(
        role_id = role_id,
        name = name,
    )
    
    vampytest.assert_instance(hash(audit_log_role), int)


def test__AuditLogRole__eq():
    """
    Tests whether ``AuditLogRole.__eq__`` works as intended.
    """
    role_id = 202308300005
    name = 'Red'
    
    keyword_parameters = {
        'role_id': role_id,
        'name': name,
    }
    
    audit_log_role = AuditLogRole(**keyword_parameters)
    
    vampytest.assert_eq(audit_log_role, audit_log_role)
    vampytest.assert_ne(audit_log_role, object())
    
    for field_name, field_value in (
        ('role_id', 202308300006),
        ('name', 'Suwako'),
    ):
        test_audit_log_role = AuditLogRole(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(audit_log_role, test_audit_log_role)
