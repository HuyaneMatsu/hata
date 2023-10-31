import vampytest

from ...audit_log import AuditLog
from ...audit_log_change import AuditLogChange
from ...audit_log_change.flags import FLAG_IS_MODIFICATION

from ..audit_log_entry import AuditLogEntry
from ..preinstanced import AuditLogEntryType

from .test__AuditLogEntry__constructor import _assert_fields_set


def test__AuditLogEntry__from_data():
    """
    Tests whether ``AuditLogEntry.from_data`` works as intended.
    
    Case: default.
    """
    entry_id = 202310290016
    
    changes = [AuditLogChange('name', FLAG_IS_MODIFICATION, after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290017
    reason = 'satori'
    target_id = 202310290018
    user_id = 202310290019
    
    parent = AuditLog(None, guild_id = guild_id)
    
    data = {
        'id': str(entry_id),
        'changes': [{'key': change.attribute_name, 'new_value': change.after} for change in changes],
        'options': {'members_removed': details['users_removed']},
        'action_type': entry_type.value,
        'guild_id': str(guild_id),
        'reason': reason,
        'target_id': str(target_id),
        'user_id': str(user_id),
    }
    
    audit_log_entry = AuditLogEntry.from_data(data, parent)
    
    _assert_fields_set(audit_log_entry)
    
    vampytest.assert_eq(audit_log_entry.id, entry_id)
    vampytest.assert_is(audit_log_entry.parent, parent)

    vampytest.assert_eq(audit_log_entry.changes, {change.attribute_name: change for change in changes})
    vampytest.assert_eq(audit_log_entry.details, details)
    vampytest.assert_eq(audit_log_entry.type, entry_type)
    vampytest.assert_eq(audit_log_entry.guild_id, guild_id)
    vampytest.assert_eq(audit_log_entry.reason, reason)
    vampytest.assert_eq(audit_log_entry.target_id, target_id)
    vampytest.assert_eq(audit_log_entry.user_id, user_id)


def test__AuditLogEntry__to_data():
    """
    Tests whether ``AuditLogEntry.to_data`` works as intended.
    
    Case: include defaults & internals.
    """
    entry_id = 202310290020
    
    changes = [AuditLogChange('name', FLAG_IS_MODIFICATION, after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290021
    reason = 'satori'
    target_id = 202310290022
    user_id = 202310290023
    
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
    
    expected_output = {
        'id': str(entry_id),
        'changes': [{'key': change.attribute_name, 'new_value': change.after} for change in changes],
        'options': {'members_removed': details['users_removed']},
        'action_type': entry_type.value,
        'guild_id': str(guild_id),
        'reason': reason,
        'target_id': str(target_id),
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        audit_log_entry.to_data(
            defaults = True,
        ),
        expected_output,
    )
