# class `reaction_mapping_line`

A set, which contains the [users](User.md) who reacted with the given
[`emoji`](Emoji.md) on a [message](Message.md). Stores the users ordered by
their id.

- source : [emoji.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/emoji.py)

- `__imul__`

## Superclasses

- `set`

## Instance attributes

### `unknown`

- type : `int`
- default : 0

Tells how much user reacted on the [message](Message.md), but they are not
loaded. This can happen if a [message](Message.md) is "older" and has
reactions on it.

## Methods:

### `count(self,user)`

- returns : `int`
- values : 0 / 1

Counts how much time is the user in self. So is it in self or nope basically.

### `copy(self)`

- returns : [`reaction_mapping_line`](reaction_mapping_line.md)

Copies the object.

## Magic methods

### `__len__(self)`

Returns the the amount of the reacters with the emoji. This amount is the sum of
the set's length itself and of the `unknown` attribute's value.

## Internal

### `__init__(self)` (magic method)

Sets the `unknown` attribute to 0.

### `relative_id_index(self,user_id)` (method)

- returns : `int`

Returns the index, where the object with the given id would be inserted to.

### `add(self,user)` (method)

- returns : `None`

Adds a user to the reacters.

### `update(self,users)` (method)

- returns : `None`

Mkes sure that all of the `users` is in `self`. If the user is in `self` does
nothing. If the `user` is missing from `self`, then puts it at the right index
and reduces `.unknown`.

### `filter(self,limit,after,before)` (method)

- returns : `list`
- values : [`User`](User.md) / [`Client`](Client.md)

If we know all the reacters, then insctead of executing a Discord API request
we filter the reacters locally using this method.


### `clear(self)` (method)

- returns : `None`

Clears all the [`User`](User.md) type objects from self to save reduce object
size. This method should not be called by itself, because
[`reaction_mapping`](reaction_mapping.md) has a `fully_loaded` loaded flag, so
the flag must be refreshed after calling a `clear`.
