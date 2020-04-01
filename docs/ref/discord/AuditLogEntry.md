# class `AuditLogEntry`

Represents an audit log entry at an [`AuditLog`](AuditLog.md).

- Source : [audit_logs.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/audit_logs.py) 

## Instance attributes

### `changes`

- type : `list`
- elements : [`AuditLogChange`](AuditLogChange.md)

A `list` of [`AuditLogChange`](AuditLogChange.md), which contain the changes
of the entry.

### `details`

- type : `dict` / `NoneType`
- items : (`str`, `Any`)
- default : `None`

Details are additional information for a specific action types.

Theese are the following:

| Key           | Value type                                                                        | Description                                                                                                   | Audit log event                                                                  |
|---------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| amount        | int                                                                               | Number of messages, which were been deleted.                                                                  | MESSAGE_DELETE & MESSAGE_BULK_DELETE & MEMBER_DISCONNECT & MEMBER_MOVE           |
| channel       | [Channel](CHANNEL_TYPES.md) / [Unknown](Unknown.md)                               | The channel, where the entity was targeted.                                                                   | MEMBER_MOVE & MESSAGE_PIN & MESSAGE_UNPIN & MESSAGE_DELETE & MESSAGE_BULK_DELETE |
| days          | int                                                                               | The number of days after which the inactive users were removed by the prune.                                  | MEMBER_PRUNE                                                                     |
| message       | [Unknown](Unknown.md)                                                             | id of the message that was targeted                                                                           | MESSAGE_PIN & MESSAGE_UNPIN                                                      |
| target        | [Role](Role.md) / [User](User.md) / [Client](Client.md) / [Unknown](Unknown.md)   | The mentioned entity at a [permission overwrite](PermOW.md). Can be [user](User.md) or [role](Role.md) id.    | CHANNEL_OVERWRITE_CREATE & CHANNEL_OVERWRITE_UPDATE & CHANNEL_OVERWRITE_DELETE   |
| users_removed | int                                                                               | The amount of users removed from teh guild by the prune.                                                      | MEMBER_PRUNE                                                                     |

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)

The unique identificator number of the [`AuditLogEntry`](AuditLogEntry.md)

### `reason`

- type : `str` / `NoneType`
- default : `None`

The reason provided with the logged action.

### `target`

- type : [`Guild`](Guild.md) / [`Channel`](CHANNEL_TYPES.md) /
[`User`](User.md) / [`Client`](Client.md) / [`Role`](Role.md) /
[`Invite`](Invite.md) / [`Webhook`](Webhook.md) / [`Emoji`](Emoji.md) /
[`Integration`](Integration.md) / [`Unknown`](Unknown.md) / `NoneType`
- default : `None`

The target entity of the logged action. If the entity is not found, it will be
set as an [`Unknown`](Unknown.md) instance. It can happen, that target entity
is not provided, at that case target is set to `None`.

### `type`

- type : [`AuditLogEvent`](AuditLogEvent.md)

The event type of the logged action.

### `user`

- type : [`User`](User.md) / [`Client`](Client.md) / `NoneType`
- default : `None`

The user, who executed the logged action. If no user is provided by Discord,
it can be set as `None` as well.

## Properties

### `created_at`

- returns : `datetime`

The creation time of the entry.

## Magic methods

### `__repr__(self)`

- returns : `None`

Returns the representation of the entry.

## Internal

### `__init__(self,data,guild,webhooks,users)`

Creates an [`AuditLogEntry`](AuditLogEntry.md) from the given entry
data by `Discord` and from the creator [`AuditLog`](AuditLog.md)'s 
[`.guild`](AuditLog.md#guild), [`.webhooks`](AuditLog.md#webhooks) and
[`.users`](AuditLog.md#users).
