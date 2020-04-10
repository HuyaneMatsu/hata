# class `UserBase`

The `UserBase` class is the superclass of the different kind of classes, which
represent a user or an user like object (like a webhook).

- Source : [user.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/user.py)

## Subclasses : 

- [Client](Client.md)
- [User](User.md)
- [UserOA2](UserOA2.md)
- [Webhook](Webhook.md)
- [WebhookRepr](WebhookRepr.md)

## Instance attributes

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)

The user's unique identificator number.

### `name`

- type : `str`
- lenght : 2-32

The user's name.

### `discriminator`

- type : `int`
- values : 1-9999

An identificator number to distinguish users with the same name.

### `avatar`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The user's avatar's hash. If the user has no avatar, then 0.

### `has_animated_avatar`

- type : `bool`
- values : `True` / `False`

## Properties

### `activity`

- returns : [`Activity`](ACTIVITY_TYPES.md)
- default : [`ActivityUnknown`](ActivityUnknown.md)

Returns the top activity of the user. If it has no activities returns
`ActivityUnknown`.

> This method will be a [rich](#__rich__) method if the cubclass implements
`'activities'` in it's slots.

### `avatar_url`

- returns : `str`

The user's avatar's url. If the user has no avatar, then it returns the
user's default avatar's url.

### `created_at`

- returns : `datetime`

The creation time of the user.

### `default_avatar`

- returns : [`DefaultAvatar`](DefaultAvatar.md)

A default avatar object representing the user's default avatar.

### `default_avatar_url`

- returns : `str`

The user's default avatar's url.

### `full_name`

- returns : `str`

The user's "full" name. Example: "derpfish#1337"

### `mention`

- returns : `str`

The user's mention.

### `mention_nick`

- returns : `str`

The user's mention. It is not a real nick mention, because it does not depends
on nick, can be used anywhere.

### `platform`

- returns : `str`
- default : `''` (empty string)
- values : `''` / `'desktop'` / `'mobile'` / `'web'`
    
Returns the user's top status' platform. If the user is offline it will
return `''`.

> This method will be a [rich](#__rich__-module) method if the subclass
implements `'statuses'` in it's slots.

### `activities`

- returns : `list`
- elements : [`Activity`](ACTIVITY_TYPES.md)

Returns an empty `list` by default. Subclasses might overwrite it to return 
a `list` of the user's [activities](ACTIVITY_TYPES.md).

### `guild_profiles`

- type : `dict`
- default : `{}` (Empty dict)
- items : ([`Guild`](Guild.md), [`GuildProfile`](GuildProfile.md))

A dictionary, which contains the user's guild profiles. If any running client
shares a guild with a user, then the user will have a (guild, GuildProfile)
pair accordingly. Subclasses might overwrite this property to return a non
empty `dict`.

### `is_bot`

- returns : `bool`
- default : `False`

Bot accounts have `is_bot` set to `True`, user accounts to `False`.
Subclasses might overwrite this property.

### `flags`

- returns : [`UserFlag`](UserFlag.md)
- default : `UserFlag()`

The flags of the account.

### `status`

- returns : [`Status`](Status.md)
- default : `Status.offline`

Returns `Status.offline` by default. Subclasses might overwrite it to
return any kind of [status](Status.md).

### `statuses`

- type : `dict`
- default `{}` (empty dict)
- items : (`str`, `str`)

Returns an empty `dict` by default. Subclasses might overwrite it to return
a `dict` what contains `(platfrom (str), status (str))` items.

| platforms | statuses  |
|-----------|-----------|
| desktop   | online    |
| mobile    | idle      |
| web       | dnd       |
|           | offline   |

### `partial`

- returns : `bool`
- default : `False`

A user is partial if we do know only it's id. The rest of it's attributes
is set to their default. Subclasses might overwrite this peroperty.

## Methods

### `avatar_url_as(self,ext=None,size=None)`

- returns : `str`
- raises : `ValueError`

If the user has no avatar, then it returns the user's default avatar's url.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
If the user has animated avatar it can be 'gif' too.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

### `name_at(self,guild)`

- returns : `str`

Returns the users's nick at the guild if it has, else it's name.

> This method will be a [rich](#__rich__) method if the cubclass implements
`'guild_profiles'` in it's slots.

### `color_at(self,guild)`

- returns : [`Color`](Color.md)
- default : `Color(0)`

A method which returns the user's color at a guild.

> This method will be a [rich](#__rich__-module) method if the cubclass
implements `'guild_profiles'` in it's slots.

### `mentioned_in(self,message)`

- returns : `bool`

If the user is mentioned at a message.

> This method will be a [rich](#__rich__-module) method if the cubclass
implements `'guild_profiles'` in it's slots.

### `has_role(self,role)`

- returns : `bool`

If the user has the specific role.

> This method will be a [rich](#__rich__-module) method if the cubclass
implements `'guild_profiles'` in it's slots.

### `top_role_at(self, guild, default=None)`

- returns : [`Role`](Role.md) / `default`
- default : `default`

Returns the user's top role at the given [guild](Guild.md). If the user is
not at the given guild, or has no roles, returns the `default` value.

> This method will be a [rich](#__rich__-module) method if the cubclass
implements `'guild_profiles'` in it's slots.

### `can_use_emoji(self, emoji)`

- returns : `bool`

Returns whether the user can use the given emoji.

> This method will be a [rich](#__rich__-module) method if the cubclass
implements `'guild_profiles'` in it's slots. Webhook subclasses get their own
[rich](#__rich__-module) specific method as well.

### `has_higher_role_than(self, role)`

- returns : `bool`

Returns whether the user has higher role at the passed [`role`](Role.md)'s
[guild](Guild.md). If the user is the owner of the respective guild, then
returns `True`.

> This method will be a [rich](#__rich__-module) method if the cubclass
implements `'guild_profiles'` in it's slots.

### `has_higher_role_than_at(self, user, guild)`

Returns whether our user (`self`) has higher [role](Role.md) at the given
[guild](Guild.md) than the other user (`user`). Ownership is always prefered
over the top roles.

> This method will be a [rich](#__rich__-module) method if the cubclass
implements `'guild_profiles'` in it's slots.

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Returns the user's hash value, which equals to the user's id.

### `__str__(self)`

- returns : `str`

Returns the user's [`.name`](#name).

### `__repr__(self)`

- returns : `str`

Returns the representation of the user.

### `__format__(self,code)`

- returns : `str`
- raises `ValueError`

```python
f'{user}'   # -> user.name
f'{user:f}' # -> user.full_name
f'{user:m}' # -> user.mention
f'{user:c}' # -> user.created_at with '%Y.%m.%d-%H:%M:%S' format
```

Raises `ValueError` on invalid format code.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two user's id.

## Internal

### `__init_subclass__` (magic method)

- returns : `None`

Checks the subclass's `__slots__`, if it should overwrite some of it's
methods and properties with [`rich`](#__rich__-module).

### `__rich__` (module)

A module, what contains the rich methods and properties for subclasses.
