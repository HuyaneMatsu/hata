# class `MFA`

Represents Discord's Multi-Factor Authentication's levels.

- source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py)

## Instance attributes

| name      | type              |
|-----------|-------------------|
| name      | str               |
| value     | int               |

## Class attributes

##### Predefined class attributes

There are 2 multi-factor authentication levels:

| name      | value     |
|-----------|-----------|
| none      | 0         |
| elevated  | 1         |

### `INSTANCES`

- type : `list`
- elements : [`MFA`](MFA.md)

Stores all the created [`MFA`](MFA.md) instance.
They can be accessed with their `value` as key.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`MFA`](MFA.md) and stores
it at the classe's [`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the message MFA's name.

### `__int__(self)`

- returns : `int`

Returns the message MFA's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the MFA.
