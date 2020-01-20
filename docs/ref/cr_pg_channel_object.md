# def `cr_pg_channel_object`

Creates a json serializable object representing a
[guild channel](ChannelGuildBase.md).

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/channel.py)

## `cr_pg_channel_object(name, type_, ...)` (function)

- returns : `dict`
- items : (`str`, `Any`)
- raises : `ValueError`

##### `name`

- type : `str`

The name of the [guild channel](ChannelGuildBase.md). Can be between 2 and 100
characters.

##### `type`

- type : `int` / [`ChannelBase`](ChannelBase.md) subclass.

The type of the channel. Accepts channel type as `int` or as the channel's type
itself.

### Optional keyword arguments

##### `overwrites`

- type : `list`
- elements : [`cr_p_overwrite_object`](cr_p_overwrite_object.md) returns
- default : `None`

The overwrites of the channel.

##### `topic`

- type : `str`
- default : `None`

The topic of the channel. Can be between length 0 and 1024.

> Bound to any Guild Text channel type.

##### `nsfw`

- type : `bool`
- default : `False`

Whether the channel is nsfw.

> Bound to any Guild Text or to any Guild Store channel type.

##### `slowmode`

- type : `int`
- default : `0`

The amount of seconds a user has to wait before sending an another message.
Can be between 0 and 21600 (seconds).

> Bound to Guild Text channel type only.

##### `bitrate`

- type : `int`
- default : `64000`

The bitrate of the voice channel. Can be between 8000 and 96000. For guilds
with `vip` [feature](GuildFeature.md) can be up to 128000, or for guilds with
premium tier it can be 128000, 125000, 384000 depeneding on it. With changing
the [`bitrate_limit`](#bitrate_limit) argument, the check limit can be
modified.

> Bound to any Guild Voice channel type.

##### `user_limit`

- type : `int`
- default : `0`

The limit, how much users can be connected to the voice channel at the same
time. Can be `0` for unlimited, or between 1 and 99 for the exact amount.

> Bound to any Guild Voice channel type.

##### `bitrate_limit`

- type : `int`
- default : `96000`

The bitrate limit used, when validating the passed [`bitrate`](#bitrate)'s
value.
