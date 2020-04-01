# class `IntentFlag`

An `int` subclass representing the intents to receive specific events. The
wrapper picks these up as well and optimizes the dispatch events' parsers.

- Source : [parsers.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/parsers.py)

##### Intents and their parsers

| Intent flag postion name  | Shift value   | intent name           | Coresponding parser                                                                                                                                                                       |
|---------------------------|---------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| INTENT_GUILDS             | 0             | guilds                | GUILD_CREATE<br>GUILD_DELETE<br>GUILD_UPDATE<br>GUILD_ROLE_CREATE<br>GUILD_ROLE_UPDATE<br>GUILD_ROLE_DELETE<br>CHANNEL_CREATE<br>CHANNEL_UPDATE<br>CHANNEL_DELETE<br>CHANNEL_PINS_UPDATE  |
| INTENT_GUILD_USERS        | 1             | guild_users           | GUILD_MEMBER_ADD<br>GUILD_MEMBER_UPDATE<br>GUILD_MEMBER_REMOVE                                                                                                                            |
| INTENT_GUILD_BANS         | 2             | guild_bans            | GUILD_BAN_ADD<br>GUILD_BAN_REMOVE                                                                                                                                                         |
| INTENT_GUILD_EMOJIS       | 3             | guild_emojis          | GUILD_EMOJIS_UPDATE                                                                                                                                                                       |
| INTENT_GUILD_INTEGRATIONS | 4             | guild_integrations    | GUILD_INTEGRATIONS_UPDATE                                                                                                                                                                 |
| INTENT_GUILD_WEBHOOKS     | 5             | guild_webhooks        | WEBHOOKS_UPDATE                                                                                                                                                                           |
| INTENT_GUILD_INVITES      | 6             | guild_invites         | INVITE_CREATE<br>INVITE_DELETE                                                                                                                                                            |
| INTENT_GUILD_VOICE_STATES | 7             | guild_voice_states    | VOICE_STATE_UPDATE                                                                                                                                                                        |
| INTENT_GUILD_PRESENCES    | 8             | guild_presences       | PRESENCE_UPDATE                                                                                                                                                                           |
| INTENT_GUILD_MESSAGES     | 9             | guild_messages        | MESSAGE_CREATE<br>MESSAGE_UPDATE<br>MESSAGE_DELETE<br>MESSAGE_DELETE_BULK                                                                                                                 |
| INTENT_GUILD_REACTIONS    | 10            | guild_reactions       | MESSAGE_REACTION_ADD<br>MESSAGE_REACTION_REMOVE<br>MESSAGE_REACTION_REMOVE_ALL<br>MESSAGE_REACTION_REMOVE_EMOJI                                                                           |
| INTENT_GUILD_TYPINGS      | 11            | guild_typings         | TYPING_START                                                                                                                                                                              |
| INTENT_DIRECT_MESSAGES    | 12            | direct_messages       | CHANNEL_CREATE<br>CHANNEL_PINS_UPDATE<br>MESSAGE_CREATE<br>MESSAGE_UPDATE<br>MESSAGE_DELETE                                                                                               |
| INTENT_DIRECT_REACTIONS   | 13            | direct_reactions      | MESSAGE_REACTION_ADD<br>MESSAGE_REACTION_REMOVE<br>MESSAGE_REACTION_REMOVE_ALL<br>MESSAGE_REACTION_REMOVE_EMOJI                                                                           |
| INTENT_DIRECT_TYPINGS     | 14            | direct_typings        | TYPING_START                                                                                                                                                                              |

> Parsers, which are not listed, are handled every time.

## factory methods and properties

### `receives_{intent_name}` (property)

- returns : `int`
- values : `0` / `1`

Returns whether the specific flag of the intent is enabled.

### `deny_{intent_name}` (method)

- returns : [`IntentFlag`](IntentFlag.md)

Creates a new intent with that specific flag denied.

### `allowed_{intent_name}` (method)

- returns : [`IntentFlag`](IntentFlag.md)

Creates a new intent with that specific flag allowed.

## Methods

### `keys(self)`

- yields : `str`

Yields every intent's name, what the [`IntentFlag`](IntentFlag.md) includes.

### `values(self)`

- yields : `str`

Yields every intent's position, what the [`IntentFlag`](IntentFlag.md) includes.

### `items(self)`

- yields : (`str`, `int`)

Yields every intent's name and `0` or `1`, depending if the
[`IntentFlag`](IntentFlag.md) object includes.

### `iterate_parser_names(self)`

- yields : `str`

Yields every parser's name, what the [`IntentFlag`](IntentFlag.md) allows to
be received.

> Can yield the same name twice.

###`update_by_keys(self,**kwargs)`

- returns : [`IntentFlag`](IntentFlag.md)
- raises : `KeyError`

Creates a new [`IntentFlag`](IntentFlag.md), what is modified with the
speicifed intent names and values (`True` or `False` prefered) based on the
current one.

> Raises `KeyError` on invalid keyword.

## Magic Methods

### `__new__(cls,int_)`

- returns : [`IntentFlag`](IntentFlag.md)

Creates a new [`IntentFlag`](IntentFlag.md) object from a passed `int`
subclass instance. If any invalid intent flag is passed, those will be
removed. if the wrapper is started up without presence caching, then
`.guild_presences` will be set to `False` every time.

### `__repr__(self)`

- returns : `str`

Returns the representation of the intent flag.

### `__getitem__(self,key)`

- returns : `int`
- values : `0`, `1`

Returns whether the client received data from the pecific ontent
The `key` should be passed as type `str`, as one of the intent's name.

### `__iter__(self)`

- yields : `str`

Returns each intent's name, which are included within the intent flag.


