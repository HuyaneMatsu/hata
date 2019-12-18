# class `EmbedAuthor`

An `author` slot's representation of an [embed](EmbedCore.md).

- Source : [embed.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/embed.py)

## Instance attributes

| name              | type              | default       | description       |
|-------------------|-------------------|---------------|-------------------|
| icon_url          | str / NoneType    | None          | send - receive    |
| name              | str / NoneType    | None          | send - receive    |
| url               | str / NoneType    | None          | send - receive    |
| proxy_icon_url    | str / NoneType    | None          | receive           |

## Method

### `to_data(self)`

- returns : `dict`
- items : (`str`, `str`)

Converts the [`EmbedAuthor`](EmbedAuthor.md) to json serializable `dict`.

## Classmethods

### `from_data(cls,data)`

- returns : [`EmbedAuthor`](EmbedAuthor.md)

Creates an [`EmbedAuthor`](EmbedAuthor.md) object from the data sent by Discord.

## Magic methods

### `__init__(self,icon_url=None,name=None,url=None)`

Creates an [`EmbedAuthor`](EmbedAuthor.md) with the given `icon_url`, `name`
and `url`. All argument is optional, but at least one of them should be passed.

### `__len__(self)`

- returns : `int`

Returns the [`EmbedAuthor`](EmbedAuthor.md)'s `name` field's length.

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`EmbedAuthor`](EmbedAuthor.md).

### `__eq__`

Compares two [`EmbedAuthor`](EmbedAuthor.md)'s `icon_url`, `name` and `url`
field.
