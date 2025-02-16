__all__ = ('create_partial_invite_data', 'create_partial_invite_from_data')

from ...core import INVITES

from .fields import parse_code, put_channel_id, put_code, put_guild_id,\
    validate_max_age, put_max_age, validate_max_uses, put_temporary, \
    put_max_uses, validate_temporary, validate_unique, put_unique, \
    validate_target_type, validate_target_application_id, put_target_application_id, \
    put_target_user_id, put_target_type, validate_target_user_id

from .invite import Invite


INVITE_GUILD_FIELD_CONVERTERS = {
    'max_age': (validate_max_age, put_max_age),
    'max_uses': (validate_max_uses, put_max_uses),
    'target_application': (validate_target_application_id, put_target_application_id),
    'target_application_id': (validate_target_application_id, put_target_application_id),
    'target_type': (validate_target_type, put_target_type),
    'target_user': (validate_target_user_id, put_target_user_id),
    'target_user_id': (validate_target_user_id, put_target_user_id),
    'temporary': (validate_temporary, put_temporary),
    'unique': (validate_unique, put_unique),
}


def create_partial_invite_from_data(data):
    """
    Creates a partial invite from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Partial invite data.
    
    Returns
    -------
    invite : ``Invite``
    """
    invite_code = parse_code(data)
    
    try:
        invite = INVITES[invite_code]
    except KeyError:
        invite = Invite._create_empty(invite_code)
        invite._update_attributes_partial(data)
        INVITES[invite_code] = invite
    else:
        invite._update_attributes_partial(data)
    
    return invite


def create_partial_invite_data(invite):
    """
    Creates partial invite data.
    
    Parameters
    ----------
    invite : ``Invite``
        Invite to create data from.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    put_channel_id(invite.channel_id, data, True)
    put_code(invite.code, data, True)
    put_guild_id(invite.guild_id, data, True)
    return data
