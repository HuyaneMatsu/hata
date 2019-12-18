# class `ChannelPrivate`

`ChannelPrivate` represents a private (direct message) channel. The 
channel's Discord side channel type is 1.

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

### `users`

- type : `list`
- elements : [`User`](User.md) / [`Client`](Client.md)

A list of the channel's recipient.

## Class attributes

##### Inherited class attributes

- [`MC_GC_LIMIT`](ChannelTextBase.md#mc_gc_limit)

### `INTERCHANGE`

- value : `(1,)`

This attribute defines, if the channel's type is interchangeable or not.

### `type`

- type : `int`
- value : `1`

The channel's Discord side type.

## Properties

##### Inherited properties

- [`clients`](ChannelBase.md#clients)
- [`created_at`](ChannelBase.md#created_at)
- [`mc_gc_limit`](ChannelTextBase.md#mc_gc_limit-getset)
- [`mention`](ChannelBase.md#mention)

### `name`

- returns : `str`

Returns the channel's sideless name. The wrapper cannot detect from
which client is this method called, so the wrapper acts, like the
channel's name is acquired from a third person.

### `display_name`

- returns : `str`

Same as [`.name`](#name).

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
Bot permissions are restricted at private channels. If the given user is
not at the channel, then it returns none permissions.

### `cached_permissions_for(self,user)`

- returns : [`Permission`](Permission.md)
- default : `Permission.none`

Same as [`.permissions_for(...)`](#permissions_forselfuser). There is no
reason to cache permissions at a private channel, but for compability
with different [channel types](CHANNEL_TYPES.md) it is necessary.

## Classmethods

### `precreate(cls,channel_id,**kwargs)`

- returns : [`ChannelPrivate`](ChannelPrivate.md)
- raises : `ValueError`

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

Returns the channel's [`.name`](#name).

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

### `_delete(self,client)` (method)

- returns : `None`

Removes the channel's references.

### `_dispatch(cls,data,client)` (classmethod)

- returns : [`ChannelPrivate`](ChannelPrivate.md) / `None`

Discord sends a channel create event with each direct
[message](Message.md). This method decides whenever it is really a new
channel (returns the channel), or it is just an another message (returns
`None`).

### `_from_partial_data(cls,data,channel_id,partial_guild)` (classmethod)

- returns : [`ChannelPrivate`](ChannelPrivate.md)

Creates a [`ChannelPrivate`](ChannelPrivate.md) from partial data.
