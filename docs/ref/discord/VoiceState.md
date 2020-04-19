# class `VoiceState`

A `VoiceState` represents a user's at voice channel. It stores the
various information about the user, what other users can check aswell.

- Source : [user.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/user.py)

## Instance Attributes

| name          | type                                  | description                                                                           |
|---------------|---------------------------------------|---------------------------------------------------------------------------------------|
| channel       | [ChannelVoice](ChannelVoice.md)       | The voice channel, where the user is connected to.                                    |
| deaf          | bool                                  | Whether the user is deafen.                                                           |
| mute          | bool                                  | Whether the user is muted.                                                            |
| self_deaf     | bool                                  | Whether the user muted everyone else.                                                 |
| self_mute     | bool                                  | Whether the user muted itself.                                                        |
| self_stream   | bool                                  | Whether the user screen shares with the go live option.                               |
| self_video    | bool                                  | Whether the user sends video from a camera source                                     |
| session_id    | str                                   | The user's voice session id.                                                          |
| user          | [User](User.md) / [Client](Client.md) | The user at the voice channel.If user caching is disabled, it will be partial user.   |

> `channel` could be [`ChannelGroup`](ChannelGroup.md) or
[`ChannelPrivate`](ChannelPrivate.md), but bots cannot meet those.

## Properties

### `guild`

- returns : [`Guild`](Guild.md) / `None`

Returns the VoiceState's channel's guild.

## Magic method

### `__repr__(self)`

- returns : `str`

Returns the VoiceState's representation.

## Internal

### `__init__(self,data,channel)` (magic method)

Creates a VoiceState from the data given by Discord.

### `_update(self,data,channel)` (method)

- returns : `dict`
- items : (`str`, `Any`)

Updates the VoiceState and returns it's old attributes as (attribute name,
old value) pairs.

| name          | description                       |
|---------------|-----------------------------------|
| channel       | [ChannelVoice](ChannelVoice.md)   |
| deaf          | bool                              |
| mute          | bool                              |
| self_deaf     | bool                              |
| self_mute     | bool                              |
| self_stream   | bool                              |
| self_video    | bool                              |


### `_update_no_return(self,data,channel)` (method)

- returns : `None`

Familiar to [`._update`](#_updateselfdata-method), but instead of calculating
the differences and returning them, it just overwrites the attributes.


