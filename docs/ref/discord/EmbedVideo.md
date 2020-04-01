# class `EmbedVideo`

A `video` slot's representation of an [embed](EmbedCore.md). This slot cannot
be added to embeds however, it is receive only.

- Source : [embed.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/embed.py)

## Instance attributes

| name              | type              | default       | description       |
|-------------------|-------------------|---------------|-------------------|
| height            | int               | 0             | receive           |
| url               | str / NoneType    | None          | receive           |
| proxy_url         | str / NoneType    | None          | receive           |
| width             | int               | 0             | receive           |

## Method

### `to_data(self)`

- returns : `dict`
- value : `{}` (always empty)

[`EmbedVideo`](EmbedVideo.md) is receive only. This method wont be called at
serialization either. It is just a spaceholder.

## Classmethods

### `from_data(cls,data)`

- returns : [`EmbedVideo`](EmbedVideo.md)

Creates an [`EmbedVideo`](EmbedVideo.md) object from the data sent by Discord.

## Magic methods

### `__init__(self)`

Creates an empty [`EmbedVideo`](EmbedVideo.md) instance.

### `__len__(self)`

- returns : `int`
- value : `0`

An [`EmbedVideo`](EmbedVideo.md) has no fields, which count to the global
length limit, so calling `len()` it, will return `0` every time.

### `__repr__(self)`

- returns : `str`

Retrurns the representation of the [`EmbedVideo`](EmbedVideo.md).

### `__eq__`

Compares two [`EmbedVideo`](EmbedVideo.md)'s `url` field.
