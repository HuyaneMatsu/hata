__all__ = ('create_partial_invite_data', 'create_partial_invite_from_data')

from ...core import INVITES

from .fields import parse_code, put_channel_id_into, put_code_into, put_guild_id_into,\
    validate_max_age, put_max_age_into, validate_max_uses, put_temporary_into, \
    put_max_uses_into, validate_temporary, validate_unique, put_unique_into, \
    validate_target_type, validate_target_application_id, put_target_application_id_into, \
    put_target_user_id_into, put_target_type_into, validate_target_user_id

from .invite import Invite


INVITE_GUILD_FIELD_CONVERTERS = {
    'max_age': (validate_max_age, put_max_age_into),
    'max_uses': (validate_max_uses, put_max_uses_into),
    'target_application': (validate_target_application_id, put_target_application_id_into),
    'target_application_id': (validate_target_application_id, put_target_application_id_into),
    'target_type': (validate_target_type, put_target_type_into),
    'target_user': (validate_target_user_id, put_target_user_id_into),
    'target_user_id': (validate_target_user_id, put_target_user_id_into),
    'temporary': (validate_temporary, put_temporary_into),
    'unique': (validate_unique, put_unique_into),
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
    put_channel_id_into(invite.channel_id, data, True)
    put_code_into(invite.code, data, True)
    put_guild_id_into(invite.guild_id, data, True)
    return data
