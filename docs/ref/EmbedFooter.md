# class `EmbedFooter`

An `footer` slot's representation of an [embed](EmbedCore.md).

- Source : [embed.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/embed.py)

## Instance attributes

| name              | type              | default       | description       |
|-------------------|-------------------|---------------|-------------------|
| icon_url          | str / NoneType    | None          | send - receive    |
| proxy_icon_url    | str / NoneType    | None          | receive           |
| text              | str               |               | send - receive    |

## Method

### `to_data(self)`

- returns : `dict`
- items : (`str`, `str`)

Converts the [`EmbedFooter`](EmbedFooter.md) to json serializable `dict`.

## Classmethods

### `from_data(cls,data)`

- returns : [`EmbedFooter`](EmbedFooter.md)

Creates an [`EmbedFooter`](EmbedFooter.md) object from the data sent by Discord.

## Magic methods

### `__init__(self,text,icon_url=None)`

Creates an [`EmbedFooter`](EmbedFooter.md) with the given `text` and with an
optional `url`.

### `__len__(self)`

- returns : `int`

Returns the [`EmbedFooter`](EmbedFooter.md)'s `text` field's length.

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`EmbedFooter`](EmbedFooter.md).

### `__eq__`

Compares two [`EmbedFooter`](EmbedFooter.md)'s `icon_url` and `text` field.
