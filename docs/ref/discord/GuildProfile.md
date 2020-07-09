# class `GuildProfile`

Represents a user's profile at a guild.

- Source : [user.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/user.py)

## Instance attributes

### `boosts_since`

- type : `NoneType` / `datetime`
- default : `None`

Since when the user uses it's Nitro to boost the [guild](Guild.md). If the user
does not boost the guild, this attribute is set to `None`.

### `joined_at`

- type : `datetime` / `NoneType`
- default : `None`

The date, since the user is the member of the guild. If this data was not
received with the initial data, then it is set to `None`.

### `nick`

- type : `str` / `Nonetype`
- default : `None`

The user's nick at the guild, or None if it has not.

### `roles`

- type : `list`
- elements : [`Role`](Role.md)

The user's roles at the guild.

> Feel free to `.sort()` it whenever you need it.

## Properties

### `created_at`

- returns : `datetime`

For compability purposes with other types. Returns
[`self.joined_at`](#joined_at) if set, else the Discord epoch in datetime.

### `color`

- returns : [`Color`](Color.md)
- default : `Color(0)`

Returns the color of the respective user at the respective guild of the
profile.

## Methods

### `get_top_role(self, default=None)`

- returns : [`Role`](Role.md) / `default`
- default : `default`

Returns the top role of the guild profile. If the profile has no roles, then
returns the `default`'s value.

## Internal

### `__init__(self,data,guild)` (magic method)

Creates a new [GuildProfile](GuildProfile.md) object from a user, from a guild,
and from the user's member data at the guild.

### `_update_no_return(self,data,guild)` (method)

- returns : `None`

Updates the guild profile and return None.

### `_update(self,data,guild)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the guild profile and returns it's old attributes with
(`attribute name`, `old value`) items.

| name                      | description               |
|---------------------------|---------------------------|
| nick                      | str / None                |
| roles                     | list of [Role](Role.md)   |
| boosts_since              | datetime / None           |

### `_set_created(self,data)` (method)

- returns : `None`

If the [`.created_at`](#created_at) attribute of the profile is `None`, and the
data includes it, then sets the attribute.


