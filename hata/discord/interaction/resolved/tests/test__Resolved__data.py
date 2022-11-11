import vampytest

from ....channel import Channel
from ....message import Attachment, Message
from ....role import Role
from ....user import User

from ...interaction_event import InteractionEvent

from ..resolved import Resolved

from .test__Resolved__constructor import _assert_is_all_field_set


def test__Resolved__from_data():
    """
    Tests whether ``Resolved.from_data`` works as intended.
    """
    guild_id = 202211050028
    entity_id = 202211050029
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    attachment = Attachment.precreate(entity_id)
    channel = Channel.precreate(entity_id)
    role = Role.precreate(entity_id)
    message = Message.precreate(entity_id)
    user = User.precreate(entity_id)
    
    data = {
        'attachments': {str(attachment.id): attachment.to_data(defaults = True, include_internals = True)},
        'channels': {str(channel.id): channel.to_data(defaults = True, include_internals = True)},
        'roles': {str(role.id): role.to_data(defaults = True, include_internals = True)},
        'messages': {str(message.id): message.to_data(defaults = True, include_internals = True)},
        'users': {str(user.id): user.to_data(defaults = True, include_internals = True)},
    }
    
    resolved = Resolved.from_data(data, interaction_event)
    _assert_is_all_field_set(resolved)
    
    vampytest.assert_eq(resolved.attachments, {attachment.id: attachment})
    vampytest.assert_eq(resolved.channels, {channel.id: channel})
    vampytest.assert_eq(resolved.roles, {role.id: role})
    vampytest.assert_eq(resolved.messages, {message.id: message})
    vampytest.assert_eq(resolved.users, {user.id: user})
    

def test__Resolved__to_data():
    """
    Tests whether ``Resolved.to_data`` works as intended.
    
    Case: include defaults.
    """
    guild_id = 202211050030
    entity_id = 202211050031
    interaction_event = InteractionEvent(guild_id = guild_id)
    
    attachment = Attachment.precreate(entity_id)
    channel = Channel.precreate(entity_id)
    role = Role.precreate(entity_id)
    message = Message.precreate(entity_id)
    user = User.precreate(entity_id)
    
    resolved = Resolved(
        attachments = [attachment],
        channels = [channel],
        roles = [role],
        messages = [message],
        users = [user],
    )
    
    data = {
        'attachments': {str(attachment.id): attachment.to_data(defaults = True, include_internals = True)},
        'channels': {str(channel.id): channel.to_data(defaults = True, include_internals = True)},
        'roles': {str(role.id): role.to_data(defaults = True, include_internals = True)},
        'messages': {str(message.id): message.to_data(defaults = True, include_internals = True)},
        'users': {str(user.id): user.to_data(defaults = True, include_internals = True)},
        'members': {},
    }
    
    vampytest.assert_eq(
        resolved.to_data(
            defaults = True,
            interaction_event = interaction_event,
        ),
        data,
    )
