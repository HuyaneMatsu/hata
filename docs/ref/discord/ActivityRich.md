# class `ActivityRich`

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/activity.py)

`activity_rich` represents a discord rich activity. It can be used as any type
other [`activity type`](ACTIVITY_TYPES.md). Which
means it has every `activity.ACTIVITY_FLAG`, what is equal to:
`0b0001111111111111`.

`activity.ACTIVITY_FLAG` represents which attribute group can an activity type
have. These are:

| group name     | binary value       |
| -------------- | ------------------ |
| timestamps     | 0b0000000000000001 |
| details        | 0b0000000000000010 |
| state          | 0b0000000000000100 |
| party          | 0b0000000000001000 |
| asset          | 0b0000000000010000 |
| secret         | 0b0000000000100000 |
| url            | 0b0000000001000000 |
| sync_id        | 0b0000000010000000 |
| session_id     | 0b0000000100000000 |
| flags          | 0b0000001000000000 |
| application_id | 0b0000010000000000 |
| emoji          | 0b0000100000000000 |
| id             | 0b0001000000000000 |

> `activity.ACTIVITY_FLAG` is not equal to `activity.flags`,
> `activity.ACTIVITY_FLAG` is for internal use, meanwhile `activity.flags`
> is an activity instance attribute sent by Discord.

Each activity's `DATA_SIZE_LIMIT` tells, over how much data an activity
will be created as `activity_rich` over sub-activity types. This value is
calulates easily, with summing all the `1`s in the type's `ACTIVITY_FLAG` and
adding `3` to it (because every activity data contains `type`, `name` and
`created`). Becuase `activity_rich` can be any activity type, means it's
`DATA_SIZE_LIMIT` is the maximal, `16`.

## Superclasses

- [`ActivityBase`](ActivityBase.md)

## Instance attributes

### `application_id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
- default : `0`

The id of the application.

> Bound to `ACTIVITY_FLAG&0b0000010000000000` (application_id).

### `asset_image_large`

- type : `str`
- default : `''` (empty string)

The id of the large asset to display.

> Bound to `ACTIVITY_FLAG&0b0000000000010000` (asset).

### `asset_image_small`

- type : `str`
- default : `''` (empty string)

The id of the small asset to display.

> Bound to `ACTIVITY_FLAG&0b0000000000010000` (asset).

### `asset_text_large`

- type : `str`
- default : `''` (empty string)

The hover text of the large asset.

> Bound to `ACTIVITY_FLAG&0b0000000000010000` (asset).

### `asset_text_small`

- type : `str`
- default : `''` (empty string)

The hover text of the small asset.

> Bound to `ACTIVITY_FLAG&0b0000000000010000` (asset).

### `created`

- type : `int` (unix time in milliseconds)
- default : `0`

Tells, when the status was created.

### `details`

- type : `str`
- default : `''` (empty string)

Tells, what the player is currently doing.

> Bound to `ACTIVITY_FLAG&0b00000000000000010` (details).

### `emoji`

- type : `NoneType` / [`Emoji`](Emoji.md)
- default : `None`

The emoji used for [custom activity](ActivityCustom.md).

> Bound to `ACTIVITY_FLAG&0b0000100000000000` (emoji).

### `flags`

- type : [`ActivityFlag`](ActivityFlag.md)
- default : `ActivityFlag.none`

The flags of the activity.

> Bound to `ACTIVITY_FLAG&0b0000001000000000` (flags).

### `id`

- type : `int`
- default : `0`

The id of the activity.

> Bound to `ACTIVITY_FLAG&0b0001000000000000` (id)

### `name`

- type : `str`

The activity's name.

### `party_id`

- type : `str`
- default : `''` (empty string)

The party's id, which in the player is.

> Bound to `ACTIVITY_FLAG&0b0000000000001000` (party).

### `party_max`

- type : `int`
- default : 0

The party's maximal size, which in the player is.

> Bound to `ACTIVITY_FLAG&0b0000000000001000` (party).

### `party_size`

- type : `int`
- default : 0

The party's actual size, which in the player is.

> Bound to `ACTIVITY_FLAG&0b0000000000001000` (party).

### `secret_join`

- type : `str`
- default : `''` (empty string)

Unique hash given for the match context.

> Bound to `ACTIVITY_FLAG&0b0000000000100000` (secret).

### `secret_match`

- type : `str`
- default : `''` (empty string)

Unique hash for Spectate button.

> Bound to `ACTIVITY_FLAG&0b0000000000100000` (secret).

### `secret_spectate`

- type : `str`
- default : `''` (empty string)

Unique hash for chat invites and Ask to Join.

> Bound to `ACTIVITY_FLAG&0b0000000000100000` (secret).

### `session_id`

- type : `str`
- default : `''` (empty string)

Used at [`ActivitySpotify`](ActivitySpotify.md).

>Bound to `ACTIVITY_FLAG&0b0000000100000000` (session_id).

### `state`

- type : `str` / `NoneType`
- default : `None`

The player's current party status.

> Bound to `ACTIVITY_FLAG&0b0000000000000100` (state).

### `sync_id`

- type : `str`
- default : `''` (empty string)

Used at [`ActivitySpotify`](ActivitySpotify.md).  The ID of the currently
playing track.

> Bound to `ACTIVITY_FLAG&0b0000000010000000` (sync_id).

### `timestamp_end`

- type : `int` (unix time in milliseconds)
- default : `0`

The time when the activity ends.

> Bound to `ACTIVITY_FLAG&0b0000000000000001` (timestamps).

### `timestamp_start` 

- type : `int` (unix time in milliseconds)
- default : `0`

The time when the activity starts.

> Bound to `ACTIVITY_FLAG&0b0000000000000001` (timestamps).

### `type`

- type : `int`
- values : `0` / `1` / `2` / `3` / `4`

An integer, which represent the activity's type for Discord.

### `url`

- type : `str`
- default : `''` (empty string)

Twitch url only, the url of the stream.

> Bound to `ACTIVITY_FLAG&0b0000000001000000` (url).

## Class attributes

| name              | value                 |
|-------------------|-----------------------|
| ACTIVITY_FLAG     | 0b0001111111111111    |
| DATA_SIZE_LIMIT   | 16                    |

## Properties

##### Inherited properties

- [`.discord_side_id`](ActivityBase.md#discord_side_id)
- [`.created_at`](ActivityBase.md#created_at)

### `color`

- returns : [`Color`](Color.md)

The color of the activity.

### `start`

- returns : `None` / `datetime`

Returns when the activity was started, if set.

### `end`

- returns : `None` / `datetime`

Returns when the activity is going to end, if set.

### `image_large_url`

- returns : `str` / `None`
- defult : `None`

Returns the activity's large asset image's url. If the activity has no
large asset image, then returns `None`.

> Bound to `ACTIVITY_FLAG&0b0000010000010000` (application_id | asset).

### `image_small_url`

- returns : `str` / `None`
- defult : `None`

Returns the activity's small asset image's url. If the actvitiy has no
small asset image url, then returns `None`.

> Bound to `ACTIVITY_FLAG&0b0000010000010000` (application_id | asset).

## Methods

### `image_large_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- defult : `None`
- raises : `ValueError`

Returns the activity's large asset image's url. If the activity has no
large asset image, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

> Bound to `ACTIVITY_FLAG&0b0000010000010000` (application_id | asset).

### `image_small_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- defult : `None`
- raises : `ValueError`

Returns the activity's small asset image's url. If the actvitiy has no
small asset image url, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

> Bound to `ACTIVITY_FLAG&0b0000010000010000` (application_id | asset).

## Classmethods

##### Inherited classmethods

- [`.create`](ActivityBase.md#createclsnameurltype_0)

## Magic Method

### Inherited magic methods

- [`.__eq__`](ActivityBase.md#__eq__-__ne__)
- [`.__ne__`](ActivityBase.md#__eq__-__ne__)

### `__hash__(self)`

- returns : `int`

Returns the activity's [`.id`](#id).

### `__str__(self)`

- returns : `str`

Returns the activity's [`.name`](#name).

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
| application_id            | int                               |
| asset_image_large         | str                               |
| asset_image_small         | str                               |
| asset_text_large          | str                               |
| asset_text_small          | str                               |
| created                   | int                               |
| details                   | str                               |
| emoji                     | [Emoji](Emoji.md) / None          |
| flags                     | [ActivityFlag](ActivityFlag.md)   |
| id                        | int                               |
| name                      | str                               |
| party_id                  | str                               |
| party_max                 | int                               |
| party_size                | int                               |
| secret_join               | str                               |
| secret_match              | str                               |
| secret_spectate           | str                               |
| session_id                | str                               |
| state                     | str / None                        |
| sync_id                   | str                               |
| timestamp_end             | int                               |
| timestamp_start           | int                               |
| type                      | int                               |
| url                       | str                               |

### `_update_no_return (self,data)` (method)

- returns : `None`

Updates the activity and returns `None`.

### `_fillup(self)` (method)

- returns : `None`

Called at the end of [`.create`](#inherited-classmethods), to fill up the
missing attributes.
