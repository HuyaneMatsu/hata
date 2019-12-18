# class `ReadyState`

[Clients](Client.md) meanwhile logging in have their
[`.ready_state`](Client.md#ready_state) attribute set to a `ReadyState` object.

`ReadyState` delays [`Client._delay_ready`](Client.md#_delay_readyself-method),
till receiving all guild data is done. If it happens the client will request
the members of large guilds, then ensure
[Client.events.ready](EventDescriptor.md#readyclient).

- source : [parsers.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/parsers.py)

## Instance attributes

### `counter`

- type : `int`
- default : `0`

A counter, what defines how much guilds we expect to receive. Every time, when
a shard gets ready, it increases this counter by the amount of guilds, what the
shard has. Meanwhile whenever we receive a guild's data, this counter is 
descreased by one.

It can happen, that a shard receives all it's guilds before an other gets
ready, so we wait at least 1 second after a shard got ready. An exception is,
when the client has only 1 shard (/0) total.

### `guilds`

- type : `list`
- elements : [`Guild`](Guild.md)

A list of the received [guilds](Guild.md), of which we will request users.

### `last_guild`

- type : `float`

`monotonic` time, when the last guild's data was received.

By default this value is set to the time, when the object was created.

### `last_ready`

- type : `float`

`monotonoic` time, when the last shard launched. Used to calculate minimum 
waiting time.

### `waiter`

- type : `Future`

A `Future`, on which the waiting is executed.

## Methods

### `shard_ready(self,guilds_data)`

- returns : `None`

Whenever a shard launched up (except the first), this method is called to
increase [`.counter`](#counter), by the amount of guilds received, and resets
[`.last_ready`](#last_ready) to the current `monotonic` time.

### `feed(self,guild)`

- returns : `None`

Meanwhile the [client](Client.md) has [`.ready_state`](Client.md#ready_state)
and we receive a guild's data, it will be fed to it. Depending on the options,
how the wrapper was loaded, this method desides, if we should request the users
of the guild later.

This method also descreases [`.counter`](#counter), and if it hits 0, the
[`.waiter`](#waiter) will be awaken at [`.last_ready`](#last_ready) + 1 second.

## Magic Methods

### `__init__(self,client,guild_datas)`

Creates a new `ReadyState`. The started amount of the `ReadyState`'s
[`.counter`](#counter) will be the length of the passed `guild_datas`.
If the [`client`](Client.md) has 1 (/0) shard, then
[`.last_ready`](#last_ready) is set to the current `monotonic` time -1 second,
what causes [`__await__`](#__await__self) to yield instantly, when the last
guild's data is received.

### `__await__(self)`

- returns : `None`

Loops inifinitly meanwhile we receive data from Discord. If we do not get
data from Discord for at least 1 second, then yields.
