import vampytest

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

from .test__AuditLog__constructor import _assert_fields_set


def test__AuditLog__from_data():
    """
    Tests whether ``AuditLog.from_data`` works as intended.
    """
    guild_id = 202407010017
    
    application_commands = [
        ApplicationCommand.precreate(202407010018),
        ApplicationCommand.precreate(202407010019),
    ]
    
    auto_moderation_rules = [
        AutoModerationRule.precreate(202407010020),
        AutoModerationRule.precreate(202407010021),
    ]
    
    entries = [
        AuditLogEntry.precreate(
            202407010022,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = guild_id,
        ),
        AuditLogEntry.precreate(
            202407010023,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = guild_id,
        ),
    ]
    
    integrations = [
        Integration.precreate(202407010024),
        Integration.precreate(202407010025),
    ]
    
    scheduled_events = [
        ScheduledEvent.precreate(202407010026),
        ScheduledEvent.precreate(202407010027),
    ]
    
    threads = [
        Channel.precreate(202407010028, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
        Channel.precreate(202407010029, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
    ]
    
    users = [
        User.precreate(202407010030),
        User.precreate(202407010031),
    ]
    
    webhooks = [
        Webhook.precreate(202407010032),
        Webhook.precreate(202407010033),
    ]
    
    data = {
        'application_commands': [
            application_command.to_data(include_internals = True)
            for application_command in application_commands
        ],
        'auto_moderation_rules': [
            auto_moderation_rule.to_data(include_internals = True)
            for auto_moderation_rule in auto_moderation_rules
        ],
        'audit_log_entries': [
            entry.to_data()
            for entry in entries
        ],
        'integrations': [
            integration.to_data(include_internals = True)
            for integration in integrations
        ],
        'guild_scheduled_events': [
            scheduled_event.to_data(include_internals = True)
            for scheduled_event in scheduled_events
        ],
        'threads': [
            channel.to_data(include_internals = True)
            for channel in threads
        ],
        'users': [
            user.to_data(include_internals = True)
            for user in users
        ],
        'webhooks': [
            webhook.to_data(include_internals = True)
            for webhook in webhooks
        ],
    }
    
    audit_log = AuditLog.from_data(data, guild_id)
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
    
    for entry in audit_log.iter_entries():
        vampytest.assert_is(entry.parent, audit_log)


def test__AuditLog__to_data():
    """
    Tests whether ``AuditLog.to_data`` works as intended.
    
    Case: Include defaults.
    """
    guild_id = 202407010034
    
    application_commands = [
        ApplicationCommand.precreate(202407010035),
        ApplicationCommand.precreate(202407010036),
    ]
    
    auto_moderation_rules = [
        AutoModerationRule.precreate(202407010037),
        AutoModerationRule.precreate(202407010038),
    ]
    
    entries = [
        AuditLogEntry.precreate(
            202407010039,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = guild_id,
        ),
        AuditLogEntry.precreate(
            202407010040,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = guild_id,
        ),
    ]
    
    integrations = [
        Integration.precreate(202407010041),
        Integration.precreate(202407010042),
    ]
    
    scheduled_events = [
        ScheduledEvent.precreate(202407010043),
        ScheduledEvent.precreate(202407010044),
    ]
    
    threads = [
        Channel.precreate(202407010045, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
        Channel.precreate(202407010046, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
    ]
    
    users = [
        User.precreate(202407010047),
        User.precreate(202407010048),
    ]
    
    webhooks = [
        Webhook.precreate(202407010049),
        Webhook.precreate(202407010050),
    ]
    
    data = {
        'application_commands': [
            application_command.to_data(defaults = True, include_internals = True)
            for application_command in application_commands
        ],
        'auto_moderation_rules': [
            auto_moderation_rule.to_data(defaults = True, include_internals = True)
            for auto_moderation_rule in auto_moderation_rules
        ],
        'audit_log_entries': [
            entry.to_data(defaults = True)
            for entry in entries
        ],
        'integrations': [
            integration.to_data(defaults = True, include_internals = True)
            for integration in integrations
        ],
        'guild_scheduled_events': [
            scheduled_event.to_data(defaults = True, include_internals = True)
            for scheduled_event in scheduled_events
        ],
        'threads': [
            channel.to_data(defaults = True, include_internals = True)
            for channel in threads
        ],
        'users': [
            user.to_data(defaults = True, include_internals = True)
            for user in users
        ],
        'webhooks': [
            webhook.to_data(defaults = True, include_internals = True)
            for webhook in webhooks
        ],
    }
    
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
    
    vampytest.assert_eq(
        audit_log.to_data(defaults = True),
        data,
    )
