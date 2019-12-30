# class `RelationshipType`

Represents a [relationship's](Relationship.md) type.

- Source : [others.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/others.py)

Each relationship type is stored in the classe's [`.INSTANCES`](#instances)
`list` class attribute, with [`RelationshipType`](RelationshipType.md)
elements. But they can also be accessed as `RelationshipType.<name>`.

## Instance attributes

| name      | type      |
|-----------|-----------|
| name      | str       |
| value     | int       |

## Class attributes

##### Predefined class attributes

There are 4 (+1 placeholder) relationship types:

| name              | value     |
|-------------------|-----------|
| stranger          | 0         |
| friend            | 1         |
| blocked           | 2         |
| received_request  | 3         |
| sent_request      | 4         |

> The `stranger` relationship type is just a placeholder for type `0`.
> Discord does not uses it.

### `INSTANCES`

- type : `list`
- elements : [`RelationshipType`](RelationshipType.md)

Stores the created [`RelationshipType`](RelationshipType.md) instances. This
container is accessed when translating a Discord relationship type's value to
it's representation.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`RelationshipType`](RelationshipType.md) and stores it at the
classe's [`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the relationship type's name.

### `__int__(self)`

- returns : `int`

Returns the relationship type's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the object.
