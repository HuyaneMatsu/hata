# class `Webhook`

Represents a Discord webhook and at cases it might be even it's user
represetation.

- Source : [webhook.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/webhook.py)

## Familiar types

- [User](User.md)
- [Client](Client.md)
- [UserOA2](UserOA2.md)
- [WebhookRepr](WebhookRepr.md)

## Superclasses

- [`UserBase`](UserBase.md)

## Instance attributes

##### Inherited instance attributes

- [`id`](UserBase.md#id)
- [`name`](UserBase.md#name)
- [`discriminator`](UserBase.md#discriminator)
- [`avatar`](UserBase.md#avatar)
- [`has_animated_avatar`](UserBase.md#has_animated_avatar)

### `channel`

- type : [`Channel`](CHANNEL_TYPES.md)

The channel, where the webhook going to send it's [messages](Message.md).

### `token`

- type : `str`

The webhooks's token. You need an id and a token to send webhook message.

### `type`

- type : [`WebhookType`](WebhookType.md)

The webhook's type.

### `user`

- type : [`User`](User.md) / [`Client`](Client.md)
- default : [ZEROUSER](ZEROUSER.md)

The creator of the webhook, or [ZEROUSER](ZEROUSER.md) if unknown.

## Properties

##### Inherited properties

- [`activity`](UserBase.md#activity)
- [`created_at`](UserBase.md#created_at)
- [`default_avatar`](UserBase.md#default_avatar)
- [`default_avatar_url`](UserBase.md#default_avatar_url)
- [`full_name`](UserBase.md#full_name)
- [`mention`](UserBase.md#mention)
- [`mention_nick`](UserBase.md#mention_nick)
- [`platform`](UserBase.md#platform)
- [`activities`](UserBase.md#activities)
- [`guild_profiles`](UserBase.md#guild_profiles)
- [`status`](UserBase.md#status)
- [`statuses`](UserBase.md#statuses)

### `avatar_url`

- returns : `str`

Returns the webhook's avatar's url. If the webhook has no avatar, then it
returns the it's default avatar.

> Webhooks can not have animated avatars.

### `guild`

- returns : [`Guild`](Guild.md)

The guild where the webhook is.

### `is_bot`

- returns : `bool`
- values : `True`

Webhooks are always bots.

### `partial`

- returns : `bool`
- values : `True` / `False`

If the webhook's [`.guild`](#guild) attribute is unknown, then it is partial.

## Classmethods

### `precreate(cls,webhook_id,**kwargs)`

- returns : [`User`](User.md)
- raises : `AttributeError` / `TypeError` / `ValueError`

Tries to query the given webhook from the existing ones, if it fails, it creates
a one. At the end it updates the webhook with the given kwargs.

Some attributes are set automatically or processed from kwargs:

| name                  | default                           | type                                  | alternatives                                                                                                                                  |
|-----------------------|-----------------------------------|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| name                  | ''                                | str (2-80 char)                       | str instances                                                                                                                                 |
| token                 | ''                                | str (60-68 char)                      | str instances                                                                                                                                 |
| avatar                | 0                                 | int (uint128)                         | None, int instances, str instances ([image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)) |
| has_animated_avatar   | False                             | bool                                  | int instance 0 or 1                                                                                                                           |
| user                  | [ZEROUSER](ZEROUSER.md)           | [User](User.md) / [Client](Client.md) | -                                                                                                                                             |
| channel               | None                              | [ChannelText](ChannelText.md)         | -                                                                                                                                             |
| type                  | [WebhookType](WebhookType.md).bot | [WebhookType](WebhookType.md)         | int instances                                                                                                                                 |

### `from_url(cls,url)`

- returns : `NoneType` / [`Webhook`](Webhook.md)
- default : `None`

Tries to parse the webhook's `id` and `token` from an `url`. If succeeds,
returns a partial webhook with only [`.id`](#inherited-instance-attributes)
and [`.token`](#token) set. The rest of the attributes will be set on
their default.

If the parsing fails, then returns `None`.

## Methods

- [`name_at`](UserBase.md#name_atselfguild)
- [`color_at`](UserBase.md#color_atselfguild)
- [`mentioned_in`](UserBase.md#mentioned_inselfmessage)
- [`has_role`](UserBase.md#has_roleselfrole)
- [`top_role_at`](UserBase.md#top_role_atself-guild-defaultnone)
- [`can_use_emoji`](UserBase.md#can_use_emojiself-emoji)
- [`has_higher_role_than`](UserBase.md#has_higher_role_thanself-role)
- [`has_higher_role_than_at`](UserBase.md#has_higher_role_than_atself-user-guild)

### `avatar_url_as(self,ext=None,size=None)`

- returns : `str`
- raises : `ValueError`

If the user webhook has no avatar, then it returns the blue default avatar.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

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

### `__new__(cls,data)` (magic method)

- returns : [`Webhook`](Webhook.md)

Tries to get the webhook from the existing ones, then update it. If the webhook
is not exising yet, then it will create a new one and fill it's attributes from
the data.

### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the webhook with the given data.

### `_delete` (method)

- returns : `None`

If requesting a [guild's](Guild.md) webhooks does not shows up webhook that
showed up before, this method gets called.

### `_from_follow_data(cls,data,source_channel,target_channel,client)` (classmethod)

- `awaitable`
- returns : [`Webhook`](Webhook.md)

Creates the webhook, what executes the cross messaging. This method is ensured
after requesting channel following.
