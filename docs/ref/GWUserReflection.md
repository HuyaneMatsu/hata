# class `GWUserReflection`

Represents a user object sent with [guild widget](GuildWidget.md) data.

- Source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/guild.py)

## Familiar types

- [Webhook](Webhook.md)
- [User](User.md)
- [Client](Client.md)
- [UserOA2](UserOA2.md)
- [WebhookRepr](WebhookRepr.md)

## Superclasses

- [`UserBase`](UserBase.md)

## Instance attributes

##### Inherited instance attributes

- [`id`](UserBase.md#id)
- [`name`](UserBase.md#name)
- [`discriminator`](UserBase.md#discriminator)
- [`avatar`](UserBase.md#avatar)
- [`has_animated_avatar`](UserBase.md#has_animated_avatar)

##### Overwritten properties to instance attributes

- [`is_bot`](UserBase.md#is_bot)
- [`status`](UserBase.md#status)

### `activity_name`

- type : `str` / `Nonetype`
- default : `None`

The user's top activity's name.

### `nick`

- type : `str`

The nick of the user at it's [guild](GuildWidget.md).

## Properties

##### Inherited properties

- [`activity`](UserBase.md#activity)
- [`avatar_url`](UserBase.md#avatar_url)
- [`created_at`](UserBase.md#created_at)
- [`default_avatar`](UserBase.md#default_avatar)
- [`default_avatar_url`](UserBase.md#default_avatar_url)
- [`full_name`](UserBase.md#full_name)
- [`mention`](UserBase.md#mention)
- [`platform`](UserBase.md#platform)
- [`activities`](UserBase.md#activities)
- [`guild_profiles`](UserBase.md#guild_profiles)
- [`status`](UserBase.md#status)
- [`statuses`](UserBase.md#statuses)

### `partial`

- returns : `bool`
- values : `False`

[`GWUserReflection`](GWUserReflection.md)-s are always full users.

## Methods

- [`avatar_url_as`](UserBase.md#avatar_url_asselfextnonesizenone)
- [`name_at`](UserBase.md#name_atselfguild)
- [`color`](UserBase.md#colorselfguild)
- [`mentioned_in`](UserBase.md#mentioned_inselfmessage)

## Magic methods

#### Inherited magic methods

- [`__str__`](UserBase.md#__str__self)
- [`__repr__`](UserBase.md#__repr__self)
- [`__hash__`](UserBase.md#__hash__self)
- [`__format__`](UserBase.md#__format__selfcode)
- [`__gt__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__ge__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__eq__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__le__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__lt__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)

## Internal

### `__init__(self,data)` (magic method)

Creates a [`GWUserReflection`](GWUserReflection.md) from user data included
with a [guild widget](GuildWidget.md).
