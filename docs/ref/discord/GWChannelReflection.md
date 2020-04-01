# class `GWChannelReflection`

Represents a [guild widget](GuildWidget.md)'s channel. These channels are
always a reflection of a [voice channel](ChannelVoice.md).

- source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/guild.py)

## Instance attributes

### `id`

- returns : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)

The channel's unique identificator number.

### `name`

- returns : `str`

The channel's name.

### `position`

- returns: `int`

The channel's position.

## Magic methods

### `__str__(self)`

- returns : `str`

Retruns the channel's [`.name`](#name).

### `__repr__(self)`

- returns : `str`

Returns the channel's representation.

### `__hash__(self)`

- returns : `int`

Returns the channel's hash, what is equal to it's [`.id`](#id).

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two `GWChannelReflection` by their position and id.

## Internal

### `__init__(self,data)` (magic method)

Creates a [`GWChannelReflection`](GWChannelReflection.md) from channel data
included with a [guild widget](GuildWidget.md).
