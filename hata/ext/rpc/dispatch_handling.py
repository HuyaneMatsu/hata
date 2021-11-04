__all__ = ()

from ...backend.futures import Task
from ...discord.user import User
from ...discord.events.handling_helpers import asynclist
from ...discord.core import KOKORO, MESSAGES, CHANNELS
from ...discord.guild import create_partial_guild_from_data
from ...discord.message import Message, MessageRepr


from .constants import DISPATCH_EVENT_READY, DISPATCH_EVENT_GUILD_STATUS_UPDATE, \
    DISPATCH_EVENT_GUILD_CREATE, DISPATCH_EVENT_USER_VOICE_CREATE, DISPATCH_EVENT_USER_VOICE_UPDATE, \
    DISPATCH_EVENT_CHANNEL_CREATE, DISPATCH_EVENT_CHANNEL_VOICE_SELECT, DISPATCH_EVENT_USER_VOICE_DELETE, \
    DISPATCH_EVENT_VOICE_SETTINGS_UPDATE, DISPATCH_EVENT_VOICE_CONNECTION_STATUS, DISPATCH_EVENT_MESSAGE_CREATE, \
    DISPATCH_EVENT_MESSAGE_UPDATE, DISPATCH_EVENT_MESSAGE_DELETE, DISPATCH_EVENT_SPEAKING_START, \
    DISPATCH_EVENT_SPEAKING_STOP, DISPATCH_EVENT_NOTIFICATION_CREATE, DISPATCH_EVENT_ACTIVITY_JOIN, \
    DISPATCH_EVENT_ACTIVITY_SPECTATE, DISPATCH_EVENT_ACTIVITY_JOIN_REQUEST

from .event_types import GuildCreateEvent, ChannelCreateEvent, ChannelVoiceSelectEvent
from .voice_settings import VoiceSettings
from .rich_voice_state import RichVoiceState
from .voice_connection_status import VoiceConnectionStatus

def handle_dispatch_ready(rpc_client, data):
    rpc_client.user = User(data['user'])
    rpc_client._set_connection_waiter_result(True)
    
    Task(rpc_client.events.ready(rpc_client), KOKORO)


def handle_dispatch_guild_status_update(rpc_client, data):
    guild = create_partial_guild_from_data(data['guild'])
    
    Task(rpc_client.events.guild_status_update(rpc_client, guild), KOKORO)



def handle_dispatch_guild_create(rpc_client, data):
    guild_id = int(data['id'])
    guild_name = data['name']
    
    event = GuildCreateEvent(guild_id, guild_name)
    
    Task(rpc_client.events.guild_create(rpc_client, event), KOKORO)


def handle_dispatch_channel_create(rpc_client, data):
    channel_id = int(data['id'])
    channel_name = data['name']
    channel_type = data['type']
    
    event = ChannelCreateEvent(channel_id, channel_name, channel_type)
    
    Task(rpc_client.events.channel_create(rpc_client, event), KOKORO)


def handle_dispatch_voice_channel_select(rpc_client, data):
    channel_id = data.get('channel_id', None)
    if (channel_id is None):
        channel_id = 0
    else:
        channel_id = int(channel_id)
    
    guild_id = data.get('guild_id', None)
    if (guild_id is None):
        guild_id = 0
    else:
        guild_id = int(guild_id)
    
    event = ChannelVoiceSelectEvent(channel_id, guild_id)
    
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
    
    Task(rpc_client.events.message_create(rpc_client, message, old_attributes), KOKORO)


def handle_dispatch_message_delete(rpc_client, data):
    message_id = int(data['id'])
    try:
        message = MESSAGES[message_id]
    except KeyError:
        message = MessageRepr(message_id, 0, 0)
    else:
        channel_id = message.channel_id
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            pass
        else:
            channel._pop_message(message_id)
    
    Task(rpc_client.events.message_delete(rpc_client, message), KOKORO)


def handle_dispatch_speaking_start(rpc_client, data):
    user_id = int(data['user_id'])
    
    Task(rpc_client.events.speaking_start(rpc_client, user_id), KOKORO)


def handle_dispatch_speaking_stop(rpc_client, data):
    user_id = int(data['user_id'])
    
    Task(rpc_client.events.speaking_stop(rpc_client, user_id), KOKORO)


DISPATCH_EVENT_HANDLERS = {
    DISPATCH_EVENT_READY: handle_dispatch_ready,
    DISPATCH_EVENT_GUILD_STATUS_UPDATE: handle_dispatch_guild_status_update,
    DISPATCH_EVENT_GUILD_CREATE: handle_dispatch_guild_create,
    DISPATCH_EVENT_CHANNEL_CREATE: handle_dispatch_channel_create,
    DISPATCH_EVENT_CHANNEL_VOICE_SELECT: handle_dispatch_voice_channel_select,
    DISPATCH_EVENT_VOICE_SETTINGS_UPDATE: handle_dispatch_event_voice_settings_update,
    DISPATCH_EVENT_USER_VOICE_CREATE: handle_dispatch_user_voice_create,
    DISPATCH_EVENT_USER_VOICE_UPDATE: handle_dispatch_user_voice_update,
    DISPATCH_EVENT_USER_VOICE_DELETE: handle_dispatch_user_voice_delete,
    DISPATCH_EVENT_VOICE_CONNECTION_STATUS: handle_dispatch_voice_connection_status,
    DISPATCH_EVENT_MESSAGE_CREATE: handle_dispatch_message_create,
    DISPATCH_EVENT_MESSAGE_UPDATE: handle_dispatch_message_edit,
    DISPATCH_EVENT_MESSAGE_DELETE: handle_dispatch_message_delete,
    DISPATCH_EVENT_SPEAKING_START: handle_dispatch_speaking_start,
    DISPATCH_EVENT_SPEAKING_STOP: handle_dispatch_speaking_stop,
}


del handle_dispatch_ready
del handle_dispatch_guild_status_update
del handle_dispatch_guild_create
del handle_dispatch_channel_create
del handle_dispatch_voice_channel_select
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
