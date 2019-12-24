# class `User`

A `User` object represents a user in Discord, including [guild](Guild.md) members.

- Source : [user.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/user.py)

## Familiar types

- [Webhook](Webhook.md)
- [Client](Client.md)
- [UserOA2](UserOA2.md)
- [WebhookRepr](WebhookRepr.md)
- [GWUserReflection](GWUserReflection.md)

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

- [`guild_profiles`](UserBase.md#guild_profiles)
- [`is_bot`](UserBase.md#is_bot)
- [`partial`](UserBase.md#partial)

##### Overwritten properties to instance attributes if presence is not cached

- [`activities`](UserBase.md#activities)
- [`status`](UserBase.md#status)
- [`statuses`](UserBase.md#statuses)

## Properties

##### Inherited Properties

- [`activity`](UserBase.md#activity)
- [`avatar_url`](UserBase.md#avatar_url)
- [`created_at`](UserBase.md#created_at)
- [`default_avatar`](UserBase.md#default_avatar)
- [`default_avatar_url`](UserBase.md#default_avatar_url)
- [`full_name`](UserBase.md#full_name)
- [`mention`](UserBase.md#mention)
- [`mention_nick`](UserBase.md#mention_nick)

## Classmethods

### `precreate(cls,user_id,**kwargs)`

- returns : [`User`](User.md)
- raises : `AttributeError` / `TypeError`

Tries to query the given user from the existing ones. If it fails, it creates a
user with the given kwargs and with the given ID. Precreated users are created
as partial, so when the user will get loaded first time, it will have it's
attributes replaced.

Some attributes are set automatically or processed from kwargs:
- [`name`](#inherited-properties) : default is `''`.
- [`discriminator`](#inherited-properties) : default is `0`, can be set as `str` and
`int`.
- [`avatar`](#Inherited Properties) : default is `0`, accepts `None`,
[image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)
and `int`.
- [`has_animated_avatar`](#inherited-properties), default is `False`.

## Methods

##### Inherited methods

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

### `__new__(cls,data,guild=None)` (magic method)

- returns : [`User`](User.md) / [`Client`](Client.md)

The method first tries to find the user by id. If it fails creates a new User object.
If guild is set and the data contains member data too, then it creates guild profile too.

### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the user with the given user data.

### `_create_and_update(cls,data,guild=None)` (classmethod)

- returns : [`User`](User.md)

Creates a user with the given data. If the user already exsists updates it.

### `_update_presence(self,data)` (method)

- returns : `dict`
- items : (`str` : `Any`)

Used at dispatch events if a user's presence (status and activity) might be
updated. Returns a `dict` with the following optional elements:

- `statuses` : a `dict` with (`str`, `str`) items. Contains the user's status
by platform.
- `status` : type [`Status`](Status.md). Mentioned only if the users top status
changed.
- `activities` : a `list` which contains the old activities of the user. If an
acitivty is updated, then it returns a `dict` instead of that activity, which
contains for sure an `activity` key, to show which activity got update.

### `_update_presence_no_return(self,data)` (method)

- returns :`None`

Updates the user's presences and returns `None`.

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the user with the data and returns it's changed attributes with
(attribute name, old value) items.

### `_update_profile(cls,data,guild)` (classmethod)

- returns : [`User`](User.md) / [`Client`](Client.md), `dict`

First tries to find the user, if it cant creates it and adds it to the
[`guild`](Guild.md). If the user was found, tries to update it's
[`guild profile`](GuildProfile.md) if it has. If not, it creates it. At any
point, when the method cant find the user or the profile, it fills up the
missing data and returns.

### `_update_profile_no_return(cls,data,guild)` (classmethod)

- returns : `None`

Familiar to [`.update_profile`], but it does not checks changes and returns
`None`.

### `_from_GWU_data(cls,data)` (classmethod)

- returns : [`User`](User.md) / [`Client`](Client.md)

Tries to get the user. If fails, creates a new one from the given
[guild widget](GuildWidget.md) user data.

### `_bypass_no_cache(data,guild)` staticmethod

- returns : `None`

Only available when user or presence caching is disabled. Called to set a
[`Client`](Client.md)'s [`GuildProfile`](GuildProfile.md).

