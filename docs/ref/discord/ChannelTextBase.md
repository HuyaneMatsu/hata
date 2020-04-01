# class `ChannelTextBase`

The superclass of all messageable channel types.

- Source : [channel.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/channel.py)

Check [`CHANNEL_TYPES`](CHANNEL_TYPES.md) for more channel type related info.

## Subclasses

- [`ChannelText`](ChannelText.md)
- [`ChannelPrivate`](ChannelPrivate.md)
- [`ChannelGroup`](ChannelGroup.md)

## Instance attributes

This class cannot implement instance attributes, because its is only the second
inherited base class, but every subclass of it implements the following 
instance attributes:

### `message_history_reached_end`

- type : `bool`
- values : `True` / `False`
- default : `False`

Tells if all the [messages](Message.md) are loaded at the channel. If they are 
`message_history_reached_end` is set to `True` and no more requests will be
executed on requesting older [messages](Message.md).

### `messages`

- type : [`deque`](https://docs.python.org/3/library/collections.html#collections.deque)
- elements : [`Message`](Message.md)

A `deque` of the messages stored from the channel. The deque's maximal
lenght by default is same as [`MC_GC_LIMIT`](ChannelTextBase.md#mc_gc_limit)
defined at [`ChannelTextBase`](ChannelTextBase.md). Or it can be
changed locally with the
[`mc_gc_limit`](ChannelTextBase.md#mc_gc_limit-getset) property.

## Class attributes

### `MC_GC_LIMIT`

The default limit of the kept messages at a channel. If there are requests to
older messages, then the channel's history turns into unlimited and ignores
this limit.

## Properties

### `mc_gc_limit` (get/set)

- returns : `int`
- accepts : `int`

Allows to modify the channel's message limit without touching the default one.

## Internal

### `_mc_init(channel)` (method)

- returns : `None`

Sets the default values specific to text channels. These are the following:
    
- `message_history_reached_end`, is set to `True` if all the messages of the
channel loaded, and if they are, then we wont request anymore messages of the
channel.
- `turn_GC_on_at`, if the channel's message history's limit passed the default
amount, then it will have a time when we ll turn back the length limitation of
the messages. This time depends how much times and how old messages we request
from the channel.
- `messages`, a `deque` contains the messages of the channel.

### `_mc_find(channel,message_id)` (method)

- returns : [`Message`](Message.md) / `NoneType`
- default : `None`

Tries to find the message by it's `id` at the history of the channel. If it finds
the message returns it, else returns `None`.

### `_mc_insert_new_message(channel,message)` (method)

- returns : [`Message`](Message.md)

The inputted message should be a partial message object only with an `id`
attribute. If the channel's most recent message is older, then it returns the
new message, if they are the same, returns the already existing one. If the new
message is not so now, then it tries to find the message at the loaded messages
of the channel. If it does fidns it returns it, else returns the new message.
This method is used when we create a new message. if we find the message
between the already loaded ones we save a message initialization.

### `_mc_insert_old_message(channel,message)` (method)

- returns : [`Message`](Message.md)

Similar to
[`._mc_insert_new_message`](#_mc_insert_new_messagechannelmessage-method),
but it tries to find the message between the oldest message of the channel
instead.

### `_mc_insert_asynced_message(channel,message)` (method)

- returns : [`Message`](Message.md)

This method gets caled if
[`._mc_insert_new_message`](#_mc_insert_new_messagechannelmessage-method)
sees that the message is older than it's first one, or if
[`._mc_insert_old_message`](#_mc_insert_old_messagechannelmessage-method)
sees that the message is newer than it's last. As the method's name says,
it tries to find the message by it's  `id` and insert to the right place
if not exists. If it exists returns the found one.

### `_mc_pop(channel,message_id)` (method)

- returns : [`Message`](Message.md) / `NoneType`
- default : `None`

Called when we parse a `message_delete` event. If the message is found removes
it from the channel's message history and returns it. If it cant, returns `None`.

### `_mc_pop_multiple(channel,message_ids)` (method)

- returns : `list`
- elements : [`Message`](Message.md)

Familiar to [`._mc_pop`](#_mc_popchannelmessage_id-method),
but it tries to find and pop more message ids. It is called at parsing
`message_delete_multiple` event. 

### `_mc_process_chunk(channel,data)` (method)

- returns : `list`
- elemnts : [`Message`](Message.md)

Called when we request older messages of the channel. It checks if we can chain
the messages to the channel's history. If we can it chains them and removes the
length limitation too if needed. When the method is done returns a `list` of the
created [`messages`](Message.md).

### `_mc_generator(channel,after,before,limit)` (method)

- yields : [`Message`](Message.md)

A generator, wich realizes an api request from the already loaded messages of
the channel.




