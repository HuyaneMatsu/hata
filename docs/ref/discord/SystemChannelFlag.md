# class `SystemChannelFlag`

The flags of a [guild](Guild.md)'s [system channel](Guild.md#system_channel),
stored at [`guild.system_channel_flags`](Guild.md#system_channel_flags).

- Source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/guild.py)

From Discord side, the flags tell, what [type of message](MessageType.md) are
**not** sent to the guild's system channel, but at the wrapper the properties
and methods are reversed -> they tell, what are sent.

## Superclasses

- `int`

## Class attributes

##### Predefined class attribtes

There are 2 flags predefined to tell, what means a full and an empty system
channel flag.

| attribute name    | value     |
|-------------------|-----------|
| NONE              | 0b11      |
| ALL               | 0b00      |

## Properties

### `welcome`

- returns : `int`
- values : `1` / `0`

Returns 1 if [welcome](MessageType.md#predefined-class-attributes)
[messages](Message.md) are sent to the respective [guild](Guild.md)'s
[system channel](Guild.md#system_channel).

### `boost`

- returns : `int`
- values : `1` / `0`

Returns 1 if [boost](MessageType.md#predefined-class-attributes)
[messages](Message.md) are sent to the respective [guild](Guild.md)'s
[system channel](Guild.md#system_channel).

### `all`

- returns : `bool`

Returns `True`, if **all** the system [message types](MessageType.md) are
sent to the respective [guild](Guild.md)'s
[system channel](Guild.md#system_channel).

### `none`

- returns : `bool`

Returns `True`, if **none** of the system [message types](MessageType.md) are
sent to the respective [guild](Guild.md)'s
[system channel](Guild.md#system_channel).


## Magic methods

### `__iter__(self)`

- returns : `generator`
- yields : `str`

At the case of iterating a flag, it yields all of it's attribute's names, what
it has set to True.

### `__repr__(self)`

- returns : `str`

Returns the representation of the system channel flag.
