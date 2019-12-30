# class `MessageApplication`

Might be sent with a [message](Message.md), if it has Rich Presence-related
chat embeds.

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/webhook.py)

## Instance attributes

### `cover`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The message application's cover's image's hash. If the message application has
no cover, then this attribute is set as `0`.

### `description`

- type : `str`

The description of the message applciation.

### `icon`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The message application's icon's image's hash. If the message application has
no icon, then this attribute is set as `0`.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The message application's unique identificator number.

### `name`

- type : `str`

The message application's name.

## Properties

### `created_at`

- returns : `datetime`

The creation time of the message application.

### `cover_url`

- returns : `str` / `None`
- default : `None`

The message application's cover's url. If the message application has no cover,
then returns `None`.

### `icon_url`

- returns : `str` / `None`
- default : `None`

The message application's icon's url. If the message application has no icon,
then returns `None`.

## Methods

### `cover_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

Returns the message application's cover's url.
If the message application has no cover, then returns `None`

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

### `icon_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

Returns the message application's icon's url.
If the message application has no icon, then returns `None`

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

## Magic Methods

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two message application's id.

### `__hash__(self)`

- returns : `int`
- size : 64 bit

A message application's hash value is equals to it's id.

### `__repr__(self)`

- returns : `str`

Returns the representation of the message application.

## Internal

### `__init__(self,data)` (magic method)

Creates a new [`MessageApplication`](MessageApplication.md) from the data
sent by Discord.
