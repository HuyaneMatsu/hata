# class `ChannelGuildBase`

The superclass of all guild channels.

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/channel.py)

Check [`CHANNEL_TYPES`](CHANNEL_TYPES.md) for more channel type related info.

## Superclasses

- [`ChannelBase`](ChannelBase.md)

## Subclasses

- [`ChannelText`](ChannelText.md)
- [`ChannelVoice`](ChannelVoice.md)
- [`ChannelCategory`](ChannelCategory.md)
- [`ChannelStore`](ChannelStore.md)

## Class attributes

##### Inherited class attributes

- [`INTERCHANGE`](ChannelBase.md#interchange)

## Properties

### `users`

- returns : `list`
- elements : [`User`](User.md) / [`Client`](Client.md)

Returns a list of the users, who have permissions to see the channel.
                       
### `clients`

- returns : `list`
- elements : [`Client`](Client.md)

Returns the channel's [`guild's`](Guild.md) clients if applicable.

## Methods

### `cached_permissions_for(self,user)`

- returns : [`Permission`](Permission.md)

Returns the permissions for the user if cached. If not generates and stores it.
                       
### `get_user(self,name,default=None)`

- returns : [`User`](User.md) / [`Client`](Client.md)

Tries to find a user from the channel's users.

The search order is the following:

- `full_name`
- `name`
- `nick`

If the method cannot find the user, then returns the `default` value.

### `get_user_like(self,name,default=None)`

- returns : `default` / [`User`](User.md) / [`Client`](Client.md)

Tries to find a user from the channel's users, who's name or nick starts like
the passed one. Returns on first match. If the method cannot find the user,
then returns the `default` value.

### `get_users_like(self,name)`

- returns : `list`
- values : [`User`](User.md) / [`Client`](Client.md)

Tries to find all the user of the channel's users, who's name or nick starts
like the passed one. Returns a `list` of all the matched users.

### `permissions_for(self,user)`

- returns : [`Permission`](Permission.md)
- default : `Permission.permission_none`

Returns the permissions at the channel for the given [user](User.md).

## Magic methods

### `__str__(self)`

- returns : `str`

Returns the channel's `.name`.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

If the other channel is instance of
[`ChannelGuildBase`](ChannelGuildBase.md), then these methods
compare the two channel's `ORDER_GROUP` first, which is a class attribute
implemented by every guild channel type. Second it compares the two channel's
`position`, what is an instance attribute of each guild channel type, and as
last it compares the two channel's `id`.

If the other channel is not instance of
[`ChannelGuildBase`](ChannelGuildBase.md), then it just simply
compare the two object's `id` if applicable.

## Internal

### `_init_catpos(self,data,guild)` (method)

- returns : `None`

Inicializes the `category` and the `position` of the channel. If a channel is
under the [`guild`](Guild.md), and not in a category (category channels are all
like these), then their `category` is the [`guild`](Guild.md) itself. This
method is used when we inicialize a guild channel.

### `_set_catpos(self,data)` (method)

- returns : `None`

Similar to the [`._init_catpos`](#_init_catposselfdataguild-method) method,
but this method applies the changes too, so moves the channel between
categories and moves the channel inside of the catgeory too, to keep the
order. We use this method when we call `_update_no_return` of a guild channel.

### `_update_catpos(self,data,old)` (method)

- returns : `None`

Acts same as [`._set_catpos`](#_set_catposselfdata-method), but it sets the
modified attrbiutes' previous value to `old`. The method is called when the
`_update` method is called of a guild channel.

### `_parse_overwrites(self,data)` (method)

- returns : `list`
- elements : [`PermOW`](PermOW.md)

Parses the permission overwrites of the given data and returns them. We do not
set any attributes of the channel here.

### `_permissions_for(self,user)` (method)

- returns : `int`
- default : `Permission.none`

Calculates the permissions of the `user` at the channel's [`guild`](Guild.md),
then applies the channel specific overwrites to it. If the user is a 
[`webhook`](Webhook.md) of the channel, then applies only the default role's
permissions and it's overwrites and returns it. If the user is not a meber
of the guild, returns no permissions.


