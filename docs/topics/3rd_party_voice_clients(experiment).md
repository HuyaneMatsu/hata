# 3rd party voice clients (VIP)

When using python and want to play music, you might meet a big problem, which is python's GIL. Single core processing
power is not a good thing, when you have CPU intensive tasks.

For this purpose, you may integrate 3rd party voice playing libraries to hata, and soon you will see, how to.

## Getting started

First check, what python bindings you, or the 3rd party library uses.
- If it uses blocking io code, make sure to executors, or start other threads.
- If it is asyncio based, make sure to import `hata.ext.asyncio`, which adds support for asyncio based modules when
using hata.

## Related events

Hata separates many different voice related events, which can be separated to 4 groups:

### Internal
    
- `voice_client_ghost`

    Called when the client logs in and detects a "ghost" voice state.
    
    Ghost voice states are voice states of the client. You can either decide to connect, connect and disconnect,
    or to do nothing with it at all.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)

- `voice_client_shutdown`
    
    Called when the client logs out.
    
    Pretty self explanatory, the user should log their voice clients and / or store their details, for reconnect.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)

### Voice server update

- `voice_server_update`

    Called initially when a voice client joins, and when a guild's voice server is updated.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceServerUpdateEvent](https://www.astil.dev/project/hata/docs/hata/discord/events/event_types/VoiceServerUpdateEvent)
    
    Voice server update event exposes the following attributes:
    ```
    .endpoint
    .guild_id
    .token
    ```

### Voice client updates

Voice client updates relate directly to the client, not like [user voice updates](#user-voice-updates), which are
related to every user.

Voice client updated usually operate with voice states, which expose the following related attributes:
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
    - `old_channel_id` (`int`) The channel's identifier from where the client left from.

- `voice_client_move`
    
    Called when the client moves / is moved between two channels.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_channel_id` (`int`) The channel's identifier from where the client moved from.

- `voice_client_update`
    
    Called when the client's voice state is updated.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_attributes` (`dict`) `attribute-name` - `old_value` pairs of the client voice state's changed attributes.

### User voice updates

- `user_voice_join`
    
    Called when the client join a voice channel.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)

- `user_voice_leave`
    
    Called when a user leaves from a voice channel.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_channel_id` (`int`) The channel's identifier from where the user left from.

- `user_voice_move`
    
    Called when a user moves / is moved between two channels.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_channel_id` (`int`) The channel's identifier from where the user moved from.

- `user_voice_update`
    
    Called when a user's voice state is updated.
    
    Parameters:
    - [Client](https://www.astil.dev/project/hata/docs/hata/discord/client/client/Client)
    - [VoiceState](https://www.astil.dev/project/hata/docs/hata/discord/user/voice_state/VoiceState)
    - `old_attributes` (`dict`) `attribute-name` - `old_value` pairs of the voice state's changed attributes.

## Api usage

To deal with voice client connections, you will need to get the respective guild's gateway.

```py
gateway = client.gateway_for(guild_id)
```

For modifying the a voice client's state, use `gateway.change_voice_state(...)`.
 
For `IDENTIFY` and `RESUME` voice gateway operations, you will need the guilds gateways's `session_id`.
It can be access as `gateway.session_id`.

### Joining to voice channel

For joining, first get the gateway of the guild where you wish to join, then call it's `.change_voice_state`.

```py
gateway = client.gateway_for(guild_id)
await gateway.change_voice_state(guild_id, channel_id)
```

When you joined the channel, `client.events.voice_client_join` is called, where you should update the voice client's
channel.

```py
@client.events(overwrite=True)
async def voice_client_join(client, voice_state):
    voice_client.channel_id = voice_state.channel_id
```

> Both `.channel` and `.channel_id` works.

### Moving between voice channels.

Moving between voice channel is familiar to joining.

```py
gateway = client.gateway_for(guild_id)
await gateway.change_voice_state(guild_id, channel_id)
```

```py
@client.events(overwrite=True)
async def voice_client_move(client, voice_state, old_channel_id):
    voice_client.channel_id = voice_state.channel_id
```

### Leaving from voice channel

To leave from a voice channel, pass `channel_id` parameter of `change_voice_state` as `0`.

```py
gateway = client.gateway_for(guild_id)
await gateway.change_voice_state(guild_id, 0)
```

```py
@client.events(overwrite=True)
async def voice_client_leave(client, voice_state, old_channel_id):
    await voice_client.disconnect()
```

### Editing voice state

To edit voice state use the `self_mute` and the `self_deaf` parameters of `change_voice_state`.

```py
gateway = client.gateway_for(guild_id)
await gateway.change_voice_state(guild_id, channel_id, self_mute=..., self_deaf=...)
```

```py
@client.events(overwrite=True)
async def voice_client_update(client, voice_state, old_attributes):
    ...
```

TODO:

Mention `voice_client_ghost`
Mention `voice_client_shutdown`
Mention getting voice region.
Mention getting entities from cache.
Ask braindead for a rework.
