# class `MessageReference`

A cross guild reference used as a [`message`](Message.md)'s
[`.cross_reference`](Message.md#cross_reference) at crosspost messages.

- Source : [message.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/message.py)

## Properties

### `channel_id`

- returns : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
- default : `0`

Returns the referred message's channel's id. If no `channel_id` was received
from Discord, returns `0`.

### `guild_id`

- returns : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
- default : `0`

Returns the referred message's guild's id. If no `guild_id` was received from
Discord, then returns `0`.

### `message_id`

- returns : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
- default : `0`

Returns the referred message's id. If no `message_id` was received from
Discord, then returns `0`.

## Cached properties

### `channel`

- returns : `None` / [`ChannelText`](ChannelText.md)
- default : `None`

Tries to find the referred message's channel and return it. If fails on any
step, then returns `None`.

### `guild`

- returns : `None` / [`Guild`](Guild.md)
- default : `None`

Tries to find the referred message's guild and return it. If fails on any
step, then returns `None`.

### `message`

- returns : `None` / [`Message`](Message.md)
- default : `None`

Tries to find the referred message and return it. If fails on any step, then
returns `None`.

## Magic methods

## `__repr__(self)`

- returns : `str`

Returns the representation of the object.

## Internal

###`__init__(self,data)` (magic method)

Creates a [`MessageReference`](MessageReference.md) instance from the data sent
by Discord.

### `_cache` (instance attribute)

- type : `dict`
- items : (`str` / `Any`)

A dictionary used to store the cached data.
