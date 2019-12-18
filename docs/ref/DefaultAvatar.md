# class `DefaultAvatar`

Represents a default avatar of the user, if it has no avatars set.

- source : [color.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/color.py)
                      
## Instance attributes

| name      | type              |
|-----------|-------------------|
| color     | [Color](Color.md) |
| name      | str               |
| value     | int               |

## Class attributes

##### Predefined class attributes

There are 5 default avatars:

| name      | value     | color     |
|-----------|-----------|-----------|
| blue      | 0         | 0x7289da  |
| gray      | 1         | 0x747f8d  |
| green     | 2         | 0x43b581  |
| orange    | 3         | 0xfaa61a  |
| red       | 4         | 0xf04747  |

### `INSTANCES`

- type : `list`
- elements : [`DefaultAvatar`](DefaultAvatar.md)

Stores all the created [`DefaultAvatar`](DefaultAvatar.md) instance.
They can be accessed with their `value` as index.

### `COUNT`

- type : `int`

The number of the default avatars defined.

## Properties

### `url`

- returns : `str`

Returns the default avatar's url.

## Classmethods

### `for_(cls,user)`

- returns : [`DefaultAvatar`](DefaultAvatar.md)

Returns the user's default avatar.

## Magic methods

### `__init__(self,value,name,color)`

Creates a [`DefaultAvatar`](DefaultAvatar.md) instance. Put's it into the
classe's [`.INSTANCES`](#instances).

### `__str__`

- returns : `str`

Returns the [`DefaultAvatar`](DefaultAvatar.md)'s `.name`.

### `__int__`

- returns : `int`

Returns the [`DefaultAvatar`](DefaultAvatar.md)'s `.value`.

### `__repr__`

- returns : `str`

Returns the represetation of the object.
