# class `ChannelStore`

`ChannelStore` represents a [guild](Guild.md) store channel. The
channel's Discord side channel type is 6.

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/channel.py)

## Superclasses

- [`ChannelGuildBase`](ChannelGuildBase.md)

## Instance attributes

### `category`

- type : [`ChannelCategory`](ChannelCategory.md) / [`Guild`](Guild.md)

The category of the channel. If the channel is not in any category, then
it is directly under the guild. At that case it's guild is it's
category.

### `guild`

- type : [`Guild`](Guild.md) / `NoneType`

The channel's guild. If the channel is deleted, then it's guild is modifed
to `None`.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The channel's unique identificator number.

### `name`

- type : `str`

The channel's name.

### `nsfw`

- type : `bool`
- values : ` True` / `False`
- default : `False`

Tells if the channel is marked as `nsfw` or not.

### `overwrites`

- type : `list`
- elements : [`PermOW`](PermOW.md)

A list of [permission overwrites](PermOW.md), which are modifying specific
[roles'](Role.md) or directly the [users'](User.md) permissions at the channel.

### `position`

- type : `int`

The channel's position at it's [cagegory](#category).
 
It is not the channel's real position, because channel ordering is a pretty
complicated topic and to make it worse, most of the Discord clients just
derp out when changing the channel order.

## Class attributes

### `INTERCHANGE`

- value : `(6,)`

This attribute defines, if the channel's type is interchangeable or not.

### `type`

- type : `int`
- value : `6`

The channel's Discord side type.

### `ORDER_GROUP`

- type : `int`
- value `0`

A helper attribute at sorting
[guild channels](ChannelGuildBase.md).

## Properties

##### Inherited properties

- [`clients`](ChannelGuildBase.md#clients)
- [`created_at`](ChannelBase.md#created_at)
- [`mention`](ChannelBase.md#mention)
- [`users`](ChannelGuildBase.md#users)

### `display_name`

- returns : `str`

Guild store channels are displayed with lower case, but they are not
necessarily stored like that.

Because different kind of channels are displayed on different ways, each
[channel type](CHANNEL_TYPES.md) defines it's own `display_name` method.

## Methods

##### Inherited methods

- [`cached_permissions_for`](ChannelGuildBase.md#cached_permissions_forselfuser)
- [`get_user`](ChannelGuildBase.md#get_userselfnamedefaultnone)
- [`get_user_like`](ChannelGuildBase.md#get_user_likeselfnamedefaultnone)
- [`get_users_like`](ChannelGuildBase.md#get_users_likeselfname)

### `permissions_for(self,user)`

- returns : [`Permission`](Permission.md)
- default : `Permission.permission_none`

Returns the permissions at the channel for the given [user](User.md).
Users at store channels do not have neither text and voice related permissions.

## Classmethods

### `precreate(cls, channel_id, **kwargs)`

- returns : [`ChannelStore`](ChannelStore.md)
- raises : `ValueError`

Some attributes are processed from kwargs, the rest is set automatically:

| name      | default   | type              | alternatives              |
|-----------|-----------|-------------------|---------------------------|
| name      | ''        | str (2-100 char)  | str instances             |
| nsfw      | False     | bool              | int instance as 0 or 1    |

## Magic methods

##### Inherited magic methods

- [`__str__`](ChannelGuildBase.md#__str__self)
- [`__repr__`](ChannelBase.md#__repr__self)
- [`__hash__`](ChannelBase.md#__hash__self)
- [`__format__`](ChannelBase.md#__format__selfcode)
- [`__gt__`](ChannelGuildBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__ge__`](ChannelGuildBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__eq__`](ChannelGuildBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__le__`](ChannelGuildBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__lt__`](ChannelGuildBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)

## Internal

##### Inherited internal

- [`__new__`](ChannelBase.md#__new__clsdataclientnoneguildnone-magic-method)
- [`_init_catpos`](ChannelGuildBase.md#_init_catposselfdataguild-method)
- [`_parse_overwrites`](ChannelGuildBase.md#_parse_overwritesselfdata-method)
- [`_permissions_for`](ChannelGuildBase.md#_permissions_forselfuser-method)
- [`_set_catpos`](ChannelGuildBase.md#_set_catposselfdata-method)
- [`_update_catpos`](ChannelGuildBase.md#_update_catposselfdataold-method)

### `_cache_perm` (instance attribute)

- type : `dict`
- items : (`int`, [`Permission`](Permission.md))

Cached permissions stored by the
[`cached_permissions_for`](ChannelGuildBase.md#cached_permissions_forselfuser)
method. When the channel is updated, then the cached permissions of it are
cleared.

### `_finish_init(self,data,client,parent)` (method)

- returns : `None`

Called by `.__new__` if the channel was not found. This method fills up 
the type bound attributes of the channel and also calls the other inherited
initializers.

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the channel and returns it's old attributes as (attribute name,
old value).

| name              | description                                               |
|-------------------|-----------------------------------------------------------|
| category          | [ChannelCategory](ChannelCategory.md) / [Guild](Guild.md) |
| name              | str                                                       |
| nsfw              | bool                                                      |
| overwrites        | list of [PermOW](PermOW.md)                               |
| position          | int                                                       |

### `_update_no_return(self,data)` (method)

- returns : `None`

Familar to [`._update`](#_updateselfdata-method), but it does not calculates
the changes.

### `_from_partial_data(cls,data,channel_id,partial_guild)` (classmethod)

- returns : [`ChannelStore`](ChannelStore.md)

Creates a [`ChannelStore`](ChannelStore.md) from partial data.
