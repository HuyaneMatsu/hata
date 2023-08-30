import vampytest

from ..audit_log_role import AuditLogRole

from .test__AuditLogRole__constructor import _assert_fields_set


def test__AuditLogRole__from_data():
    """
    Tests whether ``AuditLogRole.from_data`` works as intended.
    
    Case: Default.
    """
    role_id = 202308300001
    name = 'Red'
    
    data = {
        'id': str(role_id),
        'name': name,
    }
    
    audit_log_role = AuditLogRole.from_data(data)
    _assert_fields_set(audit_log_role)
    
    vampytest.assert_eq(audit_log_role.id, role_id)
    vampytest.assert_eq(audit_log_role.name, name)


def test__AuditLogRole__to_data():
    """
    Tests whether ``AuditLogRole.to_data`` works as intended.
    
    Case: include defaults.
    """
    role_id = 202308300002
    name = 'Red'
    
    expected_output = {
        'id': str(role_id),
        'name': name,
    }
    
    audit_log_role = AuditLogRole(
        role_id = role_id,
        name = name,
    )
    
    vampytest.assert_eq(audit_log_role.to_data(defaults = True), expected_output)
