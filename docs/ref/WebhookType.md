# class `WebhookType`

Represents a [webhook's](Webhook.md) type. [`WebhookRepr`](WebhookRepr.md)
objects also have a `.type` attribute included.

- Source : [webhook.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/webhook.py)

Each webhook type is stored in the classe's [`.INSTANCES`](#instances)
`list` class attribute, with [`WebhookType`](WebhookType.md)
elements. But they can also be accessed as `WebhookType.<name>`.

## Instance attributes

| name      | type      |
|-----------|-----------|
| name      | str       |
| value     | int       |

## Class attributes

##### Predefined class attributes

There are 2 (+1:placeholder) webhook types :

| name              | value     |
|-------------------|-----------|
| NONE              | 0         |
| BOT               | 1         |
| SERVER            | 2         |

> The `NONE` webhook type is just a placeholder for type `0`.
> Discord does not uses it.

### `INSTANCES`

- type : `list`
- elements : [`WebhookType`](WebhookType.md)

Stores the created [`WebhookType`](WebhookType.md) instances. This
container is accessed when translating a Discord webhook type's value to
it's representation.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`WebhookType`](WebhookType.md) and stores it at the
classe's [`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the webhook type's name.

### `__int__(self)`

- returns : `int`

Returns the webhook type's value.

### `__repr__(self)`

- returns : `str`

Returns the webhook type's representation.
