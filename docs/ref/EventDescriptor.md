# class `EventDescriptor`

After we get a dispatch event from Discord, it's parser might ensure an
event. These events are stored as instance attributes at an
`EventDescriptor` objects. All of these events should return an
awaitable object.

- Source : [parsers.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/parsers.py)

## All method

### `__init__(self, client)`

`EventDescriptor` is created at `Client.__init__` with a weakreference to it'
 client.

### `__call__(self,func=None,name=None,pass_content=False,sub_name=None,overwrite=False)`

- returns : `callable`

The main reason why we can use `EventDescriptor` with `@` is of cource
it is the `__call__` method. But this method does way more as you would
suspect on first look.

Additionally this method returns the added object on success.

### `clear(self)`

- returns : `None`

Cleares the `EventDescriptor`, to the same state as it were just created.

#### First case:

The general usage is when you add just an event:

```py
async def coroutine_function(self,*args):
    pass

client.events(coroutine_function)

# is same as

@client.events
async def coroutine_function(self,*args):
    pass

# even this works:

@client.events()
async def coroutine_function(self,*args):
    pass

# if you add more events, all will be called, except if you pass `overwrite`
# as True, because at that case the old one will be replaced.

@client.events(overwrite=True)
async def coroutine_function(self,*args):
    pass
```

If you add a coroutine function it will get the event's name by default.
If the name is incorrect raises an exception as expected. Then will check
how much arguments the parser passes when the event is called. If the
argument number is incorrect will raise an exception too. If your function
accepts `*args`, then argument count will be ignored as expected.

But actually you dont really need to pass a `coroutine function`, It can
be a callable object too with async `__call__`. If the object has
`__async_call__` attribute, then even the async check will be ignored.
It is a usefull option, if you just want to return an awaitable.

But you can even pass just a `type` instance itself too, at that case
every check is same as above, but a difference is, that it will initialize
it.

#### Second case:

When you pass a name:
    
```py
@client.events(name='gift_update')
async def coroutine_function(self,*args):
    pass

# Or you can do:
client.events(coroutine_function, name='example')
```

At this case instead of checking the object's name it will use the passed
name instead. But there are other ways too, to pass name. One of them if
you pass an object with a `__name__` (function name check mimic) instance
attribute, or when you pass an object with an `__event_name__` attribute.

#### Third case:

When you pass a `pass_to_hanler=True` and an optional `sub_name`.

```py
client.events(coroutine_function, name='example', pass_to_handler=True)
client.events(coroutine_function, name='example', pass_to_handler=True, sub_name='owo')
```

At these cases instead of setting an event to the `client.events` it will
call:

```py
client.event.<name>.__setevent__(func, name)
```

If `sub_name` is `None` it will try to get the sub name on the same way as we
get the `name` above.

Using this option we can get an additional `ValueError` if we did not pass
a `name` argument or an `AttributeError` if the event is not implemented
yet or if it has no `__setevent__` method.

## Events

Additional information:
- All item in `old` arguements is optional, but it contains at least one.
- All event is called as method from the [client](Client.md), so the client is
always passed as first argument.

### `achievement(client,data)`

Called when one of the [client](Client.md)'s [achievement](Achievement.md)
changes. Because I cannot reproduce this event, it just passes the data
sent by Discord.

### `channel_create(client,channel)`

Called when a [channel](CHANNEL_TYPES.md) is created.

> Private channels are created only once too.

### `channel_delete(client,channel)`

Called when a [channel](CHANNEL_TYPES.md) is deleted.

### `channel_edit(client,channel,old)`

Called when a [channel](CHANNEL_TYPES.md) is edited. The `old` argument is a `dict`
of the changed attributes what contains (`attribute name`, `old value`) items.

| name                      | description                                               |
|---------------------------|-----------------------------------------------------------|
| bitrate                   | int                                                       |
| category                  | [Guild](Guild.md) / [ChannelCategory](ChannelCategory.md) |
| icon                      | int                                                       |
| name                      | str                                                       |
| nsfw                      | bool                                                      |
| overwrites                | list of [PermOW](PermOW.md)                               |
| owner                     | [User](User.md) / [Client](Client.md)                     |
| position                  | int                                                       |
| slowmode                  | int                                                       |
| topic                     | str                                                       |
| type                      | int                                                       |
| user_limit                | int                                                       |
| users                     | list of [User](User.md) / [Client](Client.md)             |

### `channel_group_user_add(client,channel,user)`

Called when a [`User`](User.md) is added to a [group channel](ChannelGroup.md).

### `channel_group_user_delete(client,channel,user)`

Called when a [`User`](User.md) is removed from a [group channel](ChannelGroup.md).

### `channel_pin_update(client,channel)`

Called when a pin is added or removed at a channel.

### `client_edit(client,old)`

Called when the  client is edited. If you edit yourself, you should not receive
this event. The `old` argument is a `dict` of the changed attributes, what
contains (`attribute name`, `old value`) items.

| name                      | description                       |
|---------------------------|-----------------------------------|
| avatar                    | int                               |
| discriminator             | int                               |
| email                     | str                               |
| flags                     | [UserFlag](UserFlag.md)           |
| has_animated_avatar       | bool                              |
| locale                    | str                               |
| mfa                       | bool                              |
| name                      | str                               |
| premium_type              | [PremiumType](PremiumType.md)     |
| verified                  | bool                              |

### `client_edit_settings(client,old)`

Called when the client's settings are edited. The `old` argument is a `dict`
of the changed attributes, what contains (`attribute name`, `old value`) items.

| name                      | description                                       |
|---------------------------|---------------------------------------------------|
| accessibility_detection   | bool                                              |
| afk_timeout               | int                                               |
| animate_emojis            | bool                                              |
| compact_mode              | bool                                              |
| content_filter            | [ContentFilterLevel](ContentFilterLevel.md)       |
| convert_emojis            | bool                                              |
| custom_status             | dict / None                                       |
| detect_platform_accounts  | bool                                              |
| developer_mode            | bool                                              |
| enable_tts_command        | bool                                              |
| friend_request_flag       | [FriendRequestFlag](FriendRequestFlag.md)         |
| games_tab                 | bool                                              |
| guild_folders             | list of GuildFolder                               |
| guild_order_ids           | list of int                                       |
| locale                    | str                                               |
| no_DM_from_new_guilds     | bool                                              |
| no_DM_guild_ids           | list of int                                       |
| gif_auto_play             | bool                                              |
| render_attachments        | bool                                              |
| render_embeds             | bool                                              |
| render_links              | bool                                              |
| render_reactions          | bool                                              |
| show_current_game         | bool                                              |
| status                    | [Status](Status.md)                               |
| stream_notifications      | bool                                              |
| theme                     | [Theme](Theme.md)                                 |
| timezone_offset           | int                                               |

###### `custom_status` structure

| key           | value                         | default   |
|---------------|-------------------------------|-----------|
| text          | `str` / `None`                | `None`    |
| expires_at    | `datetime` / `None`           | `None`    |
| emoji         | [`Emoji`](Emoji.md) / `None`  | `None`    |

### `embed_update(client,message,result)`

Called when only a [message](Message.md)'s embeds are updated and the message
is not edited.

The `result` can be:
 - `1` if sizes are updated.
 - `2` if embed links are added.
 - `3` the amount of the embeds is lowered. Should be caused only by a bug.

### `emoji_create(client,guild,emoji)`

Called, when an [emoji](Emoji.md) is created at a [guild](Guild.md).

### `emoji_delete(client,guild,emoji)`

Called, when an [emoji](Emoji.md) is deleted at a [guild](Guild.md).

> Deleted emojis's [`.guild`](Emoji.md#guild) attribute is set to `None`.

### `emoji_edit(client,guild,emoji,old)`

Called when an [emoji](Emoji.md) is edited. The `old` argument is a `dict`
of the changed attributes, what contains (`attribute name`, `old value`) items.

| name                      | description                   |
|---------------------------|-------------------------------|
| animated                  | bool                          |
| available                 | bool                          |
| managed                   | bool                          |
| name                      | str                           |
| require_colons            | bool                          |
| roles                     | set of [Role](Role.md) / None |

> If an [emoji](Emoji.md) is upated it's `.user` instance attribute might be
> set too.

### `error(client,event,err)`

Called when an unexpected error happens. Mostly the user itself should define
where it is called, because it is not Discord event bound, but an internal
event.

The `event` argument should be a `str` what tell where the error occured,
and `err` should be an `Exception` or an error message (so preferably `str`).

This event has a default dispatcher called `default_error_event`, what
writes an error message to `file=sys.stderr`.

### `gift_update(client,channel,gift)`

Called when a [gift](Gift.md) code is sent to a [channel](CHANNEL_TYPES.md)
what the client sees.

### `guild_ban_add(client,guild,user)`

Called when a [user](User.md) is banned from a [guild](Guild.md).

### `guild_ban_delete(client,guild,user)`

Called when a [user](User.md) is unbanned at a [guild](Guild.md).

### `guild_create(client,guild)`

Called when the [client](Client.md) joins or creates a [guild](Guild.md).

### `guild_delete(client,guild,profile)`

Called when the [guild](Guild.md) is deleted or just the [client](Client.md)
left (got kicked or banned too) from it. The `profile` is the
[`GuildProfile`](GuildProfile.md) of the client there.

### `guild_edit(client,guild,old)`

Called when a [guild](Guild.md) is edited. The `old` argument is a `dict`
of the changed attributes, what contains (`attribute name`, `old value`) items.

| name                      | description                                               |
|---------------------------|-----------------------------------------------------------|
| afk_channel               | [ChannelVoice](ChannelVoice.md) / None                    |
| afk_timeout               | int                                                       |
| available                 | bool                                                      |
| banner                    | int                                                       |
| booster_count             | int                                                       |
| content_filter            | [ContentFilterLevel](ContentFilterLevel.md)               |
| description               | str / None                                                |
| embed_channel             | [ChannelText](ChannelText.md) / None                      |
| embed_enabled             | bool                                                      |
| features                  | list of [GuildFeature](GuildFeature.md)                   |
| has_animated_icon         | bool                                                      |
| icon                      | int                                                       |
| max_presences             | int                                                       |
| max_users                 | int                                                       |
| message_notification      | [MessageNotificationLevel](MessageNotificationLevel.md)   |
| mfa                       | [MFA](MFA.md)                                             |
| name                      | str                                                       |
| owner                     | [User](User.md) / [Client](Client.md)                     |
| preferred_locale          | str                                                       |
| premium_tier              | int                                                       |
| public_updates_channel    | [ChannelText](ChannelText.md) / None                      |
| region                    | [VoiceRegion](VoiceRegion.md)                             |
| splash                    | int                                                       |
| system_channel            | [ChannelText](ChannelText.md) / None                      |
| system_channel_flags      | [SystemChannelFlag](SystemChannelFlag.md)                 |
| vanity_code               | str / None                                                |
| verification_level        | [VerificationLevel](VerificationLevel.md)                 |
| widget_channel            | [ChannelText](ChannelText.md) / None                      |
| widget_enabled            | bool                                                      |

### `guild_user_add(client,guild,user)`

Called when a [User](User.md) joins a [guild](Guild.md).

### `guild_user_chunk(client,guild,collected)`

Called when a chunk of [users](User.md) is received from a [guild](Guild.md).
Used only at the case of `large` guilds. Also this event plays a big role when
logging in, because it delays the ready state, till we get all the user chunks.

This event has a default dispatcher called `ChunkQueue`. Overwriting it is
not recommended.

### `guild_user_delete(client,guild,user,profile)`

Called when a [User](User.md) left (kick and ban counts too) from [guild](Guild.md).
The `profile` is the [`GuildProfile`](GuildProfile.md) of the user at guild.

### `integration_update(client,guild)`

Called when an [integration](Integration.md) of a [guild](Guild.md) is updated.
Sadly Discord does not sends details, so we pass only the guild as argument.

### `invite_create(client,invite)`

Called when an [invite](Invite.md) is created.

### `invite_delete(client,invite)`

Called when an [invite](Invite.md) is deleted.

### `message_create(client,message)`

Called when a [message](Message.md) is sent at any of the [client](Client.md)'s
[text channels](ChannelTextBase.md).

### `message_delete(client,message)`

Called when a loaded [message](Message.md) is deleted.

### `message_delete_multyple(client,channel,messages,message_ids)`

Called when more [messages](Message.md) are delete at once at a
[text channel](ChannelTextBase.md). The `messages` argument is a list of the
loaded messages, which were found and the `message_ids` argument is a list of
all the message's id-s, independently if they were loaded or not.

### `message_edit(client,message,old)`

Called when a loaded [message](Message.md) is edited. The `old` argument is a
`dict` of the changed attributes, what contains (`attribute name`, `old value`)
items. A special case is if a message is (un)pinned or (un)suppressed , because
then the `old` is not going to contain `'edited'`, only `'pinned'` or `flags`.
If the embeds are (un)suppressed of the message, then `old` might contain also
`'embeds'`.

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

### `reaction_add(client,message,emoji,user)`

Called when a [User](User.md) reacts on a [messages](Message.md) with and
[emoji](Emoji.md).

### `reaction_clear(client,message,old_reactions)`

Called when the (reactions)[reaction_mapping.md] are cleared from a
[messages](Message.md).

### `reaction_delete(client,message,emoji,user)`

Called when a [user](User.md)'s [reaction](Emoji.md) is removed from a
[messages](Message.md).

### `reaction_delete_emoji(client,message,emoji,users)`

Called when all the [reaction](Emoji.md) of a specific emoji are removed from a
[messages](Message.md). `users` is passed as a
[`reaction_mapping_line`](reaction_mapping_line.md) instance.

### `ready(client)`

Called when the client finishes logging in. This event can be called more
times, because we might disconnect or Discord might ask us to reconnect as
well.

### `relationship_add(client,new_relationship)`

Called when the [client](Client.md) gets a [relationship](Relationship.md)
independently to it's type.

### `relationship_change(client,old_relationship,new_relationship)`

Called when one of the [client](Client.md)'s [relationship](Relationship.md)
changes.

### `relationship_delete(client,old_relationship)`

Called when one of the [client](Client.md)'s [relationship](Relationship.md)
is removed.

### `role_create(client,role)`

Called when a [role](Role.md) is created at a [guild](Guild.md).

### `role_delete(client,role)`

Called when a [role](Role.md) is deleted at a [guild](Guild.md).

### `role_edit(client,role,old)`

Called when a [role](Role.md) is edited at a [guild](Guild.md). The `old`
argument is a `dict` of the changed attributes, what contains
(`attribute name`, `old value`) items.

| name                      | description                   |
|---------------------------|-------------------------------|
| color                     | [Color](Color.md)             |
| managed                   | bool                          |
| mentionable               | bool                          |
| name                      | str                           |
| permissions               | [Permission](Permission.md)   |
| position                  | int                           |
| separated                 | bool                          |

### `typing(client,channel,user,timestamp)`

Called if a [user](User.md) is typing at a
[channel](ChannelTextBase.md). `timestamp` argument is a `datetime`
object when the typing started to happen.

However a typing request stands for 8 seconds of typing, official Discord
clients DO NOT WAIT till that 8 seconds is about to pass, they just spam it.

### `user_edit(client,user,old)`

Called when a [user](User.md) is edited. This event does not includes
[GuildProfile](GuildProfile.md) changes. The `old` argument is a `dict` of
the changed attributes, what contains (`attribute name`, `old value`) items.

| name                      | description                       |
|---------------------------|-----------------------------------|
| avatar                    | int                               |
| discriminator             | int                               |
| has_animated_avatar       | bool                              |
| name                      | str                               |

### `user_presence_update(client,user,old)`

Called when a [user](User.md)'s presence is updated.

| name                      | description                                   |
|---------------------------|-----------------------------------------------|
| status                    | Status                                        |
| statuses                  | dict of (str, str) items                      |
| activities                | list of ([activity](ACTIVITY_TYPES.md) / dict)|

If an [activity](ACTIVITY_TYPES.md) is removed, then thats passed in the
`activities` list, but if the activity is updated, then there is an again
an `old` dict, what has 1 fix item: `('activity', activity)` to tell, which
activity got update.

| name                      | description                       |
|---------------------------|-----------------------------------|
| application_id            | int                               |
| asset_image_large         | str                               |
| asset_image_small         | str                               |
| asset_text_large          | str                               |
| asset_text_small          | str                               |
| created                   | int                               |
| details                   | str                               |
| emoji                     | [Emoji](Emoji.md) / None          |
| flags                     | [ActivityFlag](ActivityFlag.md)   |
| id                        | int                               |
| name                      | str                               |
| party_id                  | str                               |
| party_max                 | int                               |
| party_size                | int                               |
| secret_join               | str                               |
| secret_match              | str                               |
| secret_spectate           | str                               |
| session_id                | str                               |
| state                     | str / None                        |
| sync_id                   | str                               |
| timestamp_end             | int                               |
| timestamp_start           | int                               |
| type                      | int                               |
| url                       | str                               |

### `user_profile_edit(client,user,old,guild)`

Called when a [user](User.md)'s [GuildProfile](GuildProfile.md) is edited.  at a
[guild](Guild.md). The `old` argument is a `dict` of the changed attributes,
what contains (`attribute name`, `old value`) items.

Not like at other cases, this event updates not only
[GuildProfile](GuildProfile.md) attributes.

| name                      | description               |
|---------------------------|---------------------------|
| nick                      | str / None                |
| roles                     | list of [Role](Role.md)   |
| boosts_since              | datetime / None           |

### `voice_state_update(client,state,action,old)`

Called when a [voice state](VoiceState.md) is updated a
[voice channel](ChannelVoice.md). The `action` argument can be `l` if a
[user](User.md) `left` from the guild's channels (or got removed), `j` if the
user just `joined`, or `u` if the voice state was `updated`. `old` is passed
as `None` every time if it is not an `update`, anyways it is a `dict` what
contains the changed attributes with (`attribute name`, `old value`) items.

| name                      | description                       |
|---------------------------|-----------------------------------|
| channel                   | [ChannelVoice](ChannelVoice.md)   |
| deaf                      | bool                              |
| mute                      | bool                              |
| self_deaf                 | bool                              |
| self_mute                 | bool                              |
| self_video                | bool                              |

### `webhook_update(client,channel)`

Called when a [webhook](Webhook.md) of the [channel](CHANNEL_TYPES.md) is
updated. Sadly Discord does not sends details, so we pass only the channel as
argument.

## Instance attirbutes

### `client`

- type : `weakref.ReferenceType`

A weakreference to the owner client.

## Magic methods

### `__setatrr__`

Sets the event of the `EventDescriptor` to the specified function. Then updates
the event's parser if needed.

If an event is set of any clients, what is not `DEFAULT_EVENT`,
then the event's parser will be updated.

### `__delattr__`

Removes the event with switching it to `DEFAULT_EVENT`. Then updates the
event's parser if needed.
