# class `Permission`

Represents Disocrd permissions.

- Source : [permission.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/permission.py)

##### permission table

Each permission has it's own name used by the wrapper and a bitwize position.

| name                      | position  |
|---------------------------|-----------|
| create_instant_invite     |  0        |
| kick_users                |  1        |
| ban_users                 |  2        |
| administrator             |  3        |
| manage_channel            |  4        |
| manage_guild              |  5        |
| add_reactions             |  6        |
| view_audit_logs           |  7        |
| priority_speaker          |  8        |
| stream                    |  9        |
| view_channel              | 10        |
| send_messages             | 11        |
| send_tts_messages         | 12        |
| manage_messages           | 13        |
| embed_links               | 14        |
| attach_files              | 15        |
| read_message_history      | 16        |
| mention_everyone          | 17        |
| use_external_emojis       | 18        |
| connect                   | 20        |
| speak                     | 21        |
| mute_users                | 22        |
| deafen_users              | 23        |
| move_users                | 24        |
| use_voice_activation      | 25        |
| change_nickname           | 26        |
| manage_nicknames          | 27        |
| manage_roles              | 28        |
| manage_webhooks           | 29        |
| manage_emojis             | 30        |

> Theese names might differ from Discord's.

> Permission at position 19 and permissions over 30 (not includes 30) are
unused.

## Superclasses

- `int`

## Class Attributes

Some permissions or just their values are predefined to save time at
permission calculations:

| name                      | type                          | value                                 |
|---------------------------|-------------------------------|---------------------------------------|
| voice                     | int                           | 0b00000011111100000000001100000000    |
| none                      | int                           | 0b00000000000000000000000000000000    |
| all                       | int                           | 0b01111111111101111111111111111111    |
| all_channel               | int                           | 0b00110011111101111111111001010001    |
| text                      | int                           | 0b00000000000001111111110001000000    |
| general                   | int                           | 0b01111100000000000000000010111111    |
| deny_text                 | int                           | 0b11111111111111011000011111111111    |
| deny_voice                | int                           | 0b11111100000011111111111011111111    |
| deny_voice_con            | int                           | 0b11111100000011111111111011111111    |
| deny_both                 | int                           | deny_text & deny_voice                |
| permission_all            | [Permission](Permission.md)   | all                                   |
| permission_none           | [Permission](Permission.md)   | none                                  |
| permission_private        | [Permission](Permission.md)   | 0b00000000000001111100110001000000    |
| permission_private_bot    | [Permission](Permission.md)   | 0b00000000000001101100110001000000    |
| permission_group          | [Permission](Permission.md)   | 0b00000000000001111100010001000000    |
| permission_group_owner    | [Permission](Permission.md)   | 0b00000000000001111100110001000010    |
| permission_all_deny_text  | [Permission](Permission.md)   | deny_text                             |
| permission_all_deny_voice | [Permission](Permission.md)   | deny_voice                            |
| permission_all_deny_both  | [Permission](Permission.md)   | deny_both                             |

## Properties

### `can_{name}`

- returns : `int`
- values : `0` / `1`

Returns if the permission object allows the specific action.

> This property is implemented for each [permission name](#permission-table).

## Methods

### `allow_{name}(self)`

- returns : [`Permission`](Permission.md)

Returns a copy of this permision object, where the specific permission is
allowed.

> This method is implemented for each [permission name](#permission-table).

### `deny_{name}(self)`

- returns : [`Permission`](Permission.md)

Returns a copy of this permision object, where the specific permission is
denied.

> This method is implemented for each [permission name](#permission-table).

### `is_subset(self,other)`

- returns : `bool`

Returns `True` if self has the same or fever permissions than other.

### `is_superset(self,other)`

- returns : `bool`

Returns `True` if self has the same or more permissions than other.

### `is_strict_subset(self,other)`

- returns : `bool`

Returns `True` if the permissions on other are a strict subset of those on
self.

### `is_strict_superset(self,other)`

- returns : `bool`

Returns `True` if the permissions on other are a strict superset of those on
self.

### `update_by_keys(self,**kwargs)`

- returns : [`Permission`](Permission.md)
- raises : `KeyError`

Applies the kwargs for a new permission and returns it. If a kwargs is not a
valid [permission name](#permission-table), raises `KeyError`.

### `handle_overwrite(self,allow,deny)`

- returns : [`Permission`](Permission.md)

Applies an allow and a deny overwrite on the permission.

## Magic methods

### `__repr__(self)`

- returns : `str`

Returns the representation of the permission.

### `__getitem__(self,key)`

- returns : `int`
- values : `0` / `1`
- raises : `KeyError`

Returns if the permission allows the given permission under a name.
If the [permission name](#permission-table) is invalid raises `KeyError`.

### `__iter__(self)`

- yields : `str`

Yields each [permission's name](#permission-table), what the permission object allows.

### `__conatins__(self,key)`

- returns : `int`
- values : `0` / `1`
- default : `0`

Returns if the permission object allows the given
[permission name](#permission-table).
If the [permission name](#permission-table) is invalid returns `0`.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

returns : `bool`

Compares self if it is
[strict superset](#is_strict_supersetselfother),
[superset](#is_supersetselfother), equal, not equal,
[strict subset](#is_strict_subsetselfother) or
[subset](#is_subsetselfother) of the other.





