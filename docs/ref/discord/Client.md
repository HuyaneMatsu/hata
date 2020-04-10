# class `Client`

A Client represent a connection to Discord. It is a valid user and is used to
interact with the Discord API.

- Source : [client.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/client.py)

## Superclasses

- [UserBase](UserBase.md)

## Creating a Client

### `Client(token,secret=None,client_id=0,activity=ActivityUnknown,status=None,is_bot=True,shard_count=0,intents=-1,**kwargs)`

##### `token`

The wrapper can login to Discord only if the `token` is a valid Discord token.

##### `secret`

If you want to request oauth2 access tokens with your client, then the `secret`
argument should set to the application's `secret` key.

##### `client_id`

Optinal argument.

##### `activity`

The starting activity of the client on login. By default it is
[`ActivityUnknown`](ActivityUnknown.md).

##### `status`

The status of the client on login. By default it is set to `None`, what
evaluates to `online`. It can be passed as type `str` or [`Status`](Status.md).

##### `is_bot`

If `is_bot` argument is set to `False`, then the login accepts only user tokens.
This case is not tested (so should not work), and using selfbot is against
Discord too.

##### `shard_count`

If `shard_count` argument is passed as `0` (so by default), then the client
will launch up without sharding (so with 1 gateway). If `shard_count` is passed
as `1`, then the client will launch up with the requested shard amount on first
login. If `shard_count` is more than `1`, then it will use the passed amount.

##### `intents`

The intents of the client can be defined by passing it. Any `int` instance is
accepted. If not passed as type [`IntentFlag`](IntentFlag.md) will be
converted. When validating the intents, negative values will be interpretered
as using all the intents, meanwhile if passed as positive, non existing intent
flags are removed.

##### `**kwargs`

These keyword arguments are set as instance attributes of the client. The type
implements `__dict__`, but at the case of overwriting a class attribute it
still raises `AttributeError`

Some extra attributes are set automatically or processed from kwargs:
- `name` : default : `''`.
- `discriminator` : default : `0`, can be set as `str` and
`int`.
- `avatar` : default : `0`, accepts `None`,
[image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)
and `int`.

## Familiar types

- [User](User.md)
- [Webhook](Webhook.md)
- [UserOA2](UserOA2.md)
- [WebhookRepr](WebhookRepr.md)

Because of a client is a valid user it inherits more attributes, methods and
properties from User like classes:

Instance Attributes:

- [`UserBase`](UserBase.md) :
    - [`id`](UserBase.md#id)
    - [`name`](UserBase.md#name)
    - [`discriminator`](UserBase.md#discriminator)
    - [`avatar`](UserBase.md#avatar)
    - [`has_animated_avatar`](UserBase.md#has_animated_avatar)
    - [`is_bot`](UserBase.md#is_bot) (from property)
    - [`flags`](UserBase.md#flags) (from property)
    - [`guild_profiles`](UserBase.md#guild_profiles) (from property)
    - [`partial`](UserBase.md#partial) (from property)
    - [`status`](UserBase.md#status) (from property)
    - [`statuses`](UserBase.md#statuses) (from property)
    - [`activities`](UserBase.md#activities) (from property)
- [`UserOA2`](UserOA2.md):
    - [`mfa`](UserOA2.md#mfa)
    - [`locale`](UserOA2.md#locale)
    - [`system`](UserOA2.md#system)
    - [`verified`](UserOA2.md#verified)
    - [`email`](UserOA2.md#email)
    - [`flags`](UserOA2.md#flags)
    - [`premium_type`](UserOA2.md#premium_type)

Properties:

- [`UserBase`](UserBase.md) :
    - [`avatar_url`](UserBase.md#avatar_url)
    - [`default_avatar`](UserBase.md#default_avatar)
    - [`default_avatar_url`](UserBase.md#default_avatar_url)
    - [`full_name`](UserBase.md#full_name)
    - [`mention`](UserBase.md#mention)
    - [`mention_nick`](UserBase.md#mention_nick)
    - [`created_at`](UserBase.md#created_at)
    - [`activity`](UserBase.md#activity)
    - [`platform`](UserBase.md#platform)
    - [`has_higher_role_than`](UserBase.md#has_higher_role_thanself-role)
    - [`has_higher_role_than_at`](UserBase.md#has_higher_role_than_atself-user-guild)

Methods:

- [`UserBase`](UserBase.md) :
    - [`avatar_url_as`](UserBase.md#avatar_url_asselfextnonesizenone)
    - [`name_at`](UserBase.md#name_atselfguild)
    - [`color_at`](UserBase.md#color_atselfguild)
    - [`mentioned_in`](UserBase.md#mentioned_inselfmessage)
    - [`hasrole`](UserBase.md#has_roleselfrole)
    - [`top_role_at`](UserBase.md#top_role_atself-guild-defaultnone)
    - [`can_use_emoji`](UserBase.md#can_use_emojiself-emoji)
- [`User`](User.md) :
    - [`_update_presence`](User.md#_update_presenceselfdata-method)
    - [`_update_presence_no_return`](User.md#_update_presence_no_returnselfdata-method)

Magic Methods:

- [`UserBase`](UserBase.md) :
    - [`__hash__`](UserBase.md#__hash__self)
    - [`__str__`](UserBase.md#__str__self)
    - [`__repr__`](UserBase.md#__repr__self)
    - [`__format__`](UserBase.md#__format__selfcode)
    - [`__gt__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
    - [`__ge__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
    - [`__eq__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
    - [`__ne__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
    - [`__le__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)
    - [`__lt__`](UserBase.md#__gt__-__ge__-__eq__-__ne__-__le__-__lt__)

## Instance attributes

Some instance attributes are not used / tested or they might be deprecated right
now:

- `mar_token` (user account only, not tested)
- `calls` (deprecated?)

### `_acitivity`

- type : [`activity`](ACTIVITY_TYPES.md)
- default : [`ActivityUnknown`](ActivityUnknown.md)

The client's local activity.

### `_gateway_pair`

- type : `tuple` (`str`, `float`)

An `url`, `time` pair used, when requesting gateway url. When the client
launches with more shards, keep requesting gateway url might take up most of
the time, so we cache the generated url and the timestamp of the request.
If the last timestamp is within 1 minute of the last request, then we will
just use the last generated one.

### `application`

- type : [`Application`](Application.md)

The client's application info. By default is an empty `Application`, but after
using the `Client.update_application_info()` method it should be updated. Only
bots can request their application info.

> Application info is updated on logon.

### `channels`

- type : `dict`
- items : (`int`, [`Guild`](Guild.md))

Stores all the [private](ChannelPrivate.md) and [group](ChannelGroup.md)
[channels](CHANNEL_TYPES.md) of the client as `(channel_id, Channel)` pairs.

### `events`

- type : [`EventDescriptor`](EventDescriptor.md)

Contains the dispatch events of the client.

### `gateway`

- type : [`DiscordGateway`](DiscordGateway.md) / [`DiscordGatewaySharder`](DiscordGatewaySharder.md)

The gateway of the client towards Discord. A gateway uses a websocket to
communicate with Discord.

### `http`

- type : [`DiscordHTTPClient`](DiscordHTTPClient.md)

The http session of the client. It executes the API requests and returns the
response after it. This http session is a valid http client, and can be used
to execute any type of requests.


### `intents`

- type : [`IntentFlag`](IntentFlag.md)

The intents of the client.

### `is_bot`

- type : `bool`
- values : `True` / `False`
- default : `False`

Defines if the token is a user account's or a bot's token. Even if a token is
right, defining this argument badly will cause the client to not be able to
login. This attribute is used at more cases to check how a bot / user account
acts at different API requests too.

### `loop`

- type : `event loop`

The event loop of the client.

### `private_channels`

- type : `dict`
- items : (`int`, [`ChannelPrivate`](ChannelPrivate.md))

Stores the private channels of the clients, but for easy access as:
`(user_id, Channel)` pairs, where the `user_id` is every time the channel's
other recipient's id.

### `ready_state`

- type : [`ReadyState`](ReadyState.md) / `NoneType`
- default : `None`

The client on login fills up it's `ready_state` with [guilds](Guild.md), which
will have their members requested, if it's is `None` we already received every
member from each guild.

### `relationships`

- type : `dict`
- items : (`int`, [`Relationship`](Relationship.md))

Stores the relationships of the client. The relationships' users' ids are the
keys and the relationships themselves are the values.

### `running`

- type : `bool`
- values : `True` / `False`

Defines if the client is running. Meanwhile the client is running, the
attribute is set to `True`. If the client is stopping it is changed to
`False`, what means, at the next exception the client's [`gateway`](#gateway)
will not be connected. If the client is stopping, then it stops heartbeating,
so the exception is guaranteed.

### `secret`

- type : `str` / `NoneType`
- default : `None`

The bot's application's `secret` key. Used at requesting oauth2 access tokens.

### `settings`

- type : [`Settings`](Settings.md)

The client's settings.

### `shard_count`

- type : `int`

The amount of shards, what the client uses. `0`, if the client is not using
sharding.

### `token`

- type : `str`

The token of the client. A valid token is a must to login the client.

### `voice_clients`

- type : `dict`
- items : (`guild_id`, [`VoiceClient`](VoiceClient.md))

The client's voice clients. Each bot can join a channel at every
[guild](Guild.md) and meanwhile they does, they have an active voice client
for that guild. `.voice_clients` stores
[`VoiceClient`](VoiceClient.md) in
(`guild_id`, [`VoiceClient`](VoiceClient.md)) item.

## Properties

### `owner`

- returns : [`User`](User.md) / [`Client`](Client.md)
- default : [`ZEROUSER`](ZEROUSER.md)

If the client is user account or
[`update_application_info`](#update_application_infoself) was not called since
stratup then returns  [`ZEROUSER`](ZEROUSER.md).

If the bot's [application](Application.md) is owned by a team, then returns the
[team's](Team.md) owner.

### `_platform`

- returns : `str`
- values : `''` / `'web'`
- default : `''` (empty string)

Returns the client's local platform. If the client is offline returns
`''`, else `'web`'.

### `friends`

- returns : `list`
- values : [`Relationship`](Relationship.md)

Returns the client's friends.

### `blocked`

- returns : `list`
- values : [`Relationship`](Relationship.md)

Returns the blocked users by the client.

### `received_requests`

- returns : `list`
- values : [`Relationship`](Relationship.md)

Returns the received friend requests of the client.

### `sent_requests`

- returns : `list`
- elements : [`Relationship`](Relationship.md)

Returns the out going friend requests of the client.

### `guild_order`

- returns : `list`
- elements : [`Guild`](Guild.md)

Returns the display order of the client's guild on the sidebar.

### `guild_order_with_folders`

- returns : `list`
- elements : [`Guild`](Guild.md) / `GuildFolder`

Returns the display order of the client's guilds on the sidebar. Gouped up
guilds will be returned as a `GuildFolder`.

### `no_DM_guilds`

- returns : `list`
- elements : [`Guild`](Guild.md)

Returns the list of guilds, from which the client cant get DM messages.

### `allowed_DM_guilds`

- returns : `list`
- values : [`Guild`](Guild.md)

Returns the list of guilds, from which the client can get DM messages.

## `Discord API side methods`

All Discord API method might raise [`DiscordException`](DiscordException.md).

### `client_edit(self,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Edits the client. If an argument is not passed, it wont be edited. Every
argument what refers to a user account is not tested.

- `password`, default : `None`. A must for user accounts, it should be a `str`
instance.
- `new_password`, default : `None`. It should be a `str` instance as well, it is
a user account only argument.
- `email`, default : `None`. Bots have no `email`, however it should be a `str`
instance if set.
- `house`, default : `_spaceholder`. A user account only argument, it's type
should be [`HypesquadHouse`](HypesquadHouse.md) if beeing changed. If passed
as `None`, will leave from the actual ones.
- `name`, default : `None`. Can be 2-32 character long.
- `avatar`, default : `_spaceholder`. Should be `bytes` in `'jpg'`, `'png'`, `'webp'`
format. If the client has premium account, it can be `gif` too.

### `client_edit_settings(self,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`
- user account only, not tested

Edits the client's settings. Accepted kwargs:

| name                      | description                                       |
|---------------------------|---------------------------------------------------|
| accessibility_detection   | bool                                              |
| afk_timeout               | int                                               |
| animate_emojis            | bool                                              |
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
| guild_order_ids           | list of int                                       |
| locale                    | str                                               |
| no_DM_from_new_guilds     | bool                                              |
| no_DM_guild_ids           | list of int                                       |
| play_gifs                 | bool                                              |
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

### `client_sync_settings(self)`

- `awaitable`
- returns : `None`
- raises : `ValueError`
- user account only, not tested

Requests and syncs the client's [settings](Settings.md).

### `client_edit_nick(self,guild,nick,reason=None)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Changes the client's nick at the [guild](Guild.md). A nickname's length can be
between 1-32. An extra argument reason can be set too. It should show up at the
guild's [audit logs](AuditLog.md).

### `client_connections(self)`

- `awaitable`
- returns : `list`
- elements : [`Connection`](Connection.md)

Returns a list of the client's connections to another platforms, like twitch,
twitter and so on. A bot has no connections, so it will return an empty list.

### `client_edit_presence(self,...):`

- `awaitable`
- returns : `None`
- raises : `ValueError` / `TypeError`

Changes the client's presence.

- `activity`, default : `None`. Can be any [activity type](ACTIVITY_TYPES.md).
If activity is set to `None` (so by default) it wont change the client's
activity, but if it is set to [`ActivityUnknown`](ActivityUnknown.md), it will
be removed.
- `status`, default : `None`. Can be any [`Status`](Status.md),
or `str` representing it.
- `afk`, default : `False`. Unlike other arguments this needs to be set to
`True` or to `False`.


### `activate_authorization_code(self,redirect_url,code,scopes)`

- `awaitable`
- returns : [`OA2Access`](OA2Access.md) / `None`

Activates a user's oauth2 code. The method requeires the `redirect_url`, where
the activation page redirected and the `code`, with which it redirected.
There is a function ro parse redirect url and code from a full url at
`others.py`, called [`parse_oauth2_redirect_url`](parse_oauth2_redirect_url.md).
The scopes parameter is a list of oauth2 scopes, which you want to request.
If code, redirect url or the scopes are invalid, the methods returns
`None`.

> Cannot grant (bug?): 'activities.read', 'activities.write', 'applications.builds.upload'

### `owners_access(self,scopes)`

- `awaitable`
- returns : [`OA2Access`](OA2Access.md) / `None`

Similar to `activate_authorization_code`, but it requests the application's
owner's access. It does not requires the `redirect_url` and the `code`
argument either.

### `user_info(self,access)`

- `awaitable`
- returns : [`UserOA2`](UserOA2.md)

Request the a user's information with oauth2 access token. By default a bot
account should be able to request every base infomation about a user (but you
do not need oauth2 for that). If the access token has `email` or/and `identify`
more information should show up.

### `user_connections(self,access)`

- `awaitable`
- returns : `list`
- elements : [`Connection`](Connection.md)

Requests a user's connections. This method will work only if the access token
has the `connections` scope. At the returned list even the hidden connections
of the user will show up.

### `renew_access_token(self,access)`

- `awaitable`
- returns : `None`

Renews the access token of an [`OA2Access`](OA2Access.md) object. By
default access tokens expire after one week.

### `guild_user_add(self,guild,access_or_compuser,...)`

- `awaitable`
- returns : `None`
- raises : `TypeError` / `ValueError`

Adds a user to the [guild](Guild.md). The bot must be a member of the guild
already, and the user must have been granted `guilds.join` oauth2 scope for
the application too. The `access_or_compuser` argument can be
[`OA2Access`](OA2Access.md) object or a
[`UserOA2`](UserOA2.md) one.

- `user`, default : `None`. If `access_or_compuser` is set with
[`UserOA2`](UserOA2.md), then this argument is unnecesarry.
- `nick`, default : `None`. The `nick` with which the user will be added.
- `roles`, default : `[]`. The user will be added with these [roles](Role.md).
- `mute`, default : `False`. The user can be added initially as muted.
- `deaf`, default : `False`. The user can be added as deafen.

### `user_guilds(self,access)`

- `awaitable`
- returns : `list`
- elements : [`Guilds`](Guild.md)

Requests a user's guilds with it's [`OA2Access`](OA2Access.md).
The user must provide the `guilds` oauth2 scope for this request to succeed.
These guilds will be partial guilds, if non of the active clients is member
of them.

### `achievement_get_all(self)`

- `awaitable`
- returns : `list`
- elements : [`Achievement`](Achievement.md)

Requests all the achievements of the application and returns them.

### `achievement_get(self,achievement_id)`

- `awaitable`
- returns : [`Achievement`](Achievement.md)

Requests an achievement by it's id.

### `achievement_create(self,name,description,icon,secret=False,secure=False)`

 - `awaitable`
- returns : [`Achievement`](Achievement.md)

Creates an achievement.

| argument      | type  |
|---------------|-------|
| name          | str   |
| description   | str   |
| secret        | bool  |
| secure        | bool  |
| icon          | bytes |

`icon` can be in `jpg`, `png`, `webp` or `gif` format.

### `achievement_edit(self,achievement,...)`
 
- `awaitable`
- returns : [`Achievement`](Achievement.md)
- raises : `ValueError`

Edits an [`Achievement`](Achievement.md), then updates it.

All argument to this method is optional.
 
| argument      | type  | default       |
|---------------|-------|---------------|
| name          | str   | None          |
| description   | str   | None          |
| secret        | bool  | None          |
| secure        | bool  | None          |
| icon          | bytes | _spaceholder  |

`icon` can be in `jpg`, `png`, `webp` or `gif` format.

### `achievement_delete(self,achievement)`

- `awaitable`
- returns : `None`

Deletes the achievement.

### `user_achievements(self,access)`

- `awaitable`
- returns : `list`
- elements : [`Achievement`](Achievement.md)
 
Requests the user's achievement with it's [oauth2 access](OA2Access.md).
The user must grant `applications.store.update` scope for the application to
do it.

> DiscordException UNAUTHORIZED (401): 401: Unauthorized

### `user_achievement_update(self,user,achievement,percent_complete)`

- `awaitable`
- returns : `None`

Updates the `user`'s achievement with the given percentage (`int`). The 
achevement should be `secure`. This method only updates the achievement's
percentage, what means, the achievement already should be granted for the user.

> When updating secure achievement:
> - DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
>
> When updating non secure:
> - DiscordException FORBIDDEN (403), code=40001: Unauthorized

### `application_get(self,application_id)`

- `awaitable`
- returns : [`Application`](Application.md)
- user account only, not tested

Requests the application with the given id and returns it.

### `download_url(self,url)`

- `awaitable`
- returns : `bytes`

Requests an url and returns the response's content.

### `download_attachment(self,attachment)`

- `awaitable`
- returns : `bytes`

Downloads a [`Attachment`](Attachment.md) object, and returns it's content.

### `channel_group_leave(self,channel)`

- `awaitable`
- returns : `None`
- user account only, not tested

The client leaves from the [group channel](ChannelGroup.md).

### `channel_group_user_add(self,channel,*users)`

- `awaitable`
- returns : `None`
- user account only, not tested

Adds the users to the [group channel](ChannelGroup.md).

### `channel_group_user_delete(self,channel,*users)`

- `awaitable`
- returns : `None`
- user account only, not tested

Removes the users from the [group channel](ChannelGroup.md).

### `channel_group_edit(self,channel,...)`

- `awaitable`
- returns : `None`
- raises `ValueError`
- user account only, not tested

Edits the [group channel](ChannelGroup.md).

- `name`, default : `_spaceholder`. Can be `None`, or `str` type.
- `icon`, default : `_spaceholder`. Passing `None` removes the current one.

### `channel_group_create(self,users)`

- `awaitable`
- returns : [`ChannelGroup`](ChannelGroup.md)
- raises `ValueError`
- user account only, not tested

Creates and returns a group channel with the given users. if less than 2 user is
passed, then raises `ValueError`.

### `channel_private_create(self,user)`

- `awaitable`
- returns : [`ChannelPrivate`](ChannelPrivate.md)

Creates and returns a private channel with the user. If there is an existing
private channel with the user, returns that instead of requesting it from the
Discord API.

### `channel_private_get_all(self)`

- `awaitable`
- returns : `list`
- elements : [`ChannelPrivate`](ChannelPrivate.md) / [`ChannelGroup`](ChannelGroup.md)

Request the client's private (+ group) channels and returns them in a list.
At the case of bot accounts the request returns an empty list, so we skip it.

### `channel_move(self,channel,visual_position,...)`

- `awaitable`
- returns : `None`
- raises `ValueError` / `TypeError`

Moves a [guild channel](ChannelGuildBase.md). The `visual_position`
stands for the place where the channel is going to be moved under the
[category](ChannelCategory.md) / [guild](Guild.md). If the algorithm can
not place the channel exactly on that location, it will place it as close,
as it can. If there is nothing to move, then skips the request.

- `category`, default : `_spaceholder`. If the `category` is not set, then the
channel will keep it's current parent. If the arguments is set to the
[guild](Guild.md) or to `None`, then the channel will be moved under the guild
itself, or if the argument is set to a [category channel](ChannelCategory.md),
then it will be moved under the category.
- `lock_permissions`, default : `False`. If you want to sync the permissions
with the new category set it to `True`.
- `reason`, default : `None`. Shows up at the [logs](AuditLog.md) of the
[guild](Guild.md).

### `channel_edit(self,channel,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Edits the [guild channel](ChannelGuildBase.md) with the given values.
Different channal types accept different arguments, and they ignore the rest.
Important note to mention, that `Text channel` and `Guild news` both share
the same [`ChannelText`](ChannelText.md) class.

- `name`, default : `None`. Accepted by every type of channel.
- `topic`, default : `None`.  Only [`ChannelText`](ChannelText.md) and
`guild news` have topic.
- `nsfw`, default : `None`. `Text channels` and `Guild news` can be `nsfw`,
Not Safe For Work.
- `slowmode`, default : None. `Text channel` only, If slowmode is applied,
then every user needs to wait some time between sending a message.
Slowmode is set in seconds, can be between 0 and 21600 seconds.
- `user_limit`, default : `None`. Reperesents how much user can be at the
[Voice channel](ChannelVoice.md) at the same time. If this argumnet is set to 0,
means that there is no limit, else it can between 1 and 99.
- `bitrate`, default : [ChannelVoice](ChannelVoice.md) only. Higher birate
should yield better quality.
- `type_`, default : 128. A `Text channel` can be turned into 
`Guild news channel`, or back by changing the `type_` argument. The
`text channel`'s type is `0`, meanwhile `Guild news`' is 5.
- `reason`, default : `None`. Shows up at the [logs](AuditLog.md) of the
[guild](Guild.md).

### `channel_create(self,guild,category=None,*args,reason=None,**kwargs)`

- `awaitable`
- returns : [`guild channel`](ChannelGuildBase.md)
- raises : `ValueError`

Creates a channel at the given [guild](Guild.md). Most of the arguments are
same as at the [`channel_edit`](#channel_editselfchannel). if the channel is
succesfully created, returns it.

Arguments:
- `guild`
- `category=None` If the argument is set to `None`, so by default, the channel
will go under the [guild](Guild.md). Same, if the argument is set to the guild
itself.

*Arguments:
- `name`
- `type` Can be 0, 2, 4, 5, 6 or [`ChannelText`](ChannelText.md),
[`ChannelVoice`](ChannelVoice.md), [`ChannelGroup`](ChannelGroup.md),
[`ChannelStore`](ChannelStore.md) are the valid channel types to create in a
guild.

Keyword arguments:
- `reason`, default : `None`. Shows up at the [audit logs](AuditLog.md) of the
[guild](Guild.md).

**Keyword arguments:
- `overwrites=[]` A channel can be created with
[permission overwrites](PermOW.md). These overwrites should be created with
[`cr_p_overwrite_object`](cr_p_overwrite_object.md) function.
- `topic`, default : `None`.
- `nsfw`, default : `False`.
- `slowmode`, default : `0`.                                          
- `bitrate`, default : `64000`.
- `user_limit`, default : `0`.
- `vip`, default : `False` If the [guild](Guild.md) of the planed channel has VIP
feature, then it can have it's bitrate set up to 128000 from the default 96000.
- `premium_tier`, default : `0`. If the guild has higher premium tier, it
can have it's voice channel's bitrate up to 128000, 256000, 384000, depends
on the tier (max tier is 3).

### `channel_delete(self,channel,reason=None)`

- `awaitable`
- returns : `None`

Deletes a channel of the guild with the given reason. If a
[category channel](ChannelCategory.md) is deteleted, then every channel under
it wont be deleted, they will move under the [guild](Guild.md) itself. 

### `channel_follow(self,source_channel,target_channel)`

- `awaitable`
- returns : [`Webhook`](Webhook.md)
- raises : `ValueError`

Follows the `source_channel` with the `target_channel`. The `source_channel`
must be channel type 1, so new (announcements) channel. The `target_channel`
must type 0 or 5, so any guild text channel.

Returns the [webhook](Webhook.md), which follows the `target_channel`. This
webhook will have no [`.token`](Webhook.md#token), because Discord itself
does the actions.

### `message_mar(self,message)`

- `awaitable`
- returns : `None`
- user account only, not tested

Marks the [message](Message.md) as read.

### `message_logs(self,channel,limit=100,after=None,around=None,before=None)`

- `awaitable`
- returns : `list`
- values : [`Message`](Message.md)
- raises : `ValueError` / `TypeError`

Request messages at the given channel from Discord. The `after`, `around` and
the `before` arguments can be a valid discord type with `id`, a
[`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
, or a `datetime` object. If there is at least 2 already loaded messages at a
channel's history between the requested ones, the wrapper will chain the rest
to the history. If a channel passes it's history's limit like this, it will
remove it's limitation for an amount of time, however requesting older
messages more times with different methods will extend that duration.

### `message_logs_fromzero(self,channel,limit=100)`

- `awaitable`
- returns : `list`
- values : [`Message`](Message.md)

If the channel has 2 or less messages stored in it's history, then using the
`message_logs` wont be able to channel the messages together. This method
requests the newest messages of a channel and returns them as a list.

### `message_get(self,channel,message_id)`

- `awaitable`
- returns : [`Message`](Message.md)

Requests and returns the message for the given id at the given channel.

### `message_create(self, channel, ...)`

- `awaitable`
- returns : [`Message`](Message.md) / `None`
- raises : `ValueError` / `TypeError`

Creates and returns a message at the given `channel`. If there is nothing to
send, then returns `None`.

- `content`, default : `None`. The content of the message.
- `embed`, default : `None`. The embedned content sent with the message. It
should be [`Embed`](Embed.md), [`EmbedCore`](EmbedCore.md), or any
compatible type's instance.
- `file`, default : `None`. [For details](#_create_file_formdatafile-staticmethod).
- `allowed_mentions`, default : `_spaceholder`. [For details](#_parse_allowed_mentionsallowed_mentions-staticmethod).
- `tts`, default : `False`. Is the message `tts`, text-to-speech.
- `nonce`, default : `None`. `nonce` is used for validating a message was sent (?).

### `message_delete(self,message,reason=None)`

- `awaitable`
- returns : `None`

Deletes the given message. An additional `reason` argument can be passed to,
which should show up at the [guild's](Guild.md) audit logs.

### `message_delete_multiple(self,messages,reason=None)`

- `awaitable`
- returns : `None`

Deletes the given messages. The messages needs to be from the same channel. An
additional `reason` argument can be passed too, which should show up the
[guild's](Guild.md) audit logs.


### `message_delete_multiple2(self,message,reason=None)`

- `awaitable`
- returns : `None` / `list` of [`DiscordException`](DiscordException.md)

Similar to `message_delete_multiple`, but it accepts messages from different
channels. Groups them up by channel and creates
[`.message_delete_multiple`](#message_delete_multipleselfmessagesreasonnone)
tasks for them. Returns when all the task are finished. If any exception was
rasised meanwhile, then returns each of them in a list.

### `message_delete_sequence(self,channel,after=None,before=None,limit=None,filter=None,reason=None)`

- `awaitable`
- returns : `None`

Deletes messages between an intervallum determined by `before` and `after`.
`before` and `after` can be a valid Discord object with `.id`, a `datetime`
object, or a [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes).

If `after` is not passed, then there will be no lower time limit.

If `before` is not passed, then there will be no upper time limit.

The method also accepts `limit`, to set how much message you want to delete
at most.

If `filter` is passed, then it will be called on each message, to decide, if it
should be deleted. It should be passed as a callable, what accepts 1 argument,
a [message](Message.md), and it should return `True` or `False`.

### `message_edit(self, message, content=None, embed=_spaceholder, allowed_mentions=_spaceholder, suppress=None)`

- `awaitable`
- returns : `None`

Edits the message with the given `content` and [`embed`](Embed.md).
Pass `content` as `''` to remove it. Pass `embed` as `None` to remove it.
You can also use [`allowed_mentions`](#_parse_allowed_mentionsallowed_mentions-staticmethod)
as well. This method also supports editing a message's suppress, with editing it's
[`.flags`](Message.md#flags).

### `message_suppress_embeds(self,message,suppress=True)`

- `awaitable`
- returns : `None`

Suppresses the [`message`](Message.md)'s embeds. If `suppress` is set to
`False`, then reverses the suppress.

### `message_pin(self,message)`

- `awaitable`
- returns : `None`

Pins the message.

### `message_unpin(self,message)`

- `awaitable`
- returns : `None`

Unpins the message.

### `channel_pins(self,channel)`

- `awaitable`
- returns : `list`
- values : [`Message`](Message.md)

Returns the pinned messages at the given channel.

### `message_at_index(self,channel,index)`

- `awaitable`
- returns : [`Message`](Message.md)
- raises : `IndexError` / `PermissionError`

Returns the message at the given channel at the specific index. Raises
`IndexError` if there is not that much message at the channel, or
`PermissionError` if the client has no permission to request older messages.

### `messages_till_index(self,channel,start=0,end=100)`

- `awaitable`
- returns : `list`
- values : [`Message`](Message.md)

Returns a list of the message between the `start` - `end` area. If the client
has no permission to request messages, or there are no messages at the given
area, it returns an empty list.

### `message_iterator(self,channel,chunksize=97)`

- returns : [`MessageIterator`](MessageIterator.md)

### `typing(self,channel)`

- `awaitable`
- returns : `None`

Sends typing to the channel. The client will type for eight seconds, or till it
sends a meesage to the channel.

### `keep_typing(self,channel,timeout=300.)`

- returns : [`typer`](Typer.md)

`Typer` is used with `with` context. Timeout stands for the maximal
duration of typing. The typing ends, when the the `with` block is exited.

### `reaction_add(self,message,emoji)`

- `awaitable`
- returns : `None`

Reacts on the message with an [`emoji`](Emoji.md).

### `reaction_delete(self,message,emoji,user)`

- `awaitable`
- returns : `None`

Removes the user's reaction ([`Emoji`](Emoji.md)) from the [message](Message.md).

### `reaction_delete_own(self,message,emoji)`

- `awaitable`
- returns : `None`

Removes your own reaction ([`Emoji`](Emoji.md)) from the [message](Message.md).

### `reaction_clear(self,message)`

- `awaitable`
- returns : `None`

Clears all the reactions from the [message](Message.md).

### `reaction_users(self,message,emoji,limit=None,after=None)`

- `awaitable`
- returns : `list`
- values : [`User`](User.md) / [`Client`](Client.md)
- raises : `ValueError` / `TypeError`

Requests the [users](User.md), who reacted on the [message](Message.md)
with the [`Emoji`](Emoji.md).

If the message has no reacters at all or no reacters with that emoji, returns
an empty list. If we know the emoji's every reacters we query the parameters
from that.

The `after` arguments can be a valid discord type with `id`, a
[`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
, or a `datetime` object.
`limit` can be `int` between 1 and 100.

### `reaction_users_all(self,message,emoji)`

- `awaitable`
- returns : `list`
- values : [`User`](User.md) / [`Client`](Client.md)

Requests the all the [users](User.md), which reacted on the [message](Message.md)
with the [`emoji`](Emoji.md).

If the message has no reacters at all or no reacters with that emoji returns
an empty list. If we know the emoji's every reacters we query the parameters
from that.

### `reaction_load_all(self,message)`

- `awaitable`
- returns : `None`

Requests all the [users](User.md) reacted on a [message](Message.md)
with any [emojis](Emoji.md).

### `guild_preview(self,guild_id)

- `awaitable`
- returns : [`GuildPreview`](GuildPreview.md)

Requests the preview of a public guild.

### `guild_user_delete(self,guild,user,reason=None)`

- `awaitable`
- returns : `None`

Kicks the user from the guild. An additional `reason` argument is passable too,
which will show up at the guild's audit logs.

### `guild_ban_add(self,guild,user,delete_message_days=0,reason=None)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Bans the user from the guild. An additional `reason` argument is passable too,
which will show up at the guild's audit logs. `delete_message_days` can be
between 0 and 7.

### `guild_ban_delete(self,guild,user,reason=None)`

- `awaitable`
- returns : `None`

Unbans a user from the guild.  An additional `reason` argument is passable too,
which will show up at the guild's audit logs.

### `guild_sync(self,guild_id)`

- `awaitable`
- returns : [`Guild`](Guild.md)

Requests a [`guild`](Guild.md) by id and syncs it with the wrapper.

### `guild_mar(self,guild)`

- `awaitable`
- returns : `None`
- user account only, not tested

Marks the guild as read.

### `guild_leave(self,guild)`

- `awaitable`
- returns : `None`

The client leaves from the guild.

### `guild_delete(self,guild)`

- `awaitable`
- returns : `None`

Deletes the guild. Only the guild's owner can perform this action.

### `guild_create(self,...)`

- `awaitable`
- returns : [`partial Guild`](Guild.md)

Creates a guild with the given attributes. A user account cant be member of
100 guidls maximum and a user account can create a guild only if it is member
of less than 10 guilds.

- `name`, can have length from 2 up to 100.
- `icon`, default : `None`, should be `bytes` object if set.
- `roles`, default : `[]`. The listed roles should be created with the
[`cr_p_role_object`](cr_p_role_object.md) function. The role's id represent
just a symbolic number, which with they can be mentioned at permission
overwrites. Role 0 is `@everyone`.
- `channels`, default : `[]`. The listed channels should be created with
[`cr_pg_channel_object`](cr_pg_channel_object.md) function.
- `afk_channel_id`, default : `None`. The `id` of the guild's afk channel.
- `system_channel_id`, default : `None`. The `id` of the guild's system
channel.
- `afk_timeout`, default : `None`. The afk timeout in seconds, of the afk
channel. Should be passed as one of: 60, 300, 900, 1800, 3600.
- `region`, default  : `VoiceRegion.eu_central`. Any 
[`voice region`](VoiceRegion.md).
- `verification_level` default : `verification_levels.medium`. The
[verifacation level](VerificationLevel.md) required for users to join the
guild.
- `message_notification_level`, default :
`MessageNotificationLevel.only_mentions`. Everyone will
[notified](MessageNotificationLevel.md) if any message is created, or only if
mentioned.
- `ContentFilterLevel`, default : `ContentFilterLevel.disabled`. The
[explicit content filter level](ContentFilterLevel.md) of the guild.

### `guild_prune(self,guild,days,count=False,reason=None)`

- `awaitable`
- returns : `int` / `None`

Kicks the members of the [guild](Guild.md), which were inactive since x days.
`days` needs to be at least 1. If count is set to `True`, then returns how
much user got pruned, but if the guild is large it will be set to `False`
anyways. An addittional `reason` argumnet is passable, which will show up
the guild's audit logs. The method returns the number of pruned members or
`None` if `count` is set to `False`

### `guild_prune_estimate(self,guild,days)`

- `awaitable`
- returns : `int`

Returns the amount of members, who would been pruned by calling `guild_prune`.

### `guild_edit(self,guild,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Edits the [guild](Guild.md) with the given arguments. If an argument is not
changed from default, then it will not change that.

- `name`, default : `None`, can be between length 2 and 100.
- `icon`, default : `_spaceholder`. If set to `None` removes the guild's icon.
Excepts a `jpg`, `png`, `webp` as `bytes`. If the guild has `ANIMATED_ICON`
feature, then it can have `gif` icon too.
- `banner`, default : `_spaceholder`. The guild must have `BANNER` feature.
Acts similar to `icon`, except it can not be animated.
- `splash`, default : `spaceholder`. The guild must have `INVITE_SPLASH`
feature. Acts similar to `icon`, except it can not be animated.
- `discovery_splash`, default : `_spaceholder`. The guild must have
`DISCOVERABLE` feature. Acts similar to `icon`, except it can not be animated.
- `afk_channel`, default : `_spaceholder`. Setting this argument to `None`
removes the guild's actual voice channel, else it should be a
[voice channel](ChannelVoice.md).
- `system_channel`, default : `_spaceholder`. `None` removes the guild's
current system channel. If you wanna set it to a channel, it should be a
[text channel](ChannelText.md).
- `rules_channel`, default : `_spaceholder`. The guild must have `DISCOVERABLE`
feature. If passed as `None` removes the guild's current rules channel. If you
want to set it, then it should be passed as a [text channel](ChannelText.md).
- `public_updates_channel`, default : `_spaceholder`. The guild must have
`DISCOVERABLE` feature. If passed as `None` removes the guild's current updates
channel. If you want to set it, then it should be passed as a
[text channel](ChannelText.md).
- `owner`, default : `None`, transfers the guild's ownership to an another
user. Guild owner only.
- `region`, default : `None`. Changes the guild's voice region, accepts type
[`VoiceRegion`](VoiceRegion.md).
- `afk_timeout`, default : `None`. Represents the timeout at the `afk_channel`.
Accepts only 60, 300, 900, 1800, 3600. These represent the afk timeout in
seconds.
- `verification_level`, default : `None`. Should be type 
[VerificationLevel](VerificationLevel.md).
- `content_filter`, default : `None`. Should be type
[ContentFilterLevel](ContentFilterLevel.md).
- `message_notification`, default : `None`, should be type
[MessageNotificationLevel](MessageNotificationLevel.md).
- `description`, default : `_spaceholder`, should be type `str` or `None`.
- `system_channel_flags`, default : `None`. Should be passed as type
`int` or [`SystemChannelFlag`](SystemChannelFlag.md).
- `reason`, default : `None`. Reason shows up at the guild's audit logs.

### `guild_bans(self,guild)`:

- `awaitable`
- returns : `list`
- values : ( [`User`](User.md)/[`Client`](Client.md), `str`/`None` ) pairs

Returns a list of the banned users at the guild as `(User, reason)` pairs.

### `guild_ban_get(self,guild,user_id)`

- `awaitable`
- returns : ( [`User`](User.md)/[`Client`](Client.md), `str`/`None` ) pair

Returns the `(User, reason)` ban pair for the given id.


### `guild_embed_get(self,guild)`

- `awaitable`
- returns : [`GuildEmbed`](GuildEmbed.md)

Request, updates and returns's the guild's embed. This function is symbolic,
because `guild_edit` dispatch event updates the guild's embed and
`Guild.embed` returns it.

### `guild_embed_edit(self,guild,enabled=None,channel=_spaceholder)`

- `awaitable`
- returns : `None`

Edits the guild's embed ith the given arguments. `enabled` can be `True` or
`False`, meanwhile `channel` can be `None` or [ChannelText](ChannelText.md).

### `guild_widget_get(self,guild_or_id)`

- `awaitable`
- returns : `None` / [`GuildWidget`](GuildWidget.md)
- raises : `TypeError`

Requests the passed [`Guild`](Guild.md)'s or guild id's widget json and
returns a  [`GuildWidget`](GuildWidget.md) object. If the guild has no
widget disabled, returns `None`.

### `guild_users(self,guild)`

- `awaitable`
- returns : `list`
- elements : [`User`](User.md) / [`Client`](Client.md)

Requests all the users of the Guild and returns them in a list. If caching
is allowed, these users should be already loaded.

### `guild_get_all(self)`

- `awaitable`
- returns : `list`
- values : [`Guild`](Guild.md)

Requests, then returns the client's guilds.

### `guild_regions(self,guild)`

- `awaitable`
- returns : `([...], [...])`
- values : [`VoiceRegion`](VoiceRegion.md)

Requests the available voice regions for the client and returns two lists.
The First contains all the regions and the second the optimal ones.

### `guild_sync_channels(self,guild)`

- `awaitable`
- returns : `None`

Request all the channels of the [`guild`](Guild.md). If there is any desync
between  the wrapper and Discord, it applies the changes to the guild.

### `guild_sync_roles(self,guild)`

- `awaitable`
- `returns : `None`

Request all the roles of the [`guild`](Guild.md). If there is any desync
between  the wrapper and Discord, it applies the changes to the guild.

### `audit_logs(self,guild,limit=100,before=None,after=None,user=None,event=None)`

- `awaitable`
- returns: [`AuditLog`](AuditLog.md)
- raises : `ValueError`

Request the audit logs of the guild and returns it. The `after`, `around` and
the `before` arguments can be a valid discord type with `id`, a
[`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
, or a `datetime` object. `event` argument should be
[`AuditLogEvent`](AuditLogEvent.md) instance or `None` for all.

### `audit_log_iterator(self, guild, user=None, event=None)`

- returns : [`AuditLogIterator`](AuditLogIterator.md)

### `user_edit(self,guild,user,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Edits the user at the given [guild](Guild.md). If any argument is let on default,
those ont be edited.

- `nick`, default : `_spaceholder`. If set to `None` removes the user's nick.
It should be type `str`.
- `deaf`, default : `None`. `True` or `False`.
- `mute`, default : `None`. `True` or `False`.
- `voice_channel`, default : `_spaceholder`. Moves the user to the selected
[voice channels](ChannelVoice.md). Only applicable if the user is already at
a voice channel. If this argument is set to `None`, then the user is removed
from it's voice channel.
- `roles`, default : `None`. A list of [roles](Role.md). 
- `reason`, default : `None`. The reason shows up at the audit logs of the
guild.

### `user_role_add(self,user,role,reason=None)`

- `awaitable`
- returns : `None`

Adds the [role](Role.md) to the user.

### `user_role_delete(self,user,role,reason=None)`

- `awaitable`
- returns : `None`

Removes the [`role`](Role.md) from the user.

### `user_voice_move(self,user,voice_channel)`

- `awaitable`
- returns : `None`

Moves the user to the passed [voice channels](ChannelVoice.md). Only
applicable if the user is already at a voice channel.

### `user_voice_kick(self,user,guild)`

- `awaitable`
- returns : `None`

Kicks the user from the [`guild`](Guild.md)'s voice channels. Only applicable
if the user is already at a voice channel.

### `user_get(self,user_id)`

- `awaitable`
- returns : [`User`](User.md) / [`Client`](Client.md)

Request the user's data and returns the user. If the user already exists
updates it.

### `guild_user_get(self,guild,user_id)`

- `awaitable`
- returns : [`User`](User.md) / [`Client`](Client.md)

Requests the user by it's id at the given [`guild`](Guild.md). Updates the
user and it's profile.

### `user_profile(self,user_id)`

- `awaitable`
- returns : [`User`](User.md) / [`Client`](Client.md)
- (user account only, not tested, the returned data is unknown)

Request the user's profile and returns the user. If the user already exists
updates it.


### `integration_get_all(self,guild)`

- `awaitable`
- returns : `list`
- values : [`Integration`](Integration.md)

Request the [integrations](Integration.md) of the [guild](Guild.md) and
returns them.

### `integration_create(self,guild,integration_id,type_)`

- `awaitable`
- returns : [`Integration`](Integration.md)
- (needs integration to test)

Creates an [integration](Integration.md) with the given arguments at the
[guild](Guild.md).

### `integration_edit(self,integration,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`
- (needs integration to test)

Edits the [integration](Integration.md) with the given arguments.

- `expire_behavior`, default : `None`. Should be 0 for kick or 1 for role 
remove.
- `expire_grace_period`, default : `None`. Should be 1, 3, 7, 14, 30. The time
in days, after the subscribtion will be ignored.
- `enable_emojis`, default : `None`. Should be `True` or `False`. Twitch only.

### `integration_delete(self,integration)`

- `awaitable`
- returns : `None`
- (needs integration to test)

Deletes the [integration](Integration.md).

### `integration_sync(self,integration)`

- `awaitable`
- returns : `None`
- (needs integration to test)

Syncs the [integration](Integration.md).

### `permission_ow_edit(self,channel,overwrite,allow,deny,reason=None)`

- `awaitable`
- returns : `None`

Edits the given [permission overwrite](PermOW.md) of the given channel. The
`allow` and `deny` arguments should be the new [permissions](Permission.md) of
the overwtire. The given `reason` shows up at the audit logs of the
[guild](Guild.md).

### `permission_ow_delete(self,channel,overwrite,reason=None)`

- `awaitable`
- returns : `None`

Deletes the given [permission overwrite](PermOW.md) from the channel. The
`reason` shows up at the [guild's](Guild.md) audit logs.

### `permission_ow_create(self,channel,target,allow,deny,reason=None)`

- `awaitable`
- returns : `None`
- raises : `TypeError`

Creates a [permission overwrite](PermOW.md) at the given channel for the given
target. The target can be a [role](Role.md) or a [user](User.md). The `allow`
and `deny` should be [permissions](Permission.md). The `reason` shows up at
the [guild's](Guild.md) audit logs.

### `webhook_create(self,channel,name,avatar=None)`

- `awaitable`
- returns : [`Webhook`](Webhook.md)
- raises : `ValueError`
 
Creates a [webhook](Webhook.md) at the channel with the given name and avatar.
The `anme`'s length can be between 1 and 80.
`avatar` is optional. It should be passed as a `bytes` like and should have`
'jpg'`, `'png'`, `'webp'` or `'gif'` format. If `gif` is passed it will ignore
the animation however.

### `webhook_get(self,webhook_id)`

- `awaitable`
- returns : [`Webhook`](Webhook.md)

Tries to query the webhook. If it exists and it is up to date returns it.
If it is not up to date requests and updates it. If it doesnt exsist requests
and creates it.

### `webhook_get_token(self,webhook_id,webhook_token)`

- `awaitable`
- returns : [`Webhook`](Webhook.md)

The `token` at the method means, that it uses the webhook's token as
authorization instead of the client's token itself.

This method similar to [`webhook_get`](#webhook_getselfwebhook_id), but it
needs two arguments, the webhook's id and token.

### `webhook_update(self,webhook)`
 
- `awaitable`
- returns : `None`

Updates the given webhook.

### `webhook_update_token(self,webhook)`

- `awaitable`
- returns : `None`

The `token` at the method means, that it uses the webhook's token as
authorization instead of the client's token itself.

This method basically does the same as
[`webhook_update`](#webhook_updateselfwebhook).

### `webhook_get_channel(self,channel)`
 
- `awaitable`
- returns : `list`
- values : [`Webhook`](Webhook.md)

Request and returns the channel's wehooks.
 
### `webhook_get_guild(self,guild)`
 
- `awaitable`
- returns : `list`
- values : [`Webhook`](Webhook.md)

If the guild's webhooks are up to date, just returns them, else it request,
calculates differences and applies them too.

### `webhook_delete(self,webhook)`

- `awaitable`
- returns : `None`

Deletes the webhook.

### `webhook_delete_token(self,webhook)`

- `awaitable`
- returns : `None`

The `token` at the method means, that it uses the webhook's token as
authorization instead of the client's token itself.

Does the same as [`webhook_delete`](#webhook_deleteselfwebhook).

### `webhook_edit(self,webhook,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Edits the webhook with the given arguments. Not like other `edit` methods,
this methods actually updates the webhook with the given data instanlty,
because of Discord API does not gives dispatch event with the new data, only
the fact that they changed.

- `name`, default : `None`. If set changes the webhook's name.
- `avatar`, default : `_spaceholder`. Can be set to `None` to remove the actual
avatar of the webhook, or `bytes` type in `'jpg'`, `'png'`, `'webp'` or
`'gif'` format. If `gif` is passed it will ignore the animation however.
- `channel`, default : `None`. Any [text channel](ChannelText.md).

### `webhook_edit_token(self,webhook,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

The `token` at the method means, that it uses the webhook's token as
authorization instead of the client's token itself. Same as
[`webhook_edit`](#webhook_editselfwebhook), but it accepts only `name` and
`avatar`.

### `webhook_send(self,webhook,...)`

- `awaitable`
- returns : [`Message`](Message.md) / `None`
- raises : `ValueError` / `TypeError`

Almost same as [`.message_create`](#message_createself-channel-). Sends a message
with the [`webhook`](Webhook.md) to it's channel. If there is nothing to send,
then returns `None`. If `wait` is set to `True`, it returns the
[`message`](Message.md), else `None`.

- `content`, default : `None`. The content of the message.
- `embed`, default : `None`. The embedned content sent with the message. Not
like at `message_create`, it can be a list of embeds too, up to 10.
- `file`, default : `None`. [For details](#_create_file_formdatafile-staticmethod).
- `allowed_mentions`, default : `_spaceholder`. [For details](#_parse_allowed_mentionsallowed_mentions-staticmethod).
- `tts`, default : `False`. Is the message `tts`, text-to-speech.
- `name`, default : `None`. The webhook's name will show up differently on the
message, if the `name` argument is changed.
- `avatar_url`, default : `None`. The webhook's avatar will show up differently,
if passed.
- `wait`, default : `False`. If `wait` is set to `True` the API waits for the
message to be sent and returns it, or raises an exception. If `wait` is set to
`False` (so by default) the method returns `None`.

### `emoji_get(self,guild,emoji_id)`

- `awaitable`
- returns : [`Emoji`](Emoji.md)

Gets the [emojis](Emoji.md) by the `id` from the given [guild](Guild.md).
Every emoji is already accessable by `Guild.emojis`, but there is 1 difference.
After using this method `Emoji.user` (so the person who added it) will be
loaded.

### `guild_sync_emojis(self,guild)`

- `awaitable`
- returns : `None`

Requests all the [emojis](Emoji.md) for the given [`guild`](Guild.md)
and syncs the differences between the wrapper and Discord. An another
important factor of this method is, that, the data returned by Discord
will also contain the `Emoji.user` attribute.

### `emoji_create(self,guild,name,image,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Creates an [`emoji`](Emoji.md) at the given [guild](Guild.md). The emoji's
name can be between length 2-32 and the image can be `'jpg'`, `'png'`,
`'webp'`, `gif` format. If the emoji has `gif` format but is not animated,
still counts as `animated`.

Other arguments:
- `roles`, default : `[]`. Only the choosen people with the [roles](Role.md)
can use the emojis.
- `reason`, default : `None`. The `reason` shows up at the guild's audit logs.

Unlike other `_create` methods, this method returns `None`. The reason is,
because we get **all** the emojis from the **same** dispatch event for the
guild, so else the wrapper could not tell which emoji is new / edited /
deleted.

### `emoji_delete(self,emoji,reason=None)`

- `awaitable`
- returns : `None`

Deletes the [`emoji`](Emoji.md). The `reason` shows up at the emoji's
[guild](Guild.md)'s audit logs.

### `emoji_edit(self,emoji,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Edits the [`emoji`](Emoji.md) with the given arguments:

- `name`, default : `None`. If set changes the emoji's name. Emoji name length
can be between 2 and 32.
- `roles`, default : `None`. A list of [roles](Role.md), with which the users
can use the emoji.
- `reason`, default : `None`. Shows up at the [guild](Guild.md)'s audit logs.

### `vanity_invite(self,guild)`

- `awaitable`
- returns : [`Invite`](Invite.md) / `None`

Returns the [guild](Guild.md)'s special vanity invite if it has. The guild must
have `VANITY` feature.

### `vanity_edit(self,guild,code,reason=None)`

- `awaitable`
- returns : `None`

Edits the [guild](Guild.md)'s special vanity invite. The guild must have
`VANITY` feature ith the given `code`. The `reason` shos up at the guild's
audit logs.

### `invite_create(self,channel,...)`

- `awaitable`
- returns : [`Invite`](Invite.md)
- raises : `ValueError`

Creates an [invite](Invite.md) from the given channel. The channel cannot be
[private](ChannelPrivate.md), [group](ChannelGroup.md) channel.

- `max_age`, default : `0`. After how much time in seconds will the invite
expire. `0` means it wont expire ever.
- `max_uses`, default : `0`. How much time can the invite be used. `0` means it
is unlimited.
- `unique`, default : `True`.
- `temporary`, default : `False`.

### `stream_invite_create(self,guild,user,...)`

- `awaitable`
- returns : [`Invite`](Invite.md)
- raises : `ValueError`

Creates an STREAM [invite](Invite.md) at the given [`guild`](Guild.md) for the
specific [`user`](User.md). The user must be streaming at the
[guild](Guild.md), when the invite is created.

The other passed argumnets are same, as for
[`.invite_create(...)`](#invite_createselfchannel).

### `invite_create_pref(self,guild,*args,**kwargs)`

- `awaitable`
- returns : [`Invite`](Invite.md) / `None`
- raises : `ValueError`

Chooses the prefered channel at the [guild](Guild.md) to create the invite from.
The [`.invite_create`](#invite_createselfchannel)'s arguments are passable too:

- `max_age`, default : `0`.
- `max_uses`, default : `0`.
- `unique`, default : `True`.
- `temporary`, default : `False`.

If the client can not create invite from the prefered channel, will return
`None`.

### `invite_get(self,invite_code,with_count=True)`

- `awaitable`
- returns : [`Invite`](Invite.md)

Returns a partial [`invite`](Invite.md) with the given code. `with_count`
argument enables you to see the online members of the guild an it's member
count.

### `invite_update(self,invite,with_count=True)`

- `awaitable`
- returns : `None`

Updates the [`invite`](Invite.md). Because this method uses the same endpoint
as [`.invite_get`](#invite_getselfinvite_codewith_counttrue) means if
`with_count` is set to `False` it wont even be able to update anything.

### `invite_get_guild(self,guild)`

- `awaitable`
- returns : `list`
- values : [`Invite`](Invite.md)

Requests the [`invites`](Invite.md) of the [guild](Guild.md) and return them.

### `invite_get_channel(self,channel)`

- `awaitable`
- returns : `list`
- values : [`Invite`](Invite.md)

Requests the [`invites`](Invite.md) of the channel and return them.

### `invite_delete(self,invite,reason=None)`

- `awaitable`
- returns : `None`

Deletes the [`invites`](Invite.md). The `reason` shows up at the
[guild](Guild.md)'s audit logs.

### `invite_delete_by_code(self,invite_code,reason=None)`

- `awaitable`
- returns : `None`

Deletes an [`invites`](Invite.md) by it's code and returns it. The `reason`
shows up at the [guild](Guild.md)'s audit logs.

### `role_edit(self,role,...)`

- `awaitable`
- returns : `None`
- raises : `ValueError`

Edits the [role](Role.md) with the given arguments.

- `name`, default : `None`. If set changes the role's name.
- `color`, default : `None`. Needs to be `int` instance
([`Color`](Color.md) for example). If a role has color `0` means it will be
ignored at user color calculation.
- `separated`, default : `None`. Users are separated by their highest
`.separated==True` role.
- `mentionable`, default : `None`.
- `permissions`, default : `None`. [Permission](Permission.md) or any int
instance object.
- `position`, default : `0`. If changed moves the role. `@everyone` role is
position `0` and it is unmovable.
- `reason`, default : `None`. Shows up at the [guild](Guild.md)'s audit logs.

### `role_delete(self,role,reason=None)`

- `awaitable`
- returns : `None`

Deletes the role. The reason shows up at the [guild](Guild.md)'s audit logs.

### `role_create(self,guild,...)`

- `awaitable`
- returns : [`Role`](Role.md)
- raises : `ValueError`

Creates a [role](Role.md) at the [guild](Guild.md).

- `name`, default : `None`.
- `color`, default : `None`. Needs to be `int` instance
([`Color`](Color.md) for example). If a role has color `0` means it will be
ignored at user color calculation.
- `separated`, default : `None`. Users are separated by their highest
`.separated==True` role.
- `mentionable`, default : `None`.
- `permissions`, default : `None`. [Permission](Permission.md) or any int
instance object.
- `reason`, default : `None`. Shows up at the [guild](Guild.md)'s audit logs.

### `role_move(self,role,position,reason=None)`

- `awaitable`
- returns : `None`
- raises: `ValueError`

Moves the [role](Role.md) to the set position. The `reason` shows up at the
[guild](Guild.md)'s audit logs.

> At the case of moving a default role to not position 0, or moving a non
> default role to position 0, raises `ValueError`.

### `role_reorder(self,roles,reason=None)`

- `awaitable`
- returns : `None`
- raises : `ValueError` / `TypeError`

Moves more [roles](Role.md) of a [guild](Guild.md) to the speicifed positions.
`roles` can be passed as `list` with ([`Role`](Role.md) / `position` (int))
tuples, or as a `dict` with the same items. 

Partial roles are ignored and if passed any, every role's position after it
is reduced. If there are roles passed with different guilds, then `ValueError`
will be raised. If there are roles passed with the same position, then their
positions will be sorted out.

The `reason` shows up at the [guild](Guild.md)'s audit logs.

> At the case of moving a default role to not position 0, or moving a non
> default role to position 0, raises `ValueError`.

### `relationship_delete(self,relationship)`

- `awaitable`
- returns : `None`
- user account only, not tested

Deletes a relation between you and the [user](User.md).

### `relationship_create(self,user,relation_type=None)`

- `awaitable`
- returns : `None`
- user account only, not tested

Creates a relation between you and the [user](User.md). `relation_type`
should be a [relationship type](RelationshipType.md) if set.

### `relationship_friend_request(self,user)`

- `awaitable`
- returns : `None`
- user account only, not tested

Sends a friend request towards the [user](User.md).

### `update_application_info(self)`

- `awaitable`
- returns : `None`

Updates the client's application info (`client.application`). By default it is
not loaded so calling it on login is a good idea.

### `hypesquad_house_change(self,house_id)`

- `awaitable`
- returns : `None`
- user account only, not tested

Switches the hypesquad to the selected house id (?).

### `hypesquad_house_leave(self)`

- `awaitable`
- returns : `None`
- user account only, not tested

Leaves from the client's current hypesquad house.

### `join_voice_channel(self,channel)`

- `awaitable`
- returns : [`VoiceClient`](VoiceClient.md)
- raises : `TimeoutError` / `RuntimeError`

Joins a voice client to the channel. If there is an already existing voice
client at the [guild](Guild.md) it moves it.

If not every library is installed, raises `RuntimeError`, or if the voice
client fails to connect raises `TimeoutException`.

### `request_member(self,guild,name,limit=1)`

- `awaitable`
- returns : `list`
- elements : [`User`](User.md) / [`Client`](Client.md)

Requests `limit` (1-1000) amount of users with the given `name` (2-32 length)
from the given [`guild`](Guild.md). This request might take longer, than
others, because it uses the [client](Client.md)'s gateway's websocket and not
it's http client. If no users are matched Discord does not returns anything,
so the method returns an empty list only when the timeout occurs.

### `disconnect(self,channel)`

- `awaitable`
- returns : `None`

Disconnects the client and closes it's wewbsocket and http client too. This
might take even more than 1 minute, because bot accounts can not logout, so
they need to wait for timeout.

## Methods

### `start(self)`

- returns : `None` / `Task` / `TaskAsyncWrapper`
- raises : `RuntimeError`

Starts the clients's connecting to Discord. If the client is already running,
raises `RuntimeError`.

The return of the method depends on the thread, from which it was called
from.

| called from                           | return                                                                                                    |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------|
| The client's event thread (`KOKORO`)  | Returns an **awaitable** `Task` created from the [`self._connect`](#connectself-method)                   |
| EventThread, but not the client's     | Returns an **awaitable** `TaskAsyncwWapper`, so connecting can be awaited from the other thread as well.  |
| Any other thread                      | Returns `None`, because syncwraps and waits the connecting task.                                          |

### `is_owner(self, user)`

- returns : `bool`
- values : `True` / `False`

Returns if the passed [user](User.md) is one of the bot's owners.

### `voice_client_for(self,message)`

- returns : `None` / [`VoiceClient`](VoiceClient.md)

Returns the voice client for the [message](Message.md)'s [guild](Guild.md) or
`None`.

### `get_guild(self,name)`

- returns : `None` / [`Guild`](Guild.md)

Tries to find the [`guild`](Guild.md) by it's name. If there is no guild with
the given nam returns `None`.

### `get_ratelimits_of(self, group, limiter=None, keep_alive=False)`

- returns : `RatelimitProxy`
- raises : `RuntimeError` / `TypeError` / `RuntimeError`

Returns a proxy to the specified `ratelimit group` bound to that specific
limiter.

> Experimental.

## Internal

### `_init_on_ready(self,data)` (method)

- returns : `None`

Fills up the client's instance attributes on login. If there is an already
existing [User](User.md)(!) object with the same id, the client will replace it at
channel participans, at `USERS` weakreference dictionary, at `guild.users` and
at permission overwrites. This replacing is avoidable, if at the creation of the
client the `client_id` argument is set.

### `_delete(self)` (method)

- returns : `None`
- raises : `RuntimeError`

Cleares the client's references. If called when the client is still running,
then raises `RuntimeError`.

### `client_login_static(self)` (method)

- `awaitable`
- returns : `None`

The client uses this method to login with client token.

### `_create_file_form(data,file)` (staticmethod)

- returns : `Formdata` / `None`
- raises : `ValueError` / `TypeError`

Creates a `multipart/form-data` form from the message + file data.
If there is no files to send, will return `None`, to tell the caller, that
nothing is added to the overall data.

`file` can be:
- `dict` with `filename`, `io` items.
- `list` with `(filename, io,)` or with `io` elements.
- `tuple`, a `(filename, io)` pair.
- `io` itself.

Accepted `io` types with check order:
- `BodyPartReader` instance
- `bytes`, `bytearray`, `memoryview` instance
- `str` instance
- `BytesIO` instance
- `StringIO` instance
- `TextIOBase` instance
- `BufferedReader`, `BufferedRandom` instance
- `IOBase` instance
- [`AsyncIO`](AsyncIO.md) instance
- `StreamReader` instance
- `async iterable`

Raises `TypeError` at the case of invalid `io` type .

There are two predefined datatypes specialized to send files:
- [ReuBytesIO](ReuBytesIO.md)
- [ReuAsyncIO](ReuAsyncIO.md)

If a request is sent, the buffer is closed. So if the request fails, we would
not be able to resend the file, except if we have a datatype, what instead of
closing on `.close()` just seeks to 0 (or later if needed) on close, instead of
really closing instantly. These datatypes implement a `.real_close()` method,
but they `real_close` on `__exit__` too.

### `_parse_allowed_mentions(allowed_mentions)` (staticmethod)

- returns : `dict`
- raises : `ValueError`

If `allowed_mentions` is passed as `None`, then returns a `dict`, what will
cause all mentions to be disabled.

If passed as an `iterable`, then it's elements will be checked. They
can be either type `str` (any value from `('everyone', 'users', 'roles')`),
[`UserBase`](UserBase.md) instances or [`Role`](Role.md) instances.

Passing `everyone` will allow the message to mention `@everyone` (permissions
can overwrite this behaviour).

Passing `users` will allow the message to mention all the users, meanwhile
passing [`UserBase`](UserBase.md) instances allow to mentioned the respective
users. Using `users` and [`UserBase`](UserBase.md) instances is mutually
exclusive, and the wrapper will register only `users` to avoid getting
[`DiscordExcepton`](DiscordException.md).

`roles` and [`Role`](Role.md) instances follow the same rules as `users` and
the [`UserBase`](UserBase.md) instances.

### `client_gateway(self,encoding='json',v=6,zlib=True)` (method)

- `awaitable`
- returns : `str`
- raises : `ConnectionError`

Requests and returns the client's gateway url.

### `connect(self)` (method)

- `awaitable`
- returns : `None`

Connects the client, fills up the undefined events and creates the task, what
will keep receiving the data from Discord ([`_connect`](#_connectself-method)).

### `_connect(self)` (method)

- `awaitable`
- returns : `None`

Receives the data from websocket, calls dispatch events, reconnects,
disconnects.

### `_delay_ready(self)` (method)

- `awaitable`
- returns : `None`

Delays the client's "ready" till it receives all the data about it's guilds.
If caching is not disallowed, then we wait additional time, till the client
requests all the members of it's [guilds](Guild.md).

### `_request_members2(self,guilds)` (method)

- `awaitable`
- returns : `None`

Requests the members of the large [guilds](Guild.md) at startup.

### `_request_members(self,guild)` (method)

- `awaitable`
- returns : `None`

Requests the members of [guild](Guild.md).

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the client and returns it's old attribtes in
(`attribute name`, `old value`) items.

### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the client with simply overwriting it's old attributes.

### `_update_profile_only(self,data,guild)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Used only when user caching is disabled. Updates the client's
[guild profile](GuildProfile.md) for the given [guild](Guild.md).

### `_update_profile_only_no_return(self,data,guild)` (method)

- returns : `None`

Familiar to [`.update_profile_only`](#_update_profile_onlyselfdataguild-method),
but it does not checks changes, so returns `None` instead of them.

### `_freeze_voice(self)` (method)

- returns : `None`

Freezes all the [`.voice_clients`](#voice_clients) of the client.

### `_freeze_voice_for(self,gateway)` (method)

- returns : `None`

Freezes all the [`.voice_clients`](#voice_clients) of a specific `gateway`
of the client.

### `_unfreeze_voice(self)` (method)

- returns : `None`

Unfreezes all the [`.voice_clients`](#voice_clients) of the client.

### `_unfreeze_voice_for(self,gateway)` (method)

- returns : `None`

Unfreezes all the [`.voice_clients`](#voice_clients) of a specific `gateway`
of the client.

### `_gateway_for(self,guild)` (method)

- returns : [`DiscordGateway`](DiscordGateway.md)

Returns the coresponding gateway of the specific [`guild`](Guild.md).

> The passed `guild` can be `None`.


