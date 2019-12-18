# class `AuditLogIterator`

An async iterator over a [guild](Guild.md)'s audit logs.

- Source : [audit_logs.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/audit_logs.py)

## Creating an AuditLogIterator

### `AuditLogIterator(client, guild, user=None, event=None)`

##### `client`

The [`client`](Client.md), what will execute the API requests.

##### `guild`

The [guild](Guild.md), what's audit logs will be requested.

##### `user`

If passed, will filter the actions to those, which were executed by the passed
[user](User.md).

##### `event`

If passed, will filter the actions only for that specific
[audit log event](AuditLogEvent.md).

> [`AuditLogIterator`](AuditLogIterator.md) can be created via
> [`Client`](Client.md) with it's
> [`.audit_log_iterator`](Client.md#audit_log_iteratorself-guild-usernone-eventnone)
> method as well.

## Instance attributes

### `client`

- type : [`Client`](Client.md)

The client trough which the [`AuditLogIterator`](AuditLogIterator.md) executes
the API requests.

### `guild`

- type : [`Guild`](Guild.md)

The guild, what's audit logs the [`AuditLogIterator`](AuditLogIterator.md) going
to request.

### `logs`

- type : `list`
- elements : [`AuditLogEntry`](AuditLogEntry.md)

A list of audit log entries processed from the requested data.

### `users`

- type : `dict`
- items : (`int`, [`User`](User.md) / [`Client`](Client.md))

A dictionary, which contains the mentioned users at the
[`AuditLogIterator`](AuditLogIterator.md).
The keys are the `id` of the users, meanwhile the values are the
[`users`](User.md) themselves.

### `webhooks`

- type : `dict`
- items : (`int`, [`Webhook`](Webhook.md))

A dictionary, which contains the mentioned webhooks at the
[`AuditLogIterator`](AuditLogIterator.md).
The keys are the `id` of the webhooks, meanwhile the values are
the [`webhooks`](Webhook.md) themselves.

## Methods

### `load_all(self)`

- `awaitable`
- returns : `None`

Loads all not yet loaded audit logs of the [`.guild`](#guild-1).

### `transform(self)`

- returns : [`AuiditLog`](AuditLog.md)

Returns an [`AuiditLog`](AuditLog.md) representation of the
[`AuditLogIterator`](AuditLogIterator.md).

## Magic methods

### `__aiter__(self)`

- returns : [`AuditLogIterator`](AuditLogIterator.md)

Async iterating an audit log iterator returns itself.

### `__anext__(self)`

- `awaitable`
- returns : [`AuditLogEntry`](AuditLogEntry.md)
- raises : `StopAsyncIteration`

Returns the next element of the [`AuditLogIterator`](AuditLogIterator.md).
Whenever needed, requests more audit logs. If there are no more audit
log enitres left at the [guild](#guild-1), raises `StopAsyncIteration`.

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`AuditLogIterator`](AuditLogIterator.md).

## Internal

### `_data` (instance attribute)

- type : `dict`
- items : (`str`, `int`)

Data used for requesting audit logs. It stores information about the passed
[`user`](#user) and [event](#event) at creation.

### `_index` (instance attribute)

- type : `int`
- default : `0`

Stores from which index the last audit log was yielded.

### `_process_data(self,data)` (method)

- returns : `None`

Processes a batch of audit log data.
