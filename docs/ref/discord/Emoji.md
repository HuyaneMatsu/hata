# class `Emoji`

`Emoji` represents a Discord emoji. It can custom or builtin (unicode) emoji
too. Builtin emojis are loaded when the module is imported and they are stores
at `BUILTIN_EMOJIS` dictionary. At `BUILTIN_EMOJIS` the keys are the emoji's
name, so it is easy to access any Discord unicode emojis like that.

Custom emojis are loaded with [guilds](Guild.md) on startup. But new partial
custom emojis can be created if someone reacts, if [message](Message.md)'s
reactions are loaded, or by [`parse_emoji`](parse_emoji.md) function.

Every emoji is stored in `EMOJIS` `WeakValueDictionary`. Thats how we have
only one created instance from each emoji.

- source : [emoji.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/emoji.py)

## Instance attributes

### `animated`

- type : `bool`
- values : `True` / `False`

Only custom emojis can be animated.

### `available`

- type : `bool`
- values : `True` / `False`
- default : `True`

Whenever the emoji is available or not.

### `guild`

- type : [`Guild`](Guild.md) / `NoneType`
- default : `None`

The custom emoji's [guild](Guild.md). If the emoji is partial, then this attrbiute
is set to `None`.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)

The custom emoji's unique identificator number. Not like at the cases of normal
types this `id` is not every time a valid Discord emoji id, because the
unicode emojis get an id too. Unicode emoji ids are maximum 22 bit long.

### `managed`

- type : `bool`
- values : `True` / `False`

Is the custom emoji managed by an integration.

### `name`

- type : `str`

The emoji's name. Custom emoji names fall into the normal naming category, so
2-32 characters, but unicode emoji names do not.

> If an emoji is deleted, then it's name might be an empty an string.

### `require_colons`

- type : `bool`
- values : `True` / `False`
- default : `True`

Whether this emoji must be wrapped in colons. At the case of Unicode emojis is
set to False.

### `roles`

- type : `set` / `NoneType`
- default : `None`
- elements : [`Role`](Role.md)

The set of roles for which the custom emoji is whitelisted to.  If the emoji
is not limited for specific roles, then this value is set to `None`. If the
emoji is a builtin (unicode) emoji, then this attribute is set to `None` as 
well.

### `unicode`

- type : `NoneType` / `str`
- default : `None`

At the case of custom emojis this attribute is always `None`, but at the case
of unicode emojis this attribute stores the emoji's unicode representation.

### `user`

- type : [`User`](User.md) / [`Client`](Client.md)
- default : [`ZEROUSER`](ZEROUSER.md)

The creator of the custom emoji. The emoji must be requested from the Discord
API, or it's user will be just the default `ZEROUSER`.

## `Properties`

### `as_emoji`

- returns : `str`

This property returns the emoji's form, when it is sent in a [message](Message.md).

### `as_reaction`

- returns : `str`

Used at `Client.reaction_add` method. This property returns the emoji's reaction
form, which is accepted by the discord API at requests.

### `created_at`

- returns : `datetime`

Returns the date when the emoji was created. If the emoji is unicode emoji, then
it returns the discord epoch's start.

### `partial`

- returns : `bool`
- values : `True` / `False`

If the emoji's [`guild`](Guild.md) attribute is `None`, then the emoji is partial.
Partial emojis get an update if `__new__` is called. Discord's builtin
emojis are all `partial`, but they never touch `Emoji.__new__`.

### `url`

- returns : `str` / `None`
- default : `None`

Returns the emoji's url if it is a custom emoji. At the case of unicode emoji, 
it returns `None`.

## Methods

### `is_custom_emoji`

- returns : `True` / `False`

Returns `True` if the emoji is a custom emoji.

### `is_unicode_emoji`

- returns : `True` / `False`

Returns `True` if the emoji is a unicode emoji.

### `url_as(emoji,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

If the emoji is a builtin (unicode) emoji, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
If the emoji is animated, then the extension can be 'gif' too.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

## Class attributes

## Classmethods

### `precreate(cls,emoji_id,**kwargs)`

- returns : [`Emoji`](Emoji.md)
- raises : `AttributeError`

Tries to query the emoji first, if it finds it, and it is not partial returns
that, else it updates the emoji. If it does not finds it it creates a new one,
stores and updates it. The precreated emojis are always partial, so when they
are created on dispatch event their attributes will be overwritten.

Some attributes are set as default or processed from kwargs:
- [`name`](#name) : default is `''`.
- [`animated`](#animated) : default is `False`.

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Returns the emoji's hash value, which equals to it's id.

### `__str__(self)`

- returns : `str`

Returns the emoji's name.

### `__repr__(self)`

- returns : `str`

Returns the representation of the emoji.

### `__format__(self,code)`

- returns : `str`

```python
f'{emoji}' #-> emoji.name
f'{emoji:e}' #-> emoji.as_emoji
f'{emoji:r}' #-> emoji.as_reaction
f'{emoji:c}' #-> emoji.created_at with '%Y.%m.%d-%H:%M:%S' format
```

Raises `ValueError` on invalid format code.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__` 

Compares the two emoji's id.

## Internal

### `__new__(cls,data)` (magic method)

- returns : [`Emoji`](Emoji.md)

The method first tries to find the emoji by id. If it fails it creates a new
`Emoji` instance. This method cannot create builin emojis, all of them
is loaded when the module is imported.

### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the emoji by the given data.

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the emoji and returns it's old attributes with
(`attribute name`, `old value`) items.

| name              | description                   |
|-------------------|-------------------------------|
| animated          | bool                          |
| available         | bool                          |
| managed           | bool                          |
| name              | str                           |
| require_colons    | bool                          |
| roles             | set of [Role](Role.md) / None |


### `_delete(self)` (method)

- returns : `None`

Called if an emoji is deleted from a guild. It removes the guild's references at
the guild, and turns the emoji partial.
