import vampytest
from scarletio import WeakReferer

from ....application_command import ApplicationCommand
from ....auto_moderation import AutoModerationRule
from ....channel import Channel, ChannelType
from ....integration import Integration
from ....scheduled_event import ScheduledEvent
from ....user import User
from ....webhook import Webhook

from ...audit_log_change import AuditLogChange
from ...audit_log_entry import AuditLogEntry, AuditLogEntryType

from ..audit_log import AuditLog


def _assert_fields_set(audit_log):
    """
    Asserts whether every fields are set of the given audit log.
    
    Parameters
    ----------
    audit_log : ``AuditLog``
        The audit log to check.
    """
    vampytest.assert_instance(audit_log, AuditLog)
    vampytest.assert_instance(audit_log._self_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(audit_log.application_commands, dict, nullable = True)
    vampytest.assert_instance(audit_log.auto_moderation_rules, dict, nullable = True)
    vampytest.assert_instance(audit_log.entries, list, nullable = True)
    vampytest.assert_instance(audit_log.guild_id, int)
    vampytest.assert_instance(audit_log.integrations, dict, nullable = True)
    vampytest.assert_instance(audit_log.scheduled_events, dict, nullable = True)
    vampytest.assert_instance(audit_log.threads, dict, nullable = True)
    vampytest.assert_instance(audit_log.users, dict, nullable = True)
    vampytest.assert_instance(audit_log.webhooks, dict, nullable = True)


def test__AuditLog__new__no_fields():
    """
    Tests whether ``AuditLog.__new__`` works as intended.
    
    Case: No fields given.
    """
    audit_log = AuditLog()
    _assert_fields_set(audit_log)


def test__AuditLog__new__all_fields():
    """
    Tests whether ``AuditLog.__new__`` works as intended.
    
    Case: All fields given.
    """
    guild_id = 202407010000
    
    application_commands = [
        ApplicationCommand.precreate(202407010001),
        ApplicationCommand.precreate(202407010002),
    ]
    
    auto_moderation_rules = [
        AutoModerationRule.precreate(202407010003),
        AutoModerationRule.precreate(202407010004),
    ]
    
    entries = [
        AuditLogEntry.precreate(
            202407010005,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = guild_id,
        ),
        AuditLogEntry.precreate(
            202407010006,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = guild_id,
        ),
    ]
    
    integrations = [
        Integration.precreate(202407010007),
        Integration.precreate(202407010008),
    ]
    
    scheduled_events = [
        ScheduledEvent.precreate(202407010009),
        ScheduledEvent.precreate(202407010010),
    ]
    
    threads = [
        Channel.precreate(202407010011, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
        Channel.precreate(202407010012, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
    ]
    
    users = [
        User.precreate(202407010013),
        User.precreate(202407010014),
    ]
    
    webhooks = [
        Webhook.precreate(202407010015),
        Webhook.precreate(202407010016),
    ]
    
    
    audit_log = AuditLog(
        application_commands = application_commands,
        auto_moderation_rules = auto_moderation_rules,
        entries = entries,
        guild_id = guild_id,
        integrations = integrations,
        scheduled_events = scheduled_events,
        threads = threads,
        users = users,
        webhooks = webhooks,
    )
    _assert_fields_set(audit_log)
    
    vampytest.assert_eq(
        audit_log.application_commands,
        {application_command.id: application_command for application_command in application_commands},
    )
    vampytest.assert_eq(
        audit_log.auto_moderation_rules,
        {auto_moderation_rule.id: auto_moderation_rule for auto_moderation_rule in auto_moderation_rules},
    )
    vampytest.assert_eq(
        audit_log.entries,
        entries,
    )
    vampytest.assert_eq(
        audit_log.guild_id,
        guild_id,
    )
    vampytest.assert_eq(
        audit_log.integrations,
        {integration.id: integration for integration in integrations},
    )
    vampytest.assert_eq(
        audit_log.scheduled_events,
        {scheduled_event.id: scheduled_event for scheduled_event in scheduled_events},
    )
    vampytest.assert_eq(
        audit_log.threads,
        {thread.id: thread for thread in threads},
    )
    vampytest.assert_eq(
        audit_log.users,
        {user.id: user for user in users},
    )
    vampytest.assert_eq(
        audit_log.webhooks,
        {webhook.id: webhook for webhook in webhooks},
    )
    
    for entry in entries:
        vampytest.assert_is(entry.parent, audit_log)



def test__AuditLog__from_many():
    """
    Tests whether ``AuditLog.from_many`` works as intended.
    """
    guild_id = 202407050000
    
    entries_0 = [
        AuditLogEntry.precreate(
            202407050001,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = guild_id,
        ),
        AuditLogEntry.precreate(
            202407050002,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = guild_id,
        ),
    ]
    
    entries_1 = [
        AuditLogEntry.precreate(
            202407050003,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'yuuka')],
            guild_id = guild_id,
        ),
        AuditLogEntry.precreate(
            202407050004,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'yukari')],
            guild_id = guild_id,
        ),
    ]
    
    audit_log_0 = AuditLog(entries = entries_0, guild_id = guild_id)
    audit_log_1 = AuditLog(entries = entries_1, guild_id = guild_id)
    
    audit_log = AuditLog.from_many([audit_log_0, audit_log_1])
    _assert_fields_set(audit_log)
    
    vampytest.assert_eq(audit_log.entries, [*entries_0, *entries_1])
    vampytest.assert_eq(audit_log.guild_id, guild_id)
