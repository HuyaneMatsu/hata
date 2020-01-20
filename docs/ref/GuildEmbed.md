# class `GuildEmbed`

Represents a [guild](Guild.md)'s embed.

- source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/guild.py)

## Instance attribtes

### `channel`

- type : [`ChannelText`](ChannelText.md) / `NoneType`
- default : `None`

The channel where the embed will generate the [invite](Invite.md) to.
Can be `None`.

### `enabled`

Whether the guild is embeddable.

### `guild`

- type : [`Guild`](Guild.md)

The guild of the `GuildEmbed`.

## Class methods

### `from_guild(cls,guild)`

- returns : `GuildEmbed`

Creates a `GuildEmbed` instance from a [`Guild`](Guild.md).

## Magic methods

### `__repr__(self)`

- returns : `str`

Returns the representation of the `GuildEmbed`.

## Internal

### `__init__(self,data,guild)` (magic method)

Creates a `GuildEmbed` object from the data sent by Discord and updates the
[guild](Guild.md)'s embed information as well.
