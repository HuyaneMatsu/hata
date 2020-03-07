# module `checks`

Checks provided to be used, when adding a [command](Command.md) to a
[`CommandProcesser`](CommandProcesser.md).

- Source : [events.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events.py)

Each check accepts an `fail_identificator` argument when they are created,
what is returned when the check fails, and then it is passed to the command's
check failure handler.

`fail_identificator` can be passed as any non negative `int`.

#### list of checks

| name                              | extra argument        | description                                                                                                                       |
|-----------------------------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| has_role                          | role                  | Whether the author has the specific role.                                                                                         |
| owner_or_has_role                 | role                  | Whether the author is the owner of the client, or the specific role.                                                              |
| has_any_role                      | roles                 | Whether the author has any of the specified roles                                                                                 |
| owner_or_has_any_role             | roles                 | Whether the author is the owner of the client or has any of te specified roles.                                                   |
| guild_only                        |                       | Whether the command was called from a guild channel.                                                                              |
| private_only                      |                       | Whether the command was called from a private (or group) channel.                                                                 |
| owner_only                        |                       | Whether the athor is the owner of the client.                                                                                     |
| guild_owner                       |                       | Whether the author is the owner of the guild, where the command was called. (Fails at private channels.)                          |
| owner_or_guild_owner              |                       | Whether the author is the client's or the guild's owner. (Fails at private channels.)                                             |
| has_permissions                   | permissions           | Whether the author has the specified permissions at the source channel.                                                           |
| owner_or_has_permissions          | permissions           | Whether the author is the client's owner or has the specified permissions at the source channel.                                  |
| has_guild_permissions             | permissions           | Whether the author has the specified permissions at the channel's guild. (Fails at private channels.)                             |
| owner_or_has_guild_permissions    | permissions           | Whether the author is the client's owner or has the specified permissions at the channel's guild. (Fails at private channesls.)   |
| client_has_permissions            | permissions           | Whether the client has the specified permissions at the source channel.                                                           |
| client_has_guild_permissions      | permissions           | Whether the client has the specified permissions at the channel's guild. (Fails at private channels.)                             |
| is_guild                          | guild_id              | Whether the command was called at the specified guild.                                                                            |
| is_any_guild                      | guild_ids             | Whether the command was called from any of the specified guilds.                                                                  |
| custom                            | function              | Whether the passed function returns `True` or `False`                                                                             |
| is_channel                        | channel_id            | Whether the comamnd was called at the speicifed channel.                                                                          |
| is_any_channel                    | channel_ids           | Whether the command was called from any of the specified channels.                                                                |

> `role` can be passed as [`Role`](Role.md) or as an id of a role.

> `roles` can be passed as an `iterable` of [`Role`](Role.md) objects or role
> id-s.
> `permissions` can be passed as a [`Permission`](Permission.md) object, or as
> an `int` representing a permission.

> `guild_id` can be passed as a [`Guild`](Guild.md) object or as a guild's id.

> `guild_ids` can an `iterable` of [`Guild`](Guild.md) objects or guild id-s.

> `function` must accept 2 arguemnt, the [`client`](Client.md) and the
> [`message`](Message.md). The check passes, if the function returns an `int`,
> instance, what evaluates to `True`

> `channel_id` can be passed as any [channel](CHANNEL_TYPES.md) object,
> or as a channel's id.

> `channel_ids` can be passed as an `iterable` of any
> [channel](CHANNEL_TYPES.md) object or channel id-s.
