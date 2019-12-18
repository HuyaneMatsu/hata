# class `EmbedImage`

An `image` slot's representation of an [embed](EmbedCore.md).

- Source : [embed.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/embed.py)

## Instance attributes

| name              | type              | default       | description       |
|-------------------|-------------------|---------------|-------------------|
| height            | int               | 0             | receive           |
| url               | str / NoneType    | None          | send - receive    |
| proxy_url         | str / NoneType    | None          | receive           |
| width             | int               | 0             | receive           |

## Method

### `to_data(self)`

- returns : `dict`
- items : (`str`, `str`)

Converts the [`EmbedImage`](EmbedImage.md) to json serializable `dict`.

## Classmethods

### `from_data(cls,data)`

- returns : [`EmbedImage`](EmbedImage.md)

Creates an [`EmbedImage`](EmbedImage.md) object from the data sent by Discord.

## Magic methods

### `__init__(self,url)`

Creates an [`EmbedImage`](EmbedImage.md) with the given `url`.

### `__len__(self)`

- returns : `int`
- value : `0`

An [`EmbedImage`](EmbedImage.md) has no fields, which count to the global
length limit, so calling `len()` it, will return `0` every time.

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`EmbedImage`](EmbedImage.md).

### `__eq__`

Compares two [`EmbedImage`](EmbedImage.md)'s `url` field.
