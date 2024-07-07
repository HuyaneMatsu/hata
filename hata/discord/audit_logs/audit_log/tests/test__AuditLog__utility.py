import vampytest
from scarletio import WeakReferer

from ....application_command import ApplicationCommand
from ....auto_moderation import AutoModerationRule
from ....channel import Channel, ChannelType
from ....guild import Guild
from ....integration import Integration
from ....scheduled_event import ScheduledEvent
from ....user import User
from ....webhook import Webhook

from ...audit_log_change import AuditLogChange
from ...audit_log_entry import AuditLogEntry, AuditLogEntryType

from ..audit_log import AuditLog

from .test__AuditLog__constructor import _assert_fields_set 


def test__AuditLog__copy():
    """
    Tests whether ``AuditLog.copy`` works as intended.
    """
    guild_id = 202407010118
    
    application_commands = [
        ApplicationCommand.precreate(202407010119),
        ApplicationCommand.precreate(202407010120),
    ]
    
    auto_moderation_rules = [
        AutoModerationRule.precreate(202407010121),
        AutoModerationRule.precreate(202407010122),
    ]
    
    entries = [
        AuditLogEntry.precreate(
            202407010123,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = guild_id,
        ),
        AuditLogEntry.precreate(
            202407010124,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = guild_id,
        ),
    ]
    
    integrations = [
        Integration.precreate(202407010125),
        Integration.precreate(202407010126),
    ]
    
    scheduled_events = [
        ScheduledEvent.precreate(202407010127),
        ScheduledEvent.precreate(202407010128),
    ]
    
    threads = [
        Channel.precreate(202407010129, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
        Channel.precreate(202407010130, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
    ]
    
    users = [
        User.precreate(202407010131),
        User.precreate(202407010132),
    ]
    
    webhooks = [
        Webhook.precreate(202407010133),
        Webhook.precreate(202407010134),
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
    
    copy = audit_log.copy()
    vampytest.assert_is_not(audit_log, copy)
    _assert_fields_set(copy)
    vampytest.assert_eq(audit_log, copy)


def test__AuditLog__copy_with__no_fields():
    """
    Tests whether ``AuditLog.copy_with`` works as intended.
    
    Case: No fields given.
    """
    guild_id = 202407010135
    
    application_commands = [
        ApplicationCommand.precreate(202407010136),
        ApplicationCommand.precreate(202407010137),
    ]
    
    auto_moderation_rules = [
        AutoModerationRule.precreate(202407010138),
        AutoModerationRule.precreate(202407010139),
    ]
    
    entries = [
        AuditLogEntry.precreate(
            202407010140,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = guild_id,
        ),
        AuditLogEntry.precreate(
            202407010141,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = guild_id,
        ),
    ]
    
    integrations = [
        Integration.precreate(202407010142),
        Integration.precreate(202407010143),
    ]
    
    scheduled_events = [
        ScheduledEvent.precreate(202407010144),
        ScheduledEvent.precreate(202407010145),
    ]
    
    threads = [
        Channel.precreate(202407010146, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
        Channel.precreate(202407010147, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
    ]
    
    users = [
        User.precreate(202407010148),
        User.precreate(202407010149),
    ]
    
    webhooks = [
        Webhook.precreate(202407010150),
        Webhook.precreate(202407010151),
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
    
    copy = audit_log.copy_with()
    vampytest.assert_is_not(audit_log, copy)
    _assert_fields_set(copy)
    vampytest.assert_eq(audit_log, copy)



def test__AuditLog__copy_with__all_fields():
    """
    Tests whether ``AuditLog.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_guild_id = 202407010135
    
    old_application_commands = [
        ApplicationCommand.precreate(202407010136),
        ApplicationCommand.precreate(202407010137),
    ]
    
    old_auto_moderation_rules = [
        AutoModerationRule.precreate(202407010138),
        AutoModerationRule.precreate(202407010139),
    ]
    
    old_entries = [
        AuditLogEntry.precreate(
            202407010140,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = old_guild_id,
        ),
        AuditLogEntry.precreate(
            202407010141,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = old_guild_id,
        ),
    ]
    
    old_integrations = [
        Integration.precreate(202407010142),
        Integration.precreate(202407010143),
    ]
    
    old_scheduled_events = [
        ScheduledEvent.precreate(202407010144),
        ScheduledEvent.precreate(202407010145),
    ]
    
    old_threads = [
        Channel.precreate(202407010146, channel_type = ChannelType.guild_thread_private, guild_id = old_guild_id),
        Channel.precreate(202407010147, channel_type = ChannelType.guild_thread_private, guild_id = old_guild_id),
    ]
    
    old_users = [
        User.precreate(202407010148),
        User.precreate(202407010149),
    ]
    
    old_webhooks = [
        Webhook.precreate(202407010150),
        Webhook.precreate(202407010151),
    ]
    
    new_guild_id = 202407010152
    
    new_application_commands = [
        ApplicationCommand.precreate(202407010153),
        ApplicationCommand.precreate(202407010154),
    ]
    
    new_auto_moderation_rules = [
        AutoModerationRule.precreate(202407010155),
        AutoModerationRule.precreate(202407010156),
    ]
    
    new_entries = [
        AuditLogEntry.precreate(
            202407010157,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'yukari')],
            guild_id = new_guild_id,
        ),
        AuditLogEntry.precreate(
            202407010158,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'yuuka')],
            guild_id = new_guild_id,
        ),
    ]
    
    new_integrations = [
        Integration.precreate(202407010159),
        Integration.precreate(202407010160),
    ]
    
    new_scheduled_events = [
        ScheduledEvent.precreate(202407010161),
        ScheduledEvent.precreate(202407010162),
    ]
    
    new_threads = [
        Channel.precreate(202407010163, channel_type = ChannelType.guild_thread_private, guild_id = new_guild_id),
        Channel.precreate(202407010164, channel_type = ChannelType.guild_thread_private, guild_id = new_guild_id),
    ]
    
    new_users = [
        User.precreate(202407010165),
        User.precreate(202407010166),
    ]
    
    new_webhooks = [
        Webhook.precreate(202407010167),
        Webhook.precreate(202407010168),
    ]
    
    audit_log = AuditLog(
        application_commands = old_application_commands,
        auto_moderation_rules = old_auto_moderation_rules,
        entries = old_entries,
        guild_id = old_guild_id,
        integrations = old_integrations,
        scheduled_events = old_scheduled_events,
        threads = old_threads,
        users = old_users,
        webhooks = old_webhooks,
    )
    
    copy = audit_log.copy_with(
        application_commands = new_application_commands,
        auto_moderation_rules = new_auto_moderation_rules,
        entries = new_entries,
        guild_id = new_guild_id,
        integrations = new_integrations,
        scheduled_events = new_scheduled_events,
        threads = new_threads,
        users = new_users,
        webhooks = new_webhooks,
    )
    vampytest.assert_is_not(audit_log, copy)
    _assert_fields_set(copy)
    vampytest.assert_ne(audit_log, copy)
    
    vampytest.assert_eq(
        copy.application_commands,
        {application_command.id: application_command for application_command in new_application_commands},
    )
    vampytest.assert_eq(
        copy.auto_moderation_rules,
        {auto_moderation_rule.id: auto_moderation_rule for auto_moderation_rule in new_auto_moderation_rules},
    )
    vampytest.assert_eq(
        copy.entries,
        new_entries,
    )
    vampytest.assert_eq(
        copy.guild_id,
        new_guild_id,
    )
    vampytest.assert_eq(
        copy.integrations,
        {integration.id: integration for integration in new_integrations},
    )
    vampytest.assert_eq(
        copy.scheduled_events,
        {scheduled_event.id: scheduled_event for scheduled_event in new_scheduled_events},
    )
    vampytest.assert_eq(
        copy.threads,
        {thread.id: thread for thread in new_threads},
    )
    vampytest.assert_eq(
        copy.users,
        {user.id: user for user in new_users},
    )
    vampytest.assert_eq(
        copy.webhooks,
        {webhook.id: webhook for webhook in new_webhooks},
    )
    
    for entry in new_entries:
        vampytest.assert_is(entry.parent, copy)



def test__AuditLog__get_self_reference():
    """
    Tests whether ``AuditLog._get_self_reference`` works as intended.
    """
    audit_log = AuditLog()
    
    self_reference_0 = audit_log._get_self_reference()
    vampytest.assert_instance(self_reference_0, WeakReferer)
    
    self_reference_1 = audit_log._get_self_reference()
    vampytest.assert_instance(self_reference_1, WeakReferer)
    
    vampytest.assert_is(self_reference_0, self_reference_1)


def _iter_options__guild():
    guild_id = 0
    yield guild_id, None
    
    guild_id = 202407010169
    yield guild_id, None
    
    guild_id = 202407010170
    yield guild_id, Guild.precreate(guild_id)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__AuditLog__guild(guild_id):
    """
    Tests whether ``AuditLog.guild`` works as intended.
    
    Parameters
    ----------
    role_id : `int`
        Identifier to create the role with.
    guild_id : `int`
        Guild identifier to create the audit log with.
    
    Returns
    -------
    output : `None | Guild`
    """
    role = AuditLog(guild_id = guild_id)
    output = role.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output


def _iter_options__get_application_command():
    application_command_id_0 = 202407010171
    application_command_id_1 = 202407010172
    
    application_command_0 = ApplicationCommand.precreate(application_command_id_0)
    application_command_1 = ApplicationCommand.precreate(application_command_id_1)
    
    yield None, application_command_id_0, None
    yield [application_command_0], application_command_id_0, application_command_0
    yield [application_command_0], application_command_id_1, None
    yield [application_command_0, application_command_1], application_command_id_1, application_command_1


@vampytest._(vampytest.call_from(_iter_options__get_application_command()).returning_last())
def test__AuditLog__get_application_command(application_commands, application_command_id):
    """
    Tests whether ``AuditLog.get_application_command`` works as intended.
    
    Parameters
    ----------
    application_commands : `None | list<ApplicationCommand>`
        Application commands to create the audit log with.
    application_command_id : `int`
        Application command identifier.
    
    Returns
    -------
    output : `None | ApplicationCommand`
    """
    audit_log = AuditLog(application_commands = application_commands)
    output = audit_log.get_application_command(application_command_id)
    vampytest.assert_instance(output, ApplicationCommand, nullable = True)
    return output


def _iter_options__iter_application_command():
    application_command_id_0 = 202407010173
    application_command_id_1 = 202407010174
    
    application_command_0 = ApplicationCommand.precreate(application_command_id_0)
    application_command_1 = ApplicationCommand.precreate(application_command_id_1)
    
    yield None, set()
    yield [application_command_0], {application_command_0}
    yield [application_command_0, application_command_1], {application_command_0, application_command_1}


@vampytest._(vampytest.call_from(_iter_options__iter_application_command()).returning_last())
def test__AuditLog__iter_application_command(application_commands):
    """
    Tests whether ``AuditLog.iter_application_command`` works as intended.
    
    Parameters
    ----------
    application_commands : `None | list<ApplicationCommand>`
        Application commands to create the audit log with.
    
    Returns
    -------
    output : `set<ApplicationCommand>`
    """
    audit_log = AuditLog(application_commands = application_commands)
    return {*audit_log.iter_application_commands()}


def _iter_options__get_auto_moderation_rule():
    auto_moderation_rule_id_0 = 202407010175
    auto_moderation_rule_id_1 = 202407010176
    
    auto_moderation_rule_0 = AutoModerationRule.precreate(auto_moderation_rule_id_0)
    auto_moderation_rule_1 = AutoModerationRule.precreate(auto_moderation_rule_id_1)
    
    yield None, auto_moderation_rule_id_0, None
    yield [auto_moderation_rule_0], auto_moderation_rule_id_0, auto_moderation_rule_0
    yield [auto_moderation_rule_0], auto_moderation_rule_id_1, None
    yield [auto_moderation_rule_0, auto_moderation_rule_1], auto_moderation_rule_id_1, auto_moderation_rule_1


@vampytest._(vampytest.call_from(_iter_options__get_auto_moderation_rule()).returning_last())
def test__AuditLog__get_auto_moderation_rule(auto_moderation_rules, auto_moderation_rule_id):
    """
    Tests whether ``AuditLog.get_auto_moderation_rule`` works as intended.
    
    Parameters
    ----------
    auto_moderation_rules : `None | list<AutoModerationRule>`
        Auto moderation rules to create the audit log with.
    auto_moderation_rule_id : `int`
        Auto moderation rule identifier.
    
    Returns
    -------
    output : `None | AutoModerationRule`
    """
    audit_log = AuditLog(auto_moderation_rules = auto_moderation_rules)
    output = audit_log.get_auto_moderation_rule(auto_moderation_rule_id)
    vampytest.assert_instance(output, AutoModerationRule, nullable = True)
    return output


def _iter_options__iter_auto_moderation_rule():
    auto_moderation_rule_id_0 = 202407010177
    auto_moderation_rule_id_1 = 202407010178
    
    auto_moderation_rule_0 = AutoModerationRule.precreate(auto_moderation_rule_id_0)
    auto_moderation_rule_1 = AutoModerationRule.precreate(auto_moderation_rule_id_1)
    
    yield None, set()
    yield [auto_moderation_rule_0], {auto_moderation_rule_0}
    yield [auto_moderation_rule_0, auto_moderation_rule_1], {auto_moderation_rule_0, auto_moderation_rule_1}


@vampytest._(vampytest.call_from(_iter_options__iter_auto_moderation_rule()).returning_last())
def test__AuditLog__iter_auto_moderation_rule(auto_moderation_rules):
    """
    Tests whether ``AuditLog.iter_auto_moderation_rule`` works as intended.
    
    Parameters
    ----------
    auto_moderation_rules : `None | list<AutoModerationRule>`
        Auto moderation rules to create the audit log with.
    
    Returns
    -------
    output : `set<AutoModerationRule>`
    """
    audit_log = AuditLog(auto_moderation_rules = auto_moderation_rules)
    return {*audit_log.iter_auto_moderation_rules()}


def _iter_options__iter_integration():
    integration_id_0 = 202407010179
    integration_id_1 = 202407010180
    
    integration_0 = Integration.precreate(integration_id_0)
    integration_1 = Integration.precreate(integration_id_1)
    
    yield None, set()
    yield [integration_0], {integration_0}
    yield [integration_0, integration_1], {integration_0, integration_1}


@vampytest._(vampytest.call_from(_iter_options__iter_integration()).returning_last())
def test__AuditLog__iter_integration(integrations):
    """
    Tests whether ``AuditLog.iter_integration`` works as intended.
    
    Parameters
    ----------
    integrations : `None | list<Integration>`
        Integrations to create the audit log with.
    
    Returns
    -------
    output : `set<Integration>`
    """
    audit_log = AuditLog(integrations = integrations)
    return {*audit_log.iter_integrations()}


def _iter_options__get_auto_moderation_rule():
    auto_moderation_rule_id_0 = 202407010181
    auto_moderation_rule_id_1 = 202407010182
    
    auto_moderation_rule_0 = AutoModerationRule.precreate(auto_moderation_rule_id_0)
    auto_moderation_rule_1 = AutoModerationRule.precreate(auto_moderation_rule_id_1)
    
    yield None, auto_moderation_rule_id_0, None
    yield [auto_moderation_rule_0], auto_moderation_rule_id_0, auto_moderation_rule_0
    yield [auto_moderation_rule_0], auto_moderation_rule_id_1, None
    yield [auto_moderation_rule_0, auto_moderation_rule_1], auto_moderation_rule_id_1, auto_moderation_rule_1



def _iter_options__get_scheduled_event():
    scheduled_event_id_0 = 202407010183
    scheduled_event_id_1 = 202407010184
    
    scheduled_event_0 = ScheduledEvent.precreate(scheduled_event_id_0)
    scheduled_event_1 = ScheduledEvent.precreate(scheduled_event_id_1)
    
    yield None, scheduled_event_id_0, None
    yield [scheduled_event_0], scheduled_event_id_0, scheduled_event_0
    yield [scheduled_event_0], scheduled_event_id_1, None
    yield [scheduled_event_0, scheduled_event_1], scheduled_event_id_1, scheduled_event_1


@vampytest._(vampytest.call_from(_iter_options__get_scheduled_event()).returning_last())
def test__AuditLog__get_scheduled_event(scheduled_events, scheduled_event_id):
    """
    Tests whether ``AuditLog.get_scheduled_event`` works as intended.
    
    Parameters
    ----------
    scheduled_events : `None | list<ScheduledEvent>`
        Scheduled events to create the audit log with.
    scheduled_event_id : `int`
        Scheduled event identifier.
    
    Returns
    -------
    output : `None | ScheduledEvent`
    """
    audit_log = AuditLog(scheduled_events = scheduled_events)
    output = audit_log.get_scheduled_event(scheduled_event_id)
    vampytest.assert_instance(output, ScheduledEvent, nullable = True)
    return output


def _iter_options__iter_scheduled_event():
    scheduled_event_id_0 = 202407010185
    scheduled_event_id_1 = 202407010186
    
    scheduled_event_0 = ScheduledEvent.precreate(scheduled_event_id_0)
    scheduled_event_1 = ScheduledEvent.precreate(scheduled_event_id_1)
    
    yield None, set()
    yield [scheduled_event_0], {scheduled_event_0}
    yield [scheduled_event_0, scheduled_event_1], {scheduled_event_0, scheduled_event_1}


@vampytest._(vampytest.call_from(_iter_options__iter_scheduled_event()).returning_last())
def test__AuditLog__iter_scheduled_event(scheduled_events):
    """
    Tests whether ``AuditLog.iter_scheduled_event`` works as intended.
    
    Parameters
    ----------
    scheduled_events : `None | list<ScheduledEvent>`
        Scheduled events to create the audit log with.
    
    Returns
    -------
    output : `set<ScheduledEvent>`
    """
    audit_log = AuditLog(scheduled_events = scheduled_events)
    return {*audit_log.iter_scheduled_events()}


def _iter_options__get_thread():
    thread_id_0 = 202407010187
    thread_id_1 = 202407010188
    guild_id = 202407010189
    
    thread_0 = Channel.precreate(thread_id_0, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    thread_1 = Channel.precreate(thread_id_1, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    
    yield None, thread_id_0, None
    yield [thread_0], thread_id_0, thread_0
    yield [thread_0], thread_id_1, None
    yield [thread_0, thread_1], thread_id_1, thread_1


@vampytest._(vampytest.call_from(_iter_options__get_thread()).returning_last())
def test__AuditLog__get_thread(threads, thread_id):
    """
    Tests whether ``AuditLog.get_thread`` works as intended.
    
    Parameters
    ----------
    threads : `None | list<Channel>`
        Threads to create the audit log with.
    thread_id : `int`
        Thread identifier.
    
    Returns
    -------
    output : `None | Channel`
    """
    audit_log = AuditLog(threads = threads)
    output = audit_log.get_thread(thread_id)
    vampytest.assert_instance(output, Channel, nullable = True)
    return output


def _iter_options__iter_thread():
    thread_id_0 = 202407010190
    thread_id_1 = 202407010191
    guild_id = 202407010192
    
    thread_0 = Channel.precreate(thread_id_0, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    thread_1 = Channel.precreate(thread_id_1, channel_type = ChannelType.guild_thread_public, guild_id = guild_id)
    
    yield None, set()
    yield [thread_0], {thread_0}
    yield [thread_0, thread_1], {thread_0, thread_1}


@vampytest._(vampytest.call_from(_iter_options__iter_thread()).returning_last())
def test__AuditLog__iter_thread(threads):
    """
    Tests whether ``AuditLog.iter_thread`` works as intended.
    
    Parameters
    ----------
    threads : `None | list<Channel>`
        Threads to create the audit log with.
    
    Returns
    -------
    output : `set<Channel>`
    """
    audit_log = AuditLog(threads = threads)
    return {*audit_log.iter_threads()}


def _iter_options__get_user():
    user_id_0 = 202407010193
    user_id_1 = 202407010194
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield None, user_id_0, None
    yield [user_0], user_id_0, user_0
    yield [user_0], user_id_1, None
    yield [user_0, user_1], user_id_1, user_1


@vampytest._(vampytest.call_from(_iter_options__get_user()).returning_last())
def test__AuditLog__get_user(users, user_id):
    """
    Tests whether ``AuditLog.get_user`` works as intended.
    
    Parameters
    ----------
    users : `None | list<ClientUserBase>`
        Users to create the audit log with.
    user_id : `int`
        User identifier.
    
    Returns
    -------
    output : `None | ClientUserBase`
    """
    audit_log = AuditLog(users = users)
    output = audit_log.get_user(user_id)
    vampytest.assert_instance(output, User, nullable = True)
    return output


def _iter_options__iter_user():
    user_id_0 = 202407010195
    user_id_1 = 202407010196
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield None, set()
    yield [user_0], {user_0}
    yield [user_0, user_1], {user_0, user_1}


@vampytest._(vampytest.call_from(_iter_options__iter_user()).returning_last())
def test__AuditLog__iter_user(users):
    """
    Tests whether ``AuditLog.iter_user`` works as intended.
    
    Parameters
    ----------
    users : `None | list<ClientUserBase>`
        Users to create the audit log with.
    
    Returns
    -------
    output : `set<ClientUserBase>`
    """
    audit_log = AuditLog(users = users)
    return {*audit_log.iter_users()}


def _iter_options__get_webhook():
    webhook_id_0 = 202407010197
    webhook_id_1 = 202407010198
    
    webhook_0 = Webhook.precreate(webhook_id_0)
    webhook_1 = Webhook.precreate(webhook_id_1)
    
    yield None, webhook_id_0, None
    yield [webhook_0], webhook_id_0, webhook_0
    yield [webhook_0], webhook_id_1, None
    yield [webhook_0, webhook_1], webhook_id_1, webhook_1


@vampytest._(vampytest.call_from(_iter_options__get_webhook()).returning_last())
def test__AuditLog__get_webhook(webhooks, webhook_id):
    """
    Tests whether ``AuditLog.get_webhook`` works as intended.
    
    Parameters
    ----------
    webhooks : `None | list<Webhook>`
        Webhooks to create the audit log with.
    webhook_id : `int`
        Webhook identifier.
    
    Returns
    -------
    output : `None | Webhook`
    """
    audit_log = AuditLog(webhooks = webhooks)
    output = audit_log.get_webhook(webhook_id)
    vampytest.assert_instance(output, Webhook, nullable = True)
    return output


def _iter_options__iter_webhook():
    webhook_id_0 = 202407010199
    webhook_id_1 = 202407010200
    
    webhook_0 = Webhook.precreate(webhook_id_0)
    webhook_1 = Webhook.precreate(webhook_id_1)
    
    yield None, set()
    yield [webhook_0], {webhook_0}
    yield [webhook_0, webhook_1], {webhook_0, webhook_1}


@vampytest._(vampytest.call_from(_iter_options__iter_webhook()).returning_last())
def test__AuditLog__iter_webhook(webhooks):
    """
    Tests whether ``AuditLog.iter_webhook`` works as intended.
    
    Parameters
    ----------
    webhooks : `None | list<Webhook>`
        Webhooks to create the audit log with.
    
    Returns
    -------
    output : `set<Webhook>`
    """
    audit_log = AuditLog(webhooks = webhooks)
    return {*audit_log.iter_webhooks()}


def _iter_options__iter_entries():
    guild_id = 202407010201
    
    entry_0 = AuditLogEntry.precreate(
        202407010202,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    
    entry_1 = AuditLogEntry.precreate(
        202407010203,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield None, []
    yield [entry_1], [entry_1]
    yield [entry_0, entry_1], [entry_0, entry_1]


@vampytest._(vampytest.call_from(_iter_options__iter_entries()).returning_last())
def test__AuditLog__iter_entries(entries):
    """
    Tests whether ``AuditLog.iter_entries`` works as intended.
    
    Parameters
    ----------
    entries : `None | list<AuditLogEntry>`
        Entries to create the audit log with.
    
    Returns
    -------
    output : `list<AuditLogEntry>`
    """
    audit_log = AuditLog(entries = entries)
    return [*audit_log.iter_entries()]
