__all__ = ()

from ...backend.futures import Task
from ...discord.user import User
from ...discord.events.handling_helpers import asynclist
from ...discord.core import KOKORO
from ...discord.guild import create_partial_guild_from_data

from .constants import DISPATCH_EVENT_READY, DISPATCH_EVENT_GUILD_STATUS_UPDATE, \
    DISPATCH_EVENT_GUILD_CREATE, DISPATCH_EVENT_USER_VOICE_CREATE, DISPATCH_EVENT_USER_VOICE_UPDATE, \
    DISPATCH_EVENT_CHANNEL_CREATE, DISPATCH_EVENT_CHANNEL_VOICE_SELECT, DISPATCH_EVENT_USER_VOICE_DELETE, \
    DISPATCH_EVENT_VOICE_SETTINGS_UPDATE, \
    
from .event_types import GuildCreateEvent, ChannelCreateEvent, ChannelVoiceSelectEvent
from .voice_settings import VoiceSettings
from .rich_voice_state import RichVoiceState

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



DISPATCH_EVENT_HANDLERS = {
    DISPATCH_EVENT_READY: handle_dispatch_ready,
    DISPATCH_EVENT_GUILD_STATUS_UPDATE: handle_dispatch_guild_status_update,
    DISPATCH_EVENT_GUILD_CREATE: handle_dispatch_guild_create,
    DISPATCH_EVENT_CHANNEL_CREATE: handle_dispatch_channel_create,
    DISPATCH_EVENT_CHANNEL_VOICE_SELECT: handle_dispatch_voice_channel_select,
    DISPATCH_EVENT_VOICE_SETTINGS_UPDATE: handle_dispatch_event_voice_settings_update,
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
