# def `cr_p_role_object`

Creates a json serializable object representing a [role](Role.md).

- Source : [role.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/role.py)

## `cr_p_role_object(name, ...)` (function)

- returns : `dict`
- items : (`str`, `Any`)

##### `name`

- type : `str`

The name of the [role](Role.md).

### Optional keyword arguments

##### `id_`

- type : `int`
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
- default : `None`

The `id` of the [role](Role.md). If passed as `None`, a random id will be
generated.


##### `color`

- type : `int` / [`Color`](Color.md)
- default : `Color(0)`

The RGB color of the [role](Role.md).

##### `separated`

- type : `bool`
- default : `False`

Whether the user having this role, should be displayed separately in the
sidebar.

##### `position`

- type : `int`
- default : `0`

The position of the role.

##### `permissions`

- type : `int` / [`Permission`](Permission.md)
- default : `Permission(0)`

The bitwise value of teh enabled/disabled [permissions](Permission.md).

##### `managed`

- type : `bool`
- default : `False`

Whether the [role](Role.md) is managed by an [`Integration`](Integration.md).

##### `mentionable`

- type : `bool`
- default : `False`

Whether the users can mention the [role](Role.md).
