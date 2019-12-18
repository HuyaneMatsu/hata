# class `VoiceClient`

Represents a [client](Client.md), who is connected to a
[voice channel](ChannelVoice.md).

- Source : [voice_client.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/voice_client.py)

## Instance Attributes

### `call_after`

- type : `function`
- `awaitable`

A coroutine function what is awaited, when the voice clients's current
audio finished playing. By default this attribute is set to the
[`._play_next`](#_play_nextselflock-method) function, what as it says plays the
next audio at the voice clients's [`.queue`](#queue).

This attribute of the client can be modified freely. Two arguments are passed;
The [`VoiceClient`](VoiceClient.md) itself and `lock` (`True` / `False`). If
`lock` is passed as `True` means that the [`.player`](#player) thread called
this method and this method should not it's [`.lock`](#lock) meanwhile.
If the function is called from the own thread, then the `lock` argument is passed
as `True`, so the method should be using [`.lock`](#lock) meanwhile it operates.

### `channel`

- type : [`ChannelVoice`](ChannelVoice.md)

The channel where the voice client currently is.

> Calls, so [`private`](ChannelPrivate.md) and [`group`](ChannelGroup.md)
channels are not supported (/tested) yet.

### `client`

- type : [`Client`](Client.md)

The [voice client](VoiceClient.md)'s owner [client](Client.md).

### `connected`

- type : `threading.Event`

Used to communicate with the [AudioPlayer](AudioPlayer.md) thread.

### `gateway`

- type : [`DiscordGatewayVoice`](DiscordGatewayVoice.md)

The gateway through what the voice client communicates with Discord.

### `lock`

- type : `threading.Lock`

A `Lock` used meanwile changing the currently playing audio to avoid chaging
it multyple times at the same time.

### `loop`

- type : `EventThread`

The eventloop of the [voice client](VoiceClient.md)'s owner
[client](Client.md).

### `player`

- type : [AudioPlayer](AudioPlayer.md) / `Nonetype`
- default : `None`

The actual player of the [VoiceClient.md]. If the voice client is not playing
nor paused, then this value is set to `None`.

### `queue`

- type : `list`
- elements : [`AudioSource`](AudioSource.md) instances

A list of the scheduled audios.

### `socket`

- type : `socket.socket` / `NoneType`
- default : `None`

The socket through what the [`VoiceClient`](VoiceClient.md) sends the
voice data to Discord. Created by the
[`._create_socket`](#_create_socketself-data-method) method, when the client's gateway
receives response after connecting. If the client leaves the voice
channel, then the socket is closed and set back to `None`.

### `speaking`

- type : `int`
- default : `0`

If the client is showed by Discord as `speaking`, then this attribute should
be set to `1`. This attribute can be modified, with the
[`.set_speaking`](#set_speakingself-value) method, but that is called automatically, when
the audio of the [`VoiceClient`](VoiceClient.md) is playing or not.

### `reader`

- type : [`AudioReader`](AudioReader.md) / `NoneType`
- default : `None`

Meqnhile the received audio data is processed this attribute is set to a
running [`AudioReader`](AudioReader.md).

### `sources`

- type : `dict`
- items : (`int`, `int`)

A [user](User.md)_id, ssrc mapping used by the [`.reader`](#reader).

## Properties

### `guild`

- returns : [`Guild`](Guild.md)

Returns the [`VoiceClient`](VoiceClient.md)'s [`.channel`](#channel)'s guild.

### `volume` (get/set)

- returns : `float`

The voice client's volume. It can be between 0.0 and 2.0.

### `source`

- returns : [`AudioSource`](AudioSource.md) instances / `NoneType`
- default : `None`

Returns the [`VoiceClient`](VoiceClient.md)'s [`.player`](#player)'s source.
If the voice client has no player or the player has no source returns `None`.

## Methods

### `set_speaking(self, value)`

- `awaitable`
- returns : `None`

A coroutine, what is used to change the [`.speaking`](#speaking) state of the
voice client. If audio is not played, then the speaking state is changed to
`False`, and when it is playing, then changed to `True` by default, so 
tinkering with this method is not too reasonable.

### `listen(self)`

- returns : [`AudioReader`](AudioReader.md)

If the client has a [`.reader`](#reader) returns it, else created a new one.
    
### `move_to(self, channel)`

- `awaitable`
- returns : `None`

A coroutine what can be used directly on the [`VoiceClient`](VoiceClient.md),
to move it at it's [`.guild`](#guild) between
[voice channels](ChannelVoice.md).

### `append(self, source)`

- returns : `bool`

Used to play [audio source](AudioSource.md). If the client has no player, then
start playing and returns `True` If the client has player, then adds it on the
[`.queue`](#queue) and returns `False`

### `skip(self)`

- returns : `None`

Skips the currently playing audio and starts the next if applicable.

### `pause(self)`

- returns : `None`

Pauses the currently played audio if applicable.

### `resume(self)`

- returns : `None`

Resumes the currently stopped audio if applicable.

### `stop(self)`

- returns : `None`

Stops the currently playing audio, closes the player and cleares the
[.queue](#queue).

### `is_connected(self)`

- returns : `bool`

Returns whether if the [`VoiceClient`](VoiceClient.md) is connected to a
[voice channel](ChannelVoice.md).

### `is_playing(self)`

- returns : `bool`

Returns whether the [`VoiceClient`](VoiceClient.md) 's [`.player`](#player)
is playing audio right now or not.

### `is_paused(self)`

- returns : `bool`

Returns whether the [`VoiceClient`](VoiceClient.md) 's [`.player`](#player)
is paused right now. If the voice client has no player, return `True`.

### `connect(self)`

- returns : `Future`

Connects the [`VoiceClient`](VoiceClient.md) to it's [`.channel`](#channel).
The method returns a `Future`, what is set, when the connection is made.
If the client cannot connect to the channel, then it raises `TimeoutError`.

### `disconnect(self, force=True, terminate=True)`

- `awaitable`
- returns : `None`

Disconnects the [`VoiceClient`](VoiceClient.md).

If `force` is set to `False`, then disconnects the client only if it is
not connected (for example when it is connecting).

`terminate` is set to `True` if it is an internal disconnect. If the Disconnect
comes from Discord's side, then `terminate` is `False`, what means, we do
not need to terminate the gateway handshake.

If you want to disconnect your [`VoiceClient`](VoiceClient.md), then you
should let the method to use it's default arguments. Passing bad default
arguments at cases can cause failures.

## Magic methods

### `__repr__(self)`

- returns : `str`

Returns the representation of the voice client.

### `__new__(cls,client,channel)`

- `awaitable`
- returns : `Future` -> [`VoiceClient`](VoiceClient.md)
- raises `RuntimeError` -> `TimeoutError`

Creates a voice client. If any of the required libraries are
not present, raises `RuntimeError`.

If the voice client was succesfully created, it returns a `Future`, what
is a waiter for it's [`._connect`](#_connectself-waiternone-method) method. When the client
connets to the [voice channel](`ChannelVoice`), the future's result will
be set as the voice client. If the connection was not successfull, the
future will raise `TimeoutError`.

## Internal 

##### Internal instance attributes

| name                      | type                                          | description                                                                                       |
|---------------------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------|
| `_encoder`                | `OpusEncoder`                                 | The Opus encoder of the voice client, to encode not encoded audio data.                           |
| `_endpoint`               | `NoneType` / `str`                            | The endpoint, where the voice client sends the audio data.                                        |
| `_endpoint_ip`            | `NotImplementedType` / ( `tuple` of `ints` )  | The ip version of the `._endpoint` attribute.                                                     |
| `_freezed`                | `bool`                                        | Whether the VoiceClient is freezed to be reconnected, when the client gateway resets.             |
| `_freezed_resume`         | `bool`                                        | Whether the VoiceClient was playin when it was freezed.                                           |
| `_handshake_complete`     | `Future`                                      | Used for awaiting the connecting handshake with Discord.                                          |
| `_ip`                     | `NotImplementedType` / ( `tuple` of `ints` )  | The ip to what the voice client's gateway connects.                                               |
| `_port`                   | `NotImplementedtype` / `int`                  | The port to what the voice client's gateway connects.                                             |
| `_pref_volume`            | `float`                                       | The prefered volume of the voice client.                                                          |
| `_secret_box`             | `NoneType` / `nacl.secret.SecretBox`          | The data encoder of the voice client.                                                             |
| `_sequence`               | `int`                                         | Counter to define the sent data's sequence for Discord.                                           |
| `_session_id`             | `NoneType` / `str`                            | The session id of the voice client's owner client's shard.                                        |
| `_set_speaking_task`      | `NoneType` / `Task`                           | Synchronization task for the `.set_speaking` coroutine.                                           |
| `_source`                 | `int`                                         | An integer sent by Discord and it needs to be sent to Discord with the data.                      |
| `_timestamp`              | `int`                                         | An integer what is sent to Discord to tell how much frames we sent to it.                         |
| `_token`                  | `str`                                         | Token received by the voice client's owner client's gateway. Used to authorize the voice client.  |
| `_voice_port`             | `int`                                         | The port, where the voice client sends the audio data.                                            |

### `_connect(self, waiter=None)` (method)

- `awaitable`
- returns : `None`

Connects the [`VoiceClient`](VoiceClient.md) to Discord and keeps receiving 
events through it's gateway.

### `_start_handshake(self)` (method)

- `awaitable`
- returns : `None`
- raises : `TimeoutError`

Requests a gateway handshake from Discord. If we get answer in it, means, we
can open the socket to send audio data.

### `_terminate_handshake(self)` (method)

- `awaitable`
- returns : `None`

Called when connecting to Discord fails. It ensures, that everything is
aborted correctly.

### `_create_socket(self, data)` (method)

- `awaitable`
- returns : `None`

Ensured by the voice client's owner client's gateway. It processes the data
sent by Discord. If the data is correct, then opens the voice client's
[`.socket`](#socket) and marks the connecting handshake as completed.

### `._play_next(self,lock)` (method)

- `awaitable`
- returns : `bool`

Starts to play the next audio object on the [`.queue`](#queue) and cancels
the actual one if applicable.

If called from the same thread, the `lock` argument should be passed as
`True`, if called from other, as `False`.

The method returns `True` if there is nothing to play anymore, else`False`.

### `_freeze(self)` (method)

- returns : `None`

Freezes the voice client and pauses it's player.

### `_unfreeze(self)` (method)

- returns : `None`

Unfreezes the voice client if needed.

### `_unfreeze_task(self)` (method)

- `awaitable`
- returns : `None`

The coroutine ensured, when the voice client needs unfreezing.

### `_kill_ghost(cls,client,state)` (classmethod)

- `awaitable`
- returns : `None`

When the client is restarted, it might happen that it is still in some
[voice channels](ChannelVoice.md). If that is the case, this method is
called to kill the ghost connection.

### `__del__(self)` (magic method)

- returns : `None`

Used to cleanup the voice client's [`.socket`](#socket), if it was deleted
before closing corretly with any reason.
