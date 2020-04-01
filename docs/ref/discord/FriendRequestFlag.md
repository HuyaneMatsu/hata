# class `FriendRequestFlag`

Represents the friend request flags of a user.

- source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/others.py)

## Instance attributes

### `name`

- type : `str`

The name of the [`FriendRequestFlag`](FriendRequestFlag.md).

### `value`

- type : `int`

The identificator number of the [`FriendRequestFlag`](FriendRequestFlag.md).

## Class attributes

### `INSTANCES`

- type : `list`
- elements : [`FriendRequestFlag`](FriendRequestFlag.md)

Stores the created `FriendRequestFlag` instances.

##### Predefined class attributes

Each created [`FriendRequestFlag`](FriendRequestFlag.md)-s are stored at the
classe's [`.INSTANCES`](#instances) class attribute, but as class attributes
as well. These created `FriendRequestFlag`-s can be accessed with their
[`.name`](#name) as attributes.

| name                      | value |
|---------------------------|-------|
| none                      | 0     |
| mutual_guilds             | 1     |
| mutual_friends            | 2     |
| mutual_guilds_and_friends | 3     |
| all                       | 4     |

## Methods

### `encode(self)`

- returns : `dict`
- items : (`str`, `bool`)

Returns the [`FriendRequestFlag`](FriendRequestFlag.md)'s Discord side
representation.

## Class methods

### `decode(cls,data)`

- returns: [`FriendRequestFlag`](FriendRequestFlag.md)

Converts the friend request flag data sent by Discord to it's representation.

## Magic methods

### `__str__(self)`

- returns : `str`

Returns the `FriendRequestFlag`'s [`.name`](#name) instance attribute.

### `__int__(self)`

- returns : `int`

Returns the `FriendRequestFlag`'s [`.value`](#value) instance attribute.

### `__repr__(self)`

- returns : `str`

Returns the representation of the object.

## Internal

### `__init__(self,value,name)` (magic method)

Creates a [`FriendRequestFlag`](FriendRequestFlag.md) instance and stores it
at the classe's [`.INSTANCES`](#instances) class attribute.
