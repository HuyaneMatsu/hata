# class `Theme`

Represents a user's theme.

- source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py)

## Instance attributes

| name      | type              |
|-----------|-------------------|
| value     | str               |

## Properties

### `name`

- returns : `str`

A theme's name is same as the theme's `.value`.

## Class attributes

##### Predefined class attributes

There are 2 themes:

| value         |
|---------------|
| dark          |
| white         |

### `INSTANCES`

- type : `dict`
- items : (`str`, [`Theme`](Theme.md))

Stores all the created [`theme`](Theme.md) instance, which can be accessed
with their `.value` as key.

## Magic methods

### `__init__(self,value)`

Creates a new [`theme`](Theme.md) and stores it at the classe's
[`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the [`theme`](Theme.md)'s `.value`

### `__repr__(self)`

- returns : `str`

Returns the representation of the theme.


