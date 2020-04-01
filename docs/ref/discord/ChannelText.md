# class `ChannelText`

`ChannelText` represents a [guild](Guild.md) text channel or a guild
news (announcements) channel. The types of the channel can be
interchangeable between the two. The channel's Discord side channel type
is 0 (text) or 5 (news).

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/channel.py)

## Superclasses

- [`ChannelGuildBase`](ChannelGuildBase.md)
- [`ChannelTextBase`](ChannelTextBase.md)

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

### `message_history_reached_end`

- type : `bool`
- values : `True` / `False`
- default : `False`

Tells if all the [messages](Message.md) are loaded at the channel. If they are 
`message_history_reached_end` is set to `True` and no more requests will be
executed on requesting older [messages](Message.md).

### `messages`

- type : [`deque`](https://docs.python.org/3/library/collections.html#collections.deque)
- elements : [`Message`](Message.md)

A `deque` of the messages stored from the channel. The deque's maximal
lenght by default is same as [`MC_GC_LIMIT`](ChannelTextBase.md#mc_gc_limit)
defined at [`ChannelTextBase`](ChannelTextBase.md). Or it can be
changed locally with the
[`mc_gc_limit`](ChannelTextBase.md#mc_gc_limit-getset) property.

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
 
### `slowmode`

- type : `int`
- default : `0`

The amount of time in seconds what a user needs to wait between it's each
message. Bots are unaffected and users with `manage_messages` or
`manage_channel` [permissions](Permission.md).

### `topic`

- type : `str`
- default : `''` (empty string)

The channel's topic.

### `type`

- type : `int`
- values : `0` / `5`

[`ChannelText`](ChannelText.md) is a special case, because it's type is
interchangeable, so it has `type` as an instance attribute and not as a
class attribute.

## Class attributes

##### Inherited class attributes

- [`MC_GC_LIMIT`](ChannelTextBase.md#mc_gc_limit)

### `INTERCHANGE`

- value : `(0,5)`

This attribute defines, if the channel's type is interchangeable or not.

### `ORDER_GROUP`

- type : `int`
- value `0`

A helper attribute at sorting
[guild channels](ChannelGuildBase.md).

## Properties

##### Inherited properties

- [`clients`](ChannelGuildBase.md#clients)
- [`created_at`](ChannelBase.md#created_at)
- [`mc_gc_limit`](ChannelTextBase.md#mc_gc_limit-getset)
- [`mention`](ChannelBase.md#mention)
- [`users`](ChannelGuildBase.md#users)

### `display_name`

- returns : `str`

Guild text and news (announcement) channels are displayed with lower 
case, but they are not necessarily stored like that.

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
Users at text channels do not have voice related permissions.
                     
## Classmethods

### `precreate(cls,channel_id,**kwargs)`

- returns : [`ChannelText`](ChannelStore.md)
- raises : `ValueError`

Some attributes are processed from kwargs, the rest is set automatically:
- `name`, default is `''`
- `nsfw`, default is `False`
- `topic`, default is `''`
- `slowmode`, default is `0`
- `topic`, default is `0`

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
- [`_mc_find`](ChannelTextBase.md#_mc_findchannelmessage_id-method)
- [`_mc_generator`](ChannelTextBase.md#_mc_generatorchannelafterbeforelimit-method)
- [`_mc_init`](ChannelTextBase.md#_mc_initchannel-method)
- [`_mc_insert_asynced_message`](ChannelTextBase.md#_mc_insert_asynced_messagechannelmessage-method)
- [`_mc_insert_new_message`](ChannelTextBase.md#_mc_insert_new_messagechannelmessage-method)
- [`_mc_insert_old_message`](ChannelTextBase.md#_mc_insert_old_messagechannelmessage-method)
- [`_mc_pop`](ChannelTextBase.md#_mc_popchannelmessage_id-method)
- [`_mc_pop_multiple`](ChannelTextBase.md#_mc_pop_multiplechannelmessage_ids-method)
- [`_mc_process_chunk`](ChannelTextBase.md#_mc_process_chunkchanneldata-method)
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

### `_mc_gc_limit` (instance attribute)

- type : `int`

Stores the value used by the
[`mc_gc_limit`](ChannelTextBase.md#mc_gc_limit-getset) property.

### `_turn_gc_on_at` (instance attribute)

- type : `float`
- default : `0.0`

If the channel's message limit is passed by loading older messages, then
this attribute stores when we should change back the channel's
[`.messages`](#messages) to limited. This operation is executed only 
each 1200 seconds tho.

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
| slowmode          | int                                                       |
| topic             | str                                                       |
| type              | int                                                       |

### `_update_no_return(self,data)` (method)

- returns : `None`

Familar to [`._update`](#_updateselfdata-method), but it does not calculates
the changes.

### `_delete(self,client)` (method)

- returns : `None`

Removes the channel's references and changes it's [`.guild`](#guild) to `None`.

### `_from_partial_data(cls,data,channel_id,partial_guild)` (classmethod)

- returns : [`ChannelText`](ChannelText.md)

Creates a [`ChannelText`](ChannelText.md) from partial data.

