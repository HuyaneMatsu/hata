# class `GuildWidget`

Represents a [guild](Guild.md)'s widget.

- source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/guild.py)

## Instance attribtes

### `guild`

- type : [`Guild`](Guild.md)

The guild that owns the widget.

## Properties

### `id`

- returns : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)

The [`GuildWidget`](GuildWidget.md)'s [`.guild`](#guild)'s
[`.id`](Guild.md#id).

### `name`

The [`GuildWidget`](GuildWidget.md)'s [`.guild`](#guild)'s
[`.name`](Guild.md#name).

### `invite_url`

- returns : `str`
- default : `''` (empty string)

The invite url of the guild's widget. Can be empty string, if it has no invite set.

### `presence_count`

- returns : `int`

Estimated amount of the online users at the guild.

### `json_url`

- returns : `str`

Returns the url, with what the widget data of the [guild](Guild.md) can be
requested.

## Cached properties

### `users`

- returns : `list`
- elements : [`GWUserReflection`](GWUserReflection.md)

Returns a `list` of the online users at the widget's [`.guild`](#guild) as
Guild Widget User Reflections.

### `channels`

- returns : `list`
- elements : [`GWChannelReflection`](GWChannelReflection.md)

Returns a `list` of the voice channels of the widget's [`.guild`](#guild) as
Guild Widget Channel Reflections.

## Magic Method

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`GuildWidget`](GuildWidget.md).

## Internal

### `__init__(self,data)` (magic method)

Creates a `GuildWidget` instance from the data sent by Discord.

### `_cache` (instance attribute)

- type : `dict`
- items : (`str`, `Any`)

The cache used by the [cahched properties](#cached-properties).

### `_data` (instance attribute)

- type : `dict`
- items : (`str`, `Any`)

The data sent by Discord and used by the
[cahched properties](#cached-properties).
