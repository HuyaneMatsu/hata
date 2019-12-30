# class `MessageActivity`

Might be sent with a [message](Message.md), if it has Rich Presence-related
chat embeds.

- Source : [message.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/message.py)

## Instance attributes

### `party_id`

- type : `str`
- default : `''` (empty string)

The message application's party's id.

### `type`

- type : [`MessageActivityType`](MessageActivityType.md)

The message activity's type.

## Magic Methods

### `__eq__(self,other)`

Compares the two message activity.

### `__repr__(self)`

- returns : `str`

Returns the representation of the message activity.

## Internal

### `__init__(self,data)` (magic method)

Creates a new [`MessageActivity`](MessageActivity.md) from the data sent by
Discord.
