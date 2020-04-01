# class `Connection`

A connection object that the user is attached to.

- Source : [oauth2.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/oauth2.py)

## Instance attributes

### `friend_sync`

- type : `bool`

Whether the user has friend sync enabled for this connection.

### `id`

- type : `str`

The id of the connected account.

### `integrations`

- type : `NoneType` / `list`
- elements : [`Integration`](Integration.md)
- default : `None`

A list of guild integrations. If the connection has no integrations, then this
attribute is set as `None`.

### `name`

- type : `str`

The username of the connected account.

### `revoked`

- type : `bool`

Whether the connection is revoked.

### `show_activity`

- type : `bool`

Whether activities related to this connection will be shown in presence
updates.

### `type`

- type : `str`

The service of the connection, like `'twitch'` or `'youtube'`.

### `verified`

- type : `bool`

Whether the connection is verified.

### `visibility`

- type : `int`

The visibility of the connection.

| value | description                   |
|-------|-------------------------------|
| 0     | Visible only for the user.    |
| 1     | Visible to everyone.          |

## Internal

### `__init__(self,data)` (magic method)

Creates a `Connection` object from the data sent by Discord.
