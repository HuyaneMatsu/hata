# class `ActivityGame`

`ActivityGame` represents a (not rich) gaming activity. This class is a member
of [`activity types`](ACTIVITY_TYPES.md) with type value of `0`.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/activity.py)

The type's `ACTIVITY_FLAG` is `0b0001011000000001`, so it's `DATA_SIZE_LIMIT`
is 7.

| group name     | binary value       |
| -------------- | ------------------ |
| timestamps     | 0b0000000000000001 |
| flags          | 0b0000001000000000 |
| application_id | 0b0000010000000000 |
| id             | 0b0001000000000000 |

## Familiar types

- [`ActivityRich`](ActivityRich.md)
- [`ActivityUnknown`](ActivityUnknown.md)
- [`ActivityStream`](ActivityStream.md)
- [`ActivitySpotify`](ActivitySpotify.md)
- [`ActivityWatching`](ActivityWatching.md)
- [`ActivityCustom`](ActivityCustom.md)

## Superclasses

- [`ActivityBase`](ActivityBase.md)

## Instance attributes

- [`application_id`](ActivityRich.md#application_id)
- [`created`](ActivityRich.md#created)
- [`flags`](ActivityRich.md#flags)
- [`id`](ActivityRich.md#id)
- [`name`](ActivityRich.md#name)
- [`timestamp_end`](ActivityRich.md#timestamp_end)
- [`timestamp_start`](ActivityRich.md#timestamp_start)

For more details check [`ActivityRich`](ActivityRich.md).

## Class attributes

| name              | value                 |
|-------------------|-----------------------|
| ACTIVITY_FLAG     | 0b0001011000000001    |
| DATA_SIZE_LIMIT   | 7                     |

### `Color`

- type : [`Color`](Color.md)
- value : `Color(0x7289da)`

The color of the gaming activity.

## Propertis

##### Inherited properties

- [`.discord_side_id`](ActivityBase.md#discord_side_id)
- [`.created_at`](ActivityBase.md#created_at)

### `type`

- returns : `int`
- value : `0`

[`ActivityGame`](ActivityGame.md)'s type is always `0`.

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
- items : (`str`, `any`)

Updates the activity and returns a `dict` with the changed values with
(`attribute name`, `old value`) items. 

| name                      | description                       |
|---------------------------|-----------------------------------|
| created                   | int                               |
| emoji                     | [Emoji](Emoji.md) / None          |
| state                     | str / None                        |

### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the activity with the data sent by Discord.

### `_fillup(self)` (method)

- returns : `None`

Called at the end of [`.create`](#inherited-classmethods), to fill up the
missing attributes.
