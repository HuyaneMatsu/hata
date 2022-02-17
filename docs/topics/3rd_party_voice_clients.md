# Introduction

If you ever wanted to play music with Python you might have stumbled upon a big problem - Python GIL.

For CPU intensive tasks, relying on single core is not optimal and for this purpose you might want to integrate 3rd
party voice libraries which will be explained below.

# Getting started

First check which Python bindings you or the 3rd party library use:
- If it's blocking IO code then make sure to executors or start other threads.
- If it's asyncio based then make sure to import `hata.ext.asyncio`, which adds support for asyncio based modules when
using Hata.

# Related events

Hata separates many voice related events, which are separated in 4 groups:

## Internal
    
- `voice_client_ghost`

    Called when the client logs in and detects a "ghost" voice state.
    
    Ghost voice states are voice states of the client. You can either decide to connect, connect and disconnect,
    or to do nothing with it at all.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)

- `voice_client_shutdown`
    
    Called when the client logs out.
    
    Pretty self-explanatory - the user should log their voice clients and / or store their details for reconnect.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)

## Voice server update

- `voice_server_update`

    Initially called when the voice client joins and when the guilds voice server is updated.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceServerUpdateEvent](https://www.astil.dev/project/hata/docs/hata/discord/events/event_types/VoiceServerUpdateEvent)
    
   The event exposes the following attributes:
    ```
    .endpoint
    .guild_id
    .token
    ```

## Voice client updates

Voice client updates relate directly to the client unlike [user voice updates](#user-voice-updates) which are
related to every user.

Voice client update usually operate with voice states which expose the following related attributes:
```
.channel_id
.guild_id
.session_id
.user_id
```

- `voice_client_join`
    
    Called when the client join a voice channel.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)

- `voice_client_leave`
    
    Called when the client leaves from a voice channel.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_channel_id` (`int`) The channels identifier from where the client left from.

- `voice_client_move`
    
    Called when the client moves / is moved between two channels.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_channel_id` (`int`) The channels identifier from where the client moved out from.

- `voice_client_update`
    
    Called when the client voice state is updated.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_attributes` (`dict`) `attribute-name` - `old_value` pairs of the client voice state changed attributes.

## User voice updates

- `user_voice_join`
    
    Called when the client join a voice channel.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)

- `user_voice_leave`
    
    Called when a user leaves voice channel.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_channel_id` (`int`) The channels identifier from where the user left from.

- `user_voice_move`
    
    Called when a user moves / is moved between two channels.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_channel_id` (`int`) The channels identifier from where the user moved out from.

- `user_voice_update`
    
    Called when a user voice state is updated.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_attributes` (`dict`) `attribute-name` - `old_value` pairs of the voice state changed attributes.

# Api usage

To deal with voice client connections you will need to use the respective guild gateway. To get it, do:

```py
gateway = client.gateway_for(guild_id)
```

For modifying the voice client state use `gateway.change_voice_state(...)`.
 
For `IDENTIFY` and `RESUME` voice gateway operations you will need the guilds gateway `session_id`.
It can be accessed trough `gateway.session_id`.

Don't forget to overwrite **all** `voice_client_...` events when dealing with voice clients.
To overwrite (replace) one use the `overwrite=True` parameter.

## Joining to voice channel

For joining, first get the gateway of the guild where you wish to join then call its `.change_voice_state`.

```py
gateway = client.gateway_for(guild_id)
await gateway.change_voice_state(guild_id, channel_id)
```

When you join the channel, `client.events.voice_client_join` will be called, in which you should update the voice client
channel.

```py
@client.events(overwrite=True)
async def voice_client_join(client, voice_state):
    voice_client = get_voice_client(voice_state.guild_id)
    if voice_client is not None:
        voice_client.channel_id = voice_state.channel_id
```

> Both `.channel` and `.channel_id` works.

## Moving between voice channels.

Moving between voice channel is similar to joining.

```py
gateway = client.gateway_for(guild_id)
await gateway.change_voice_state(guild_id, channel_id)
```

```py
@client.events(overwrite=True)
async def voice_client_move(client, voice_state, old_channel_id):
    voice_client = get_voice_client(voice_state.guild_id)
    if voice_client is not None:
        voice_client.channel_id = voice_state.channel_id
```

## Leaving from voice channel

To leave from a voice channel, pass parameter `channel_id` as `0` to the `change_voice_state` method.

```py
gateway = client.gateway_for(guild_id)
await gateway.change_voice_state(guild_id, 0)
```

```py
@client.events(overwrite=True)
async def voice_client_leave(client, voice_state, old_channel_id):
    voice_client = get_voice_client(voice_state.guild_id)
    if voice_client is not None:
        await voice_client.disconnect()
```

## Editing voice state

To edit voice state use the `self_mute` and the `self_deaf` parameters of `change_voice_state`.

Handling this event is optional, but its recommended overwriting it.

```py
gateway = client.gateway_for(guild_id)
await gateway.change_voice_state(guild_id, channel_id, self_mute=..., self_deaf=...)
```

```py
@client.events(overwrite=True)
async def voice_client_update(client, voice_state, old_attributes):
    ...
```

# Ghost voice clients

If you do not want to deal with ghost clients, just register an empty function or just disconnect the client from the
voice channel.

```py
@client.events(overwrite=True)
async def voice_client_ghost(client, voice_state):
    voice_client = await join_voice_client(voice_state)
    await voice_client.disconnect()
```

# Shutting down voice clients

Shutting down voice clients and awaiting their shutdown.

Since only after all `voice_client_shutdown` events are completed will the clients gateways disconnect, it is recommended to
create parallel tasks for disconnects and to wait for their completion.

```py
from hata import WaitTillAll

@client.events(overwrite=True)
async def voice_client_shutdown(client):
    tasks = []
    for voice_client in voice_clients:
        task = client.loop.cretae_task(voice_client.disconnect())
        tasks.append(task)
    
    await WaitTillAll(tasks, client.loop)
```

# Voice server update

After connecting to a voice channel the `voice_server_update_event` is received. If the event has both `endpoint` and
`token` set as non-`None` you are free to create your datagram connection.

```py
@client.events(overwrite=True)
async def voice_server_update(client, event):
    voice_client = get_voice_client(event.guild_id)
    if voice_client is not None:
        await voice_client.create_socket(event)
```

# Tips

### Track voice region

The voice client is disconnected when its channel voice region changes. To avoid this, you might want to check whether
the client got disconnected indeed because ofg region change or just normal disconnect.

To get the channel voice region you can use `channel.region`.

### Getting entity from cache

In certain cases you might need rich information about entities, but you only have their ID available.
Even tho most objects will expose entity access too, e.g. they have `channel_id` attribute and a `channel` property, this may not be enough.

In these cases use `USERS`, `GUILDS`, `CHANNELS` caches to access the entities.

```py
channel = CHANNELS.get(channel_id, None)
```
