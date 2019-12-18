# class `GuildFeature`

- source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/guild.py)

## Instance attributes

### `value`

- type : `str`

The unique identificator value of the [`GuildFeature`](GuildFeature.md).

## Properties

### `name`

- returns : `str`

A [`GuildFeature`](GuildFeature.md) is same as it's [`.value`](#value).

## Class attributes

### `INSTANCES`

- type : `dict`
- items : (`str`, [`GuildFeature`](GuildFeature.md))

A container, what stores all the created [`GuildFeature`](GuildFeature.md)
instances, with their [`.value`] as the key, and them as the value.

##### Predefined class attributes

The known [`GuildFeature`](GuildFeature.md) instances can be accessed as
class attributes as well.

| attribute name        | value                 |
|-----------------------|-----------------------|
| animated_icon         | ANIMATED_ICON         |
| banner                | BANNER                |
| commerce              | COMMERCE              |
| discoverable          | DISCOVERABLE          |
| featurable            | FEATURABLE            |
| member_list_disabled  | MEMBER_LIST_DISABLED  |
| more_emoji            | MORE_EMOJI            |
| news                  | NEWS                  |
| partnered             | PARTNERED             |
| public                | PUBLIC                |
| public_disabled       | PUBLIC_DISABLED       |
| splash                | INVITE_SPLASH         |
| vanity                | VANITY_URL            |
| verified              | VERIFIED              |
| vip                   | VIP_REGIONS           |

> Guild features added at runtime are not stored as class attributes.

## Class methods

### `get(cls,value)`

- returns : [`GuildFeature`](GuildFeature.md)

Looks up the existing guild features with that specific value. If it cannot
find it, creates a new one.

## Magic methods

### `__init__(self,value)`

Creates a new [`GuildFeature`](GuildFeature.md) instance with the passed
`value`, then stores it at [`.INSTANCES`] class attribute.

### `__repr__(self)`

- returns : `str`

Returns the represnetation of the [`GuildFeature`](GuildFeature.md).

### `__str__(self)`

- returns : `str`

Returns [`.value`](#value).

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two features [.`value`](#value) as two `str`.
[`GuildFeature`](GuildFeature.md) instances can be converted with `str`
objects as well.
