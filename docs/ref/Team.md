# class `Team`

Represents a Discord Team.

- Source : [application.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/application.py)

Teams can own [applications](Application.md). An application's team can be
accessed as `Application.owner`. Except if the application is owned by a
[user](User.md).

## Instance attributes

### `icon`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The hash of the team's icon.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)

 The id of the team.
 
### `members`
 
 - type : `list`
 - elements : [TeamMember](TeamMember.md)
 
A `list`, which contains all the members of the team. This list supposed
to contain the invited users too, but Discord docs lie.

### `name`

- type : `str`

The name of the team.

### `owner`

- type : [User](User.md) / [Client](Client.md)

The owenr of the team.

## Properties

### `created_at`

- returns : `datetime`

The creation time of the team.

### `icon_url`

- returns : `str` / `None`
- defautl : `None`

The team's icon's url. If the team has no icon, then returns `None`.

### `invited`

- returns : `list`
- elements : [User](User.md) / [Client](Client.md)

Supposed to return a list of all the invited users to the team.

### `accepted`

- returns : `list`
- elements : [User](User.md) / [Client](Client.md)

Returns a list of users, who are full members of the team.

## Methods

### `icon_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`


Returns the team's icon's url.
If the team has no icon, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

## Magic methods

### `__repr__`

Return sthe representation of the team.

## Internal

### `__new__(cls,data)` (Magic method)

- returns : [`Team`](Team.md)

Tries to find the team between the cached ones. If the searche succeeds
updates it, else creates a new one and.
