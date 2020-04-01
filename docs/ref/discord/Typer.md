# class `Typer`

A context manager to keep the [client](Client.md) typing.

- Source : [client.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/client.py)

A typing request is displayed for `8` seconds, or till the client sends a
[message](Message.md) to the target [`Channel`](CHANNEL_TYPES.md). It means
the typing duration is always rounded up to a multiple of 8. Also the messages
sent by the [client](Client.md) are not taken into the account.

## Creation

Theere are two ways to keep the client typing:

```py
#shortcut
with client.keep_typing(channel,timeout=300.):
    pass # do stuffs

#or

#normal
with Typer(client,channel,timeout=300.):
    pass # do stuffs
```

##### `client`

A [`Client`](Client.md), who will keep typing.

##### `channel`

The [`Channel`](CHANNEL_TYPES.md) where the typing will be sent

##### `timeout`

Optional `float`. The maximal duration, how long the client will keep typing.

## Instance attributes

| name      | type                          | description                                               |
|-----------|-------------------------------|-----------------------------------------------------------|
| channel   | [Channel](CHANNEL_TYPES.md)   | The channel were the typing is executed.                  |
| client    | [Client](Client.md)           | The client who executes the typing.                       |
| timeout   | float                         | The maximal duration of the typing.                       |
| waiter    | [Future](Future.md)           | A sleeping future what wakes up the task to send typing.  |

## Methods

### `cancel(self)`

If the context manager is still active, cancels it.

## Magic methods

### `__enter__`, `__exit__`

Meanwile the contextmanager is entered it will keep sending typing to it's
[channel](CHANNEL_TYPES.md), till it is exited, the `timeout` occures, or it
cancelled.

## Internal

### `run(self)`

- awaitable

The coroutine what keeps sending the typing requests.



