# class `WebhookRepr`

Represents a Discord webhook's user representation.

- Source : [webhook.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/webhook.py)

## Familiar types

- [Webhook](Webhook.md)
- [User](User.md)
- [Client](Client.md)
- [UserOA2](UserOA2.md)

## Superclasses

- [`UserBase`](UserBase.md)

## Instance attributes

##### Inherited instance attributes

- [`id`](UserBase.md#id)
- [`name`](UserBase.md#name)
- [`discriminator`](UserBase.md#discriminator)
- [`avatar`](UserBase.md#avatar)
- [`has_animated_avatar`](UserBase.md#has_animated_avatar)

### `type`

- type : [`WebhookType`](WebhookType.md)

The representation's webhook's type.

## Properties

##### Inherited properties

- [`activity`](UserBase.md#activity)
- [`avatar_url`](UserBase.md#avatar_url)
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

### `is_bot`

- returns : `bool`
- values : `True`

Webhooks are always bots.

### `partial`

- returns : `bool`
- values : `False`

[`WebhookRepr`](WebhookRepr.md)-s are always full users.

### `webhook`

- returns : [`Webhook`](Webhook.md)

Returns the webhook of the [`WebhookRepr`](WebhookRepr.md). This webhook is
always partial and has only it's `.id` set.

## Methods

- [`avatar_url_as`](UserBase.md#avatar_url_asselfextnonesizenone)
- [`name_at`](UserBase.md#name_atselfguild)
- [`mention_at`](UserBase.md#mention_atselfguild)
- [`color`](UserBase.md#colorselfguild)
- [`mentioned_in`](UserBase.md#mentioned_inselfmessage)

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

### `__init__(self,data,webhook_id,type_)` (magic method)

Creates a [`WebhookRepr`](WebhookRepr.md) from the given data and from the
[webhook](Webhook.md)'s id.
