# class `ActivityStream`

`ActivityStream` represents a streaming activity. Right now only twitch is
supported by discord. This class is a member of
[`activity type`](ACTIVITY_TYPES.md) with type value of `1`.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/activity.py)

The type's `ACTIVITY_FLAG` is `0b0001000111010010`, so it's `DATA_SIZE_LIMIT`
is 9.

| group name     | binary value       |
| -------------- | ------------------ |
| details        | 0b0000000000000010 |
| asset          | 0b0000000000010000 |
| url            | 0b0000000001000000 |
| sync_id        | 0b0000000010000000 |
| session_id     | 0b0000000100000000 |
| id             | 0b0001000000000000 |
                   
## Familiar types

- [`ActivityRich`](ActivityRich.md)
- [`ActivityUnknown`](ActivityUnknown.md)
- [`ActivityGame`](ActivityGame.md)
- [`ActivitySpotify`](ActivitySpotify.md)
- [`ActivityWatching`](ActivityWatching.md)
- [`ActivityCustom`](ActivityCustom.md)

## Superclasses

- [`ActivityBase`](ActivityBase.md)

## Instance attributes

- [`asset_image_large`](ActivityRich.md#created)
- [`asset_image_small`](ActivityRich.md#created)
- [`asset_text_large`](ActivityRich.md#created)
- [`asset_text_small`](ActivityRich.md#created)
- [`created`](ActivityRich.md#created)
- [`details`](ActivityRich.md#created)
- [`flags`](ActivityRich.md#created)
- [`id`](ActivityRich.md#created)
- [`name`](ActivityRich.md#created)
- [`session_id`](ActivityRich.md#created)
- [`sync_id`](ActivityRich.md#created)
- [`url`](ActivityRich.md#created)

For more details check [`ActivityRich`](ActivityRich.md).

## Class attributes

| name              | value                 |
|-------------------|-----------------------|
| ACTIVITY_FLAG     | 0b0001000111010010    |
| DATA_SIZE_LIMIT   | 9                     |

### `default_color`

- type : [`Color`](Color.md)
- value : `Color(0x593695)`

The color of the activity if it has `.url`.

## Properties

##### Inherited properties

- [`.discord_side_id`](ActivityBase.md#discord_side_id)
- [`.created_at`](ActivityBase.md#created_at)

### `type`

- returns : `int`
- value : `1`

[`ActivityStream`](ActivityStream.md)'s type is always `1`.

### `color`

- returns : [`Color`](Color.md)
- values : `Color(0x593695)` / `Color(0x7289da)`

Returns the activity's color. If the activity has
[`.url`](#Instance-attributes), then `Color(0x593695)`, else `Color(0x7289da)`.

### `twitch_name`

- returns : `str`
- default : `''` (empty string)

If the user streams on twitch, returns it's twitch name, else empty string.

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
| asset_image_large         | str                               |
| asset_image_small         | str                               |
| asset_text_large          | str                               |
| asset_text_small          | str                               |
| created                   | int                               |
| details                   | str                               |
| emoji                     | [Emoji](Emoji.md) / None          |
| id                        | int                               |
| name                      | str                               |
| session_id                | str                               |
| sync_id                   | str                               |
| url                       | str                               |

### `_update_no_return (self,data)` (method)

- returns : `None`

Updates the activity and returns `None`.

### `_fillup(self)` (method)

- returns : `None`

Called at the end of [`.create`](#inherited-classmethods), to fill up the
missing attributes.


