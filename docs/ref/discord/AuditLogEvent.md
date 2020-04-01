# class `AuditLogEvent`

Represents the event type of an [`AuditLogEntry`](AuditLogEntry.md).

- Source : [audit_logs.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/audit_logs.py) 

## Instance attributes

| name      | type              |
|-----------|-------------------|
| name      | str               |
| value     | int               |

## Class attributes

##### Predefined class attributes

There are 35 [`AuditLogEvent`](AuditLogEvent.md)-s.

| name                      | value     |
|---------------------------|-----------|
| GUILD_UPDATE              |  1        |
| CHANNEL_CREATE            | 10        |
| CHANNEL_UPDATE            | 11        |
| CHANNEL_DELETE            | 12        |
| CHANNEL_OVERWRITE_CREATE  | 13        |
| CHANNEL_OVERWRITE_UPDATE  | 14        |
| CHANNEL_OVERWRITE_DELETE  | 15        |
| MEMBER_KICK               | 20        |
| MEMBER_PRUNE              | 21        |
| MEMBER_BAN_ADD            | 22        |
| MEMBER_BAN_REMOVE         | 23        |
| MEMBER_UPDATE             | 24        |
| MEMBER_ROLE_UPDATE        | 25        |
| MEMBER_MOVE               | 26        |
| MEMBER_DISCONNECT         | 27        |
| BOT_ADD                   | 28        |
| ROLE_CREATE               | 30        |
| ROLE_UPDATE               | 31        |
| ROLE_DELETE               | 32        |
| INVITE_CREATE             | 40        |
| INVITE_UPDATE             | 41        |
| INVITE_DELETE             | 42        |
| WEBHOOK_CREATE            | 50        |
| WEBHOOK_UPDATE            | 51        |
| WEBHOOK_DELETE            | 52        |
| EMOJI_CREATE              | 60        |
| EMOJI_UPDATE              | 61        |
| EMOJI_DELETE              | 62        |
| MESSAGE_DELETE            | 72        |
| MESSAGE_BULK_DELETE       | 73        |
| MESSAGE_PIN               | 74        |
| MESSAGE_UNPIN             | 75        |
| INTEGRATION_CREATE        | 80        |
| INTEGRATION_UPDATE        | 81        |
| INTEGRATION_DELETE        | 82        |

### `INSTANCES`

- type : `dict`
- items : (`int`, [`AuditLogEvent`](AuditLogEvent.md))

Stores all the created [`AuditLogEvent`](AuditLogEvent.md) instance.
These can be accessed with their `value` as key.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`AuditLogEvent`](AuditLogEvent.md) and stores
it at the classe's [`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the audit log event's name.

### `__int__(self)`

- returns : `int`

Returns the audit log event's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the audit log event.
