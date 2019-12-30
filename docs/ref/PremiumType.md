# class `PremiumType`

Represents Discord's premium types.

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py)

Each premium type is stored in the classe's [`.INSTANCES`](#instances) `list` class
attribute, with [`PremiumType`](PremiumType.md) elements. But they can also be
accessed as `PremiumType.<name>`.

## Instance attributes

| name      | type      |
|-----------|-----------|
| name      | str       |
| value     | int       |

## Class attributes

##### Predefined class attributes

There are 3 premium types:

| name          | value     |
|---------------|-----------|
| none          | 0         |
| nitro_classic | 1         |
| nitro         | 2         |

### `INSTANCES`

- type : `list`
- elements : [`PremiumType`](PremiumType.md)

Stores the created [`PremiumType`](PremiumType.md) instances. This
container is accessed when translating a Discord premium type's value to
it's representation.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`PremiumType`](PremiumType.md) and stores it at the classe's
[`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the premium type's name.

### `__int__(self)`

- returns : `int`

Returns the premium type's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the object.
