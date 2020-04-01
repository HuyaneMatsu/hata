# class `AuditLogChange`

Represents a change at an [`AuditLogEntry`](AuditLogEntry.md).

- Source : [audit_logs.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/audit_logs.py) 

## Instance attributes

##### Types of different attributes at cases

| attr                  | before's / after's description                            |
|-----------------------|-----------------------------------------------------------|
| account_id            | int                                                       |
| afk_channel           | [ChannelVoice](ChannelVoice.md)                           |
| allow                 | [Permission](Permission.md)                               |
| application_id        | int                                                       |
| avatar                | tuple (bool, int)                                         |
| bitrate               | int                                                       |
| channel               | [Guild channel](ChannelGuildBase.md)                      |
| code                  | str                                                       |
| color                 | [Color](Color.md)                                         |
| content_filter        | [ContentFilterLevel](ContentFilterLevel.md)               |
| days                  | int                                                       |
| deaf                  | bool                                                      |
| deny                  | [Permission](Permission.md)                               |
| enable_emoticons      | bool                                                      |
| expire_behavior       | int                                                       |
| expire_grace_period   | int                                                       |
| icon                  | tuple (bool, int)                                         |
| id                    | int                                                       |
| inviter               | [User](User.md) / [Client](Client.md)                     |
| mentionable           | bool                                                      |
| max_age               | int                                                       |
| max_uses              | int                                                       |
| message_notification  | [MessageNotificationLevel](MessageNotificationLevel.md)   |
| mfa                   | [MFA](MFA.md)                                             |
| mute                  | bool                                                      |
| name                  | str                                                       |
| nick                  | str                                                       |
| nsfw                  | bool                                                      |
| owner                 | [User](User.md) / [Client](Client.md)                     |
| position              | int                                                       |
| overwrites            | list of [PermOW](PermOW.md)                               |
| permissions           | [Permission](Permission.md)                               |
| region                | [VoiceRegion](VoiceRegion.md)                             |
| role                  | list of [Role](Role.md)                                   |
| separated             | bool                                                      |
| slowmode              | int                                                       |
| splash                | tuple (bool, int)                                         |
| system_channel        | [ChannelText](ChannelText.md)                             |
| temporary             | bool                                                      |
| topic                 | str                                                       |
| type                  | int                                                       |
| uses                  | int                                                       |
| vanity_code           | str                                                       |
| verification_level    | [VerificationLevel](VerificationLevel.md)                 |
| widget_channel        | [ChannelText](ChannelText.md)                             |
| widget_enabled        | bool                                                      |

> Every `before`and `after` can be `None` by default.

### `attr`

- type : `str`

The name of the attribute, what changed of the target entity.

### `before`

- type : `Any`
- default : `None`

The changed attribute's original value.

### `after`

- type : `Any`
- default : `None`

The changed attribute's new value.

## Magic methods

### `__repr__(self)`

- returns : `str`

Returns the [`AuditLogChange`](AuditLogChange.md)'s representation.
