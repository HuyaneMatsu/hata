# class `reaction_mapping`

A dict, which contains the reactions on a [message](Message.md) with 
([`Emoji`](Emoji.md), [`reaction_mapping_line`](reaction_mapping_line.md)) items.

- source : [emoji.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/emoji.py)

## Superclasses

- `dict`

## Instance attributes

### `fully_loaded`

- type : `bool`
- values : `True` / `False`

A flag which tells if every reacter is loaded on the message.

## Methods:

### `clear(self)` (method)

- returns : `None`

Clears all the [`User`](User.md) type objects from self to save reduce object
size. This method should not be called by itself, because
[`reaction_mapping`](reaction_mapping.md) has a `fully_loaded` loaded flag, so
the flag must be refreshed after calling a `clear`.

## Magic methods

### `__len__(self)`

Returns the the amount of the reacters with the emoji. This amount is the sum of
the list's length itself and of the `unknown` attribute's value.

## Internal

### `__init__(self,data)` (magic method)

Fills the object with the given data. `data` can be `None` too.

### `add(self,emoji,user)` (method)

- returns : `None`

Adds a user to the reacters.

### `remove(self,emoji,user,client_count)` (method)

- returns : `None`

Removes the user from the reacters.


### `remove_emoji(self,emoji)` (method)

- returns : `None` / [`reaction_mapping_line`](reaction_mapping_line.md)

Removes all the users, who reacted with the specific [emoji](Emoji.md). If no
users reacted with the emoji, then returns `None`, else it returns the whole
[`reaction_mapping_line`](reaction_mapping_line.md) itself.

### `_full_check(self)` (method)

- returns : `None`

Called when an emoji loses all of it's unknown reacters.

### `_update_some_users(self,emoji,users)` (method)

- returns : `None`

Called when we update some reacters of an emoji.

### `_update_all_users(self,emoji,users)` (method)

Called when we update all of the reacters of an emoji.
