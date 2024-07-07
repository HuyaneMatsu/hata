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


def _iter_options__iter():
    guild_id = 202407010051
    
    entry_0 = AuditLogEntry.precreate(
        202407010052,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    
    entry_1 = AuditLogEntry.precreate(
        202407010053,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield None, []
    yield [entry_1], [entry_1]
    yield [entry_0, entry_1], [entry_0, entry_1]


@vampytest._(vampytest.call_from(_iter_options__iter()).returning_last())
def test__AuditLog__iter(entries):
    """
    Tests whether ``AuditLog.__iter__`` works as intended.
    
    Parameters
    ----------
    entries : `None | list<AuditLogEntry>`
        Entries to create the audit log with.
    
    Returns
    -------
    output : `list<AuditLogEntry>`
    """
    audit_log = AuditLog(entries = entries)
    return [*iter(audit_log)]


def _reversed_options__reversed():
    guild_id = 202407010054
    
    entry_0 = AuditLogEntry.precreate(
        202407010055,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    
    entry_1 = AuditLogEntry.precreate(
        202407010056,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield None, []
    yield [entry_1], [entry_1]
    yield [entry_0, entry_1], [entry_1, entry_0]


@vampytest._(vampytest.call_from(_reversed_options__reversed()).returning_last())
def test__AuditLog__reversed(entries):
    """
    Tests whether ``AuditLog.__reversed__`` works as intended.
    
    Parameters
    ----------
    entries : `None | list<AuditLogEntry>`
        Entries to create the audit log with.
    
    Returns
    -------
    output : `list<AuditLogEntry>`
    """
    audit_log = AuditLog(entries = entries)
    return [*reversed(audit_log)]


def _iter_options__len():
    guild_id = 202407010057
    
    entry_0 = AuditLogEntry.precreate(
        202407010058,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    
    entry_1 = AuditLogEntry.precreate(
        202407010059,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield None, 0
    yield [entry_1], 1
    yield [entry_0, entry_1], 2


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__AuditLog__len(entries):
    """
    Tests whether ``AuditLog.__len__`` works as intended.
    
    Parameters
    ----------
    entries : `None | list<AuditLogEntry>`
        Entries to create the audit log with.
    
    Returns
    -------
    output : `int`
    """
    audit_log = AuditLog(entries = entries)
    output = len(audit_log)
    vampytest.assert_instance(output, int)
    return output


def _bool_options__bool():
    guild_id = 202407040000
    
    entry_0 = AuditLogEntry.precreate(
        202407040001,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    
    entry_1 = AuditLogEntry.precreate(
        202407040002,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield None, False
    yield [entry_1], True
    yield [entry_0, entry_1], True


@vampytest._(vampytest.call_from(_bool_options__bool()).returning_last())
def test__AuditLog__bool(entries):
    """
    Tests whether ``AuditLog.__bool__`` works as intended.
    
    Parameters
    ----------
    entries : `None | list<AuditLogEntry>`
        Entries to create the audit log with.
    
    Returns
    -------
    output : `bool`
    """
    audit_log = AuditLog(entries = entries)
    output = bool(audit_log)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__getitem__index():
    guild_id = 202407010060
    
    entry_0 = AuditLogEntry.precreate(
        202407010061,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    
    entry_1 = AuditLogEntry.precreate(
        202407010062,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield [entry_1], 0, entry_1
    yield [entry_1], -1, entry_1
    yield [entry_0, entry_1], 0, entry_0
    yield [entry_0, entry_1], 1, entry_1


def _iter_options__getitem__slice():
    guild_id = 202407010062
    
    entry_0 = AuditLogEntry.precreate(
        202407010063,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    
    entry_1 = AuditLogEntry.precreate(
        202407010064,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield None, slice(0, 1, 1), []
    yield [entry_1], slice(1, 2, 1), []
    yield [entry_1], slice(0, 1, 1), [entry_1]
    yield [entry_0, entry_1], slice(1, 2, 1), [entry_1]
    yield [entry_0, entry_1], slice(0, 1, 1), [entry_0]
    yield [entry_0, entry_1], slice(None, None, None), [entry_0, entry_1]


def _iter_options__getitem__index_error():
    guild_id = 202407010065
    
    entry_0 = AuditLogEntry.precreate(
        202407010066,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
        guild_id = guild_id,
    )
    
    entry_1 = AuditLogEntry.precreate(
        202407010067,
        entry_type = AuditLogEntryType.guild_update,
        changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
        guild_id = guild_id,
    )
    
    yield None, 0
    yield [entry_1], 1
    yield [entry_1], -2
    yield [entry_0, entry_1], 2


@vampytest._(vampytest.call_from(_iter_options__getitem__index()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__getitem__slice()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__getitem__index_error()).raising(IndexError))
def test__AuditLog__getitem(entries, index):
    """
    Tests whether ``AuditLog.__len__`` works as intended.
    
    Parameters
    ----------
    entries : `None | list<AuditLogEntry>`
        Entries to create the audit log with.
    index : `int | slice`
        The index to get the item for.
    
    Returns
    -------
    output : `int`
    """
    audit_log = AuditLog(entries = entries)
    return audit_log[index]


def test__AuditLog__repr():
    """
    Tests whether ``AuditLog.__repr__`` works as intended.
    """
    guild_id = 202407010068
    
    application_commands = [
        ApplicationCommand.precreate(202407010069),
        ApplicationCommand.precreate(202407010070),
    ]
    
    auto_moderation_rules = [
        AutoModerationRule.precreate(202407010071),
        AutoModerationRule.precreate(202407010072),
    ]
    
    entries = [
        AuditLogEntry.precreate(
            202407010073,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = guild_id,
        ),
        AuditLogEntry.precreate(
            202407010074,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = guild_id,
        ),
    ]
    
    integrations = [
        Integration.precreate(202407010075),
        Integration.precreate(202407010076),
    ]
    
    scheduled_events = [
        ScheduledEvent.precreate(202407010077),
        ScheduledEvent.precreate(202407010078),
    ]
    
    threads = [
        Channel.precreate(202407010079, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
        Channel.precreate(202407010080, channel_type = ChannelType.guild_thread_private, guild_id = guild_id),
    ]
    
    users = [
        User.precreate(202407010081),
        User.precreate(202407010082),
    ]
    
    webhooks = [
        Webhook.precreate(202407010083),
        Webhook.precreate(202407010084),
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
    
    output = repr(audit_log)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    guild_id_0 = 202407010085
    application_commands_0 = [
        ApplicationCommand.precreate(202407010087),
        ApplicationCommand.precreate(202407010088),
    ]
    auto_moderation_rules_0 = [
        AutoModerationRule.precreate(202407010091),
        AutoModerationRule.precreate(202407010092),
    ]
    entries_0 = [
        AuditLogEntry.precreate(
            202407010095,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
            guild_id = guild_id_0,
        ),
        AuditLogEntry.precreate(
            202407010096,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'okuu')],
            guild_id = guild_id_0,
        ),
    ]
    integrations_0 = [
        Integration.precreate(202407010099),
        Integration.precreate(202407010100),
    ]
    scheduled_events_0 = [
        ScheduledEvent.precreate(202407010102),
        ScheduledEvent.precreate(202407010103),
    ]
    threads_0 = [
        Channel.precreate(202407010106, channel_type = ChannelType.guild_thread_private, guild_id = guild_id_0),
        Channel.precreate(202407010107, channel_type = ChannelType.guild_thread_private, guild_id = guild_id_0),
    ]
    users_0 = [
        User.precreate(202407010110),
        User.precreate(202407010111),
    ]
    webhooks_0 = [
        Webhook.precreate(202407010114),
        Webhook.precreate(202407010115),
    ]
    
    
    guild_id_1 = 202407010086
    application_commands_1 = [
        ApplicationCommand.precreate(202407010089),
        ApplicationCommand.precreate(202407010090),
    ]
    auto_moderation_rules_1 = [
        AutoModerationRule.precreate(202407010093),
        AutoModerationRule.precreate(202407010094),
    ]
    entries_1 = [
        AuditLogEntry.precreate(
            202407010097,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'okuu', after = 'koishi')],
            guild_id = guild_id_1,
        ),
        AuditLogEntry.precreate(
            202407010098,
            entry_type = AuditLogEntryType.guild_update,
            changes = [AuditLogChange('name', before = 'orin', after = 'satori')],
            guild_id = guild_id_1,
        ),
    ]
    integrations_1 = [
        Integration.precreate(202407010100),
        Integration.precreate(202407010101),
    ]
    scheduled_events_1 = [
        ScheduledEvent.precreate(202407010104),
        ScheduledEvent.precreate(202407010105),
    ]
    threads_1 = [
        Channel.precreate(202407010108, channel_type = ChannelType.guild_thread_private, guild_id = guild_id_0),
        Channel.precreate(202407010109, channel_type = ChannelType.guild_thread_private, guild_id = guild_id_0),
    ]
    users_1 = [
        User.precreate(202407010112),
        User.precreate(202407010113),
    ]
    webhooks_1 = [
        Webhook.precreate(202407010116),
        Webhook.precreate(202407010117),
    ]
    
    
    keyword_parameters = {
        'application_commands': application_commands_0,
        'auto_moderation_rules': auto_moderation_rules_0,
        'entries': entries_0,
        'guild_id': guild_id_0,
        'integrations': integrations_0,
        'scheduled_events': scheduled_events_0,
        'threads': threads_0,
        'users': users_0,
        'webhooks': webhooks_0,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_commands': application_commands_1,
        },
        False,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'auto_moderation_rules': auto_moderation_rules_1,
        },
        False,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'entries': entries_1,
        },
        False,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': guild_id_1,
        },
        False,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'integrations': integrations_1,
        },
        False,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'scheduled_events': scheduled_events_1,
        },
        False,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'threads': threads_1,
        },
        False,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'users': users_1,
        },
        False,
    )

    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'webhooks': webhooks_1,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__AudigLog__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``AuditLog.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `str`
    """
    instance_0 = AuditLog(**keyword_parameters_0)
    instance_1 = AuditLog(**keyword_parameters_1)
    
    output = instance_0 == instance_1
    vampytest.assert_instance(output, bool)
    return output


def test__AuditLog__eq__same():
    """
    Tests whether ``AuditLog.__eq__`` works as intended.
    
    Case: same.
    
    An other test catched this issue luckily, but making sure it does happen.
    """
    audit_log = AuditLog()
    
    vampytest.assert_eq(audit_log, audit_log)
