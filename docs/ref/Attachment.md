# class `Attachment`

Represents an attachemnt of a [message](Message.md)

- Source : [message.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/message.py)

## Instance attributes

### `height`

- type : `int`
- default : `0`

The height of the attachment. This attribute might not be sent by Discord.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The attachment's unique identificator number.

### `name`

- type : `str`

The attachment's name.

### `proxy_url`

A proxied url of the attachment via Discord's content delivery network.

### `size`

- type : `int`

The attachment's size in bytes.

### `url`

- type : `str`

The attachment's url.

### `width`

- type : `int`
- default : `0`

The width of the attachment. This attribute might not be sent by Discord.

## Properties

### `created_at`

- returns : `datetime`

The creation time of the attachment.

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

An attachment's hash value is equal to it's id.

### `__repr__(self)`

- returns : `str`

Returns the representation of the attachment.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two attachment's id.

## Internal

### `__init__(self,data)` (magic method)

Creates an attachment object from the data sent by Discord.
