# class `EmbedField`

Represents an element of an [embed](EmbedCore.md)'s `fields` list.

- Source : [embed.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/embed.py)

## Instance attributes

| name              | type              | default       | description       |
|-------------------|-------------------|---------------|-------------------|
| inline            | bool              | False         | send - receive    |
| name              | str               |               | send - receive    |
| value             | str               |               | send - receive    |

## Method

### `to_data(self)`

- returns : `dict`
- items : (`str`, `str` / `bool`)

Converts the [`EmbedField`](EmbedField.md) to json serializable `dict`.

## Classmethods

### `from_data(cls,data)`

- returns : [`EmbedField`](EmbedField.md)

Creates an [`EmbedField`](EmbedField.md) object from the data sent by Discord.

## Magic methods

### `__init__(self,name,value,inline=False)`

Creates an [`EmbedField`](EmbedField.md) with the given `name` and
`value` attribute and with an optional `inline` one.

### `__len__(self)`

- returns : `int`

Returns the [`EmbedField`](EmbedField.md)'s `name` and `value` field's length.

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`EmbedField`](EmbedField.md).

### `__eq__`

Compares two [`EmbedField`](EmbedField.md)'s `inline`, `name` and `value`.
