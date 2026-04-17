__all__ = ()

from ...core import (
    APPLICATION_COMMANDS, AUTO_MODERATION_RULES, CHANNELS, EMOJIS, INTEGRATIONS, ROLES, SCHEDULED_EVENTS,
    SOUNDBOARD_SOUNDS, STAGES, STICKERS, USERS
)
from ...invite import Invite


def target_converter_guild(entry):
    return entry.guild


def target_converter_channel(entry):
    target_id = entry.target_id
    if target_id:
        return CHANNELS.get(target_id, None)


def target_converter_user(entry):
    target_id = entry.target_id
    if target_id:
        return USERS.get(target_id, None)


def target_converter_role(entry):
    target_id = entry.target_id
    if target_id:
        return ROLES.get(target_id, None)


def target_converter_invite(entry):
    # every other data is at # change
    change = entry.get_change('code')
    if change is None:
        code = None
    elif change.has_after():
        code = change.after
    elif change.has_before():
        code = change.before
    else:
        code = None
    
    if code is None:
        return None
    
    return Invite.precreate(code, guild = entry.guild)


def target_converter_webhook(entry):
    target_id = entry.target_id
    if target_id:
        return USERS.get(target_id, None)


def target_converter_emoji(entry):
    target_id = entry.target_id
    if target_id:
        return EMOJIS.get(target_id, None)


def target_converter_integration(entry):
    target_id = entry.target_id
    if target_id:
        return INTEGRATIONS.get(target_id, None)


def target_converter_stage(entry):
    target_id = entry.target_id
    if target_id:
        return STAGES.get(target_id, None)


def target_converter_sticker(entry):
    target_id = entry.target_id
    if target_id:
        return STICKERS.get(target_id, None)


def target_converter_scheduled_event(entry):
    target_id = entry.target_id
    if target_id:
        return SCHEDULED_EVENTS.get(target_id, None)


def target_converter_application_command(entry):
    target_id = entry.target_id
    if target_id:
        return APPLICATION_COMMANDS.get(target_id, None)


def target_converter_auto_moderation_rule(entry):
    target_id = entry.target_id
    if target_id:
        return AUTO_MODERATION_RULES.get(target_id, None)


def target_converter_soundboard_sound(entry):
    target_id = entry.target_id
    if target_id:
        return SOUNDBOARD_SOUNDS.get(target_id, None)
