__all__ = ()

from scarletio import include

from ..core import (
    AUTO_MODERATION_RULES, CHANNELS, EMOJIS, INTEGRATIONS, ROLES, SCHEDULED_EVENTS, STAGES, STICKERS, USERS
)

AuditLogEvent = include('AuditLogEvent')
Invite = include('Invite')

def target_converter_none(entry):
    return None


def target_converter_guild(entry):
    parent = entry.parent
    if (parent is not None):
        return parent.guild


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
    for change in entry.changes:
        if change.attribute_name != 'code':
            continue
        
        if entry.type is AuditLogEvent.invite_delete:
            code = change.before
        else:
            code = change.after
        break
    
    else:
        code = '' # malformed ?
    
    
    parent = entry.parent
    if (parent is None):
        guild = None
    else:
        guild = parent.guild
    
    return Invite.precreate(code, guild = guild)


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


def target_converter_thread(entry):
    target_id = entry.target_id
    if target_id:
        return CHANNELS.get(target_id, None)


def target_converter_application_command(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.application_commands(target_id, None)


def target_converter_auto_moderation_rule(entry):
    target_id = entry.target_id
    if target_id:
        return AUTO_MODERATION_RULES.get(target_id, None)
