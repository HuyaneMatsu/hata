# class `DiscordGatewayVoice`

The gateway used by [VoiceClients](Client.md) to communicate with Discord with
secure websocket.

- Source : [gateway.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/gateway.py)

## Instance attributes

### `client`

- type : [VoiceClient](VoiceClient.md)

The owner voice client of the gateway.

### `kokoro`

- type : `Kokoro` / `NoneType`
- default : `None`

The heart of the gateway, sends beat-data at set intervals. If does not
receives answer in time, restarts the gateway.

### `loop`

- type : `EventThread` / `NoneType`
- default : `None`

The loop used by the gateway. (Same as it's client's).

### `websocket`

- type : `WSClient` / `NoneType`
- default : `None`

The websocket client of the gateway.

## Class attributes

| name                  | value | description       | used at                                                                                                                   |
|-----------------------|-------|-------------------|---------------------------------------------------------------------------------------------------------------------------|
| IDENTIFY              | 0     | send              | [`._identify`](#_identifyself-method)                                                                                     |
| SELECT_PROTOCOL       | 1     | send              | [`._select_protocol`](#_select_protocolselfipport-method)                                                                 |
| READY                 | 2     | receive           | [`._initial_connection`](#_initial_connectionselfdata-method)                                                             |
| HEARTBEAT             | 3     | send              | [`._beat`](#_beatself-method)                                                                                             |
| SESSION_DESCRIPTION   | 4     | receive           | [`._received_message`](#_received_messageselfmessage-method)                                                              |
| SPEAKING              | 5     | send /receive     | [`._set_speaking`](#_set_speakingselfis_speaking-method)<br>[.`_received_message`](#_received_messageselfmessage-method)  |
| HEARTBEAT_ACK         | 6     | receive           | [`._received_message`](#_received_messageselfmessage-method)                                                              |
| RESUME                | 7     | send              | [`._resume`](#_resumeself-method)                                                                                         |
| HELLO                 | 8     | receive           | [`._received_message`](#_received_messageselfmessage-method)                                                              |
| INVALIDATE_SESSION    | 9     | receive           | [`._received_message`](#_received_messageselfmessage-method)                                                              |
| CLIENT_CONNECT        | 12    | receive           | [`._received_message`](#_received_messageselfmessage-method)                                                              |
| CLIENT_DISCONNECT     | 13    | receive           | [`._received_message`](#_received_messageselfmessage-method)                                                              |

## Properties

### `latency`

- type : `float`

The latency of the websocket. If no latency is recorded, will return
`kokoro.DEFAULT_LATENCY`.

## Methods

### `start(self,loop)`

- `awaitable`
- returns : `None`

Starts the voice gateway and it's [`.kokoro`](#kokoro) on the given loop.

### `connect(self)`

- returns : `None`
- raises : `OSError` / `ConnectionError` / `ConnectionClosed` / `WebSocketProtocolError` / `InvalidHandshake`

Connects the voice gateway to Discord. If the connecting was successfull,
will start it's [.`kokoro`](kokoro) as well.

### `send_as_json(self,data)`

- awaitable`
- returns : `None`

Sends the data as json to Discord on the [`.websocket`](#webscoket). If there
is no websocket, or the websocket is closed will not raise.

### `close(self,*args,**kwargs)`

- `awaitbale`
- returns : `None`

Cancels the gateway's [`.kokoro`](#kokoro) and closes it's [.`websocket`](#websocket)
with the given args and kwargs.

## Magic methods

### `__init__(self,voice_client)`

Creates a voice gateway with it's default attributes.

### `__repr__(self)`

- returns : `str`

Returns the representation of the voice gateway.

## Internal

### `_poll_event(self)` (method)

- returns : `bool`
- raises : `TimeoutError` / `ConnectionClosed` / `WebSocketProtocolError` / `InvalidHandshake` / `ValueError`

Waits for sockets from Discord, If it received one, processes it.

### `_received_message(self,message)` (method)

- returns : `bool`
- raises : `TimeoutError`

Processes the message sent by Discord.

### `_identify(self)` (method)

- `awaitable`
- returns : `None`

Sends an `IDENTIFY` packet to Discord.

### `_resume(self)` (method)

- `awaitable`
- returns : `None`

Sends a `RESUME` packet to Discord.

### `_select_protocol(self,ip,port)` (method)

- `awaitable`
- returns : `None`

Sends a `SELECT_PROTOCOL` packet to Discord.

### `_beat(self)` (method)

- `awaitable`
- returns : `None`

Sends a `HEARTBEAT` packet to Discord.

### `_initial_connection(self,data)` (method)

- `awaitiable`
- returns : `None`

Processes the data from `READY` operation and
[selects protocol](#_select_protocolselfipport-method).

### `_send_silente_packet(self)` (method)

- `awaitable`
- returns : `None`

Sends silence packets to Discord on [voice client's](VoiceClient.md)
[socket](VoiceClient.md#socket). Used after connecting.

### `_set_speaking(self,is_speaking)` (method)

- `awaitable`
- returns : `None`

Sends a `SPEAKING` packet with the specific `is_speaking` state.

### `_terminate(self,*args,**kwargs)` (method)

- `awaitable`
- returns : `None`

Familiar to [`.close`](#closeselfargskwargs), but it just terminates
[`.kokoro`](#kokoro) instead of cancelling it.


