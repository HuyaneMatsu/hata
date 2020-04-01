# class `ContentFilterLevel`

The representation of Discord's content filter level.

- source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/others.py)

## Instance attributes

| name      | type              |
|-----------|-------------------|
| name      | str               |
| value     | int               |

## Class attributes

##### Predefined class attributes

There are 3 content filter levels:

| name      | value     |
|-----------|-----------|
| disabled  | 0         |
| no_role   | 1         |
| everyone  | 2         |

### `INSTANCES`

- type : `list`
- elements : [`ContentFilterLevel`](ContentFilterLevel.md)

Stores all the created [`ContentFilterLevel`](ContentFilterLevel.md) instance.
They can be accessed with their `value` as index.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`ContentFilterLevel`](ContentFilterLevel.md) and stores
it at the classe's [`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the content filter's name.

### `__int__(self)`

- returns : `int`

Returns the content filter's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the content filter.
