import vampytest

from ....guild import Guild
from ....user import User, ClientUserBase

from ...audit_log import AuditLog
from ...audit_log_change import AuditLogChange

from ..audit_log_entry import AuditLogEntry
from ..preinstanced import AuditLogEntryType
from .test__AuditLogEntry__constructor import _assert_fields_set


def test__AuditLogEntry__copy():
    """
    Tests whether ``AuditLogEntry.copy`` works as intended.
    """
    changes = [AuditLogChange('name', after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290037
    reason = 'satori'
    target_id = 202310290038
    user_id = 202310290039
    
    audit_log_entry = AuditLogEntry(
        changes = changes,
        details = details,
        entry_type = entry_type,
        guild_id = guild_id,
        reason = reason,
        target_id = target_id,
        user_id = user_id,
    )
    copy = audit_log_entry.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(audit_log_entry, copy)
    
    vampytest.assert_eq(audit_log_entry, copy)


def test__AuditLogEntry__copy_with__no_fields():
    """
    Tests whether ``AuditLogEntry.copy_with`` works as intended.
    
    Case: no fields given.
    """
    changes = [AuditLogChange('name', after = 'koishi')]
    details = {'users_removed': 6}
    entry_type = AuditLogEntryType.guild_update
    guild_id = 202310290040
    reason = 'satori'
    target_id = 202310290041
    user_id = 202310290042
    
    audit_log_entry = AuditLogEntry(
        changes = changes,
        details = details,
        entry_type = entry_type,
        guild_id = guild_id,
        reason = reason,
        target_id = target_id,
        user_id = user_id,
    )
    copy = audit_log_entry.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(audit_log_entry, copy)
    
    vampytest.assert_eq(audit_log_entry, copy)


def test__AuditLogEntry__copy_with__all_fields():
    """
    Tests whether ``AuditLogEntry.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_changes = [AuditLogChange('name', after = 'koishi')]
    old_details = {'users_removed': 6}
    old_entry_type = AuditLogEntryType.guild_update
    old_guild_id = 202310290043
    old_reason = 'satori'
    old_target_id = 202310290044
    old_user_id = 202310290045
    
    new_changes = [AuditLogChange('name', after = 'orin')]
    new_details = {'status': 'party'}
    new_entry_type = AuditLogEntryType.channel_update
    new_guild_id = 202310290046
    new_reason = 'okuu'
    new_target_id = 202310290047
    new_user_id = 202310290048
    
    audit_log_entry = AuditLogEntry(
        changes = old_changes,
        details = old_details,
        entry_type = old_entry_type,
        guild_id = old_guild_id,
        reason = old_reason,
        target_id = old_target_id,
        user_id = old_user_id,
    )
    
    copy = audit_log_entry.copy_with(
        changes = new_changes,
        details = new_details,
        entry_type = new_entry_type,
        guild_id = new_guild_id,
        reason = new_reason,
        target_id = new_target_id,
        user_id = new_user_id,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(audit_log_entry, copy)

    vampytest.assert_eq(copy.changes, {change.attribute_name: change for change in new_changes})
    vampytest.assert_eq(copy.details, new_details)
    vampytest.assert_eq(copy.type, new_entry_type)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.reason, new_reason)
    vampytest.assert_eq(copy.target_id, new_target_id)
    vampytest.assert_eq(copy.user_id, new_user_id)


def _iter_options__target():
    yield AuditLogEntry(), None
    
    target_id = 202310300006
    yield AuditLogEntry(entry_type = AuditLogEntryType.user_update, target_id = target_id), User.precreate(target_id)


@vampytest._(vampytest.call_from(_iter_options__target()).returning_last())
def test_AuditLogEntry__target(audit_log_entry):
    """
    Tests whether ``AuditLogEntry.target`` works as intended.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        Entry to get its target of.
    
    Returns
    -------
    output : `None | ClientUserBase`
    """
    return audit_log_entry.target


def _iter_options__parent():
    yield AuditLogEntry(), None
    
    parent = AuditLog(None)
    yield AuditLogEntry.precreate(202310300007, parent = parent), parent


@vampytest._(vampytest.call_from(_iter_options__parent()).returning_last())
def test_AuditLogEntry__parent(audit_log_entry):
    """
    Tests whether ``AuditLogEntry.parent`` works as intended.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        Entry to get its parent of.
    
    Returns
    -------
    output : `None | AuditLog`
    """
    return audit_log_entry.parent


def _iter_options__guild():
    yield AuditLogEntry(), None
    yield AuditLogEntry(guild_id = 202310300010), None
    
    guild_id = 202310300011
    yield AuditLogEntry(guild_id = guild_id), Guild.precreate(guild_id)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test_AuditLogEntry__guild(audit_log_entry):
    """
    Tests whether ``AuditLogEntry.guild`` works as intended.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        Entry to get its guild of.
    
    Returns
    -------
    output : `None | Guild`
    """
    return audit_log_entry.guild


def _iter_options__user():
    yield AuditLogEntry(), None
    
    user_id = 202310300012
    yield AuditLogEntry(user_id = user_id), User.precreate(user_id)


@vampytest._(vampytest.call_from(_iter_options__user()).returning_last())
def test_AuditLogEntry__user(audit_log_entry):
    """
    Tests whether ``AuditLogEntry.user`` works as intended.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        Entry to get its user of.
    
    Returns
    -------
    output : `None | ClientUserBase`
    """
    return audit_log_entry.user


def _iter_options__get_change():
    yield AuditLogEntry(), 'name', None
    
    change_0 = AuditLogChange('description', after = None)
    change_1 = AuditLogChange('name', after = 'mister')
    
    yield (
        AuditLogEntry(
            entry_type = AuditLogEntryType.guild_update,
            changes = [change_0],
        ),
        'name',
        None,
    )

    yield (
        AuditLogEntry(
            entry_type = AuditLogEntryType.guild_update,
            changes = [change_0, change_1],
        ),
        'name',
        change_1,
    )


@vampytest._(vampytest.call_from(_iter_options__get_change()).returning_last())
def test_AuditLogEntry__get_change(audit_log_entry, attribute_name):
    """
    Tests whether ``AuditLogEntry.get_change`` works as intended.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        Entry to get its change of.
    attribute_name : `str`
        Attribute name to get change for.
    
    Returns
    -------
    output : `None | AuditLogChange`
    """
    return audit_log_entry.get_change(attribute_name)


def _iter_options__iter_changes():
    yield AuditLogEntry(), set()
    
    change_0 = AuditLogChange('description', after = None)
    change_1 = AuditLogChange('name', after = 'mister')
    
    yield (
        AuditLogEntry(
            entry_type = AuditLogEntryType.guild_update,
            changes = [change_0],
        ),
        {change_0},
    )

    yield (
        AuditLogEntry(
            entry_type = AuditLogEntryType.guild_update,
            changes = [change_0, change_1],
        ),
        {change_0, change_1},
    )


@vampytest._(vampytest.call_from(_iter_options__iter_changes()).returning_last())
def test_AuditLogEntry__iter_changes(audit_log_entry):
    """
    Tests whether ``AuditLogEntry.iter_changes`` works as intended.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        Entry to to iter its changes of.
    
    Returns
    -------
    output : `set<AuditLogChange>`
    """
    return {*audit_log_entry.iter_changes()}



def _iter_options__get_detail():
    yield AuditLogEntry(), 'users_removed', None
    
    detail_0 = ('days', 60)
    detail_1 = ('users_removed', 2)
    
    yield (
        AuditLogEntry(
            entry_type = AuditLogEntryType.guild_update,
            details = dict([detail_0]),
        ),
        'users_removed',
        None,
    )

    yield (
        AuditLogEntry(
            entry_type = AuditLogEntryType.guild_update,
            details = dict([detail_0, detail_1]),
        ),
        'users_removed',
        detail_1[1],
    )


@vampytest._(vampytest.call_from(_iter_options__get_detail()).returning_last())
def test_AuditLogEntry__get_detail(audit_log_entry, name):
    """
    Tests whether ``AuditLogEntry.get_detail`` works as intended.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        Entry to get its detail of.
    name : `str`
        The detail's name.
    
    Returns
    -------
    output : `None | object`
    """
    return audit_log_entry.get_detail(name)


def _iter_options__iter_details():
    yield AuditLogEntry(), set()
    
    detail_0 = ('days', 60)
    detail_1 = ('users_removed', 2)
    
    yield (
        AuditLogEntry(
            entry_type = AuditLogEntryType.guild_update,
            details = dict([detail_0]),
        ),
        {detail_0},
    )

    yield (
        AuditLogEntry(
            entry_type = AuditLogEntryType.guild_update,
            details = dict([detail_0, detail_1]),
        ),
        {detail_0, detail_1},
    )


@vampytest._(vampytest.call_from(_iter_options__iter_details()).returning_last())
def test_AuditLogEntry__iter_details(audit_log_entry):
    """
    Tests whether ``AuditLogEntry.iter_details`` works as intended.
    
    Parameters
    ----------
    audit_log_entry : ``AuditLogEntry``
        Entry to to iter its details of.
    
    Returns
    -------
    output : `set<(str, object)>`
    """
    return {*audit_log_entry.iter_details()}
