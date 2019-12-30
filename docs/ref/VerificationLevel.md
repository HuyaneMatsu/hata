# class `VerificationLevel`

Represents Discord's verification level. 

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py)

Each verification level is stored in the classe's [`.INSTANCES`](#instances)
`list` class attribute, with [`VerificationLevel`](VerificationLevel.md)
elements. But they can also be accessed as `VerificationLevel.<name>`.

## Instance attributes

| name      | type      |
|-----------|-----------|
| name      | str       |
| value     | int       |

## Class attributes

##### Predefined class attributes

There are 5 verificatin levels:

| name      | value     |
|-----------|-----------|
| none      | 0         |
| low       | 1         |
| medium    | 2         |
| high      | 3         |
| extreme   | 4         |

### `INSTANCES`

- type : `list`
- items : [`VerificationLevel`](VerificationLevel.md)

Stores the created [`VerificationLevel`](VerificationLevel.md) instances. This
container is accessed when translating a Discord verification level's value to
it's representation.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`VerificationLevel`](VerificationLevel.md) and stores
it at the classe's [`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the verification level's name.

### `__int__(self)`

- returns : `int`

Returns the verification level's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the object.
