# Commands (extension)

The last chapter was all about basic event handling and some example cases, but at this chapter we will look into one
of hata's extension, into `commands`. It is a higher level modular command framework.

All features of the extension can be setupped with using the `setup_ext_commands` function.

```py
from hata import Client, start_clients
from hata.ext.commands import setup_ext_commands

TOKEN = ''
NekoBot = Client(TOKEN)

setup_ext_commands(NekoBot, 'n!')

@NekoBot.commands
async def pat(client, message):
    await client.message_create(message.channel, 'Puurs !')

@NekoBot.commands
async def say(client, message, content):
    if content:
        await client.message_create(message.channel, content)

start_clients()
```

`setup_ext_commands` function accepts the following parameters:

| name                  | type                                          | default   | description                                                                                           |
|-----------------------|-----------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------|
| client                | `Client`                                      | -         | The client on what the extension will be setupped.                                                    |
| prefix                | `str` or `iterable` of `str` or `callable`    | -         | The prefix used for by the client's `CommandProcesser`                                                |
| ignorecase            | `bool`                                        | `True`    | Whether the prefixe's case should be ignored.                                                         |
| mention_prefix        | `bool`                                        | `True`    | Whether the client should accept it's mention at the start of the messages as an alternative prefix.  |
| default_category_name | `None` or `str`                               | `None`    | The CommandProcesser's default `Category`'s name.                                                     |
| category_name_rule    | `None` or `function`                          | `None`    | Function to generate display names for categories.                                                    |
| command_name_rule     | `None` or `function`                          | `None`    | Function to generate display names for commands.                                                      |

After the client is created and `setup_ext_commands` is called on it, commands can be registered to the it, with using
it's newly added `.commands` attribute as a decorator.

## Command Arguments

To every command at least 2 argument is passed: `client` and `message`. But you can add more arguments as well. The
extra arguments's annotations and default values will be checked and used up to generate content parser for the
command.

For example, if the command accepts 3 arguments and the last has annotation given as `User` type, then the command's
content parser will try to search for the user on local scope.
```
from hata import User

@NekoBot.commands
async def hug(client, message, user: User = None):
    if user is None:
        user = message.author
    
    await client.message_create(message.channel, f'Hugs {user:m} !')
```
If the user was not found and the argument has default value given as well, then that will be passed instead.

The supported types are the following:

| Type          | String representation | Alternative types                                                                                                                         |
|---------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| User          | 'user'                | UserBase                                                                                                                                  |
| Client        | 'client'              | N/A                                                                                                                                       |
| ChannelBase   | 'channel'             | ChannelGuildBase, ChannelTextBase, ChannelText, ChannelPrivate, ChannelVoice, ChannelGroup, ChannelCategory, ChannelStore, ChannelThread  |
| Role          | 'role'                | N/A                                                                                                                                       |
| Emoji         | 'emoji'               | N/A                                                                                                                                       |
| Guild         | 'guild'               | N/A                                                                                                                                       |
| Message       | 'message'             | N/A                                                                                                                                       |
| Invite        | 'invite'              | N/A                                                                                                                                       |
| str           | N/A                   | N/A                                                                                                                                       |
| int           | N/A                   | N/A                                                                                                                                       |
| timedelta     | 'tdelta'              | N/A                                                                                                                                       |
| relativedelta | 'rdelta'              | N/A                                                                                                                                       |
| N/A           | 'rest'                | N/A                                                                                                                                       |

Notes:
- If `'user'` is given as `UserBase`, then the parser behaviour will not be altered, it also means, that if it is given
    `User`, then it will still let trough the `Client`-s as well.
- If `'channel'` is given as a channel type, then every chanenl with different type will be ignored.
- For using `'rdelta'` converter, you must have `deateutil` installed.
- `'rest' converter returns the unused part of the message's content, till the first linebreak if applicable.

If you do not give annotations for the axtra parameters, then every of them (except the last) will be interpretered as
`str` parser, meanwhile the last of them will be interpretered as a `rest` parser. Tho, you can use `*args`, to
get as much object of the given as possible. If at the case of `*args` no annotation is given, then instead of `rest`
parser, it will be picked up as `str`.

```
@NekoBot.commands
async def separate(client, message, *args):
    if not args:
        result = 'Nothing to separate'
    else:
        result = ', '. join(args)
    await client.message_create(message.channel, result)
```
By default the parser separate the message's content by words, but you can use double quote to alter this behaviour:

| input	                            | output                                                |
|-----------------------------------|-------------------------------------------------------|
| `'Nekos are cute and fluffy.'`	| `'Nekos'`, `'are'`, `'cute'`, `'and'`, `'fluffy.'`    |
| `'Nekos are "cute and fluffy."'`	| `'Nekos'`, `'are'`, `'cute and fluffy.'`              |
| `'"Nekos are cute and fluffy."'`	| `'Nekos are cute and fluffy.'`                        |


You can alter the separating behaviour by giving `separator` parameter when adding a command.

```py
@NekoBot.commands(separator=',')
async def separate(client, message, *args):
    if not args:
        result = 'Nothing to separate'
    else:
        result = ', '. join(args)
    await client.message_create(message.channel, result)
```

or

```py
@NekoBot.commands(separator=('[', ']'))
async def separate(client, message, *args):
    if not args:
        result = 'Nothing to separate'
    else:
        result = ', '. join(args)
    await client.message_create(message.channel, result)
```

or

```py
@NekoBot.commands(separator=('*', '*'))
async def separate(client, message, *args):
    if not args:
        result = 'Nothing to separate'
    else:
        result = ', '. join(args)
    await client.message_create(message.channel, result)
```

`separator` can be given as a `str` instance with length of `1`, or as a `tuple` of `2` `str` instances with length
`1`.

Input-output examples:

| Separator     | Input	                                            | Output                                                                |
|---------------|---------------------------------------------------|-----------------------------------------------------------------------|
| `,`           | `'Reach for the Moon, Immortal Smoke'`	        | `'Reach for the Moon'`,`'Immortal Smoke'`                             |
| `('[', ']')`  | `'[Touhou vocal] Lost Emotion'`                   | `'[Touhou vocal]'`, `'Lost'`, `'Emotion'`                             |
| `('*', '*')`  | `'Legacy of Lunatic Kingdom *Pandemonic Planet*'` | `'Legacy'`, `'of'`, `'Lunatic'`, `'Kingdom'`, `'Pandemonic Planet'`   |


It also possible to customize parsers with `FlaggedAnnotation` or with `ConverterFlag`-s. For it, you need to import
them with `ConverterFlag` as well.

You can modify a `ConverterFlag` with it's `.update_by_keys` method, by giving a flag's name as keyword and it's new
value.

`ConverterFlag` implements the following flags:
| Name          | Description                                                                                                                       |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------|
| url           | Whether the entity should be parsed from it's url.                                                                                |
| mention       | Whether the entity should be parsed out from it's mention.                                                                        |
| name          | Whether the entity should be picked up by it's name.                                                                              |
| id            | Whether the entity should be picked up by it's name.                                                                              |
| everywhere    | Whether the entity should be searched out of the local scope. Mostly pairs with the `id` flag.                                    |
| profile       | User parser only. Can be used when user cache is disabled to esnure, that the user will have local guild profile if applicable.   |

There are already precreated flags for common usage, which are:

| Name              | Included flags                            |
|-------------------|-------------------------------------------|
| user_default      | mention, name, id                         |
| user_all          | mention, name, id, everywhere, profile    |
| client_all        | mention, name, id, everywhere             |
| role_default      | mention, name, id                         |
| role_all          | mention, name, id, everywhere             |
| channel_default   | mention, name, id                         |
| channel_all       | mention, name, id, everywhere             |
| emoji_default     | mention, name, id                         |
| emoji_all         | mention, name, id, everywhere             |
| guild_default     | id                                        |
| guild_all         | id, everywhere                            |
| message_default   | url, id                                   |
| message_all       | url, id, everywhere                       |
| invite_default    | url, id                                   |
| invite_all        | url, id                                   |

Note, if you use for example a `'user'` parser, then by default it will use the `user_default` flags, and it
will ignore everyting else than `user_all`.

Some parsers, like `int`, or `str` do not have any flags, what means, their behaviour cannot be altered.

```py
from hata import Embed
from hata.ext.commands import FlaggedAnnotation, ConverterFlag

@NekoBot.commands
async def avatar(client, message, user: FlaggedAnnotation('user', ConverterFlag.user_all) = None):
    if user is None:
        user = message.author
    
    if user.avatar:
        color = user.avatar_hash&0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)
```

The main difference, between `Converter` and `FlaggedAnnotation`, that `FlaggedAnnotation` can be used to build
multy type parsers.

```py
from hata import UserBase, ChannelBase

@NekoBot.commands
async def what_is_it(client, message, entity: ('user', 'channel', 'role') = None):
    if entity is None:
        result = 'Nothing is recognized.'
    elif isinstance(entity, UserBase):
        result = 'user'
    elif isinstance(entity, ChannelBase):
        result = 'channel'
    else:
        result = 'role'
    
    await client.message_create(message.channel, result)
```

The command above will recognize the entities by their's `id`, `mention` and `name`, so If we want only `name`, we
can define it like::

```py
async def what_is_it(client, message, entity: (
        FlaggedAnnotation('user', ConverterFlag().update_by_keys(name=True)),
        FlaggedAnnotation('channel', ConverterFlag().update_by_keys(name=True)),
        FlaggedAnnotation('role', ConverterFlag().update_by_keys(name=True)),
            ) = None):
    
    if entity is None:
        result = 'Nothing is recognized.'
    elif isinstance(entity, UserBase):
        result = 'user'
    elif isinstance(entity, ChannelBase):
        result = 'channel'
    else:
        result = 'role'
    
    await client.message_create(message.channel, result)
```

The advatage of `Converter` is, that it can hold default values, or default code values as well.

We can modify the `avatar` command from above to use the `default` parameter, like:

```py
from hata.ext.commands import Converter

@NekoBot.commands
async def avatar(client, message, user: Converter('user', ConverterFlag.user_all, default=None)):
    if user is None:
        user = message.author
    
    if user.avatar:
        color = user.avatar_hash&0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)
```

Or to make it cooler, we can make it pass it the message's author, if the parser fails. To do this, there is the
`default_code` parameter (mutually exclusive with the other `default` one!).

`default_code` can be given as an `async-function`, or as a `str` representing one already precreated one.

The precreated ones are the following:

| Name                                      | Description                                                               |
|-------------------------------------------|---------------------------------------------------------------------------|
| `'message.author'`                        | Returns the message's author.                                             |
| `'message.channel'`                       | Returns the message's channel.                                            |
| `'message.guild'`                         | Returns the message's guild. (Can be `None`)                              |
| `'message.channel.guild'`                 | Same as the `'message.guild'` one.                                        |
| `'client'`                                | Returns the client, who received the message.                             |
| `'rest'`                                  | Returns the not yet used content of the message. (Can be empty string)    |
| `'message.guild.default_role'`            | Returns the message's guild's default role. (Can be `None`)               |
| `'message.channel.guild.default_role'`    | Same as the `''message.guild.default_role''` one.                         |

Defining these might can be difficult, because first you need to get along with hata internals, but to mention
an example, the `'message.author'` precreated one equals to:

```py
async def precreated_default_code__message_author(content_parser_ctx: ContentParserContext):
    return content_parser_ctx.message.author
```

To finish `Converter` off, here is the `default_code` example.

```py
@NekoBot.commands
async def avatar(client, message, user: Converter('user', ConverterFlag.user_all, default_code='message.author')):
    if user.avatar:
        color = user.avatar_hash&0xffffff
    else:
        color = user.default_avatar.color
    
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)
```

When adding a command, you can also add a handler, for the cases, when the command's content parser fails.

The following parameters are passed to a parser failure handler.

| Respective name       | Type              | Description                                                           |
|-----------------------|-------------------|-----------------------------------------------------------------------|
| client                | `Client`          | The respective client.                                                |
| message               | `Message`         | The respective message.                                               |
| command               | `Command`         | The respective command.                                               |
| content               | `str`             | The message's content, from what the arguments would have be parsed.  |
| args                  | `list` of `Any`   | The successfully parsed argument.                                     |

Can be added to a command by passing it to the decorator:

```py
async def what_is_it_parser_failure_handler(client, message, command, content, args):
    await client.message_create(message.channel, f'Please give the name of a user, role or of a channel.')

@NekoBot.commands(parser_failure_handler=what_is_it_parser_failure_handler)
async def what_is_it(client, message, entity: (
        FlaggedAnnotation('user', ConverterFlag().update_by_keys(name=True)),
        FlaggedAnnotation('channel', ConverterFlag().update_by_keys(name=True)),
        FlaggedAnnotation('role', ConverterFlag().update_by_keys(name=True)),
            )):
    
    if isinstance(entity, UserBase):
        result = 'user'
    elif isinstance(entity, ChannelBase):
        result = 'channel'
    else:
        result = 'role'
    
    await client.message_create(message.channel, result)
```

## Checks

Checks can be added to categories and to commands to limit their usage to specific users or places.

```py
from hata.ext.commands import checks

@NekoBot.commands(checks=[checks.owner_only()])
async def owner(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')
```

The implemented checks are the following:

| Name                           | Extra parameter | Description                                                                                        |
|--------------------------------|-----------------|----------------------------------------------------------------------------------------------------|
| client_has_guild_permissions   | permissions     | Whether the client has the given permissions at the guild. (Fails in private channels.)            |
| client_has_permissions         | permissions     | Wehther the client has the given permissions at the channel.                                       |
| custom                         | function        | Custom checks, to wrap a given `function`. (Can be async.)                                         |
| guild_only                     | N/A             | Whether the message was sent to a guild channel.                                                   |
| guild_owner                    | N/A             | Wehther the message's author is the guild's owner. (Fails in private channels.)                    |
| has_any_role                   | roles           | Whether the message's author has any of the given roles.                                           |
| has_guild_permissions          | permissions     | Whether the message's author has the given permissions at the guild. (Fails in private channels.)  |
| has_permissions                | permissions     | Whether the message's author has the given permissions at the channel.                             |
| has_role                       | role            | Whether the message's author has the given role.                                                   |
| is_any_channel                 | channels        | Whether the message was sent to any of the given channels.                                         |
| is_any_guild                   | guils           | Whether the message was sent to any of the given guilds.                                           |
| is_channel                     | channel         | Whether the message's channel is the given one.                                                    |
| is_guild                       | guild           | Whether the message guild is the given one.                                                        |
| nsfw_channel_only              | N/A             | Whether the message's channel is nsfw.                                                             |
| owner_only                     | N/A             | Whether the message's author is an owner of the client.                                            |
| owner_or_guild_owner           | N/A             | `owner_only` or `guild_owner` (Fails in private channels.)                                         |
| owner_or_has_any_role          | roles           | `owner_only` or `has_any_role`                                                                     |
| owner_or_has_guild_permissions | permissions     | `owner_only` or `has_guild_permissions` (Fails in private channels.)                               |
| owner_or_has_permissions       | permissions     | `owner_only` or `has_permissions`                                                                  |
| owner_or_has_role              | role            | `owner_only` or `has_any_role`                                                                     |
| private_only                   | N/A             | Whether the message's channel is a private channel.                                                |

Every check also accepts an additional keyword parameter, called `handler`, what is called, when the respective check
fails (returns `False`).

To a check's handler the following parameters are passed:

| Respective name   | Type                    |
|-------------------|-------------------------|
| client            | `Client`                |
| message           | `Message`               |
| command           | `Command` or `str`      |
| check             | `_check_base` instance  |

> If a command's check fails, then `command` is given as `Command` instance, tho checks can be added not only to
> commands and at those cases, `command` is given as `str`.

The `owner` command's check with a handler, looks like:
```
async def owner_only_handler(client, message, command, check):
    await client.message_create(message.channel, f'You must be the owner of the bot to use the `{command}` command.')

@NekoBot.commands(checks=[checks.owner_only(handler=owner_only_handler)])
async def owner(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')
```

## Name and Aliases

You can change a command's name, with giving a `name` parameter, when defining it.

```py
@NekoBot.commands(name='print')
async def print_(client, message, content):
    if content:
        await client.message_create(message.channel, content)
```

It is also possible to add a command with more name, using the `alises` parameter:

```py
@NekoBot.commands(name='print', alises=['say'])
async def print_(client, message, content):
    if content:
        await client.message_create(message.channel, content)
```

## Special command names

There are also some special command names, which have special role. The are:

- [invalid_command](#Invalid command)
- [command_error](#Command error)
- [default_event](#Default event)

Note, that `invalid_command` and `command_error` also supports checks.

###### Invalid command

Ensured when a command is referenced, what doesn't exist or if any of a command's check fail.

The following parameters are passed to `invalid_command`:

| Respective name   | Type          | Description                                                        |
|-------------------|---------------|--------------------------------------------------------------------|
| client            | ``Client``    | The respective client.                                             |
| message           | ``Message``   | The respective message.                                            |
| command           | `str`         | The command's name.                                                |
| content           | `str`         | The message'"s content after the prefix, till the first linebreak. |

```py
@NekoBot.commands
async def invalid_command(client, message, command, content):
    pass
```

###### Command Error

Ensured, when an exception occures inside of a command.

The following parameters are passed to `command_error`:

| Respective name   | Type              | Description                                                        |
|-------------------|-------------------|--------------------------------------------------------------------|
| client            | ``Client``        | The respective client.                                             |
| message           | ``Message``       | The respective message.                                            |
| command           | ``Command``       | The respective command.                                            |
| content           | `str`             | The message'"s content after the prefix, till the first linebreak. |
| err               | ``BaseException`` | The occured exception.                                             |

> If the command processer has no `command_error` set, or if `command_error` raises an exception, then
>`client.events.error` is called.

```py
@NekoBot.commands
async def command_error(client, message, command, content, exception):
    pass
```

#### Default event

Familiar to the normal `message_create` event, but it is called, at the end of command processer's call, if nothing
else was picked was picked up by it.

```py
@NekoBot.commands
async def default_event(client, message):
    lowercase_content = message.content.lower()
    
    if lowercase_content in ('owo', 'uwu', '0w0'):
        await client.message_create(message.channel, lowercase_content)
    
    elif lowercase_content.startswith('ayy'):
        await client.message_create(message.channel, 'lmao')
```

The advantage of using `default_event` over adding a new `message_create` event handler, that at this point bot 
authors and channels, where the bot cannot reply are already filtered out.
