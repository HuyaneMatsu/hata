# class `ActivityCustom`

`ActivityCustom` represents a custom settable activity. This class is a member
of [`activity types`](ACTIVITY_TYPES.md) with type value of `4`.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/activity.py)

The type's `ACTIVITY_FLAG` is `0b0001100000000100`. The type's
`DATA_SIZE_LIMIT` is 6. Discord actually sends 2 not used (`name`,
`id`) items, which are static.

| group name     | binary value       |
|----------------|--------------------|
| state          | 0b0000000000000100 |
| emoji          | 0b0000100000000000 |

## Familiar types

- [`ActivityRich`](ActivityRich.md)
- [`ActivityUnknown`](ActivityUnknown.md)
- [`ActivityGame`](ActivityGame.md)
- [`ActivityStream`](ActivityStream.md)
- [`ActivitySpotify`](ActivitySpotify.md)
- [`ActivityWatching`](ActivityWatching.md)

## Superclasses

- [`ActivityBase`](ActivityBase.md)

## Instance attributes

- [`created`](ActivityRich.md#created)
- [`emoji`](ActivityRich.md#emoji)
- [`state`](ActivityRich.md#state)

## Class attributes

### `CUSTOM_ID`

- type : `str`
- value : `'custom'`

The custom id of the activity.

## Propertis

##### Inherited properties

- [`.discord_side_id`](ActivityBase.md#discord_side_id)
- [`.created_at`](ActivityBase.md#created_at)

### `type`

- returns : `int`
- value : `3`

[`ActivityCustom`](ActivityCustom.md)'s type is always `3`.

### `name`

- returns : `str`

Returns the custom activity's connected name. At optimal case it is
`{emoji} {status}`, but any (or both) of them can be missing.

### `id`

- returns : `int`
- value : `0`

Custom activities have no `id`.

## Class attributes

| name              | value                 |
|-------------------|-----------------------|
| ACTIVITY_FLAG     | 0b0001100000000100    |
| DATA_SIZE_LIMIT   | 6                     |

### `Color`

- type : [`Color`](Color.md)
- value : `Color(0)`

Custom activity has no color.

## Classmethods

##### Inherited classmethods

- [`.create`](ActivityBase.md#createclsnameurltype_0)

## Magic Method

### Inherited magic methods

- [`.__eq__`](ActivityBase.md#__eq__-__ne__)
- [`.__ne__`](ActivityBase.md#__eq__-__ne__)

### `__hash__(self)`

- returns : `int`

Returns the activity's `.status`'s and `.emoji`'s combined hash.

### `__str__(self)`

- returns : `str`

Returns [`.name`](#name).

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

