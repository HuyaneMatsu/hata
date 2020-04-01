# class `MessageNotificationLevel`

Represents the message notification level at [guilds](Guild.md).

- source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/others.py)

## Instance attributes

| name      | type              |
|-----------|-------------------|
| name      | str               |
| value     | int               |

## Class attributes

##### Predefined class attributes

There are 2 message notification levels:

| name              | value     |
|-------------------|-----------|
| all_messages      | 0         |
| only_mentions     | 1         |


### `INSTANCES`

- type : `list`
- items : [`MessageNotificationLevel`](MessageNotificationLevel.md)

Stores all the created [`MessageNotificationLevel`](MessageNotificationLevel.md) instance.
They can be accessed with their `value` as index.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`MessageNotificationLevel`](MessageNotificationLevel.md) and stores
it at the classe's [`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the message notification level's name.

### `__int__(self)`

- returns : `int`

Returns the message notification level's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the message notification.
