# class `PermOW`

Represents a permission overwrite of a [guild channel](ChannelGuildBase.md).

- Source : [role.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/role.py)

## Instance attributes

### `allow`

- type : `int`

The allowed permissions of the overwrite.

### `deny`

- type : `int`

The denied permission of the overwrite.

### `target`

- type : [`Role`](Role.md) / [`User`](User.md) / [`Client`](Client.md)

The target user or role of the overwrite.

## Properties

### `type`

- returns : `str`
- values : `'role'` / `'member'`

How Discord desides, if the target of the overwrite is a user or a role.

## Methods

### `keys(self)`

- yields : `str`

Iterates over the permission names.

### `values(self)`

- yields : `str`
- values : `'a'`, `'d'`, `'n'`

Iterates over all the permissions and returns the corresponding 
overwrite mode for all of them. Theese can be either `'a'` for allow,
`'d'` for deny or `'n'` for none.

### `items(self)`

- yields : (`str`, `str`) pairs

Iterates over all permissions and returns their name with their value from 
`'a'`, `'d'`, `'n'` (as above) in each item.

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Hashes the permission overwrite.

### `__repr__(self)`

- returns : `str`

Returns the representation of the permission overwrite.

### `__eq__`, `__ne__`

Compares the two permission overwrite.

### `__iter__(self)`

- yields : `str`

Iterates over the permission names.

### `__getitem__(self,key)`

- returns : `str`
- values : `'a'`, `'d'`, `'n'`
- raises : `KeyError`

Returns the overwrite's mode for the given permission name.
If the permission name is invalid raises `KeyError`.

## Internal

### `__init__(self,data)` (magic method)

Creates a permission overwrite from the given data received from
Discord.
