# class `ActivityBase`

`ActivityBase` is the superclass of all
[`activity types`](ACTIVITY_TYPES.md). It contains general methods used arround
it's subclasses. And cant lie, you can check `isinstance` with it.

- Source : [activity.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/activity.py)

## Subclasses

- [`ActivityRich`](ActivityRich.md)
- [`ActivityUnknown`](ActivityUnknown.md)
- [`ActivityGame`](ActivityGame.md)
- [`ActivityStream`](ActivityStream.md)
- [`ActivitySpotify`](ActivitySpotify.md)
- [`ActivityWatching`](ActivityWatching.md)
- [`ActivityCustom`](ActivityCustom.md)

## Properties

### `discord_side_id`

- returns : `str`

Returns the activity's Discord side id.

## Class attributes

| name              | value                 |
|-------------------|-----------------------|
| ACTIVITY_FLAG     | 0b0000000000000000    |
| DATA_SIZE_LIMIT   | 0                     |

## Properties

### `created_at`

- returns : `datetime` / `None`

Returns, when the activity was created. If the creation time was not included,
will return `None`.

## Classmethods

### `create(cls,name,url='',type_=0)`

- returns : [`activity type`](ACTIVITY_TYPES.md)

Returns an activity with the given attributes. `Url` is for streaming only,
right now only twitch is supported. If called from subclass, `type` is set 
automatically. Bot account activities support only `name`, `url` and `type` 
attribute.

## Magic methods

### `__eq__`, `__ne__`

- returns : `bool`
- values : `True` / `False`

Compares two activity's `.type` and `.id`.

## Internal

### `botdict(self)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Converts the activity to json serializible dictionary, which can be sent with
bot account to change activity.

### `hoomandict(self)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Converts the activity to json serializible dictionary, which can be sent with
user account to change activity. (not tested)

### `fulldict(self)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Converts the whole activity to a dictionary.
