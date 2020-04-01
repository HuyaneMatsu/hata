# class `Integration`

- Source : [integration.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/integration.py)

## Instance Attributes

| name                  | type                          | description                                                                           |
|-----------------------|-------------------------------|---------------------------------------------------------------------------------------|
| account_id            | str                           | Integration account id.                                                               |
| account_name          | str                           | Integration account name.                                                             |
| enabled               | bool                          | Is this integration enabled. 0 for kick, or 1 for remove role.                        |
| expire_behavior       | int                           | The behavior of expiring subscribers.                                                 |
| expire_grace_period   | int                           | The grace period in days before expiring subscribers. Can be 1, 3, 7, 14, 30.         |
| id                    | int                           | The id of the integration.                                                            |
| name                  | str                           | The name of the ingegration.                                                          |
| role                  | [Role](Role.md) / NoneType    | The role what this integration is uses for `subscribers` (can be None if not found).  |
| synced_at             | datetime                      | When this integration was last synced.                                                |
| syncing               | bool                          | Is this integration syncing.                                                          |
| type                  | str                           | The type of the integration (`'twitch'`, `'youtube'`, etc).                           |
| user                  | [User](User.md)               | The user this integration is for.                                                     |

## Properties

### `created_at`

- returns : `datetime`

The creation time of the integration.

## Magic methods

### `__str__(self)`

- returns : `str`

Returns the integration's name.

### `__repr__(self)`

- returns : `str`

Returns the integration's representation.

### `__hash__(self)`

- returns : `int`

Returns the integration's `.id`.

## Internal

### `__new__(cls,data)` (magic method)

Creates an [`Integration`](Integration.md) with the given data. If the
integration exists, updates and returns that.

