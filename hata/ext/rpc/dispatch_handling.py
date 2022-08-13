__all__ = ()

from scarletio import Task

from ...discord.core import KOKORO, MESSAGES
from ...discord.guild import create_partial_guild_from_data
from ...discord.message import Message
from ...discord.user import User

from .constants import (
    DISPATCH_EVENT_ACTIVITY_JOIN, DISPATCH_EVENT_ACTIVITY_JOIN_REQUEST, DISPATCH_EVENT_ACTIVITY_SPECTATE,
    DISPATCH_EVENT_CHANNEL_CREATE, DISPATCH_EVENT_CHANNEL_VOICE_SELECT, DISPATCH_EVENT_GUILD_CREATE,
    DISPATCH_EVENT_GUILD_STATUS_UPDATE, DISPATCH_EVENT_MESSAGE_CREATE, DISPATCH_EVENT_MESSAGE_DELETE,
    DISPATCH_EVENT_MESSAGE_EDIT, DISPATCH_EVENT_NOTIFICATION_CREATE, DISPATCH_EVENT_READY,
    DISPATCH_EVENT_SPEAKING_START, DISPATCH_EVENT_SPEAKING_STOP, DISPATCH_EVENT_USER_VOICE_CREATE,
    DISPATCH_EVENT_USER_VOICE_DELETE, DISPATCH_EVENT_USER_VOICE_UPDATE, DISPATCH_EVENT_VOICE_CONNECTION_STATUS,
    DISPATCH_EVENT_VOICE_SETTINGS_UPDATE
)
from .event_types import ChannelCreateEvent, ChannelVoiceSelectEvent, GuildCreateEvent, NotificationCreateEvent
from .rich_voice_state import RichVoiceState
from .voice_connection_status import VoiceConnectionStatus
from .voice_settings import VoiceSettings


def handle_dispatch_ready(rpc_client, data):
    rpc_client.user = User.from_data(data['user'])
    rpc_client._set_connection_waiter_result(True)
    
    Task(rpc_client.events.ready(rpc_client), KOKORO)


def handle_dispatch_guild_status_update(rpc_client, data):
    guild = create_partial_guild_from_data(data['guild'])
    
    Task(rpc_client.events.guild_status_update(rpc_client, guild), KOKORO)



def handle_dispatch_guild_create(rpc_client, data):
    event = GuildCreateEvent(data)
    
    Task(rpc_client.events.guild_create(rpc_client, event), KOKORO)


def handle_dispatch_channel_create(rpc_client, data):
    event = ChannelCreateEvent(data)
    
    Task(rpc_client.events.channel_create(rpc_client, event), KOKORO)


def handle_dispatch_channel_voice_select(rpc_client, data):
    event = ChannelVoiceSelectEvent(data)
    
    Task(rpc_client.events.voice_channel_select(rpc_client, event), KOKORO)


def handle_dispatch_event_voice_settings_update(rpc_client, data):
    voice_settings = VoiceSettings.from_data(data)
    
    Task(rpc_client.events.voice_settings_update(rpc_client, voice_settings), KOKORO)


def handle_dispatch_user_voice_create(rpc_client, data):
    voice_state = RichVoiceState.from_data(data)
    
    Task(rpc_client.events.voice_state_create(rpc_client, voice_state), KOKORO)


def handle_dispatch_user_voice_update(rpc_client, data):
    voice_state = RichVoiceState.from_data(data)
    
    Task(rpc_client.events.voice_state_update(rpc_client, voice_state), KOKORO)


def handle_dispatch_user_voice_delete(rpc_client, data):
    voice_state = RichVoiceState.from_data(data)
    
    Task(rpc_client.events.voice_state_delete(rpc_client, voice_state), KOKORO)


def handle_dispatch_voice_connection_status(rpc_client, data):
    voice_connection_status = VoiceConnectionStatus.from_data(data)

    Task(rpc_client.events.voice_connection_status(rpc_client, voice_connection_status), KOKORO)


def handle_dispatch_message_create(rpc_client, data):
    message = Message(data)
    
    Task(rpc_client.events.message_create(rpc_client, message), KOKORO)


def handle_dispatch_message_edit(rpc_client, data):
    message_id = int(data['id'])
    message = MESSAGES.get(message_id, None)
    if message is None:
        if 'edited_timestamp' not in data:
            return
    
        # Dead event handling
        message = Message(data)
        old_attributes = None
    
    else:
        if 'edited_timestamp' in data:
            old_attributes = message._difference_update_attributes(data)
            if not old_attributes:
                return
        
        else:
            message._update_embed_no_return(data)
            return
    
    Task(rpc_client.events.message_edit(rpc_client, message, old_attributes), KOKORO)


def handle_dispatch_message_delete(rpc_client, data):
    message_id = int(data['id'])
    
    message = Message._create_from_partial_fields(message_id, 0, 0)
    channel = message.channel
    if (channel is not None):
        channel._pop_message(message_id)
    
    Task(rpc_client.events.message_delete(rpc_client, message), KOKORO)


def handle_dispatch_speaking_start(rpc_client, data):
    user_id = int(data['user_id'])
    
    Task(rpc_client.events.speaking_start(rpc_client, user_id), KOKORO)


def handle_dispatch_speaking_stop(rpc_client, data):
    user_id = int(data['user_id'])
    
    Task(rpc_client.events.speaking_stop(rpc_client, user_id), KOKORO)


def handle_dispatch_notification_create(rpc_client, data):
    event = NotificationCreateEvent(data)
    
    Task(rpc_client.events.notification_create(rpc_client, event), KOKORO)


def handle_dispatch_activity_join(rpc_client, data):
    secret = data['secret']
    
    Task(rpc_client.events.activity_join(rpc_client, secret), KOKORO)


def handle_dispatch_activity_spectate(rpc_client, data):
    secret = data['secret']
    
    Task(rpc_client.events.activity_spectate(rpc_client, secret), KOKORO)


def handle_dispatch_activity_join_request(rpc_client, data):
    user = User.from_data(data['user'])
    
    Task(rpc_client.events.activity_join_request(rpc_client, user), KOKORO)


DISPATCH_EVENT_HANDLERS = {
    DISPATCH_EVENT_READY: handle_dispatch_ready,
    DISPATCH_EVENT_GUILD_STATUS_UPDATE: handle_dispatch_guild_status_update,
    DISPATCH_EVENT_GUILD_CREATE: handle_dispatch_guild_create,
    DISPATCH_EVENT_CHANNEL_CREATE: handle_dispatch_channel_create,
    DISPATCH_EVENT_CHANNEL_VOICE_SELECT: handle_dispatch_channel_voice_select,
    DISPATCH_EVENT_VOICE_SETTINGS_UPDATE: handle_dispatch_event_voice_settings_update,
    DISPATCH_EVENT_USER_VOICE_CREATE: handle_dispatch_user_voice_create,
    DISPATCH_EVENT_USER_VOICE_UPDATE: handle_dispatch_user_voice_update,
    DISPATCH_EVENT_USER_VOICE_DELETE: handle_dispatch_user_voice_delete,
    DISPATCH_EVENT_VOICE_CONNECTION_STATUS: handle_dispatch_voice_connection_status,
    DISPATCH_EVENT_MESSAGE_CREATE: handle_dispatch_message_create,
    DISPATCH_EVENT_MESSAGE_EDIT: handle_dispatch_message_edit,
    DISPATCH_EVENT_MESSAGE_DELETE: handle_dispatch_message_delete,
    DISPATCH_EVENT_SPEAKING_START: handle_dispatch_speaking_start,
    DISPATCH_EVENT_SPEAKING_STOP: handle_dispatch_speaking_stop,
    DISPATCH_EVENT_NOTIFICATION_CREATE: handle_dispatch_notification_create,
    DISPATCH_EVENT_ACTIVITY_JOIN: handle_dispatch_activity_join,
    DISPATCH_EVENT_ACTIVITY_SPECTATE: handle_dispatch_activity_spectate,
    DISPATCH_EVENT_ACTIVITY_JOIN_REQUEST: handle_dispatch_activity_join_request,
}


del handle_dispatch_ready
del handle_dispatch_guild_status_update
del handle_dispatch_guild_create
del handle_dispatch_channel_create
del handle_dispatch_channel_voice_select
del handle_dispatch_event_voice_settings_update
del handle_dispatch_user_voice_create
del handle_dispatch_user_voice_update
del handle_dispatch_user_voice_delete
del handle_dispatch_voice_connection_status
del handle_dispatch_message_create
del handle_dispatch_message_edit
del handle_dispatch_message_delete
del handle_dispatch_speaking_start
del handle_dispatch_speaking_stop
del handle_dispatch_notification_create
del handle_dispatch_activity_join
del handle_dispatch_activity_spectate
del handle_dispatch_activity_join_request
