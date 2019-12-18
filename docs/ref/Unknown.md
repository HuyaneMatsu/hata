# class `Unknown`

Represents a not found object when creating an [audit log](AuditLog.md).

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py) 

These objects can be found at:
- [`AuditLogEntry`](AuditLogEntry.md).[`details`](AuditLogEntry.md#details)
- [`AuditLogEntry`](AuditLogEntry.md).[`target`](AuditLogEntry.md#target)
- [`AuditLogChange`](AuditLogChange.md).[`before`](AuditLogChange.md#before)
- [`AuditLogChange`](AuditLogChange.md).[`after`](AuditLogChange.md#after)

## Instance attribute

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The object's unique identificator number.

### `name`

- type : `str`
- default : `''`

The name of the object. This attribute is optional, so it might be set as an
empty string.

### `type`

- type : `str`

A `Unknown`'s "type" 's representative name. It can be:

- `'Channel'`
- `'Emoji'`
- `'Integration'`
- `'Invite'`
- `'Message'`
- `'Role'`
- `'User'`
- `'Webhook'`

## Properties

### `created_at`

- returns : `datetime`

The creation time of the represented object.

## Magic methods

### `__init__(self,type_,id_,name='')`

Creates an [`Unknown`](Unknown.md) object from the passed arguments.

### `__repr__(self)`

- returns : `str`

Returns the representation of the object.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Tries to compare the two object by their type and `.id`.
