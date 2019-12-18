# singleton `ActivityUnknown`

`ActivityUnknown` represents if a user has no activity set. This activity type
is not a valid Discord activity. `activity_unknown` is a singleton and member of 
[`activity type`](ACTIVITY_TYPES.md) with type value of `-1`.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/activity.py)

The type's `ACTIVITY_FLAG` is `0b0000000000000000`, what means it has only
`name` and `type`, and it's `DATA_SIZE_LIMIT` is only 2.

## Familiar types

- [`ActivityRich`](ActivityRich.md)
- [`ActivityGame`](ActivityGame.md)
- [`ActivityStream`](ActivityStream.md)
- [`ActivitySpotify`](ActivitySpotify.md)
- [`ActivityWatching`](ActivityWatching.md)
- [`ActivityCustom`](ActivityCustom.md)

## Superclasses

- [`ActivityBase`](ActivityBase.md)

## Properties

##### Inherited properties

- [`.discord_side_id`](ActivityBase.md#discord_side_id)
- [`.created_at`](ActivityBase.md#created_at)

### `type`

- returns : `int`
- value : `-1`

[`ActivityUnknown`](ActivityUnknown.md) is just a placeholder for having
no activity, so it's type is not a valid Discord activity type.

### `id`

- returns : `int`
- value : `0`

Unknown activity has no id.

### `name`

- returns : `str`
- value : `'Unknown'`

Unknown activity has no name.

### `created`

- returns : `int`
- value : `DISCORD_EPOCH`

Unknown activity was never created.

## Class attributes

| name              | value                 |
|-------------------|-----------------------|
| ACTIVITY_FLAG     | 0b0001000111010010    |
| DATA_SIZE_LIMIT   | 9                     |

### `color`

- type : [`Color`](Color.md)
- value : `Color(0)`

The display color of the activity is the default Discord color.

## Classmethods

##### Inherited classmethods

- [`.create`](ActivityBase.md#createclsnameurltype_0)

### Magic methods

### Inherited magic methods

- [`.__eq__`](ActivityBase.md#__eq__-__ne__)
- [`.__ne__`](ActivityBase.md#__eq__-__ne__)

### `__hash__(self)`

- returns : `int`

Returns the activity's [`.id`](#id), so `0`.

### `__str__(self)`

- returns : `str`

Returns the activity's [`.name`](#name), so `'Unknown'`.

### `__repr__(self)`

- returns : `str`

Returns the representation of the activity.

## Internal

##### Inherited internal

- [`.botdict`](ActivityBase.md#botdictself-method)
- [`.hoomandict`](ActivityBase.md#hoomandictself-method)
- [`.fulldict`](ActivityBase.md#fulldictself-method)

### `__init__(self,data)` (magic method)

Returns an `ActivityUnknown` instance. This method should be never used.

### `_update(self,data)` (method)

- returns : `dict`
- value : `{}` (always empty)

### `_update_no_return(self,data)` (method)

- returns : `None`

### `_fillup(self)` (method)

- returns : `None`
