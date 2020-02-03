# class `DiscordGateway`

The gateway used by [Clients](Client.md) to communicate with Discord with
secure websocket.

- Source : [gateway.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/gateway.py)

## Instance attributes

### `client`

- type : [Client](Client.md)

The owner client of the gateway.

### `kokoro`

- type : `Kokoro` / `NoneType`
- default : `None`

The heart of the gateway, sends beat-data at set intervals. If does not
receives answer in time, restarts the gateway.

### `loop`

- type : `EventThread` / `NoneType`
- default : `None`

The loop used by the gateway. (Same as it's client's).

### `sequence`

- type : `int` / `NoneType`
- default : `None`

Last sequence number received from Discord.

### `session_id`

- type : `str` / `NoneType`
- default : `None`

Last session id received at `READY`.

### `shard_id`

- type : `int`
- default : `0`

The shard id of the gateway.

### `websocket`

- type : `WSClient` / `NoneType`
- default : `None`

The websocket client of the gateway.

## Class attributes

| name                  | value | description       | used at                                                                                                                                                                                                                           |
|-----------------------|-------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DISPATCH              | 0     | receive           | [`._received_message`](#_received_messageselfmessage-method)                                                                                                                                                                      |
| HEARTBEAT             | 1     | send / receive    | [`._beat`](#_beatself-method)<br>[`._special_operation`](#_special_operationselfoperationmessage-method)                                                                                                                          |
| IDENTIFY              | 2     | send              | [`._identify`](#_identifyself-method)                                                                                                                                                                                             |
| PRESENCE              | 3     | send              | [`Client.client_edit_presence`](Client.md#client_edit_presenceself)                                                                                                                                 |
| VOICE_STATE           | 4     | send              | [`._change_voice_state`](#_change_voice_stateselfguild_idchannel_idself_mutefalseself_deaffalse-method)                                                                                                                           |
| VOICE_PING            | 5     | removed           |                                                                                                                                                                                                                                   |
| RESUME                | 6     | send              | [`._resume`](#_resumeself-method)                                                                                                                                                                                                 |
| RECONNECT             | 7     | receive           | [`._special_operation`](#_special_operationselfoperationmessage-method)                                                                                                                                                           |
| REQUEST_MEMBERS       | 8     | send              | [`Client._request_members2`](Client.md#_request_members2selfguilds-method)<br>[`Client._request_members`](Client.md#_request_membersselfguild-method)<br>[`Client.request_member`](Client.md#request_memberselfguildnamelimit1)   |
| INVALIDATE_SESSION    | 9     | receive           | [`._special_operation`](#_special_operationselfoperationmessage-method)                                                                                                                                                           |
| HELLO                 | 10    | receive           | [`._special_operation`](#_special_operationselfoperationmessage-method)                                                                                                                                                           |
| HEARTBEAT_ACK         | 11    | receive           | [`._special_operation`](#_special_operationselfoperationmessage-method)                                                                                                                                                           |
| GUILD_SYNC            | 12    | send              |                                                                                                                                                                                                                                   |

## Properties

### `latency`

- type : `float`

The latency of the websocket. If no latency is recorded, will return
`kokoro.DEFAULT_LATENCY`.

## Methods

### `start(self,loop)`

- `awaitable`
- returns : `None`

Starts the gateway and it's [`.kokoro`](#kokoro) on the given loop.

### `run(self)`

- `awaitbale`
- returns : `bool`

Keeps the gateway receiving message and processing it. If the gateway needs to
be reconnected, reconnects itself. If connecting cannot succeed, because there
i no internet returns `True`, else returns `False` if the gateway's
[`.client`](#client) is disconnected. If `True` is returned the client stops
all other gateways too and tries to reconnect, when the internet is back,
the client will launch back the gateways.

### `send_as_json(self,data)`

- awaitable`
- returns : `None`

Sends the data as json to Discord on the [`.websocket`](#websocket). If there
is no websocket, or the websocket is closed will not raise.

### `close(self,*args,**kwargs)`

- `awaitbale`
- returns : `None`

Cancels the gateway's [`.kokoro`](#kokoro) and closes it's [.`websocket`](#websocket)
with the given args and kwargs.

## Magic methods

### `__init__(self,client,shard_id=0)`

Creates a gateway with it's default attributes.

### `__repr__(self)`

- returns : `str`

Returns the representation of the gateway.

## Internal

### `_decompresser` (instance attribute)

- type : `zlib.Decompress` / `NoneType`
- default : `None`

Zlib decompresser used to decompress the received data.

### `_buffer` (instance attribute)

- type : `bytearray`

A buffer used to store not finished payloads received from Discord.

### `_connect(self,resume=False)` (method)

- returns : `None`
- raises : `OSError` / `ConnectionError` / `ConnectionClosed` / `WebSocketProtocolError` / `InvalidHandshake` / `ValueError`

Connects the gateway to Discord. If the connecting was successfull,
will start it's [.`kokoro`](#kokoro) as well.

### `_poll_event(self)` (method)

- returns : `bool`
- raises : `TimeoutError` / `ConnectionClosed` / `WebSocketProtocolError` / `InvalidHandshake`

Waits for sockets from Discord till it collected a full one. If it did,
decompresses and processes it. Returns `True`, if the gateway should reconnect.

### `_received_message(self,message)` (method)

- returns : `bool`
- raises : `TimeoutError`

Processes the message sent by Discord. If the message is `DISPATCH`, ensures
the specific parser for it and returns `False`. For every other op code, it
calls [`._special_operation`](#_special_operationselfoperationmessage-method)
and returns it's return.

### `_special_operation(self,operation,message)` (method)

- returns : `bool`
- raises : `TimeoutError`

Handles special operations (so everything except `DISPATCH`). Returns `True`
if the gateway should reconnect.

### `_identify(self)` (method)

- `awaitable`
- returns : `None`

Sends an `IDENTIFY` packet to Discord.

### `_resume(self)` (method)

- `awaitable`
- returns : `None`

Sends a `RESUME` packet to Discord.

### `_change_voice_state(self,guild_id,channel_id,self_mute=False,self_deaf=False)` (method)

- `awaitable`
- returns : `None`

Sends a `VOICE_STATE` packet to Discord.

### `_beat(self)` (method)

- `awaitable`
- returns : `None`

Sends a `HEARTBEAT` packet to Discord.

### `_terminate(self,*args,**kwargs)` (method)

- `awaitable`
- returns : `None`

Familiar to [`.close`](#closeselfargskwargs), but it just terminates
[`.kokoro`](#kokoro) instead of cancelling it.


