# class `ChannelGroup`

`ChannelPrivate` represents a group channel. The channel's Discord side
channel type is 3.

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/channel.py)

## Superclasses

- [`ChannelBase`](ChannelBase.md)
- [`ChannelTextBase`](ChannelTextBase.md)

## Instance attributes

### `call`

- type : [`GroupCall`](GroupCall.md) / `NoneType`
- default : `None`

If there is a call at the channel, then this attribute should be set.
This feature is user account only, so it is not tested.

### `icon`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The channel's icon's hash. if the channel has no icon, then the
attribute is set to `0`.

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
lenght by default is same as [`MC_GC_LIMIT`](ChannelTextBase.md#mc_gc_limit) defined at
[`ChannelTextBase`](ChannelTextBase.md). Or it can be
changed locally with the
[`mc_gc_limit`](ChannelTextBase.md#mc_gc_limit-getset) property.

### `name`

- type : `str`
- default : `''` (empty string)

The channel's name. A group channel's name is optinal, so if it is
unset, it will be an empty string.

### `owner`

- type : [`User`](User.md) / [`Client`](Client.md)

The group channel's owner.

### `users`

- type : `list`
- elements : [`User`](User.md) / [`Client`](Client.md)

A list of the channel's recipients.

## Class attributes

##### Inherited class attributes

- [`MC_GC_LIMIT`](ChannelTextBase.md#mc_gc_limit)

### `INTERCHANGE`

- value : `(3,)`

This attribute defines, if the channel's type is interchangeable or not.

### `type`

- type : `int`
- value : `3`

The channel's Discord side type.

## Properties

##### Inherited properties

- [`clients`](ChannelBase.md#clients)
- [`created_at`](ChannelBase.md#created_at)
- [`mc_gc_limit`](ChannelTextBase.md#mc_gc_limit-getset)
- [`mention`](ChannelBase.md#mention)

### `icon_url`

- returns : `str` / `None`
- default : `None`

Returns the group channel's icon's url. If the channel has no icon, then
it returns `None`

### `display_name`

- returns : `str`

Returns the channel's [`.name`](#name) if set. If it is not, then
creates a name joining up the users at the channel. If there are no
users at the channel, returns `'Unnamed'`.

### `guild`

- returns : `None`

For compability with [guild channels](ChannelGuildBase.md).

## Methods

##### Inherited methods

- [`get_user`](ChannelBase.md#get_userselfnamedefaultnone)
- [`get_user_like`](ChannelBase.md#get_user_likeselfnamedefaultnone)
- [`get_users_like`](ChannelBase.md#get_users_likeselfname)

### `permissions_for(self,user)`

- returns : [`Permission`](Permission.md)
- default : `Permission.permission_none`

Returns the permissions for the given [user](User.md) at the channel.

### `cached_permissions_for(self,user)`

- returns : [`Permission`](Permission.md)
- default : `Permission.none`

Same as [`.permissions_for(...)`](#permissions_forselfuser). There is no
reason to cache permissions at a private channel, but for compability
with different [channel types](CHANNEL_TYPES.md) it is necessary.

### `icon_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

If the channel has no icon, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'. Valid sizes: 16, 32, 64, 128, 256,
512, 1024, 2048, 4096.

## Classmethods

### `precreate(cls,channel_id,**kwargs)`

- returns : [`ChannelGroup`](ChannelGroup.md)
- raises : `ValueError` / `TypeError`

Some attributes are processed from kwargs, the rest is set automatically:
- `name`, default is `''`
- `icon`, default : `0`, accepts `None`,
[image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)
and `int`.

## Magic methods

##### Inherited magic methods

- [`__repr__`](ChannelBase.md#__repr__self)
- [`__hash__`](ChannelBase.md#__hash__self)
- [`__format__`](ChannelBase.md#__format__selfcode)
- [`__gt__`](ChannelBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__ge__`](ChannelBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__eq__`](ChannelBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__le__`](ChannelBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__lt__`](ChannelBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)

### `__str__(self)`

- returns : `str`

Returns the channel's [`.display_name`](#display_name).

## Internal

##### Inherited internal

- [`__new__`](ChannelBase.md#__new__clsdataclientnoneguildnone-magic-method)
- [`_mc_find`](ChannelTextBase.md#_mc_findchannelmessage_id-method)
- [`_mc_generator`](ChannelTextBase.md#_mc_generatorchannelafterbeforelimit-method)
- [`_mc_init`](ChannelTextBase.md#_mc_initchannel-method)
- [`_mc_insert_asynced_message`](ChannelTextBase.md#_mc_insert_asynced_messagechannelmessage-method)
- [`_mc_insert_new_message`](ChannelTextBase.md#_mc_insert_new_messagechannelmessage-method)
- [`_mc_insert_old_message`](ChannelTextBase.md#_mc_insert_old_messagechannelmessage-method)
- [`_mc_pop`](ChannelTextBase.md#_mc_popchannelmessage_id-method)
- [`_mc_pop_multiple`](ChannelTextBase.md#_mc_pop_multiplechannelmessage_ids-method)
- [`_mc_process_chunk`](ChannelTextBase.md#_mc_process_chunkchanneldata-method)

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

| name              | description                                                                               |
|-------------------|-------------------------------------------------------------------------------------------|
| icon              | int                                                                                       |
| name              | str                                                                                       |
| owner             | [`User`](User.md) / [`Client`](Client.md)                                                 |
| users             | [listdifference](listdifference.md) return of [`User`](User.md) / [`Client`](Client.md)   |

### `_update_no_return(self,data)` (method)

- returns : `None`

Familar to [`._update`](#_updateselfdata-method), but it does not calculates
the changes.

### `_delete(self,client)` (method)

- returns : `None`

Removes the channel's references.

### `_dispatch(cls,data,client)` (classmethod)

- returns : [`ChannelPrivate`](ChannelPrivate.md) / `None`

Discord sends a channel create event with each group channel's
[message](Message.md). This method decides whenever it is really a new
channel (returns the channel), or it is just an another message (returns
`None`).

### `_from_partial_data(cls,data,channel_id,partial_guild)` (classmethod)

- returns : [`ChannelGroup`](ChannelGroup.md)

Creates a [`ChannelGroup`](ChannelGroup.md) from partial data.
