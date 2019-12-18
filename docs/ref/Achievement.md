# class `Achievement`

Represents a Discord achievement created at
[Developer Portal](https://discordapp.com/developers).

- source : [client.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/client.py)

## Instance attributes

### `application_id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The achievement's [application's](Application.md)
[`.id`](Application.md#instance-attributes).

### `description`

- type : `str`

The description of the achievement.

### `icon`

- type : `int`
- lenght : 128 bit
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The achievement's icon's hash. Achievements always have icon.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The achievement's unique identificator number.

### `name`

- type : `str`

The achievement's name.

### `secret`

- type : `bool`

Secret achievements will *not* be shown to the user until they've unlocked
them.

### `secure`

- type : `bool`

Secure achievements can only be set via HTTP calls from your server, not by a
game client using the SDK.

## Properties

### `icon_url`

- returns : `str`

Returns the achievement's [`.icon`](#icon)'s url.

### `created_at`

- returns : `datetime`

Returns the achievement's creation time.

## Methods

### `icon_url_as(self,ext=None,size=None)`

- returns : `str`
- raises : `valueError`

Returns the achievement's [`.icon`](#icon)'s url with the specific extension
and size.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

## Magic methods

### `__str__(self)`

Returns The achievement's [`.name`](#name).

### `__repr__(self)`

- returns : `str`

Returns the achievement's representation.

### `__format__(self,code)`

- returns : `str`

```python
f'{achievement}' #-> achievement.name
f'{achievement:c}' #-> achievement.created_at with '%Y.%m.%d-%H:%M:%S' format
```

Raises `ValueError` on invalid format code.

## Internal

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the achievement and returns it's changed old attributes in a dictionary
with (attribute name, old value) items.

| name          | description   |
|---------------|---------------|
| description   | str           |
| icon          | int           |
| name          | str           |
| secret        | bool          |
| secure        | bool          |

### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the achievement with the given data.

### `__init__(self,data)` (magic method)

Creates an achievement from data sent by Discord.
