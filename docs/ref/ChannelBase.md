# class `ChannelBase`

The superclass of all channel types.

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/channel.py)

Check [`CHANNEL_TYPES`](CHANNEL_TYPES.md) for more channel type related info.

## Subclasses:

- [`ChannelGuildBase`](ChannelGuildBase.md)
- [`ChannelPrivate`](ChannelPrivate.md)
- [`ChannelGroup`](ChannelGroup.md)

## Class attributes

### `INTERCHANGE`

- value : `(0,)`

Placeholder for subclasses. This attribute defines, if the channel's type is
interchangeable or not.

## Properties

### `mention`

- returns : `str`

Returns the channel's mention.

### `created_at`

- returns : `datetime`

The creation time of the channel.

### `partial`

- returns : `bool`
- values : `True` / `False`

If a channel has no clients, it is partial.

### `clients`

- returns : `list`
- elements : [`Client`](Client.md)

Returns all the clients, who can see this channel.
[`guild channels`](ChannelGuildBase.md) overwrite this method, because
those get the clients from their [guild](Guild.md) instead.

## Methods

### `get_user(self,name,default=None)`

- returns : `default` / [`User`](User.md) / [`Client`](Client.md)

Tries to find a user from the channel's users.

The search order is the following:

- `full_name`
- `name`

If the method cannot find the user, then returns the `default` value.

[`Guild channels`](ChannelGuildBase.md) overwrite this method, to check
nicks too.

### `get_user_like(self,name,default=None)`

- returns : `default` / [`User`](User.md) / [`Client`](Client.md)

Tries to find a user from the channel's users, who's name starts like the
passed one. Returns on first match. If the method cannot find the user, then
returns the `default` value.

[`Guild channels`](ChannelGuildBase.md) overwrite this method, to check
nicks too.

### `get_users_like(self,name)`

- returns : `list`
- values : [`User`](User.md) / [`Client`](Client.md)

Tries to find all the user of the channel's users, who's name starts like the
passed one. Returns a `list` of all the matched users.

[`Guild channels`](ChannelGuildBase.md) overwrite this method, to check
nicks too.

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Returns the channel's hash value, which equals to it's id.

### `__repr__(self)`

- returns : `str`

Returns the representation of the channel.

### `__format__(self,code)`

- returns : `str`

```python
f'{channel}' #-> channel.__str__()
f'{channel:d}' #-> channel.display_name
f'{channel:m}' #-> channel.mention
f'{channel:c}' #-> channel.created_at with '%Y.%m.%d-%H:%M:%S' format
```

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two channel by their id.
[`guild channels`](ChannelGuildBase.md) overwrite these to check actual
position and `ORDER_GROUP` too.

## Internal

### `__new__(cls,data,client=None,guild=None)` (magic method)

- returns : [`Channel`](CHANNEL_TYPES.md)

Tries to find the channel first from the existing ones. If that fails creates
a new object. if it created a new channel or the found channel is partial
updates it by replacing it's old attributes.
If the created channel is a private channel, then it link it with the client's
private channels.
