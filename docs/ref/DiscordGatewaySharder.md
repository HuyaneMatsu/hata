# class `DiscordGatewaySharder`

Sharder gateway used to control more [`DiscordGateways`](DiscordGateway.md).

- Source : [gateway.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/gateway.py)

## Instance attributes

### `client`

- type : [Client](Client.md)

The owner client of the gateway.

### `loop`

- type : `EventThread` / `NoneType`
- default : `None`

The loop used by the gateway. (Same as it's client's).

### `gateways`

- type : `list`
- elements : [`DiscordGateway`](DiscordGateway.md)

The gateways, which the sharder controls.

## Properties

### `latency`

- type : `float`

The average latency of the gateways. If no latency is recorded, will return
`kokoro.DEFAULT_LATENCY`.

## Methods

### `start(self,loop)`

- `awaitable`
- returns : `None`

Starts the [`.gateways`](#gateways) on the given loop.

### `run(self)`

- `awaitbale`
- returns : `bool`

Runs the [`.gateways`](#gateways). If any of them returns `True`, stops the
rest and returns `True`. `False` return in ignored, because it means every
other gateway will be stopped as well.

### `send_as_json(self,data)`

- awaitable`
- returns : `None`

Sends the data as json to Discord on all of it's [gateway](#gateways).

### `close(self,*args,**kwargs)`

- `awaitbale`
- returns : `None`

Cancels the gateway's [`.kokoro`](#kokoro) and closes it's [.`websocket`](#websocket)
with the given args and kwargs.

## Magic methods

### `__init__(self,client)`

Creates an empty gateway sharder with default attributes.

### `__repr__(self)`

- returns : `str`

Returns the representation of the gateway.
