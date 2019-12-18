# class `TeamMember`

Represents a Discord [Team](Team.md)'s member.

- Source : [application.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/application.py)

Team members can be accessed trough a [`Team`](Team.md)'s
[`.members`](Team.md#members) instance attribute.

## Instance attributes

### `permissions`

- type : `list`
- elements : `str`

The permissions of the team member. Right now specific permissions are not
supported, so the list has only 1 element : `'*'`, what represents all the
permissions.

### `state`

- type : [`TeamMembershipState`](TeamMembershipState.md)

The state of the team member. A member can be invited or can have the invite
already accepted.

### `user`

- type : [`User`](User.md) / [`Client`](Client.md)

The corresponding user account of the `TeamMember` object.

## Magic methods

### `__repr__(self)`

- returns : `str`

Returns the representation of the [`TeamMember`](TeamMember.md).

### `__hash__(self)`

- returns : `int`

Returns the [`TeamMember`](TeamMember.md)'s [`.user`](#user)'s
[`.id`](UserBase.md#id).

### `__eq__(self)`

- returns : `bool`
- values : `True` / `False`

Returns whether the two [`TeamMember`](TeamMember.md) object is equal.

## Internal

### `__init__(self,data)`

Creates a [`TeamMember`](TeamMember.md) object from the data sent by Discord.
