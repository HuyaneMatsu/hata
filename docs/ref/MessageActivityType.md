# class `MessageActivityType`

Represents a [message activity](MessageActivity.md)'s type.

- Source : [message.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/message.py)

Each message activity type is stored in the classe's [`.INSTANCES`](#instances)
`list` class attribute, but they can also be accessed as
`MessageActivityType.<name>`.

## Instance attributes

### `name`

- type : `str`

The message activity type's name.

### `value`

- type : `int`

The message activity type's Discord side representation.

## Class attributes

##### Predefined class attributes

There are 4 (+2:placeholder) message activity types :

| name              | value     |
|-------------------|-----------|
| none              | 0         |
| join              | 1         |
| spectate          | 2         |
| listen            | 3         |
| unknown *         | 4         |
| join_request      | 5         |


> The `none` and `unknown` activity type is not used by Discord, they are
> just a spaceholders.

> \* message activity unknown is not added as class attribute.

### `INSTANCES`

- type : `list`
- elements : [`MessageActivityType`](MessageActivityType.md)

Stores the created [`MessageActivityType`](MessageActivityType.md) instances.
This container is accessed when translating a Discord message activity type's
value to it's representation.

## Magic methods

### `__str__(self)`

- returns : `str`

Returns the message activity type's [`.name`](#name) instance attribute.

### `__int__(self)`

- returns : `int`

Returns the message activity type's [`.value`](#value) instance attribute.

### `__repr__(self)`

Returns the representation of the message activity type.

## Internal

### `__init__(self,value,name)` (magic method)

Creates a new [`MessageActivityType`](MessageActivityType.md) instance and
stores it at the classe's [`.INSTANCES`](#instances) class attribute.
