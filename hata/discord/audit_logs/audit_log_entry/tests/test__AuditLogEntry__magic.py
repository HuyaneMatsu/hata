import vampytest

from ...audit_log import AuditLog
from ...audit_log_change import AuditLogChange
from ...audit_log_change.flags import FLAG_IS_MODIFICATION

from ..audit_log_entry import AuditLogEntry
from ..preinstanced import AuditLogEntryType


def test__AuditLogEntry__repr():
    """
    Tests whether ``AuditLogEntry.__repr__`` works as intended.
    """
    entry_id = 202310290024
    
    changes = [AuditLogChange('name', FLAG_IS_MODIFICATION, after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290025
    reason = 'satori'
    target_id = 202310290026
    user_id = 202310290027
    
    audit_log_entry = AuditLogEntry.precreate(
        entry_id,
        changes = changes,
        details = details,
        entry_type = entry_type,
        guild_id = guild_id,
        reason = reason,
        target_id = target_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(audit_log_entry), str)


def test__AuditLogEntry__hash():
    """
    Tests whether ``AuditLogEntry.__hash__`` works as intended.
    """
    entry_id = 202310290028
    
    changes = [AuditLogChange('name', FLAG_IS_MODIFICATION, after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290029
    reason = 'satori'
    target_id = 202310290030
    user_id = 202310290031
    
    audit_log_entry = AuditLogEntry.precreate(
        entry_id,
        changes = changes,
        details = details,
        entry_type = entry_type,
        guild_id = guild_id,
        reason = reason,
        target_id = target_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(audit_log_entry), int)


def test__AuditLogEntry__eq():
    """
    Tests whether ``AuditLogEntry.__eq__`` works as intended.
    """
    entry_id = 202310290032
    
    changes = [AuditLogChange('name', FLAG_IS_MODIFICATION, after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290033
    reason = 'satori'
    target_id = 202310290034
    user_id = 202310290035
    
    keyword_parameters = {
        'changes': changes,
        'details': details,
        'entry_type': entry_type,
        'guild_id': guild_id,
        'reason': reason,
        'target_id': target_id,
        'user_id': user_id,
    }
    
    audit_log_entry = AuditLogEntry.precreate(
        entry_id,
        **keyword_parameters,
    )
    
    vampytest.assert_eq(audit_log_entry, audit_log_entry)
    vampytest.assert_ne(audit_log_entry, object())
    
    # Since we do a shortcut check, we create the same audit_log_entry twice
    test_audit_log_entry = AuditLogEntry.precreate(
        entry_id,
        **keyword_parameters,
    )
    vampytest.assert_eq(audit_log_entry, test_audit_log_entry)
    
    test_audit_log_entry = AuditLogEntry(**keyword_parameters)
    vampytest.assert_eq(audit_log_entry, test_audit_log_entry)
    
    for field_name, field_value in (
        ('changes', None),
        ('details', None),
        # ('entry_type' entry_type), -> since other fields depend on this, skip
        ('guild_id', 0),
        ('reason', None),
        ('target_id', 0),
        ('user_id', 0),
    ):
        test_audit_log_entry = AuditLogEntry(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(audit_log_entry, test_audit_log_entry)
