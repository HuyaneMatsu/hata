# class `MessageIterator`

An asyncronous iterator what iterates over the [messages](Message.md) of a
[text channel](ChannelTextBase.md). This iterator is not message deletion,
neither message creation safe.

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/channel.py)

Can be created with
[client method](Client.md#message_iteratorselfchannelchunksize97), or directly
as `MessageIterator(client, channel, chunksize=97)`.

## Instance attributes

### `client`

- type : [`Client`](Client.md)

The client, with what the iterator requests the messages at it's
[`.channel`](#channel) from Discord.

### `channel`

- type : [`ChannelTextBase`](ChannelTextBase.md) subclass

The message iterator's source channel, what's messages it requests and
iterates over.

### `chunksize`

- type : `int`

Each time, when all the loaded messages of the channel are iterated over, the
[`MessageIterator`](MessageIterator.md) will request messages from Discord.
The `chunksize` attribute tells, with how much we should extend the amount
of loaded messages of the channel, when needed.

`chunksize` is preferably `97`, because at that case the wrapper with only 1
request can extend the channel's [message history](ChannelTextBase.md#messages)
with 97 messages. The wrapper chains up the messages to the already loaded
ones, but for this it need to make sure, that it did not skip any of them, so
it always request 3 extra messages.

If you do not want to request that much messages each time, a lower amount is
acceptable as well. Setting higher amount than `97` is unreasoned.

## Magic methods

### `__init__(self,client,channel,chunksize=97)`

Creates a message iterator instance.

### `__aiter__(self)`

- returns : [`MessageIterator`](MessageIterator.md)

Returns the message iterator itself.

### `__anext__(self)`

- `awaitable`
- returns : [`Message`](Message.md)
- raises : `StopAsyncIteration`

Retruns the next [message](Message.md) at the channel, or cancels the loop,
if there is no more.

### `__repr__(self)`

- returns : `str`

Returns the representation of message iterator.

## Internal

### `_index` (instance attribute)

- type : `int`

The index of the next message to be returned at the [channel](#channel)'s
[message history](ChannelTextBase.md#messages).

### `__can_read_history` (instance attribute)

- type : `bool`

Tells to the iterator if the [client](#client) can **not** request older
messages of the [channel](#channel).
