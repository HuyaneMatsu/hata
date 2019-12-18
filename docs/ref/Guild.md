# class `Guild`

- source : [guild.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/guild.py)

## Instance attributes

When a guild is loaded for first time, it might not have some attributes set
to ther correct value. These are the following:
- [`embed_channel`](#embed_channel)  
- [`embed_enabled`](#embed_enabled)
- [`max_presences`](#max_presences)
- [`max_users`](#max_users)
- [`widget_channel`](#widget_channel)
- [`widget_enabled`](#widget_enabled)
    
### `afk_channel`

- type : `NoneType` / [`ChannelVoice`](ChannelVoice.md)
- default : `None`

The afk channel of the guild if it has, else `None`.

### `afk_timeout`

- type : `int`

The afk timeout at the [`afk_channel`](#afk_channel). Can be 60, 300, 900,
1800, 3600 in seconds.

### `all_channel`

- type : `dict`
- items : (`int`, [`guild channel`](ChannelGuildBase.md))
    
All the channel of the guilds with (`channel_id`, `Channel`) item pairs.

### `all_role`

- type : `dict`
- items : (`int`, [`Role`](Role.md))

All the role of the guild with (`role_id`, `Role`) item pairs.

### `avaiable`

- type : `bool`
- values : `True` / `False`
- defualt : `False`

Is the guild avaiable or not.

### `banner`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The guilds's banner's hash. if the guild has no banner, then the attribute is
set to `0`.

### `booster_count`

- type : `int`
- default : `0`

The total number of users currently boosting the guild with their Nitro.

### `channels`

- type : `weakposlist`
- values : [`Guild Channels`](ChannelGuildBase.md)

The guild's channel in sorted form. The channels under the
[group channels](ChannelGroup.md) are not listed, but those are listen under
the category's `.channel` attribute.

### `clients`

- type : `list`
- values : [`Client`](Client.md)

A list of loaded cleints, which are the member of the guild. If the guild has
no clients, then it is partial.

### `content_filter`

- type : [`ContentFilterLevel`](ContentFilterLevel.md)
- default : `ContentFilterLevel.disabled`

The explicit content filter level of the guild.

### `description`

- type : `str`
- defaut : `''` (empty str)

Description for the guild.

### `discovery_splash`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The guilds's discovery splash's hash. The guild must have `DISCOVERABLE`
feature to have discovery splash. If the guild has no discovery splash, this
attribute is set to `0`.

### `embed_channel`

- type : `NoneType` / [`ChannelText`](ChannelText.md)
- default : `None`

The channel where the guild's embed widget will generate the invite to.

### `embed_enabled`

- type : `bool`
- values : `True` / `False`
- defualt : `False`

If the guild embeddable. (Linked to [`embed_channel`](#embed_channel).)

### `emojis`

- type : `dict`
- items : (`int`, [`Emoji`](Emoji.md))

All the emojis of the guild with (`emoji_id`, `Role`) item pairs.

### `features`

- type : `list`
- values : [`GuildFeature`](GuildFeature.md)

The guild's features, like `INVITE_SPLASH` or `VIP_REGIONS`

### `has_animated_icon`

- type : `bool`
- values : `True` / `False`

### `icon`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The guilds's icon's hash. If the guild has no icon, then the attribute
is set to `0`.

### `id`

- type : `int`
- lenght : 64 bit
- Discord side : [`snowflake`](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#snowflakes)
    
The guild's unique identificator number.

### `is_large`

- type : `bool`
- values : `True` / `False`
- default : `False`

A guild is large if it has more members than 250, or if `'large': True` is sent
with the guild's data. If a guild is large, then we requests it's members,
because it is not sent with the guild's data.

### `max_users`

- type : `int`
- default : `250000`

The maximal amount of users for the guild.

### `max_presences`

- type : `int`
- default : 5000

The maximal amount of presences for the guild.

### `message_notification`

- type : [`MessageNotificationLevel`](MessageNotificationLevel.md)

The recommended message notification is :
`MessageNotificationLevel.only_mentions`.

### `mfa`

- type: [`MFA`](MFA.md)

The required Multi-factor authentication level for the guild.

### `name`

- type : `str`

The name of the guild. It's lenght can be between 2 and 100.

### `owner`

- type : [`User`](User.md) / [`Client`](Client.md)

The owner of the guild.

### `preferred_locale`

- type : `str`
- default : `'en-US'`

The preferred language of the guild.

### `premium_tier`

- type : `int`
- values : `0`, `1`, `2`, `3`
- defualt : `0`

The guilds premium tier. More sub means higher tier.

### `region`

- type : [`VoiceRegion`](VoiceRegion.md)

The voice region of the guild.

### `roles`

- type : `autoposlist`
- values : [`Role`](Role.md)

A list containing the guild's roles in sorted form. The first role has the
lowest position and the last has the highest. (So on the reversed way as at 
the official discord client shows them up.) The first role is `@everyone`
every time and it can not be moved from position 0 either.

### `rules_channel`

- type : `NoneType` / [`ChannelText`](ChannelText.md)
- default : `None`

The channel where the rules of a discoverable guild's should be. The guild
must have `DISCOVERABLE` feature.

### `splash`

- type : `int`
- lenght : 128 bit
- default : `0`
- Discord side : [image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)

The guilds's splash's hash. if the guild has no splash, then the attribute is
set to `0`. The guild must have `INVITE_SPLASH` feature.

### `system_channel`

- type : `NoneType` / [`ChannelText`](ChannelText.md)
- default : `None`

The channel where the system messages are sent.

### `system_channel_flags`

- type : [`SystemChannelFlag`](SystemChannelFlag.md)
- default : `SystemChannelFlag.all`

The flags, which describe, which type of messages are sent automatically to the
system channel of the guild.

### `user_count`

- type : `int`
- default : `1`

The amount of users at the guild. If the guild is large, then this attribute
is set before it's users all loaded.

### `users`

- type : dict
- items : (`int`, [`User`](User.md) / [`Client`](Client.md))

All the users at the guild with (`user_id`, `User`) items.

### `verification_level`

- type : [`VerificationLevel`](VerificationLevel.md)

The minimal verification needed to join to guild.

### `vanity_url_code`

- type : `str`
- default : `''` (empty string)

The guild's vanity invite's code if it has.

### `voice_states`

- type : `dict`
- items : (`int`, [`VoiceState`](VoiceState.md))

Each [`user`](User.md) at a [voice channel](ChannelVoice.md) of the guild has a
voice state. The `voice_states` contains (`user_id`, `VoiceState`) items.

### `webhooks`

- type : `dict`
- items : (`int`, [`Webhook`](Webhook.md))

If the webhooks of the guild are requeste, then they are stored at this
attribute as (`user_id`, `VoiceState`) items. This container is updated only
on new request.

### `webhooks_uptodate`

- type : `bool`
- values : `True` / `False`
- default : `False`

If we are sure all of the webhooks of the guild's are up to date, then this
attribute is set to `True`. Various [`Client`](Client.md) methods use this
argument to save API requests. 

### `widget_channel`

- type : `NoneType` / [`ChannelText`](ChannelText.md)
- default : `None`

The channel for the guild's widget.

### `widget_enabled`

- type : `bool`
- values : `True` / `False`
- defualt : `False`

Wheter the guild widget is enabled. (Linked to
[`widget_channel`](#widget_channel).)

## Properties

### `banner_url`

- returns : `str` / `None`
- default : `None`

Returns the guild's banner's url. If the guild has no banner, then returns
`None`.

### `bitrate_limit`

- returns : `int`

The maximal bitrate to set at the voice channels of the guild.

### `category_channels`

- returns : `list`
- values : [`Category_channel`](ChannelCategory.md)

Returns all the category channels (type 4) of the guild.

### `created_at`

- returns : `datetime`

Returns the guild's creation time.

### `default_role`

- returns : [`Role`](Role.md)

Returns the default role of the guild (@everyone).

### `discovery_splash_url`

- returns : `str` / `None`
- default : `None`

Returns the guild's discovery splash's url. If the guild has no discovery
splash, then returns `None`.

### `embed`

- returns : [`GuildEmbed`](GuildEmbed.md)

Returns the guild's embed.

### `emoji_limit`

- returns : `int`

The maximal amount of emojis, what the guild can have.

### `icon_url`

- returns : `str` / `None`
- default : `None`

Returns the guild's icon's url. If the guild has no icon, then it
returns `None`.

### `messageable_channels`

- retturns : `list`
- values : [`ChannelText`](ChannelText.md)

Returns all the messageable channels (type 0 and 5) of the guild.

### `news_channels`

- returns : `list`
- values : [`ChannelText`](ChannelText.md)

Returns all the guild new channels (type 5) of the guild.

### `partial`

- returns : `bool`
- values : `True` / `False`

A guild which has no client is partial.

### `splash_url`

- returns : `str` / `None`
- default : `None`

Returns the guild's splash's url. If the guild has no splash, then returns
`None`.

### `store_channels`

- returns : `list`
- values : [`ChannelStore`](ChannelStore.md)

Returns all the store (type 6) channels of the guild.

### `text_channels`

- returns : `list`
- values : [`ChannelText`](ChannelText.md)

Returns all the text channels (type 0) of the the guild.

### `upload_limit`

- returns : `int`

The maximal size of files, which can be uploaded to the guild's channels.

### `voice_channels`

- returns : `list`
- values : [`ChannelVoice`](ChannelVoice.md)

Returns all the voice channels (type 2) of the guild.

### `widget_json_url`

- returns : `str`

Returns a json url for requesting the guild's widget.

## Classmethods

### `precreate(cls,guild_id,**kwargs)`

- returns : [`Guild`](Guild.md)
- raises : `AttributeError` / `TypeError`

Tries to query the given Guild from the existing ones. If it fails, it creates
the guild with the given kwargs and with the given ID. Precreated guilds are
created as partial, so when they will get loaded first time, they will have
it's attributes replaced.

Some attributes are set automatically or processed from kwargs:
- [`banner`](#banner) : default is `0`, accepts `None`,
[image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)
and `int`.
- [`icon`](#icon) : default is `0`, accepts `None`,
[image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)
and `int`.
- [`has_animated_icon`](#has_animated_icon) : default is `False`.
- [`name`](#name) : default is `''`.
- [`splash`](#splash) : default is `0`, accepts `None`,
[image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)
- [`discovery_splash`](#discovery_splash) : default is `0`, accepts `None`,
[image hash](https://github.com/discordapp/discord-api-docs/blob/master/docs/Reference.md#cdn-endpoints)
and `int`.

## Methods

### `banner_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

If the guild has no banner, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

### `icon_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `valueError`

If the guild has no icon, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'. If the guild has
animated avatar it can be 'gif' too. Valid sizes: 16, 32, 64, 128, 256,
512, 1024, 2048, 4096.

### `splash_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `valueError`

If the guild has no splash, then returns `None`

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

### `discovery_splash_url_as(self,ext=None,size=None)`

- returns : `str` / `None`
- default : `None`
- raises : `ValueError`

If the guild has no discovery splash, then returns `None`.

Valid extensions: 'jpg', 'jpeg', 'png', 'webp'.
Valid sizes: 16, 32, 64, 128, 256, 512, 1024, 2048, 4096.

### `embed_url(self,style='shield')`

- returns : `str`
- raises : `ValueError`

Returns the guild's embed image's url in `.png` format.
Requesting this url requires no authentication.

Style options:

- [`shield`](https://discordapp.com/api/guilds/81384788765712384/embed.png?style=shield)
- [`banner1`](https://discordapp.com/api/guilds/81384788765712384/embed.png?style=banner1)
- [`banner2`](https://discordapp.com/api/guilds/81384788765712384/embed.png?style=banner2)
- [`banner3`](https://discordapp.com/api/guilds/81384788765712384/embed.png?style=banner3)
- [`banner4`](https://discordapp.com/api/guilds/81384788765712384/embed.png?style=banner4)

### `widget_url(self,style='shield')`

- returns : `str`
- raises : `ValueError`

Returns the guild's widget image's url in `.png` format.
Requesting this url requires no authentication.

Style options:

- [`shield`](https://discordapp.com/api/guilds/81384788765712384/widget.png?style=shield)
- [`banner1`](https://discordapp.com/api/guilds/81384788765712384/widget.png?style=banner1)
- [`banner2`](https://discordapp.com/api/guilds/81384788765712384/widget.png?style=banner2)
- [`banner3`](https://discordapp.com/api/guilds/81384788765712384/widget.png?style=banner3)
- [`banner4`](https://discordapp.com/api/guilds/81384788765712384/widget.png?style=banner4)

### `get_user(self,name,default=None)`

- returns : `default` / [`User`](User.md) / [`Client`](Client.md)

Tries to find the user by it's name. If it cant returns the `default` value.
The search order is:

- user's full name (if detected)
- user's name
- user's nick

### `get_user_like(self,name,default=None)`

- returns : `default` / [`User`](User.md) / [`Client`](Client.md)

Tries to find a user of the guild, who's name or nick starts like the passed
one. Returns the first matched user. If no users are matched, returns the
`default` value.

### `get_users_like(self,name)`

- returns : `list`
- elements : [`User`](User.md) / [`Client`](Client.md)

Tries to find all the users of the guild, who's name or nick starts like the
passed one.

### `get_users_like_ordered(self,name)`

- returns : `list`
- elements : [`User`](User.md) / [`Client`](Client.md)

Tries to find all the users of the guild, who's name or nick starts like the
passed one. The result is ordered on the same way as Discord orders them when
calling [`Client.request_memebers`](Client.md/#request_memebers).

### `get_emoji(self,name,default=`None`)`

- returns : `default` / [`Emoji`](Emoji.md)

Tries to find the emoji by it's name. If it cant returns the `default` value.

### `get_channel(self,name,defualt=None)`

- returns : `default` / [`Channel`](CHANNEL_TYPES.md)

Tries to find the channel by it's name. If it cant returns the `default` value.

### `get_role(self,name,defualt=None)`

- returns : `default` / [`Role`](Role.md)

Tries to find the role by it's name. If it cant returns the `default` value.

### `permissions_for(self,user)`

- returns : [`Permission`](Permission.md)
- default : `Permissions.permission_none`

Returns the permissions at the guild for the given [`user`](User.md). If the
user is a [`webhook`](Webhook.md) of the guild, then returns the guild's
default role's permissions. Else the user has no permissions at the guild,
returns `Permissions.permission_none`.

### `cached_permissions_for(self,user)`

- returns : [`Permission`](Permission.md)
- default : `Permissions.none`

Returns the permissions for the user if cached. If not generates and stores it
at the [.`_cache_perm`](#_cache_perm-instance-attribute) instance attribute.

## Magic methods

### `__hash__(self)`

- returns : `int`
- size : 64 bit

Returns the guild's hash value, which equals to it's id.

### `__str__(self)`

- returns : `str`

Returns the guild's name.

### `__repr__(self)`

- returns : `str`

Returns the representation of the guild.

### `__format__(self,code)`

- returns : `str`

```python
f'{guild}' #-> guild.name
f'{guild:c}' #-> guild.created_at with '%Y.%m.%d-%H:%M:%S' format
```

Raises `ValueError` on invalid format code.

### `__gt__`, `__ge__`, `__eq__`, `__ne__`, `__le__`, `__lt__`

Compares the two guild's id. If two object has same id, then their type must
match too.

## Internal

### `__new__(cls,data,client)` (magic method)

- returns : [`Guild`](Guild.md)

Tries to find the guild from the already existing ones. If it can not find it
creates a new one. If the guild is partial (or freshly created) sets it's
attributes from the passed `data`. If the the guild is not added to the
client's guilds yet, then it adds the guild to them, and the client to the
guilds's clients.

### `_update_embed(self,data)` (method)

- returns : `None`

On requesting a guild's embed it gets updated.

### `_delete(self,client=None)` (method)

- returns `None`

If a [client](Client.md) leaves from the guild, then the client will get
deleted from the guild's clients and the guild will get deleted from the
client's guilds and from it's [`guild profile`](GuildProfile.md). If a guild
loses all of it's clients, then the guild will become partial, which means it
will lose it's channels, emojis, roles, users and the users will lose their
guild profiles too.

### `_update_voice_state(self,data,user)` (method)

- returns: `None` / ([`VoiceState`](VoiceState.md), `str`, `None` / `dict`)

Called by dispatch event. Updates the voice for the [`user`](User.md) with the
given `data`. If the `VoiceState` is already deleteted or updated the method
returns `None`. Else it returns 3 objects:

0.: `voices_tate` - the corecsponding voice state.

1.: `action` - `l` for leave, `j` for join and `u` for update.

2.: `old` - On voice state update it is the a `dict` containing the state's old
attributes in (attribute name, old value) pairs.

### `_update_voice_state_restricted(self,data,user)` (method)

- returns: `None` / `_spaceholder` / [`ChannelVoice`](ChannelVoice.md)

Familiar to [`._update_voice_state`](#_update_voice_stateselfdatauser-method),
but it returns only a reprezentation of the action. `None` is nothing
happened, `_spaceholder` at the case of leave, or the channel of the state
anyways.

### `_sync(self,data,client)` (method)

- returns : `None`

Called when we get a guild's data after a guild sync request. This method calls
multyple syncing submethods to apply changes.

### `_apply_presences(self,data)` (method)

- returns : `None`

Applies to the guild's members the given presences sent with guild data.

### `_sync_channels(self,data,client)` (method)

- returns : `None`

Syncs the guild's [channels](CHANNEL_TYPES.md) with the given data.

### `_sync_roles(self,data)` (method)

- returns : `None`

Syncs the guild's [roles](Role.md) with the given data.

### `_sync_emojis(self,data)` (method)

- returns `None`

Syncs the guild's [emojis](Emoji.md) with the given data.

### `_update(self,data)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the guild and returns it's old attributes as (attribute name, old value)
pairs. A lot of attributes have their own dispatch events, so they are ignored.
Exception at the returned data is only [`features`](#features), because it is
calculated with [`listdifference`](listdifference.md) and the data contains the
function's return instead of the actual old value.

| name                      | description                                                                       |
|---------------------------|-----------------------------------------------------------------------------------|
| afk_channel               | [ChannelVoice](ChannelVoice.md) / None                                            |
| afk_timeout               | int                                                                               |
| available                 | bool                                                                              |
| banner                    | int                                                                               |
| booster_count             | int                                                                               |
| content_filter            | [ContentFilterLevel](ContentFilterLevel.md)                                       |
| description               | str                                                                               |
| discovery_splash          | int                                                                               |
| embed_channel             | [ChannelText](ChannelText.md) / None                                              |
| embed_enabled             | bool                                                                              |
| features                  | [listdifference](listdifference.md) return of [GuildFeature](GuildFeature.md)     |
| has_animated_icon         | bool                                                                              |
| icon                      | int                                                                               |
| max_presences             | int                                                                               |
| max_users                 | int                                                                               |
| message_notification      | [MessageNotificationLevel](MessageNotificationLevel.md)                           |
| mfa                       | [MFA](MFA.md)                                                                     |
| name                      | str                                                                               |
| owner                     | [User](User.md) / [Client](Client.md)                                             |
| preferred_locale          | str                                                                               |
| premium_tier              | int                                                                               |
| region                    | [VoiceRegion](VoiceRegion.md)                                                     |
| rules_channel             | [ChannelText](ChannelText.md) / None                                              |
| splash                    | int                                                                               |
| system_channel            | [ChannelText](ChannelText.md) / None                                              |
| system_channel_flags      | [SystemChannelFlag](SystemChannelFlag.md)                                         |
| vanity_code               | str                                                                               |
| verification_level        | [VerificationLevel](VerificationLevel.md)                                         |
| widget_channel            | [ChannelText](ChannelText.md) / None                                              |
| widget_enabled            | bool                                                                              |


### `_update_no_return(self,data)` (method)

- returns : `None`

Updates the guild and returns `None`.

### `_update_emojis(self,data)` (method)

- returns : `list`
- values : (`str`, [`Emoji`](Emoji.md), `dict` / `None`)

Updates the emojis of the guild and returns the changes. The returned `list`
contains tuples with 3 elements, which are the following:

0.: `action` - `n` for new, `e` for edit and `d` for deletion.

1.: `emoji` - The legend itself.

2.: `old` - If the emoji is edited, then it is a `dict` containing the emoji's
old attributes. At every other case it is `None`.

### `_boosters` (instance attribute)

- type : `NoneType` / `list`
- default : `None`

Cached slot for the boosters of the guild.

### `_cache_perm` (instance attribute)

- type : `dict`
- items : (`int`, [`Permission`](Permission.md))

Cached permissions stored by the
[`.cached_permissions_for`](#cached_permissions_forselfuser) method. When a
[role](Role.md) of the guild is updated or deleted of the guild, then the
cached permissions of it are cleared.

### `_from_GW_data(cls,data)` (classmethod)

- returns : [`Guild`](Guild.md)

Tries to find the guild by id. If fails creates a new one from the guild
widget data. A guild created by this method has only `id` and `name`.


