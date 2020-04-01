# class `ActivitySpotify`

`ActivitySpotify` represents a listening to spotify activity. The type is
member of [`activity type`](ACTIVITY_TYPES.md) with type value of `2`.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/activity.py)

The type's `ACTIVITY_FLAG` is `0b0000001110011111`, what means it's
`DATA_SIZE_LIMIT` is 12 (`id` is static).

| group name     | binary value       |
| -------------- | ------------------ |
| timestamps     | 0b0000000000000001 |
| details        | 0b0000000000000010 |
| state          | 0b0000000000000100 |
| party          | 0b0000000000001000 |
| asset          | 0b0000000000010000 |
| sync_id        | 0b0000000010000000 |
| session_id     | 0b0000000100000000 |
| flags          | 0b0000001000000000 |

## Familiar types

- [`ActivityRich`](ActivityRich.md)
- [`ActivityUnknown`](ActivityUnknown.md)
- [`ActivityGame`](ActivityGame.md)
- [`ActivityStream`](ActivityStream.md)
- [`ActivityWatching`](ActivityWatching.md)
- [`ActivityCustom`](ActivityCustom.md)

## Superclasses

- [`ActivityBase`](ActivityBase.md)

## Instance attributes

- [`asset_image_large`](ActivityRich.md#asset_image_large)
- [`asset_image_small`](ActivityRich.md#asset_image_small)
- [`asset_text_large`](ActivityRich.md#asset_text_large)
- [`asset_text_small`](ActivityRich.md#asset_text_small)
- [`created`](ActivityRich.md#created)
- [`details`](ActivityRich.md#details)
- [`flags`](ActivityRich.md#flags)
- [`name`](ActivityRich.md#name)
- [`party_id`](ActivityRich.md#party_id)
- [`party_max`](ActivityRich.md#party_max)
- [`party_size`](ActivityRich.md#party_size)
- [`session_id`](ActivityRich.md#session_id)
- [`state`](ActivityRich.md#state)
- [`sync_id`](ActivityRich.md#sync_id)
- [`timestamp_end`](ActivityRich.md#timestamp_end)
- [`timestamp_start`](ActivityRich.md#timestamp_start)

For more details check [`ActivityRich`](ActivityRich.md).

One difference is that the default [`flag`](ActivityFlag.md) is
`ActivityFlag.spotify` instead of `ActivityFlag.none`.

## Class attributes

| name              | value                 |
|-------------------|-----------------------|
| ACTIVITY_FLAG     | 0b0000001110011111    |
| DATA_SIZE_LIMIT   | 12                    |

### `color`

- type : [`Color`](Color.md)
- value : `Color(0x1db954)`

The display color of the activity.

### `CUSTOM_ID`

- type : `str`
- value : `'spotify:1'`

The custom id of the activity.

## Properties

##### Inherited properties

- [`.discord_side_id`](ActivityBase.md#discord_side_id)
- [`.created_at`](ActivityBase.md#created_at)

### `type`

- returns : `int`
- value : `2`

[`ActivitySpotify`](ActivitySpotify.md)'s type is always `2`.

### `id`

- return : `int`
- value : `0`

Spotify activity has no real id.

### `album`

- returns : `str`
- default : `''` (empty string)

Returns the currently playing track's album title. This value is equal to the
`asset_text_large` instance attribute.

### `album_cover_url`

- returns : `str`
- default : `''` (empty string)

Returns the currently playing track's album url, if it has.

### `artist`

- returns : `str`
- defualt : `''` (empty string)

Returns the track's artist, If it has more, they are separetd with `';'`.

### `artists`

- returns : `list`
- elements : `str`

Returns the track's artists. If it has non or one, it still returns a list.

### `duration`

- returns : `int`

The duration of the track.

### `title`

- returns : `str`
- default : `''` (empty string)

Returns the currently playing track on spotify, which is equal to
`acitivity.details`.

### `track_id`

- returns : `str`
- default : `''` (empty string)

The id of the currently playing track. This value is same as the `sync_id`.

## Classmethods

##### Inherited classmethods

- [`.create`](ActivityBase.md#createclsnameurltype_0)

## Magic Method

### Inherited magic methods

- [`.__eq__`](ActivityBase.md#__eq__-__ne__)
- [`.__ne__`](ActivityBase.md#__eq__-__ne__)

### `__hash__(self)`

- returns : `int`

Returns the activity's [`.session_id`](#Instance-attributes)'s hash.

### `__str__(self)`

- returns : `str`

Returns the activity's [`.name`](#Instance-attributes).

### `__repr__(self)`

- returns : `str`

Returns the representation of the activity.

## Internal

##### Inherited internaal

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
| asset_image_large         | str                               |
| asset_image_small         | str                               |
| asset_text_large          | str                               |
| asset_text_small          | str                               |
| created                   | int                               |
| details                   | str                               |
| flags                     | [ActivityFlag](ActivityFlag.md)   |
| name                      | str                               |
| party_id                  | str                               |
| party_max                 | int                               |
| party_size                | int                               |
| session_id                | str                               |
| state                     | str / None                        |
| sync_id                   | str                               |
| timestamp_end             | int                               |
| timestamp_start           | int                               |

### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the activity with the data sent by Discord.

### `_fillup(self)` (method)

- returns : `None`

Called at the end of [`.create`](#inherited-classmethods), to fill up the
missing attributes.

