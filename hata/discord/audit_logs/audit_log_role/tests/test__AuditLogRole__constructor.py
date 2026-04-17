import vampytest

from ..audit_log_role import AuditLogRole


def _assert_fields_set(audit_log_role):
    """
    Asserts whether every attributes of the given are set.
    
    Parameters
    ----------
    audit_log_role : ``AuditLogRole``
        The audit log role to check.
    """
    vampytest.assert_instance(audit_log_role, AuditLogRole)
    vampytest.assert_instance(audit_log_role.id, int)
    vampytest.assert_instance(audit_log_role.name, str)


def test__AuditLogRole__new__no_fields():
    """
    Tests whether ``AuditLogRole.__new__`` works as intended.
    
    Case: No parameters given.
    """
    audit_log_role = AuditLogRole()
    _assert_fields_set(audit_log_role)


def test__AuditLogRole__new__all_fields():
    """
    Tests whether ``AuditLogRole.__new__`` works as intended.
    
    Case: All parameters given.
    """
    role_id = 202308300000
    name = 'Red'
    
    audit_log_role = AuditLogRole(
        role_id = role_id,
        name = name,
    )
    _assert_fields_set(audit_log_role)
    
    vampytest.assert_eq(audit_log_role.id, role_id)
    vampytest.assert_eq(audit_log_role.name, name)
