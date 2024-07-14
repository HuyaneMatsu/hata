# Introduction

Application command permissions are confusing, but what if you could test whether you set them correctly? Sounds scary?
It is!

Hata allows you to assert missmatch by dropping a warning (or more!) on startup.

## Getting started

When setting up the slash extension you can use the `assert_application_command_permission_missmatch_at` parameter to
define in which guild(s) you want to test missmatch.

```py3
Nitori = Client(
    TOKEN,
    extensions = 'slash',
    assert_application_command_permission_missmatch_at = TEST_GUILD,
)
```

## Setting command permissions

To set expected command permissions we use the `set_permission` decorator. This allows to add `1` specific permission
overwrite to the command. One is not much, but the limit is **1 hundred**, so there is to nothing to fear from!

The usage is pretty intuitive. *(or is it?)*. The decorator accepts 3 parameters:

| Name              | Type                                                                  | Description                                                   |
|-------------------|-----------------------------------------------------------------------|---------------------------------------------------------------|
| guild             | `Guild`, `int`                                                        | The guild where the overwrite is applied in.                  |
| target            | `ClientUserBase`, `Role`, `Channel`, `tuple` ((`str`, `type`), `int`) | The target entity. Can be either role, user or channel.       |
| allow             | `bool`                                                                | Whether the command should be allowed for the target entity.  |

The `target` parameter can be given in many ways to allow relaxing definitions:

| Description                                             | Example                   |
|---------------------------------------------------------|---------------------------|
| The entity itself.                                      | `Role.precreate(role_id)` |
| A `tuple` of the entity type and its identifier.        | `(Role, role_id)`         |
| A `tuple` of the entity type name and its identifier.   | `('role', role_id)`       |

Since the `everyone role` and `all channel` permission overwrites are unique, it is allowed to pass ID as `0` to
mention them directly instead of writing their ID out.

#### Setting command permissions / Usage

Here is a short example of disabling the permissions for everyone role, and enabling it to 1 specific role:

```py3
from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import Embed, elapsed_time, DATETIME_FORMAT_CODE
from hata.ext.slash import InteractionResponse, set_permission


@Nitori.interactions(guild = TEST_GUILD)
@set_permission(TEST_GUILD, ('role', 0), False)
@set_permission(TEST_GUILD, ('role', MODERATOR_ROLE_ID), True)
async def latest_users(event):
    """Shows the new users of the guild."""
    date_limit = DateTime.now(TimeZone.utc) - TimeDelta(days=7)
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        # `joined_at` might be set as `None` if the user is a lurker.
        # We can ignore lurkers, so use `created_at` which defaults to Discord epoch.
        created_at = user.guild_profiles[guild.id].created_at
        if created_at > date_limit:
            users.append((created_at, user))
    
    users.sort(reverse = True)
    del users[10:]
    
    embed = Embed('Recently joined users')
    if users:
        for index, (joined_at, user) in enumerate(users, 1):
            created_at = user.created_at
            embed.add_field(
                f'{index}. {user.full_name}',
                (
                    f'Id : {user.id}\n'
                    f'Mention : {user.mention}\n'
                    '\n'
                    f'Joined : {joined_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(joined_at)} ago*]\n'
                    f'Created : {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
                    f'Difference : {elapsed_time(RelativeDelta(created_at, joined_at))}'
                ),
            )
    
    else:
        embed.description = '*none*'
    
    return InteractionResponse(embed = embed, allowed_mentions = None)
```

![](assets/slash_0021.png)

## Setting guild level permissions

There is an option to set application command permission overwrites for all the commands in a guild.

> This is not applied to those which have their own specific overwrites. Discord ples.

Since we do not have a command to apply the decorator to, we will apply them to the client directly!
*It is like magic.*

### Setting guild level permissions / Usage

Here is an example, where the commands are enabled only in 1 channel of the guild:

```py3
from hata.ext.slash import set_permission

Nitori@set_permission(TEST_GUILD, ('channel', 0), False)
Nitori@set_permission(TEST_GUILD, ('channel', BOT_CHANNEL_ID), True)
```

> The matmul operator (the @) comes in handy when trying to keep syntax familiar.

## Enforcing permissions

If you want to make sure that the permissions defined in code are respected, the
`enforce_application_command_permissions` parameter will do that for you.

Even tho bots cannot edit their own command permissions, it's still an option to not link up command(s), thus denying
unexpected usage.

On the other hand, just because bots cannot do something, it does not mean it can't be done! If the bot is
**not owned by a team** the owner's OAuth2 access can be requested and with it, we can directly sync command permissions.

> This will only work in guilds where the owner has sufficient permissions to edit the commands from the client as well. 

```py
Nitori = Client(
    TOKEN,
    extensions = 'slash',
    assert_application_command_permission_missmatch_at = TEST_GUILD,
    enforce_application_command_permissions = True,
)
```
