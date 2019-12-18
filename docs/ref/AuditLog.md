# class `AuditLog`

Whenever an admin action is performed on the API, an audit log entry is added
to the respective guild's audit logs. This class represents a requested 
collections of these entries.

- Source : [audit_logs.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/audit_logs.py) 

## Instance attributes

### `guild`

- type : [`Guild`](Guild.md)

The audit logs' respective [guild](Guild.md).

### `logs`

- type : `list`
- elements : [`AuditLogEntry`](AuditLogEntry.md)

A list of [`audit log entries`](AuditLogEntry.md), what the
[`AuditLog`](AuditLog.md) contains.

### `users`

- type : `dict`
- items : (`int`, [`User`](User.md) / [`Client`](Client.md))

A dictionary, which contains the mentioned users at the
[`AuditLog`](AuditLog.md). The keys are the `id` of the users, meanwhile the
values are the [`users`](User.md) themselves.

### `webhooks`

- type : `dict`
- items : (`int`, [`Webhook`](Webhook.md))

A dictionary, which contains the mentioned webhooks at the
[`AuditLog`](AuditLog.md). The keys are the `id` of the webhooks, meanwhile the
values are the [`webhooks`](Webhook.md) themselves.

## Magic methods

### `__iter__(self)`

- retutns : `list_iterator`

Returns a list iterator over [`.logs`](#logs).

### `__reversed__(self)`

- returns : `list_reverseiterator`

Returns a reversed list iterator over [`.logs`](#logs).

### `__len__(self)`

- returns : `int`

Returns the length of [`.logs`](#logs).

### `__getitem__(self,index)`

- returns : [`AuditLogEntry`](AuditLogEntry.md) / `list` of [`AuditLogEntres`](AuditLogEntry.md)
- raises : `IndexError` / `TypeError`

Returns the specific [`AuditLogEntry`](AuditLogEntry.md) at the given error,
or a `list` of [`AuditLogEntries`](AuditLogEntry.md), if a slice is provided.
Raises `IndexError` if the given index is out of bounds.

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`AuditLogEntry`](AuditLogEntry.md).
