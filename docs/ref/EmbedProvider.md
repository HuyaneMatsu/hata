# class `EmbedProvider`

A `provider` slot's representation of an [embed](EmbedCore.md). This slot cannot
be added to embeds however, it is receive only.

- Source : [embed.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/embed.py)

## Instance attributes

| name              | type              | default       | description       |
|-------------------|-------------------|---------------|-------------------|
| name              | str / NoneType    | None          | receive           |
| url               | str / NoneType    | None          | receive           |

## Method

### `to_data(self)`

- returns : `dict`
- value : `{}` (always empty)

[`EmbedProvider`](EmbedProvider.md) is receive only. This method wont be called at
serialization either. It is just a spaceholder.

## Classmethods

### `from_data(cls,data)`

- returns : [`EmbedProvider`](EmbedProvider.md)

Creates an [`EmbedProvider`](EmbedProvider.md) object from the data sent by Discord.

## Magic methods

### `__init__(self)`

Creates an empty [`EmbedProvider`](EmbedProvider.md) instance.

### `__len__(self)`

- returns : `int`
- value : `0`

An [`EmbedProvider`](EmbedProvider.md) has no fields, which count to the global
length limit, so calling `len()` it, will return `0` every time.

### `__repr__(self)`

- returns : `str`

Retrurns the representation of the [`EmbedProvider`](EmbedProvider.md).

### `__eq__`

Compares two [`EmbedProvider`](EmbedProvider.md)'s `name` and `url` fields.
