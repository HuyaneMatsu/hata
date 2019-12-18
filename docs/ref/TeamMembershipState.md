# class `TeamMembershipState`

Represents a a [team member](TeamMember.md)'s state at the [team](Team.md).

- Source : [application.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/application.py)

## Instance attributes

| name      | type      |
|-----------|-----------|
| name      | str       |
| value     | int       |

## Class attributes

##### Predefined class attributes

There are 2 (+ spaceholder) predefined `TeamMembershipState`-s.

| name          | value     |
|---------------|-----------|
| NONE          | 0         |
| INVITED       | 1         |
| ACCEPTED      | 2         |

> The `None` state is just a placeholder for `0`, discord does not uses it.

### `INSTANCES`

- type : `list`
- length : `3`
- elements : [`TeamMembershipState`](TeamMembershipState.md)

Stores the creates [`RelationshipType`](RelationshipType.md) instances. This
container is accessed when translating a Discord relationship type's value to
it's representation.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`TeamMembershipState`](TeamMembershipState.md) and stores it at the
classe's [`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the team membership state's name.

### `__int__(self)`

- returns : `int`

Returns the team membership state's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the object.
