# class `Role`

Represents a Discord guild's role.

- Source : [role.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/role.py)

## Instance attributes

### `color`

- type : [`Color`](Color.md)
- default : `Color(0)`

The role's color. If a role's color is 0, means that it is ignored meanwhile
calculating a user's display color.

### `guild`

- type : [`Guild`](Guild.md) / `Nonetype`

The guild where the role exists. If the role is deleted, then it's guild is
set to `None`.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)

The roles's unique identificator number.

### `managed`

- type : `bool`
- values : `True` / `False`

If the role is managed by an outer integartion.

### `mentionable`

- type : `bool`
- values : `True` / `False`

If a role is mentionable.

### `name`

- type : `str`
- lenght : 2-32

The roles's name.

### `permissions`

- type : [`Permission`](Permission.md)

The permissions of the users having this role. A user's higher permissions
overwrite the lower ones' permissions meanwhile calculating towards a user's
final permission value.

### `position`

- type : `int`

The role's position at the guild.

### `separated`

- type : `bool`
- values : `True` / `False`

Users show up in separated groups by their highest role, which has `separated`
set to True.

## Properties

### `created_at`

- returns : `datetime`

The creation time of the role.

### `is_default`

- returns : `bool`
- values : `True` / `False`

Is the role the guild's default role.

### `mention`

- returns : `str`

The roles's mention.

### `partial`

- returns : `bool`
- values : `True` / `False`

Roles without a  [guild](Guild.md) are partial.

### `users`

- returns : `list`
- values : [`User`](User.md) / [`Client`](Client.md)

Returns a list of the guild's members who have this role.

## Classmethods

### `precreate(cls,role_id,**kwargs)`

- returns : [`Role`](Role.md)
- raises : `AttributeError` / `TypeError`

First tries to query the role from the already existing ones, if it fails
creates a new one with the given keyword arguments. The newly created role will
be always partial, so when it will be loaded, it's attributes will be
overwritten.

Some attributes are set as default or processed from kwargs:
- [`name`](#name) : default is `''`.
- [`color`](#color) : default is `Color(0)`, can be set with `int` and with
[`Color`](Color.md) object.


## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Returns the role's hash value, which equals to it's id.

### `__str__(self)`

- returns : `str`

Returns the role's name. If the role is partial, it returns `'partial'`.

### `__repr__(self)`

- returns : `str`

Returns the representation of the role.

### `__format__(self,code)`

- returns : `str`

```python
f'{role}' #-> role.name or 'partial' if unset
f'{role:m}' #-> role.mention
f'{role:c}' #-> role.created_at with '%Y.%m.%d-%H:%M:%S' format
```

Raises `ValueError` on invalid format code.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two role's [`.position`](#position). If the two role has the same
position, then it compares their [`.id`](#id).

## Internal

### `__new__(self,data,guild)` (magic method)

- returns : [`Role`](Role.md)

First checks if the role exists by it's ID. If it doesnt creates a new `Role`.
If the role is parital (or we just created it), we fill up it from the data.

### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the role by the given data.

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the role and returns it's old attribtes as: (attribute name, old value)
pairs.

### `_delete(self,data)` (method)

- returns : `None`

Called if a role is deleted from a [guild](Guild.md). It removes the role's
references at the guild, and with the same way it removes the role from every
user at the guild too.
