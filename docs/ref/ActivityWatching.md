# class `ActivityWatching`

`ActivityWatching` represents a watching activity. This class is a member
of [`Activity type`](ACTIVITY_TYPES.md) with type value of `3`.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/activity.py)

The type's `ACTIVITY_FLAG` is `0b0001000000000000`, so it's `DATA_SIZE_LIMIT`
is 4.

| group name     | binary value       |
| -------------- | ------------------ |
| id             | 0b0001000000000000 |

## Familiar types

- [`ActivityRich`](ActivityRich.md)
- [`ActivityUnknown`](ActivityUnknown.md)
- [`ActivityGame`](ActivityGame.md)
- [`ActivityStream`](ActivityStream.md)
- [`ActivitySpotify`](ActivitySpotify.md)
- [`ActivityCustom`](ActivityCustom.md)

## Superclasses

- [`ActivityBase`](ActivityBase.md)

## Instance attributes

- [`created`](ActivityRich.md#created)
- [`id`](ActivityRich.md#id)
- [`name`](ActivityRich.md#name)

For more details check [`ActivityRich`](ActivityRich.md).

## Class attributes

| name              | value                 |
|-------------------|-----------------------|
| ACTIVITY_FLAG     | 0b0001000000000000    |
| DATA_SIZE_LIMIT   | 4                     |

### `Color`

- type : [`Color`](Color.md)
- value : `Color(0x7289da)`

The color of the activity.

## Properties

##### Inherited properties

- [`.discord_side_id`](ActivityBase.md#discord_side_id)
- [`.created_at`](ActivityBase.md#created_at)

### `type`

- returns : `int`
- value : `1`

[`ActivityWatching`](ActivityWatching.md)'s type is always `1`.

## Classmethods

##### Inherited classmethods

- [`.create`](ActivityBase.md#createclsnameurltype_0)

## Magic Method

### Inherited magic methods

- [`.__eq__`](ActivityBase.md#__eq__-__ne__)
- [`.__ne__`](ActivityBase.md#__eq__-__ne__)

### `__hash__(self)`

- returns : `int`

Returns the activity's [`.id`](#Instance-attributes).

### `__str__(self)`

- returns : `str`

Returns the activity's [`.name`](#Instance-attributes).

### `__repr__(self)`

- returns : `str`

Returns the representation of the activity.

## Internal

##### Inherited internal

- [`.botdict`](ActivityBase.md#botdictself-method)
- [`.hoomandict`](ActivityBase.md#hoomandictself-method)
- [`.fulldict`](ActivityBase.md#fulldictself-method)

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the activity and returns a `dict` with the changed values with
(`attribute name`, `old value`) items. 

| name                      | description                       |
|---------------------------|-----------------------------------|
| created                   | int                               |
| id                        | int                               |
| name                      | str                               |

### `_update_no_return (self,data)` (method)

- returns : `None`

Updates the activity and returns `None`.

### `_fillup(self)` (method)

- returns : `None`

Called at the end of [`.create`](#inherited-classmethods), to fill up the
missing attributes.

