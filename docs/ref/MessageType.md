# class `MessageType`

Represents a [message](Message.md)'s type.

- Source : [message.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/message.py)

Each `MessageType` is stored in the classe's [`.INSTANCES`](#instances)
`list` class attribute, but they can also be accessed as `MessageType.<name>`.

## Instance attributes

### `convert`

- type : `function`

The converter function of the message type, what tries to convert the message's
content to it's Discord side representation.

These functions accept 1 argument, a [message](Message.md) object.

> `welcome` message's conversion is not working as expected (needs review).

> The conversion of `call` messages might not be accurate, because there
> can be more clients at the same channel, and these type of messages are
> different for each client's respective.

> `stream` message type is experimental and it's converter returns just an
> empty string.

## Class attributes

##### Predefined class attributes

| name                  | value     | converter                     |
|-----------------------|-----------|-------------------------------|
| default               | 0         | convert_default               |
| add_user              | 1         | convert_add_user              |
| remove_user           | 2         | convert_remove_user           |
| call                  | 3         | convert_call                  |
| channel_name_change   | 4         | convert_channel_name_change   |
| channel_icon_change   | 5         | convert_channel_icon_change   |
| new_pin               | 6         | convert_new_pin               |
| welcome               | 7         | convert_welcome               |
| new_guild_sub         | 8         | convert_new_guild_sub         |
| new_guild_sub_t1      | 9         | convert_new_guild_sub_t1      |
| new_guild_sub_t2      | 10        | convert_new_guild_sub_t2      |
| new_guild_sub_t3      | 11        | convert_new_guild_sub_t3      |
| new_follower_channel  | 12        | convert_new_follower_channel  |
| stream                | 13        | convert_stream                |

### `INSTANCES`

- type : `list`
- items : [`MessageType`](MessageType.md)

Stores the created [`MessageType`](MessageType.md) instances. This
container is accessed when translating a Discord message type's value to
it's representation.

## Magic methods

### `__init__(self,value,name)`

Creates a new [`MessageType`](MessageType.md) and stores it at the classe's
[`.INSTANCES`](#instances).

### `__str__(self)`

- returns : `str`

Returns the message type's name.

### `__int__(self)`

- returns : `int`

Returns the message type's value.

### `__repr__(self)`

- returns : `str`

Returns the representation of the message type.
