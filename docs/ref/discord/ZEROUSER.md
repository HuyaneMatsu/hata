# class `MessageReference`

The default [user](User.md) object, what s used at some cases, when a user is
not defined, but it is required.

- Source : [message.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/discord/message.py)

| attribute names       | attribute values              |
|-----------------------|-------------------------------|
| id                    | 0                             |
| name                  | ''                            |
| discriminator         | 0                             |
| avatar                | 0                             |
| has_animated_avatar   | False                         |
| guild_profiles        | { }                           |
| is_bot                | True                          |
| partial               | True                          |
| activities            | [ ]                           |
| status                | [Status.offline](Status.md)   |
| statuses              | { }                           |

> If presence or user caching is disabled, the last 3 attributes are not set,
because at that case properties are used instead.
