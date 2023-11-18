import vampytest

from ....application_command import ApplicationCommand
from ....auto_moderation import AutoModerationRule
from ....channel import Channel
from ....emoji import Emoji
from ....guild import Guild
from ....integration import Integration
from ....invite import Invite
from ....role import Role
from ....scheduled_event import ScheduledEvent
from ....soundboard import SoundboardSound
from ....stage import Stage
from ....sticker import Sticker
from ....user import User
from ....webhook import Webhook

from ...audit_log_change import AuditLogChange

from ..audit_log_entry import AuditLogEntry
from ..preinstanced import AuditLogEntryType
from ..target_converters import (
    target_converter_application_command, target_converter_auto_moderation_rule, target_converter_channel,
    target_converter_emoji, target_converter_guild, target_converter_integration, target_converter_invite,
    target_converter_role, target_converter_scheduled_event, target_converter_soundboard_sound, target_converter_stage,
    target_converter_sticker, target_converter_user, target_converter_webhook
)


def _iter_options():
    # guild
    yield target_converter_guild, AuditLogEntry(), None
    yield target_converter_guild, AuditLogEntry(target_id = 202310290049), None
    yield target_converter_guild, AuditLogEntry(guild_id = 202310290055), None
    
    guild_id = 202310290050
    guild = Guild.precreate(guild_id)
    yield target_converter_guild, AuditLogEntry(guild_id = guild_id), guild

    
    # channel
    yield target_converter_channel, AuditLogEntry(), None
    yield target_converter_channel, AuditLogEntry(target_id = 202310290051), None
    
    channel_id = 202310290052
    channel = Channel.precreate(channel_id)
    yield target_converter_channel, AuditLogEntry(target_id = channel_id), channel
    
    
    # user
    yield target_converter_user, AuditLogEntry(), None
    yield target_converter_user, AuditLogEntry(target_id = 202310290053), None
    
    user_id = 202310290054
    user = User.precreate(user_id)
    yield target_converter_user, AuditLogEntry(target_id = user_id), user


    # role
    yield target_converter_role, AuditLogEntry(), None
    yield target_converter_role, AuditLogEntry(target_id = 20231029005763), None
    
    role_id = 202310290057
    role = Role.precreate(role_id)
    yield target_converter_role, AuditLogEntry(target_id = role_id), role
    
    
    # invite
    yield target_converter_invite, AuditLogEntry(), None
    code = '202310290058'
    invite = Invite.precreate(code)
    yield (
        target_converter_invite,
        AuditLogEntry(
            changes = [AuditLogChange('code', before = code)],
            entry_type = AuditLogEntryType.invite_update,
        ),
        invite,
    )
    code = '202310290059'
    invite = Invite.precreate(code)
    yield (
        target_converter_invite,
        AuditLogEntry(
            changes = [AuditLogChange('code', after = code)],
            entry_type = AuditLogEntryType.invite_update,
        ),
        invite,
    )
    
    # webhook
    yield target_converter_webhook, AuditLogEntry(), None
    yield target_converter_webhook, AuditLogEntry(target_id = 202310290060), None
    
    webhook_id = 202310290061
    webhook = Webhook.precreate(webhook_id)
    yield target_converter_webhook, AuditLogEntry(target_id = webhook_id), webhook


    # emoji
    yield target_converter_emoji, AuditLogEntry(), None
    yield target_converter_emoji, AuditLogEntry(target_id = 202310290062), None
    
    emoji_id = 202310290063
    emoji = Emoji.precreate(emoji_id)
    yield target_converter_emoji, AuditLogEntry(target_id = emoji_id), emoji


    # integration
    yield target_converter_integration, AuditLogEntry(), None
    yield target_converter_integration, AuditLogEntry(target_id = 202310290064), None
    
    integration_id = 202310290065
    integration = Integration.precreate(integration_id)
    yield target_converter_integration, AuditLogEntry(target_id = integration_id), integration


    # stage
    yield target_converter_stage, AuditLogEntry(), None
    yield target_converter_stage, AuditLogEntry(target_id = 202310290066), None
    
    stage_id = 202310290067
    stage = Stage.precreate(stage_id)
    yield target_converter_stage, AuditLogEntry(target_id = stage_id), stage


    # sticker
    yield target_converter_sticker, AuditLogEntry(), None
    yield target_converter_sticker, AuditLogEntry(target_id = 202310290068), None
    
    sticker_id = 202310290069
    sticker = Sticker.precreate(sticker_id)
    yield target_converter_sticker, AuditLogEntry(target_id = sticker_id), sticker


    # scheduled_event
    yield target_converter_scheduled_event, AuditLogEntry(), None
    yield target_converter_scheduled_event, AuditLogEntry(target_id = 202310290070), None
    
    scheduled_event_id = 202310290071
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id)
    yield target_converter_scheduled_event, AuditLogEntry(target_id = scheduled_event_id), scheduled_event


    # application_command
    yield target_converter_application_command, AuditLogEntry(), None
    yield target_converter_application_command, AuditLogEntry(target_id = 202310290072), None
    
    application_command_id = 202310290073
    application_command = ApplicationCommand.precreate(application_command_id)
    yield target_converter_application_command, AuditLogEntry(target_id = application_command_id), application_command

    # auto_moderation_rule
    yield target_converter_auto_moderation_rule, AuditLogEntry(), None
    yield target_converter_auto_moderation_rule, AuditLogEntry(target_id = 202310290074), None
    
    auto_moderation_rule_id = 202310290075
    auto_moderation_rule = AutoModerationRule.precreate(auto_moderation_rule_id)
    yield target_converter_auto_moderation_rule, AuditLogEntry(target_id = auto_moderation_rule_id), auto_moderation_rule


    # soundboard_sound
    yield target_converter_soundboard_sound, AuditLogEntry(), None
    yield target_converter_soundboard_sound, AuditLogEntry(target_id = 202310300013), None
    
    soundboard_sound_id = 202310300014
    soundboard_sound = SoundboardSound.precreate(soundboard_sound_id)
    yield target_converter_soundboard_sound, AuditLogEntry(target_id = soundboard_sound_id), soundboard_sound


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__target_converter(converter, entry):
    """
    Tests whether the given converter works as intended.
    
    Parameters
    ----------
    converter : `FunctionType | MethodType`
        Converter to test.
    entry : ``AuditLogEntry``
        Entry to get its target of.
    
    Returns
    -------
    output : `object`
    """
    return converter(entry)
