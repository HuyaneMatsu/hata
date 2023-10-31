import vampytest
from scarletio import WeakReferer

from ...audit_log import AuditLog
from ...audit_log_change import AuditLogChange
from ...audit_log_change.flags import FLAG_IS_MODIFICATION

from ..audit_log_entry import AuditLogEntry
from ..preinstanced import AuditLogEntryType


def _assert_fields_set(audit_log_entry):
    """
    Tests whether all attributes are set of the given audit_log_entry.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        The audit_log_entry to check.
    """
    vampytest.assert_instance(audit_log_entry, AuditLogEntry)
    vampytest.assert_instance(audit_log_entry._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(audit_log_entry.changes, dict, nullable = True)
    vampytest.assert_instance(audit_log_entry.details, dict, nullable = True)
    vampytest.assert_instance(audit_log_entry.guild_id, int)
    vampytest.assert_instance(audit_log_entry.id, int)
    vampytest.assert_instance(audit_log_entry.reason, str, nullable = True)
    vampytest.assert_instance(audit_log_entry.target_id, int)
    vampytest.assert_instance(audit_log_entry.type, AuditLogEntryType)
    vampytest.assert_instance(audit_log_entry.user_id, int)


def test__AuditLogEntry__new__no_fields():
    """
    Tests whether ``AuditLogEntry.__new__`` works as intended.
    
    Case: No fields given.
    """
    audit_log_entry = AuditLogEntry()
    _assert_fields_set(audit_log_entry)


def test__AuditLogEntry__new__all_fields():
    """
    Tests whether ``AuditLogEntry.__new__`` works as intended.
    
    Case: All fields given.
    """
    changes = [AuditLogChange('name', FLAG_IS_MODIFICATION, after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290008
    reason = 'satori'
    target_id = 202310290009
    user_id = 202310290010
    
    audit_log_entry = AuditLogEntry(
        changes = changes,
        details = details,
        entry_type = entry_type,
        guild_id = guild_id,
        reason = reason,
        target_id = target_id,
        user_id = user_id,
    )
    _assert_fields_set(audit_log_entry)
    
    vampytest.assert_eq(audit_log_entry.changes, {change.attribute_name: change for change in changes})
    vampytest.assert_eq(audit_log_entry.details, details)
    vampytest.assert_eq(audit_log_entry.type, entry_type)
    vampytest.assert_eq(audit_log_entry.guild_id, guild_id)
    vampytest.assert_eq(audit_log_entry.reason, reason)
    vampytest.assert_eq(audit_log_entry.target_id, target_id)
    vampytest.assert_eq(audit_log_entry.user_id, user_id)


def test__AuditLogEntry__precreate__no_fields():
    """
    Tests whether ``AuditLogEntry.precreate`` works as intended.
    
    Case: No fields given.
    """
    entry_id = 202310290011
    
    audit_log_entry = AuditLogEntry.precreate(entry_id)
    _assert_fields_set(audit_log_entry)
    
    vampytest.assert_eq(audit_log_entry.id, entry_id)


def test__AuditLogEntry__precreate__all_fields():
    """
    Tests whether ``AuditLogEntry.precreate`` works as intended.
    
    Case: All fields given.
    """
    entry_id = 202310290012
    parent = AuditLog(None)
    
    changes = [AuditLogChange('name', FLAG_IS_MODIFICATION, after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290013
    reason = 'satori'
    target_id = 202310290014
    user_id = 202310290015
    
    audit_log_entry = AuditLogEntry.precreate(
        entry_id,
        parent = parent,
        changes = changes,
        details = details,
        entry_type = entry_type,
        guild_id = guild_id,
        reason = reason,
        target_id = target_id,
        user_id = user_id,
    )
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
