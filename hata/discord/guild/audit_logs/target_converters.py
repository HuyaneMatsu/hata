__all__ = ()

from scarletio import include

from ...core import STAGES


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
        parent = entry.parent
        if (parent is not None):
            return parent.channels.get(target_id, None)


def target_converter_user(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.users.get(target_id, None)


def target_converter_role(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.guild.roles.get(target_id, None)


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
        parent = entry.parent
        if (parent is not None):
            return parent.webhooks.get(target_id, None)


def target_converter_emoji(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.guild.emojis.get(target_id, None)


def target_converter_integration(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.integrations.get(target_id, None)


def target_converter_stage(entry):
    target_id = entry.target_id
    if target_id:
        return STAGES.get(target_id, None)


def target_converter_sticker(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.guild.stickers.get(target_id, None)


def target_converter_scheduled_event(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.scheduled_events.get(target_id, None)


def target_converter_thread(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.threads(target_id, None)


def target_converter_application_command(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.application_commands(target_id, None)


def target_converter_auto_moderation_rule(entry):
    target_id = entry.target_id
    if target_id:
        parent = entry.parent
        if (parent is not None):
            return parent.auto_moderation_rules(target_id, None)
