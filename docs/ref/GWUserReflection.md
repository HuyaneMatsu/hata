# class `GWUserReflection`

Represents a user object sent with [guild widget](GuildWidget.md) data.

- Source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/guild.py)

## Instance attributes

### `activity_name`

- type : `str` / `Nonetype`
- default : `None`

The user's top activity's name or `None`.

### `avatar_url`

- type : `str`

The user's avatar's url.

### `discrimintator`

- type : `int`

Should be `0` every case.

### `id`

- type : `int`

Should be between `0` and `99` including the limits.

### `name`

- type : `str`

The user's nick or name at the respective guild.

### `status`

- type : [Status](Status.md)

The user's status,

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Returns the `GWUserReflection`'s hash value, what equals to ir's [`.id`](#id).

### `__str__(self)`

- returns : `str`

Returns the `GWUserReflection`'s [`.name`](#name).

### `__repr__(self)`

- returns : `str`

Returns the representation of the `GWUserReflection`.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two `GWUserReflection`'s id.

## Internal

### `__init__(self,data)` (magic method)

Creates a [`GWUserReflection`](GWUserReflection.md) from user data included
with a [guild widget](GuildWidget.md).
