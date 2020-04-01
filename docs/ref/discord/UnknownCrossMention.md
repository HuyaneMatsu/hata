# class `UnknownCrossMention`

Represents an unknown channel mentioned by a cross guild mention. These
mentions are stored at [`Message.cross_mentions`](Message.md#cross_mentions).

- Source : [message.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/message.py)

## Instance attributes

### `guild_id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The channel's guild's unique identificator number.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The channel's unique identificator number.

### `name`

- type : `str`

The channel's name.

### `type`

- type : `int`

The channel's type

## Properties

### `clients`

- returns : `list`

Returns an `list`, of the [`Client`](Client.md)'s, who can see the channel
represented by the object. Because non of the clients can see a channel
represented by a `UnknownCrossMention`, this property always returns an empty
list.

### `created_at`

- returns : `datetime`

The creation time of the channel represneted by the `UnknownCrossMention` object.

### `display_name`

- returns : `str`

Returns the display name of the represented channel of the
`UnknownCrossMention`, what depends on it's type.

### `guild`

- returns : `None`

Returns the `UnknownCrossMention`'s guild, what is every time`None`, because
the `UnknownCrossMention` objects represented an unknown partial channel.

### `mention`

- returns : `str`

Returns the channel's mention represented by the `UnknownCrossMention` object.

### `partial`

- returns : `bool`
- values : `False`

`UnknownCrossMention`'s are always partial, because they represent an channel,
what non of the clients can see.

## Magic methods

### `__str__(self)`

- returns : `str`

Returns the `UnknownCrossMention`'s `.name`.

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Returns the `UnknownCrossMention`'s hash value, which equals to it's id.

### `__repr__(self)`

- returns : `str`

Returns the `UnknownCrossMention`'s representation.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two [`UnknownCrossMention`](UnknownCrossMention.md)'s `.id`. or
the [`UnknownCrossMention`](UnknownCrossMention.md) `.id` with a 
[channel](CHANNEL_TYPES.md)'s.

### `__format__(self,code)`

- returns : `str`

```python
f'{unknown_cross_mention}' #-> unknown_cross_mention.__str__()
f'{unknown_cross_mention:d}' #-> unknown_cross_mention.display_name
f'{unknown_cross_mention:m}' #-> unknown_cross_mention.mention
f'{unknown_cross_mention:c}' #-> unknown_cross_mention.created_at with '%Y.%m.%d-%H:%M:%S' format
```

## Internal

### `__new__(cls,data)` (magic method)

- returns : [`UnknownCrossMention`](UnknownCrossMention.md) / [`ChannelBase`](ChannelBase.md) subclasse's instance

Tries to find the channel by its `id`. If it cannot, then creates a
[`UnknownCrossMention`](UnknownCrossMention.md) instance and returns it.
