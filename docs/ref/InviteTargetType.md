# class `InviteTargetType`

Represents a Discord [`Invite`]'s target's type.

- Source : [invite.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/invite.py)

## Instance Attributes

### `name`

- type : `str`

The name of the type.

### `value`

- type : `int`

The invite target type's Discord side value.

## Class attributes

##### Predefined class attributes

| name              | value     |
|-------------------|-----------|
| NONE              | 0         |
| STREAM            | 1         |

### `INSTANCES`

- type : `list`
- elements : [`InviteTargetType`](InviteTargetType.md)

Stores the created [`InviteTargetType`](InviteTargetType.md) instances.
This container is accessed, when translating a the object's Discord side
representation.

## Magic methods

### `__str__(self)`

- returns : `str`

Retrurns the `InviteTargetType`'s [`.name`](#name).

### `__int__(self)`

- returns : `str`

Retrurns the `InviteTargetType`'s [`.value`](#value).

### `__repr__(self)`

- returns : `str`

Returns the object's representation.

## Internal

### `__init__(self,value,name)` (magic method)

Creates a new [`InviteTargetType`](InviteTargetType.md) instance and stores it
at the classe's [`.INSTANCES`](#instances) class attribute.
