# class `Invite`

Represents a Discord `Invite`

- Source : [invite.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/invite.py)

## Instance Attributes

### `channel`

- type : [`ChannelText`](ChannelText.md) / [`ChannelVoice`](ChannelVoice.md) / [`ChannelStore`](ChannelStore.md) / [`ChannelGroup`](ChannelGroup.md) / `NoneType`
- default : `None`

The channel where the invite redirects. If it is News (Announcements) or
[store channel](ChannelStore.md), then the invite is a lurk invite.
If channel data was not sent with the invite's, then this attribute will be
set as `None`.

> Invites can be created from [group channels](ChannelGroup.md), but thats
not supported for bots. (Neither for the wrapper yet).

### `code`

- type : `str`

The invite's unique id.

### `created_at`

- type : `datetime` / `NoneType`
- default : `None`

When the invite was created.

### `guild`

- type : [`Guild`](Guild.md) / `NoneType`
- default : `None`

The guild this invite is for.
If guild data was not sent with the invite's, then this attribute will be
set as `None`.

### `inviter`

- type : [`User`](User.md) / [`Client`](Client.md)
- default : [`ZEROUSER`](ZEROUSER.md)

The creator if the invite.
If this field is not sent with the invite's data, then it is set to `ZEROUSER`.

### `max_age`

- type : `int` / `NoneType`
- default : `None`

The time in seconds after the invite will expire. If the data is not sent by
Discord, it will set to `None`

> If the invite was created with max age 0, then this value will be negative
instead of the expected 0.

### `max_uses`

- type : `int` / `NoneType`
- default : `None`

The amount how much times the invite can be used totally. If this is not
included within the data by Discord, it will be set to `None`.

> If the invite has no use limit, then this value is 0.

### `online_count`

- type : `int`
- default : `0`

The amount of online users at the invite's [`.guild`](#guild). If not included,
then it is set to `0`.

### `target_type`

- type : [`InviteTargetType`](InviteTargetType.md)
- default : `InviteTargetType.NONE`

The type of the target user of the invite.

### `target_user`

- type : [`User`](User.md) / [`Client`](Client.md)
- default : [`ZEROUSER`](ZEROUSER.md)

The target user of this invite.

### `temporary`

- type : `bool`
- default : `False`

Whether this invite only grants temporary membership.
(I.e. they get kicked after they disconnect).
            
> Copied docs from Discord, actually ???.

### `user_count`

- type : `int`
- default : `0`

The amount of users at the invite's [`.guild`](#guild). If not included,
then it is set to `0`.

### `uses`

- type : `int` / `NoneType`
- default : `None`

The amount how much times the invite was used.

## Properties

### `partial`

- returns : `bool`

Returns if the invite is partial. The invite is partial if it's
[.`inviter`](#inviter) is set to [`ZEROUSER`](ZEROUSER.md).

### `url`

- returns : `str`

Returns the invite's url.

## Magic methods

### `__str__(self)`

- returns : `str`

Returns the invite's [`.code`](#code).

### `__repr__(self)`

- returns : `str`

Returns the invite's representation.

### `__hash__(self)`

- returns : `int`

Returns the invite's [`.code`](#code)'s hash.

## Internal

### `__init__(self,data)` (magic method)

Creates an [`Invite`](Invite.md) with the given data.

### `_create_vanity(cls,guild,data)` (classmethod)

- returns : [`Invite`](Invite.md)

Used to create a vanity invite of the [guild](Guild.md) with the requested
data, what should contain a partial channel object as well.

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the invite and returns it's old attributes as (attribute name, old value)
pairs. Sadly only two attributes of the invite can be updated:
[`.online_count`](#online_count) and [`.user_count`](#user_count).

| name          | description    |
|---------------|----------------|
| online_count  | int            |
| user_count   | int            |

### `_update_no_return(self,data)` (method)

- returns : `None`

Familiar to [`._update`](#_updateselfdata-method), but instead of calculating
the differences and returning them, it just overwrites them.

