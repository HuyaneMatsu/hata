# class `UserOA2`

Represents a Discord User with extended personal data. If a `UserOA2` is 
created it will NOT overwrite the already existing user with the same ID, if
exists.

- Source : [oauth2.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/oauth2.py)

## Familiar types

- [Webhook](Webhook.md)
- [Client](Client.md)
- [User](User.md)
- [WebhookRepr](WebhookRepr.md)
- [GWUserReflection](GWUserReflection.md)

## Superclasses : 

- [`UserBase`](UserBase.md)

## Instance attributes

##### Inherited instance attributes

- [`id`](UserBase.md#id)
- [`name`](UserBase.md#name)
- [`discriminator`](UserBase.md#discriminator)
- [`avatar`](UserBase.md#avatar)
- [`has_animated_avatar`](UserBase.md#has_animated_avatar)

### `access`

- type : [`AO2Access`](AO2Access.md)

The user's oauth2 acces token through the object is created and can be
updated.

### `email`

- type : `str`

The user's email.

### `flags`

- type : [`UserFlag`](UserFlag.md)
- default : `UserFlag(0)`

The hypesquad flags of the account.

### `has_animated_avatar`

- type : `bool`
- values : `True` / `False`

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The user's unique identificator number.

### `locale`

- type : `str`
- default : `'en-US'`

The user's choosen language option.

### `mfa`

- type : `bool`
- values : `True` / `False`

`True` if the user has two factor enabled on the account.

### `name`

- type : `str`
- lenght : 2-32

The user's name.

### `premium_type`

- type : [`premium type`](PremiumType.md)
- default : `PremiumType.none`

The type of Nitro subscription on a user's account

### `system`

- type : `bool`
- values : `True` / `False`
- default : `False`

Whether the user is a Official Discord System user (part of the urgent message
system).

### `verified`

- type : `bool`
- values : `True` / `False`

Whether the email on this account is verified.

### Properties

##### Inherited properties

- [`guild_profiles`](UserBase.md#guild_profiles)
- [`activities`](UserBase.md#activities)
- [`status`](UserBase.md#status)
- [`statuses`](UserBase.md#statuses)
- [`activity`](UserBase.md#activity)
- [`avatar_url`](UserBase.md#avatar_url)
- [`created_at`](UserBase.md#created_at)
- [`default_avatar`](UserBase.md#default_avatar)
- [`default_avatar_url`](UserBase.md#default_avatar_url)
- [`full_name`](UserBase.md#full_name)
- [`mention`](UserBase.md#mention)
- [`mention_nick`](UserBase.md#mention_nick)

### `access_token`

- returns : `str`

Returns the user's access's access_token.

## Methods

##### Inherited methods

- [`avatar_url_as`](UserBase.md#avatar_url_asselfextnonesizenone)
- [`name_at`](UserBase.md#name_atselfguild)
- [`color`](UserBase.md#colorselfguild)
- [`mentioned_in`](UserBase.md#mentioned_inselfmessage)
- [`has_role`](UserBase.md#has_roleselfrole)

## Magic methods

#### Inherited magic methods

- [`__str__`](UserBase.md#__str__self)
- [`__repr__`](UserBase.md#__repr__self)
- [`__hash__`](UserBase.md#__hash__self)
- [`__format__`](UserBase.md#__format__selfcode)
- [`__gt__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__ge__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__eq__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__le__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
- [`__lt__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)

## Internal

### `__init__(cls,data,access)` (magic method)

Creates a [`OA2User`] from oauth2 user data and stores it's access token.

