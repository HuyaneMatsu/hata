__all__ = ()


from ...application_command import ApplicationCommand
from ...auto_moderation import AutoModerationRule
from ...channel import Channel
from ...field_validators import entity_id_validator_factory
from ...guild import Guild
from ...integration import Integration
from ...scheduled_event import ScheduledEvent
from ...user import ClientUserBase, User
from ...webhook import Webhook

from ..audit_log_entry import AuditLogEntry


# application_commands

def parse_application_commands(data):
    """
    Parses an audit log entry's application commands.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    application_commands : `None | dict<int, ApplicationCommand>`
    """
    try:
        application_command_datas = data['application_commands']
    except KeyError:
        return None
    
    if not application_command_datas:
        return None
    
    application_commands = {}
    
    for application_command_data in application_command_datas:
        application_command = ApplicationCommand.from_data(application_command_data)
        application_commands[application_command.id] = application_command
    
    return application_commands


def put_application_commands_into(application_commands, data, defaults):
    """
    Serialises the application commands into the given data.
    
    Parameters
    ----------
    application_commands : `None | dict<int, ApplicationCommand>`
        The application commands to serialise.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (application_commands is not None):
        if application_commands is None:
            application_command_datas = []
        else:
            application_command_datas = [
                application_command.to_data(defaults = defaults, include_internals = True)
                for application_command in application_commands.values()
            ]
        data['application_commands'] = application_command_datas
    
    return data


def validate_application_commands(application_commands):
    """
    Validates the given application commands.
    
    Parameters
    ----------
    application_commands : `None | iterable<ApplicationCommand>`
        The application commands to validate.
    
    Returns
    -------
    application_commands : `None | dict<int, ApplicationCommand>`
    
    Raises
    ------
    TypeError
        - If `application_commands`'s type is incorrect.
    """
    validated_application_commands = None
    
    if application_commands is None:
        return validated_application_commands
        
    if (getattr(application_commands, '__iter__', None) is None):
        raise TypeError(
            f'`application_commands` can be `None`, `iterable` of `{ApplicationCommand.__name__}` elements, '
            f'got {type(application_commands).__name__}; {application_commands!r}.'
        )
    
    for application_command in application_commands:
        if not isinstance(application_command, ApplicationCommand):
            raise TypeError(
                f'`application_commands` elements can be `{ApplicationCommand.__name__}`, '
                f'got {type(application_command).__name__}; {application_command!r}; '
                f'application_commands = {application_commands!r}.'
            )
        
        if validated_application_commands is None:
            validated_application_commands = {}
        
        validated_application_commands[application_command.id] = application_command
    
    return validated_application_commands


# auto_moderation_rules

def parse_auto_moderation_rules(data):
    """
    Parses an audit log entry's application commands.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    auto_moderation_rules : `None | dict<int, AutoModerationRule>`
    """
    try:
        auto_moderation_rule_datas = data['auto_moderation_rules']
    except KeyError:
        return None
    
    if not auto_moderation_rule_datas:
        return None
    
    auto_moderation_rules = {}
    
    for auto_moderation_rule_data in auto_moderation_rule_datas:
        auto_moderation_rule = AutoModerationRule.from_data(auto_moderation_rule_data)
        auto_moderation_rules[auto_moderation_rule.id] = auto_moderation_rule
    
    return auto_moderation_rules


def put_auto_moderation_rules_into(auto_moderation_rules, data, defaults):
    """
    Serialises the auto moderation rules into the given data.
    
    Parameters
    ----------
    auto_moderation_rules : `None | dict<int, AutoModerationRule>`
        The auto moderation rules to serialise.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (auto_moderation_rules is not None):
        if auto_moderation_rules is None:
            auto_moderation_rule_datas = []
        else:
            auto_moderation_rule_datas = [
                auto_moderation_rule.to_data(defaults = defaults, include_internals = True)
                for auto_moderation_rule in auto_moderation_rules.values()
            ]
        data['auto_moderation_rules'] = auto_moderation_rule_datas
    
    return data


def validate_auto_moderation_rules(auto_moderation_rules):
    """
    Validates the given auto moderation rules.
    
    Parameters
    ----------
    auto_moderation_rules : `None | iterable<AutoModerationRule>`
        The auto moderation rules to validate.
    
    Returns
    -------
    auto_moderation_rules : `None | dict<int, AutoModerationRule>`
    
    Raises
    ------
    TypeError
        - If `auto_moderation_rules`'s type is incorrect.
    """
    validated_auto_moderation_rules = None
    
    if auto_moderation_rules is None:
        return validated_auto_moderation_rules
        
    if (getattr(auto_moderation_rules, '__iter__', None) is None):
        raise TypeError(
            f'`auto_moderation_rules` can be `None`, `iterable` of `{AutoModerationRule.__name__}` elements, '
            f'got {type(auto_moderation_rules).__name__}; {auto_moderation_rules!r}.'
        )
    
    for auto_moderation_rule in auto_moderation_rules:
        if not isinstance(auto_moderation_rule, AutoModerationRule):
            raise TypeError(
                f'`auto_moderation_rules` elements can be `{AutoModerationRule.__name__}`, '
                f'got {type(auto_moderation_rule).__name__}; {auto_moderation_rule!r}; '
                f'auto_moderation_rules = {auto_moderation_rules!r}.'
            )
        
        if validated_auto_moderation_rules is None:
            validated_auto_moderation_rules = {}
        
        validated_auto_moderation_rules[auto_moderation_rule.id] = auto_moderation_rule
    
    return validated_auto_moderation_rules


# entries

def parse_entries(data, parent = None):
    """
    Parses an audit log entry's entries.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    parent : `None | AuditLog` = `None`, Optional
        The respective parent to backlink to.
    
    Returns
    -------
    entries : `None | list<AuditLogEntry>`
    """
    try:
        entry_datas = data['audit_log_entries']
    except KeyError:
        return None
    
    if not entry_datas:
        return None
    
    entries = None
    
    for entry_data in entry_datas:
        entry = AuditLogEntry.from_data(entry_data, parent)
        if (entry is not None):
            if entries is None:
                entries = []
            
            entries.append(entry)
    
    return entries


def put_entries_into(entries, data, defaults):
    """
    Serialises the entries into the given data.
    
    Parameters
    ----------
    entries : `None | dict<int, AutoModerationRule>`
        The entries to serialise.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (entries is not None):
        if entries is None:
            entry_datas = []
        else:
            entry_datas = [
                entry.to_data(defaults = defaults)
                for entry in entries
            ]
        data['audit_log_entries'] = entry_datas
    
    return data


def validate_entries(entries):
    """
    Validates the given entries.
    
    Parameters
    ----------
    entries : `None | iterable<AuditLogEntry>`
        The entries to validate.
    
    Returns
    -------
    entries : `None | list<AuditLogEntry>`
    
    Raises
    ------
    TypeError
        - If `entries`'s type is incorrect.
    """
    validated_entries = None
    
    if entries is None:
        return validated_entries
        
    if (getattr(entries, '__iter__', None) is None):
        raise TypeError(
            f'`entries` can be `None`, `iterable` of `{AuditLogEntry.__name__}` elements, '
            f'got {type(entries).__name__}; {entries!r}.'
        )
    
    for entry in entries:
        if not isinstance(entry, AuditLogEntry):
            raise TypeError(
                f'`entries` elements can be `{AuditLogEntry.__name__}`, '
                f'got {type(entry).__name__}; {entry!r}; '
                f'entries = {entries!r}.'
            )
        
        if validated_entries is None:
            validated_entries = set()
        
        validated_entries.add(entry)
    
    if (validated_entries is not None):
        return sorted(validated_entries)


# guild_id

validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# integrations

def parse_integrations(data):
    """
    Parses an audit log entry's application commands.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    integrations : `None | dict<int, Integration>`
    """
    try:
        integration_datas = data['integrations']
    except KeyError:
        return None
    
    if not integration_datas:
        return None
    
    integrations = {}
    
    for integration_data in integration_datas:
        integration = Integration.from_data(integration_data)
        integrations[integration.id] = integration
    
    return integrations


def put_integrations_into(integrations, data, defaults):
    """
    Serialises the integrations into the given data.
    
    Parameters
    ----------
    integrations : `None | dict<int, Integration>`
        The integrations to serialise.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (integrations is not None):
        if integrations is None:
            integration_datas = []
        else:
            integration_datas = [
                integration.to_data(defaults = defaults, include_internals = True)
                for integration in integrations.values()
            ]
        data['integrations'] = integration_datas
    
    return data


def validate_integrations(integrations):
    """
    Validates the given integrations.
    
    Parameters
    ----------
    integrations : `None | iterable<Integration>`
        The integrations to validate.
    
    Returns
    -------
    integrations : `None | dict<int, Integration>`
    
    Raises
    ------
    TypeError
        - If `integrations`'s type is incorrect.
    """
    validated_integrations = None
    
    if integrations is None:
        return validated_integrations
        
    if (getattr(integrations, '__iter__', None) is None):
        raise TypeError(
            f'`integrations` can be `None`, `iterable` of `{Integration.__name__}` elements, '
            f'got {type(integrations).__name__}; {integrations!r}.'
        )
    
    for integration in integrations:
        if not isinstance(integration, Integration):
            raise TypeError(
                f'`integrations` elements can be `{Integration.__name__}`, '
                f'got {type(integration).__name__}; {integration!r}; '
                f'integrations = {integrations!r}.'
            )
        
        if validated_integrations is None:
            validated_integrations = {}
        
        validated_integrations[integration.id] = integration
    
    return validated_integrations


# scheduled_events

def parse_scheduled_events(data):
    """
    Parses an audit log entry's application commands.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    scheduled_events : `None | dict<int, ScheduledEvent>`
    """
    try:
        scheduled_event_datas = data['guild_scheduled_events']
    except KeyError:
        return None
    
    if not scheduled_event_datas:
        return None
    
    scheduled_events = {}
    
    for scheduled_event_data in scheduled_event_datas:
        scheduled_event = ScheduledEvent.from_data(scheduled_event_data)
        scheduled_events[scheduled_event.id] = scheduled_event
    
    return scheduled_events


def put_scheduled_events_into(scheduled_events, data, defaults):
    """
    Serialises the scheduled events into the given data.
    
    Parameters
    ----------
    scheduled_events : `None | dict<int, ScheduledEvent>`
        The scheduled events to serialise.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (scheduled_events is not None):
        if scheduled_events is None:
            scheduled_event_datas = []
        else:
            scheduled_event_datas = [
                scheduled_event.to_data(defaults = defaults, include_internals = True)
                for scheduled_event in scheduled_events.values()
            ]
        data['guild_scheduled_events'] = scheduled_event_datas
    
    return data


def validate_scheduled_events(scheduled_events):
    """
    Validates the given scheduled events.
    
    Parameters
    ----------
    scheduled_events : `None | iterable<ScheduledEvent>`
        The scheduled events to validate.
    
    Returns
    -------
    scheduled_events : `None | dict<int, ScheduledEvent>`
    
    Raises
    ------
    TypeError
        - If `scheduled_events`'s type is incorrect.
    """
    validated_scheduled_events = None
    
    if scheduled_events is None:
        return validated_scheduled_events
        
    if (getattr(scheduled_events, '__iter__', None) is None):
        raise TypeError(
            f'`scheduled_events` can be `None`, `iterable` of `{ScheduledEvent.__name__}` elements, '
            f'got {type(scheduled_events).__name__}; {scheduled_events!r}.'
        )
    
    for scheduled_event in scheduled_events:
        if not isinstance(scheduled_event, ScheduledEvent):
            raise TypeError(
                f'`scheduled_events` elements can be `{ScheduledEvent.__name__}`, '
                f'got {type(scheduled_event).__name__}; {scheduled_event!r}; '
                f'scheduled_events = {scheduled_events!r}.'
            )
        
        if validated_scheduled_events is None:
            validated_scheduled_events = {}
        
        validated_scheduled_events[scheduled_event.id] = scheduled_event
    
    return validated_scheduled_events


# threads

def parse_threads(data, guild_id = 0):
    """
    Parses an audit log entry's threads.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    guild_id : `int` = `0`, Optional
        The respective guild's identifier.
    
    Returns
    -------
    threads : `None | dict<int, Channel>`
    """
    try:
        thread_datas = data['threads']
    except KeyError:
        return None
    
    if not thread_datas:
        return None
    
    threads = {}
    
    for thread_data in thread_datas:
        thread = Channel.from_data(thread_data, None, guild_id)
        threads[thread.id] = thread
    
    return threads


def put_threads_into(threads, data, defaults):
    """
    Serialises the threads into the given data.
    
    Parameters
    ----------
    threads : `None | dict<int, Channel>`
        The threads to serialise.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (threads is not None):
        if threads is None:
            thread_datas = []
        else:
            thread_datas = [
                thread.to_data(defaults = defaults, include_internals = True)
                for thread in threads.values()
            ]
        data['threads'] = thread_datas
    
    return data


def validate_threads(threads):
    """
    Validates the given channels.
    
    Parameters
    ----------
    threads : `None | iterable<Channel>`
        The channels to validate.
    
    Returns
    -------
    threads : `None | dict<int, Channel>`
    
    Raises
    ------
    TypeError
        - If `threads`'s type is incorrect.
    """
    validated_threads = None
    
    if threads is None:
        return validated_threads
        
    if (getattr(threads, '__iter__', None) is None):
        raise TypeError(
            f'`threads` can be `None`, `iterable` of `{Channel.__name__}` elements, '
            f'got {type(threads).__name__}; {threads!r}.'
        )
    
    for thread in threads:
        if not isinstance(thread, Channel):
            raise TypeError(
                f'`threads` elements can be `{Channel.__name__}`, '
                f'got {type(thread).__name__}; {thread!r}; '
                f'threads = {threads!r}.'
            )
        
        if validated_threads is None:
            validated_threads = {}
        
        validated_threads[thread.id] = thread
    
    return validated_threads


# users

def parse_users(data):
    """
    Parses an audit log entry's users.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    users : `None | dict<int, ClientUserBase>`
    """
    try:
        user_datas = data['users']
    except KeyError:
        return None
    
    if not user_datas:
        return None
    
    users = {}
    
    for user_data in user_datas:
        user = User.from_data(user_data)
        users[user.id] = user
    
    return users


def put_users_into(users, data, defaults):
    """
    Serialises the users into the given data.
    
    Parameters
    ----------
    users : `None | dict<int, ClientUserBase>`
        The users to serialise.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (users is not None):
        if users is None:
            user_datas = []
        else:
            user_datas = [
                user.to_data(defaults = defaults, include_internals = True)
                for user in users.values()
            ]
        data['users'] = user_datas
    
    return data


def validate_users(users):
    """
    Validates the given users.
    
    Parameters
    ----------
    users : `None | iterable<ClientUserBase>`
        The users to validate.
    
    Returns
    -------
    users : `None | dict<int, ClientUserBase>`
    
    Raises
    ------
    TypeError
        - If `users`'s type is incorrect.
    """
    validated_users = None
    
    if users is None:
        return validated_users
        
    if (getattr(users, '__iter__', None) is None):
        raise TypeError(
            f'`users` can be `None`, `iterable` of `{ClientUserBase.__name__}` elements, '
            f'got {type(users).__name__}; {users!r}.'
        )
    
    for user in users:
        if not isinstance(user, ClientUserBase):
            raise TypeError(
                f'`users` elements can be `{ClientUserBase.__name__}`, '
                f'got {type(user).__name__}; {user!r}; '
                f'users = {users!r}.'
            )
        
        if validated_users is None:
            validated_users = {}
        
        validated_users[user.id] = user
    
    return validated_users


# webhooks

def parse_webhooks(data):
    """
    Parses an audit log entry's webhooks.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    webhooks : `None | dict<int, Webhook>`
    """
    try:
        webhook_datas = data['webhooks']
    except KeyError:
        return None
    
    if not webhook_datas:
        return None
    
    webhooks = {}
    
    for webhook_data in webhook_datas:
        webhook = Webhook.from_data(webhook_data)
        webhooks[webhook.id] = webhook
    
    return webhooks


def put_webhooks_into(webhooks, data, defaults):
    """
    Serialises the webhooks into the given data.
    
    Parameters
    ----------
    webhooks : `None | dict<int, Webhook>`
        The webhooks to serialise.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (webhooks is not None):
        if webhooks is None:
            webhook_datas = []
        else:
            webhook_datas = [
                webhook.to_data(defaults = defaults, include_internals = True)
                for webhook in webhooks.values()
            ]
        data['webhooks'] = webhook_datas
    
    return data


def validate_webhooks(webhooks):
    """
    Validates the given webhooks.
    
    Parameters
    ----------
    webhooks : `None | iterable<Webhook>`
        The webhooks to validate.
    
    Returns
    -------
    webhooks : `None | dict<int, Webhook>`
    
    Raises
    ------
    TypeError
        - If `webhooks`'s type is incorrect.
    """
    validated_webhooks = None
    
    if webhooks is None:
        return validated_webhooks
        
    if (getattr(webhooks, '__iter__', None) is None):
        raise TypeError(
            f'`webhooks` can be `None`, `iterable` of `{Webhook.__name__}` elements, '
            f'got {type(webhooks).__name__}; {webhooks!r}.'
        )
    
    for webhook in webhooks:
        if not isinstance(webhook, Webhook):
            raise TypeError(
                f'`webhooks` elements can be `{Webhook.__name__}`, '
                f'got {type(webhook).__name__}; {webhook!r}; '
                f'webhooks = {webhooks!r}.'
            )
        
        if validated_webhooks is None:
            validated_webhooks = {}
        
        validated_webhooks[webhook.id] = webhook
    
    return validated_webhooks

