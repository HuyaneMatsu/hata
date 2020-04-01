# def `cr_p_overwrite_object`

Creates a json serializable object representing a
[permission overwrite](PermOW.md).

- Source : [role.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/role.py)

## `cr_p_overwrite_object(target, allow, deny)` (function)

- returns : `dict`
- items : (`str`, `Any`)

##### `target`

- type : [`Role`](Role.md) / [`UserBase`](UserBase.md) subclass instance

The target of the [permission overwrite](PermOW.md).

##### `allow`

- type : `int` / [`Permission`](Permission.md)

The allowed permissions of the [permission overwrite](PermOW.md).

##### `deny`

- type : `int` / [`Permission`](Permission.md)

The denied permissions of the [permission overwrite](PermOW.md).
