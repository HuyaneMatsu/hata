# class `GuildPreview`

A preview object of a public [`Guild`](Guild.md).

- source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/guild.py)

## Instance attributes

### `description`

- type : `str`
- defaut : `None`

Description for the guild.

### `discovery_splash`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The guilds's discovery splash's hash. The guild must have `DISCOVERABLE`
feature to have discovery splash. If the guild has no discovery splash, this
attribute is set to `0`.

### `emojis`

- type : `dict`
- items : (`int`, [`Emoji`](Emoji.md))

All the emojis of the guild with (`emoji_id`, `Emoji`) item pairs.

### `features`

- type : `list`
- values : [`GuildFeature`](GuildFeature.md)

The guild's features, like `INVITE_SPLASH` or `VIP_REGIONS`

### `has_animated_icon`

- type : `bool`
- values : `True` / `False`

### `icon`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The guilds's icon's hash. If the guild has no icon, then the attribute
is set to `0`.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The guild's unique identificator number.

### `name`

- type : `str`

The name of the guild. It's lenght can be between 2 and 100.

### `online_count`

- type : `int`

The approximate amount of online users at the guild.

### `owner`

- type : [`User`](User.md) / [`Client`](Client.md)

The owner of the guild.

### `splash`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The guilds's splash's hash. if the guild has no splash, then the attribute is
set to `0`. The guild must have `INVITE_SPLASH` feature.

### `user_count`

- type : `int`

The approximate amount of users at the guild.

## Properties

### `created_at`

- returns : `datetime`

Returns the guild's creation time.

### `discovery_splash_url`

- returns : `str` / `None`
- default : `None`

Returns the guild's discovery splash's url. If the guild has no discovery
splash, then returns `None`.

### `icon_url`

- returns : `str` / `None`
- default : `None`

Returns the guild's icon's url. If the guild has no icon, then it
returns `None`.

### `splash_url`

- returns : `str` / `None`
- default : `None`

Returns the guild's splash's url. If the guild has no splash, then returns
`None`.

## Methods

### `icon_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `valueError`

If the guild has no icon, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'. If the guild has
animated avatar it can be 'gif' too. Valid sizes: 16, 32, 64, 128, 256,
512, 1024, 2048, 4096.

### `splash_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `valueError`

If the guild has no splash, then returns `None`

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

### `discovery_splash_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

If the guild has no discovery splash, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Returns the guild's hash value, which equals to it's id.

### `__str__(self)`

- returns : `str`

Returns the guild's name.

### `__repr__(self)`

- returns : `str`

Returns the representation of the guild.

### `__format__(self,code)`

- returns : `str`

```python
f'{guild_preview}' #-> guild_preview.name
f'{guild_preview:c}' #-> guild_preview.created_at with '%Y.%m.%d-%H:%M:%S' format
```

Raises `ValueError` on invalid format code.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two guild preview's id.

## Internal

### `__init__(self,data)` (magic method)

Creates a [`GuildPreview`](GuildPreview.md) object from the data received
from Discord.
