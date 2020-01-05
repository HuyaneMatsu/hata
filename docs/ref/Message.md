# class `Message`

- source : [message.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/message.py)

## Instance attributes

### `activity`

- type : [`MessageActivity`](MessageActivity.md) / `NoneType`
- default: `None`

Sent with "Rich presence" related embeds.

### `application`

- type : [`MessageApplication`](MessageApplication.md) / `NoneType`
- default : `None`

Sent with "Rich presence" related embeds.

### `attachments`

- type : `list` / `Nonetype`
- default : `None`
- elements : [`Attachment`](Attachment.md)

The attachments sent with the message, or `None` if none was sent.

### `author`

- type : [`User`](User.md) / [`Client`](Client.md) / [`Webhook`](Webhook.md) /
[`WebhookRepr`](WebhookRepr.md)
- default : [`ZEROUSER`](ZEROUSER.md)

The message's author. If a client runs up after a message is created with it
as author, then the author of the message wont be replaced with the
[Client](Client.md) object.

### `call`

- type : [`MessageCall`](MessageCall.md) / `NoneType`
- default : `None`

TODO or Deprecated.

### `channel`

- type : [`Channel`](CHANNEL_TYPES.md)

The channel where the message was sent.

### `content`

- type : `str`
- default: `''`

The message's content.

### `cross_mentions`

- type : `list` / `NoneType`
- default : `None`
- elements : [`Channel`](CHANNEL_TYPES.md) / [`UnknownCrossMention`](UnknownCrossMention.md)

A list if cross guild channel mentions of the message.
If the channel is not loaded by the wrapper, then it will represented with a 
[`UnknownCrossMention`](UnknownCrossMention.md) instance.
If there is non of them, it should be `None`.

### `cross_reference`

- type : [`MessageReference`](MessageReference.md) / `NoneType`
- default : `None`

If the message is sent from an another guild, this attribute should be set.

### `edited`

- type : `datetime` / `NoneType`
- default : `None`

The time when the message was edited. If it it was not, it is None.
If a message's pinned value changes, or it gets embed update, then `edited`
wont change.

### `embeds`

- type: `list` / `NoneType`
- default : `None`
- elements : [`EmbedCore`](EmbedCore.md)

A list of the embeds sent in the message.
If there are no embeds at the message, then None.
Links at a message can add embeds at end of the message, at that case the
embeds come only later and not with message itself.

### `everyone_mention`

- type : `bool`
- values : `True` / `False`

If the message contains @everyone or @here.

### `flags`

- type : [`MessageFlag`](MessageFlag.md)

The message's flags. Right now it is used only to mark, if the message's 
[`embeds`](#embeds) are suppressed or not.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)

The message's unique identificator number.

### `nonce`

- type : `int` / `str` / `NoneType`
- default : `None`
    
A nonce that is used for optimistic message sending. (?)

### `pinned`

- type : `bool
- values : `True` / `False`

If the message is pinned.

### `reactions`

- type : [`reaction_mapping`](reaction_mapping.md)

A dict like object, which contains the reactions on the message.

### `role_mentions`

- type : `list` / `Nonetype`
- default : `None`
- elements : [`Role`](Role.md)

The list of the mentioned roles at the message.
If the message has no role mentions, then None.

### `tts`

- type : `bool`
- values : `True` / `False`
- default : `False`

If the message is a "text to speech" message or not.

### `type`

- type : [`MessageType`](MessageType.md)
- default : `MessageType.default`

The type of the message.
Different events have different types.
For example a normal message's type is `MessageType.default`,
but if a user joins a [guild](Guild.md) the message type gonna be
`MessageType.new_member`.

### `user_mentions`

- type : `list` / `Nonetype`
- default : `None`
- elements : [`User`](User.md) / [`Client`](Client.md) / [`Webhook`](Webhook.md)

The list of the mentioned users with the message. If there are no mentioned
users, then `None`

## Properties

### `channel_mentions`

- returns : `list` / `NoneType`
- default : `None`
- elements : [`Channel`](CHANNEL_TYPES.md) / [`UnknownCrossMention`](UnknownCrossMention.md)

Cached property with
[`._channel_mentions`](#_channel_mentions-instance-attribute) instance
attribute. Returns the list of the mentioned channels at the message, or `None`
 if none.

### `clean_content`

- returns : `str`

Returns them message's clean content, what actually depends on the message's
type. By default it is the message's content with transformed mentions, but
for differnt message types it means different things. The converting can not
display join messages, call mesages and private channel names correctly.

### `clean_embeds`

- returns : `list`
- elements : [`EmbedCore`](EmbedCore.md)

Returns the message's embeds (which are not links) with converted content
 without mentions. (Does not changes the content of the original
embeds).

### `contents`

- returns : `list`
- values : `str`

A list of all of the contents sent in the message. It means the message's
content, the content of the embeds and the content of embeds' subparts too.

### `created_at`

- returns : `datetime`

The creation time of the message.

### `could_suppress_embeds`

- returns : `int`
- default : `0`

Returns the amount of [`embeds`](EmbedCore.md), which could be suppressed.
If a message's embeds are suppressed, they cannot be suppressed, but the
message can still have embed, that is why the *could* and not *can*.

### `guild`

- returns : [`Guild`](Guild.md) / `NoneType`
- default : `None`

Returns the message's channel's guild if applicable.

### `mentions`

- returns : `list`
- elements :
    - `None`
    - [`User`](User.md)
    - [`Client`](Client.md)
    - [`Webhook`](Webhook.md)
    - [`Roles`](Role.md)
    - [`Channel`](CHANNEL_TYPES.md)
    - [`UnknownCrossMention`](UnknownCrossMention.md)

Returns a list of all the mentions sent at the message.
If the message mentions everyone too, the list ll contain `None`.

## Methods

### `did_react(self,emoji,user)`

- returns : `bool`
- values : `True` / `False`

Returns if the [`user`](User.md) reacted with the given
[`emoji`](Emoji.md) on the message.
                       
### `weakrefer(self)`

Puts the message into `MESSAGES` `WeakValueDictionary`. If any event is
dispatched, which refers to a message, then after looking up the channel's
messages, gonna check if the message is at `MESSAGES`.

## Class methods

### `custom(cls,base=None,validate=True,**kwargs)`

- returns : [`Message`](Message.md)
- raises : `TypeError` / `ValueError`

Creates a custom message with the given `kwargs`. If any of the passed types
are incorrect, `TypeError` will be raised.

If `base` (type [`Message`](Message.md)) is passed, then it will use it's
attributes as default ones, else it will use the "real default" values as
default ones.

If `validate` is set as `True`, then the method will check if the message has any 
contradicotry between it's attributes. If it has, `ValueError` will be raised.

Kwargs can be:

| name              | aliases           | default                                       | expected values                                                                                                           | alternative values and conversions                    |
|-------------------|-------------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| activity          |                   | None                                          | None / [MessageActivity](MessageActivity.md)                                                                              |                                                       |
| application       |                   | None                                          | None / [MessageApplication](MessageApplication.md)                                                                        |                                                       |
| attachments       |                   | None                                          | None / list of [Attachment](Attachment.md)                                                                                | [ ] -> None                                           |
| author            |                   | [ZEROUSER](ZEROUSER.md)                       | [Client](Client.md) / [User](User.md) / [Webhook](Webhook.md) / [WebhookRepr](WebhookRepr.md)                             | None -> [ZEROUSER](ZEROUSER.md)                       |
| call              |                   | None                                          | None / [MessageCall](MessageCall.md)                                                                                      |                                                       |
| channel           |                   |                                               | [ChannelTextBase](ChannelTextBase.md) subclass instance                                                                   |                                                       |
| content           |                   | ''                                            | str                                                                                                                       |                                                       |
| cross_mentions    |                   | None                                          | None / list of ([ChannelGuildBase](ChannelGuildBase.md) subclass instance / [UnknownCrossMention](UnknownCrossMention.md))| [ ] -> None                                           |
| cross_reference   |                   | None                                          | None / [MessageReference](MessageReference.md)                                                                            |                                                       |
| edited            |                   | None                                          | None / datetime                                                                                                           |                                                       |
| embeds            |                   | None                                          | None / list of [EmbedCore](EmbedCore.md)                                                                                  | Embed compatible -> [EmbedCore](EmbedCore.md)         |
| everyone_mention  |                   | False                                         | bool                                                                                                                      | 0 / 1 -> bool                                         |
| flags             |                   | [MessageFlag(0)](MessageFlag.md)              | [MessageFlag](MessageFlag.md)                                                                                             | int -> [MessageFlag](MessageFlag.md)                  |
| id                | id_, message_id   | 0                                             | int (uint64)                                                                                                              |                                                       |
| nonce             |                   | None                                          | None / str / int                                                                                                          |                                                       |
| pinned            |                   | False                                         | bool                                                                                                                      | 0 / 1 -> bool                                         |
| reactions         |                   | [reaction_mapping(None)](reaction_mapping.md) | [reaction_mapping](reaction_mapping.md)                                                                                   | None -> [reaction_mapping(None)](reaction_mapping.md) |
| role_mentions     |                   | None                                          | None / list of [Role](Role.md)                                                                                            | [ ] -> None                                           |
| tts               |                   | False                                         | bool                                                                                                                      | 0 / 1 -> bool                                         |
| type              | type_             | [MessageType.default](MessageType.md)         | [MessageType](MessageType.md)                                                                                             | int -> [MessageType](MessageType.md)                  |
| user_mentions     |                   | None                                          | None / list of ([Client](Client.md) / [User](User.md) )                                                                   | [ ] -> None                                           |

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

A message's hash value is equal to it's id.

### `__repr__(self)`

- returns : `str`

Returns the representation of the message.

### `__format__(self,code)`

- returns : `str`
- raises : `ValueError`

```python
f'{message}' #-> repr(message)
f'{message:c}' #-> message.created_at with '%Y.%m.%d-%H:%M:%S' format
f'{message:e}' #-> user.edited with '%Y.%m.%d-%H:%M:%S' format / "never"
```

Raises `ValueError` on invalid format code.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two message's id.

### `__len__(self)`

- returns : `int`

Returns the cumultative length of all the content of the message.

## Internal

### `_channel_mentions` (instance attribute)

- type : `NoneType` / `list`
- default : unset
- values : [`Channels`](CHANNEL_TYPES.md) / [`UnknownCrossMention`](UnknownCrossMention.md)

Cached slot for [`channel_mentions`](#channel_mentions) property. If the
property was never called, this value is unset. After calling the property,
this value can become `None` of list of [`Channel objects`](CHANNEL_TYPES.md),
depends if the message contains non or any channel mentions. After a message
gets an update event, then this value is reseted to unset.

### `new(cls,data,channel)` (classmethod)

- returns : [`Message`](Message.md)

Creates a new empty Message object with only id, then checks if the message 
already exists. If it does returns that message, if not, then finishes the
message's initialization.

### `old(cls,data,channel)` (classmethod)

- returns : [`Message`](Message.md)

Same as `new` but for old messages. Used if we request older messages, which can
be chained with our message history's end.

### `fromchannel(cls,data,channel)` (classmethod)

- returns : [`Message`](Message.md)

Check if the message is already loaded, if yes, then returns the already existing
one. If not, then creates a new one, but this method does not adds it to the 
channel's history, because we dont actually know, where to put it.

### `exists(cls,data,channel)` (classmethod)

- returns : (`True` / `False`) , [`Message`](Message.md)

Same as [`.fromchannel`](#fromchannelclsdatachannel-classmethod), but if it
found the message, returns an additional `True`, if not, then `False`.

### `onetime(cls,data,channel)` (classmethod)

- returns : [`Message`](Message.md)

Creates a message, then returns it, with no extra operations.

### `_finish_init(self,data,channel):` (method)

- returns : `None`

This function replaces `Message.__init__`. Sets every attribute of the message,
except the [`id`](#id), because id is set at 1 of the constructors, and except
[`_channel_mentions`](#_channel_mentions-instance-attribute) instance
attribute, because thats set if the [`channel_mentions`](#channel_mentions)
property is used.

### `_parse_channel_mentions(self)` (method)
    
- returns : `None`

Looks up [every content](#contents) of the message, and searcher for channel
mentions. If found zero, then sets
[`_channel_mentions`](#_channel_mentions-instance-attribute) to `None`, if any,
then sets it to the list of the mentioned channels. Invalid channel mentions
are ignored.

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the message and returns it's old attribtes with (`attribute name`,
`old value`) items. Resets
[`_channel_mentions`](#_channel_mentions-instance-attribute) to unset.
A special case is if a message is (un)pinned or (un)suppressed , because then
the returned dict is not going to contain `'edited'`, only `'pinned'` or
`flags`.

| name                      | description                                                                                   |
|---------------------------|-----------------------------------------------------------------------------------------------|
| activity                  | Nne / [MessageActivity](MessageActivity.md)                                                   |
| application               | None /[MessageApplication](MessageApplication.md)                                             |
| content                   | str                                                                                           |
| cross_mentions            | None / (list of [Channel](CHANNEL_TYPES.md) / [UnknownCrossMention](UnknownCrossMention.md))  |
| edited                    | None / datetime                                                                               |
| embeds                    | list of [EmbedCore](EmbedCore.md)                                                             |
| flags                     | [MessageFlag](MessageFlag.md)                                                                 |
| mention_everyone          | bool                                                                                          |
| pinned                    | bool                                                                                          |
| user_mentions             | None / (list of [User](User.md)) / [lient](Client.md))                                        |
| role_mentions             | None / (list of [Role](Role.md))                                                              |

### `_update_no_return(self,data)` (method)
    
- returns : `None`

Updates the message, replacing it's attributes and reseting
[`_channel_mentions`](#_channel_mentions-instance-attribute) to unset.
    
### `_update_embed(self,data)` (method)

- returns : `int`
- values : `0`, `1`, `2`, `3`

After getting a message, it's embeds might be updated from links, or with image,
video sizes. If it happens this method is called. Returns:
 - `0` if no update took place.
 - `1` if sizes are updated.
 - `2` if embed links are added
 - `3` if the message's embeds are suppressed, but an unsuppressed embed is
added to it. Discord bug, happens when you update an embed, what is
suppressed, but instead of desuppressing and updating, it removes the old embeds
and adds new one to it. The message's flag will still show that the it's embeds
are suppressed.

### `_update_embed_no_return(self,data)` (method)

- returns : `None`

Updates the message's embeds and returns `None`.
