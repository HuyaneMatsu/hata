# class `Relationship`

Represents a Discord relationship.

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/others.py)

## Instance attributes

### `type`

- type : [`RelationshipType`](RelationshipType.md)

The type of the relationship. Can be any
[RelationshipType](RelationshipType.md).

### `user`

- type : [`User`](User.md) / [`Client`](Client.md)

The target user of the relationship.

## Magic methods

### `__repr__(self)`

- returns : `str`

Returns the representation of the relationship.

## Internal

### `__init__(self,client,user,data)` (magic method)

Creates a [`Relationship`](Relationship.md) from the data sent by Discord.
After creating the relationship, adds it to the [client's](Client.md)
relationships.
