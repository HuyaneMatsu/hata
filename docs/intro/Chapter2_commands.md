# Commands (extension)

The last chapter was all about basic event handling and some example cases,
but at this chapter we will look into one of Hata extension, the `commands` extension.
It is a high-level modular command framework that allows you to easily create commands.

All features of the extension can be setup with the `setup_ext_commands` function.

After the client is created and `setup_ext_commands` is called on it you can
register commands on said client using its new `.commands` attribute as a decorator:

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

`setup_ext_commands` function accepts the following arguments:

| name                  | type                                          | default   | description                                                                                           |
|-----------------------|-----------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------|
| client                | `Client`                                      | -         | The client on which the extension will be setup.                                                      |
| prefix                | `str` or `iterable` of `str` or `callable`    | -         | The prefix used for by the clients `CommandProcesser`                                                 |
| ignorecase            | `bool`                                        | `True`    | Whether the prefix case should be ignored.                                                            |
| mention_prefix        | `bool`                                        | `True`    | Whether the client should accept its mention at the start of the messages as an alternative prefix.   |
| default_category_name | `None` or `str`                               | `None`    | The `CommandProcesser` default `Category` name.                                                       |
| category_name_rule    | `None` or `function`                          | `None`    | Function to generate display names for categories.                                                    |
| command_name_rule     | `None` or `function`                          | `None`    | Function to generate display names for commands.                                                      |

## Command Arguments

Every command has to have at least `client` and `message` arguments, but you can add more arguments as well.

#### Non-annotated arguments

If the command accepts more arguments than the default 2, and those arguments are not annotated nor do they have 
a default value, then the message content will be split by words and passed to those arguments  (until newline).

Example for the above case:
```py
@NekoBot.commands
async def test(client, message, third):
    print(third)
```
If we call command test with `n!test abc 123 zzz` this will print `third` which would be a string with value `abc 123 zzz`

However if we call it with newline `n!test abc 123 zzz\nnewline` the newline(s) will be ignored and `third` would still
be a string with value `abc 123 zzz`

If we had multiple arguments like this:
```py
@NekoBot.commands
async def test(client, message, third, fourth, fifth):
    print(third, fourth, fifth)
```

We would have these results:
`n!test abc 123 zzz` would result in third="abc" fourth=123 fifth=zzz

#### Parsing command arguments (annotated arguments)

Sometimes we want to deal with certain types inside our command, for example let's say we want a command that hugs a user:

```py
@NekoBot.commands
async def hug(client, message, user):
    ...
```
Let's say we call the above command with `n!hug some_user#1234`, it would be easier for us if argument `user` was
already a `User` object that we can use right away inside that function instead of string which we would then need to 
additionally convert to user object inside our command.


For example we'll annotate it as User and have it's default value of None:
```
from hata import User

@NekoBot.commands
async def hug(client, message, user: User = None):
    if user is None:
        user = message.author
    
    await client.message_create(message.channel, f'Hugs {user:m} !')
```
- If the user was not found and the argument has default value given as well, then that will be passed instead.
- If the user was not found (or not passed in command call aka just `n!hug`) then user will have default value, in this case `None`.

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
- If `'user'` is given as `UserBase` then the parser behaviour will not be altered, it also means, that if it is given
    `User`, then it will still let trough the `Client`-s as well.
- If `'channel'` is given as a specific channel type then every channel with different type will be ignored.
- For using `'rdelta'` converter you must have `dateutil` installed.
- `'rest'` converter returns the unused part of the message content.

If you do not give annotations for the extra parameters then every one of them (except the last) will be interpreted as
`str` parser while the last of them will be interpreted as a `rest` parser. 
Although you can use `*args` to get as much object of the given as possible.
If at the case of `*args` no annotation is given then instead of `rest` parser it will be picked up as `str`.

```
@NekoBot.commands
async def separate(client, message, *args):
    if not args:
        result = 'Nothing to separate'
    else:
        result = ', '. join(args)
    await client.message_create(message.channel, result)
```
By default the parser separates the message content by words but you can use double quote to alter this behaviour:

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

`separator` can be given as a `str` instance with length of `1` or as a `tuple` of 2 `str` instances with length
`1`.

Input-output examples:

| Separator     | Input	                                            | Output                                                                |
|---------------|---------------------------------------------------|-----------------------------------------------------------------------|
| `,`           | `'Reach for the Moon, Immortal Smoke'`	        | `'Reach for the Moon'`,`'Immortal Smoke'`                             |
| `('[', ']')`  | `'[Touhou vocal] Lost Emotion'`                   | `'[Touhou vocal]'`, `'Lost'`, `'Emotion'`                             |
| `('*', '*')`  | `'Legacy of Lunatic Kingdom *Pandemonic Planet*'` | `'Legacy'`, `'of'`, `'Lunatic'`, `'Kingdom'`, `'Pandemonic Planet'`   |


It is also possible to customize parsers with `FlaggedAnnotation` or with `ConverterFlag`.

You can modify a `ConverterFlag` with its `.update_by_keys` method by giving flag name as keyword with its new value.

`ConverterFlag` implements the following flags:
| Name          | Description                                                                                                                       |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------|
| url           | Whether the entity should be parsed from its url.                                                                                 |
| mention       | Whether the entity should be parsed out from its mention.                                                                         |
| name          | Whether the entity should be picked up by its name.                                                                               |
| id            | Whether the entity should be picked up by its ID.                                                                                 |
| everywhere    | Whether the entity should be searched in the local scope. Mostly pairs with the `id` flag.                                        |
| profile       | User parser only. Can be used when user cache is disabled to ensure that the user will have local guild profile, if present.      |

There are already some pre-created flags for common usage:

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

- Note: If you use for example a `'user'` parser then by default it will use the `user_default` flags and it
will ignore everything else than `user_all`.

Some parsers, like `int` or `str`, do not have any flags which means that their behaviour cannot be altered.

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

The main difference between `Converter` and `FlaggedAnnotation` is that `FlaggedAnnotation` can be used to build
multi-type parsers.

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

The command above will recognize the entities by their `id`, `mention` and `name` so if we only want `name` we
can define it like:

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

The advantage of `Converter` is that it can hold default values or default code values as well.

We can modify the `avatar` command from above to use the `default` parameter, example:

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

Or to make it cooler, we can make it pass it the message author (if the parser fails). To do this there is
`default_code` parameter (mutually exclusive with the other `default` one!).

`default_code` can be given as an `async-function` or as a `str` representing already pre-created one.

The pre-created ones are:

| Name                                      | Description                                                           |
|-------------------------------------------|-----------------------------------------------------------------------|
| `'message.author'`                        | Returns the message author.                                           |
| `'message.channel'`                       | Returns the message channel.                                          |
| `'message.guild'`                         | Returns the message guild (can be `None`).                            |
| `'message.channel.guild'`                 | Same as the `'message.guild'` one.                                    |
| `'client'`                                | Returns the client who received the message.                          |
| `'rest'`                                  | Returns the unused content of the message (can be empty string).      |
| `'message.guild.default_role'`            | Returns the message guild default role (can be `None`).               |
| `'message.channel.guild.default_role'`    | Same as the `''message.guild.default_role''` one.                     |

Defining these might be difficult because first you need to get along with hata internals.
One example for the `'message.author'` pre-created one equals to:

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

When adding a command you can also add a handler for the cases when the commands content parser fails.

The following parameters are passed to a parser failure handler.

| Respective name       | Type              | Description                                                           |
|-----------------------|-------------------|-----------------------------------------------------------------------|
| client                | `Client`          | The respective client.                                                |
| message               | `Message`         | The respective message.                                               |
| command               | `Command`         | The respective command.                                               |
| content               | `str`             | The message content, from what the arguments would have be parsed.    |
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

Checks can be added to both categories and commands to limit their usage to specific cases.

Example of adding a simple check to command making that command usable only by bot owner:

```py
from hata.ext.commands import checks

@NekoBot.commands(checks=[checks.owner_only()])
async def owner(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')
```

Currently implemented checks are as follows:

| Name                           | Extra parameter | Description                                                                                        |
|--------------------------------|-----------------|----------------------------------------------------------------------------------------------------|
| client_has_guild_permissions   | permissions     | Whether the client has the given permissions in the guild (fails in private channels).             |
| client_has_permissions         | permissions     | Whether the client has the given permissions in the context channel.                               |
| custom                         | function        | Custom checks to wrap a given `function` (can be both sync and async).                             |
| guild_only                     | N/A             | Whether the message was sent to a guild channel.                                                   |
| guild_owner                    | N/A             | Whether the message author is the guild owner (fails in private channels).                         |
| has_any_role                   | roles           | Whether the message author has any of the given roles.                                             |
| has_guild_permissions          | permissions     | Whether the message author has the given permissions in the guild (fails in private channels).     |
| has_permissions                | permissions     | Whether the message author has the given permissions in the context channel.                       |
| has_role                       | role            | Whether the message author has the given role.                                                     |
| is_any_channel                 | channels        | Whether the message was sent to any of the given channels.                                         |
| is_any_guild                   | guilds          | Whether the message was sent to any of the given guilds.                                           |
| is_channel                     | channel         | Whether the message was sent in specific channel.                                                  |
| is_guild                       | guild           | Whether the message was sent in specific guild.                                                    |
| is_in_voice                    | N/A             | Whether the user is in a voice channel in the respective guild.                                    |
| nsfw_channel_only              | N/A             | Whether the message was sent in NSFW channel.                                                      |
| owner_only                     | N/A             | Whether the message author is the owner of the client.                                             |
| owner_or_guild_owner           | N/A             | `owner_only` or `guild_owner` (fails in private channels).                                         |
| owner_or_has_any_role          | roles           | `owner_only` or `has_any_role`                                                                     |
| owner_or_has_guild_permissions | permissions     | `owner_only` or `has_guild_permissions` (fails in private channels).                               |
| owner_or_has_permissions       | permissions     | `owner_only` or `has_permissions`                                                                  |
| owner_or_has_role              | role            | `owner_only` or `has_any_role`                                                                     |
| private_only                   | N/A             | Whether the message was sent in a private channel.                                                 |

Every check also accepts an additional keyword parameter called `handler` which is called when the respective check
fails (aka returns `False`).
You can use check handlers to define additional specific functionality in case the check fails.

The following arguments are passed to check handler:

| Respective name   | Type                    |
|-------------------|-------------------------|
| client            | `Client`                |
| message           | `Message`               |
| command           | `Command` or `str`      |
| check             | `_check_base` instance  |

Notice how `command` can be either `Command` or `str` instance.
The thing is that checks can be added not only to commands and in such cases you will get `command` as `str`.
In regular cases where check is added to a command then `command` will be instance of `Command`.

Example of check handler with `owner_only` check:
```
async def owner_only_handler(client, message, command, check):
    await client.message_create(message.channel, f'You must be the owner of the bot to use the `{command}` command.')

@NekoBot.commands(checks=[checks.owner_only(handler=owner_only_handler)])
async def owner(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')
```

In the above example the command `owner` can only be used by the owner of the client and if that check fails (aka the
user who tried to call that command is not the owner of the client) then `owner_only_handler` will be activated since
that is defined as handler in `checks.owner_only(handler=owner_only_handler)`. And in that handler we just reply back
saying the user is not allowed to use that command because he is not the client owner.

## Name and Aliases

Command name is by default the same as the function name that you defined as a command.
If you want to have different name other than the function name you can pass `name` kwarg to command when you define it:

```py
@NekoBot.commands(name='print')
async def printing_machine(client, message, content):
    if content:
        await client.message_create(message.channel, content)
```

The above command would usually be called with `n!printing_machine test` but that will not work since we defined 
specific name, it is now called with `n!print test`

It is also possible to add more names to command, using the `alises` kwarg:

```py
@NekoBot.commands(name='print', alises=['say', 'repeat'])
async def printing_machine(client, message, content):
    if content:
        await client.message_create(message.channel, content)
```

`alises` is just a iterable of strings, so it can be, for example, tuple too.
The above command can now be called with all of these: `n!print test` , `n!say test` and `n!repeat test`

## Special command names

There are also some special command names which have special functionality. They are:

- [invalid_command](#Invalid command)
- [command_error](#Command error)
- [default_event](#Default event)

Note that `invalid_command` and `command_error` also supports checks.

###### Invalid command

Ensured when a command is referenced but it doesn't exist or check without handlers fails.

The following arguments are passed to `invalid_command`:

| Respective name   | Type          | Description                               |
|-------------------|---------------|-------------------------------------------|
| client            | ``Client``    | The respective client.                    |
| message           | ``Message``   | The respective message.                   |
| command           | `str`         | The command name.                         |
| content           | `str`         | The message content after the prefix.     |

Example of invalid_command definition:

```py
@NekoBot.commands
async def invalid_command(client, message, command, content):
    pass
```

###### Command Error

Ensured when an exception occurs inside of a command.

The following arguments are passed to `command_error`:

| Respective name   | Type              | Description                               |
|-------------------|-------------------|-------------------------------------------|
| client            | ``Client``        | The respective client.                    |
| message           | ``Message``       | The respective message.                   |
| command           | ``Command``       | The respective command.                   |
| content           | `str`             | The message content after the prefix.     |
| err               | ``BaseException`` | The occurred exception.                   |

Example of command_error definition:

```py
@NekoBot.commands
async def command_error(client, message, command, content, exception):
    pass
```

If the command processer has no `command_error` or if your `command_error` raises an uncaught exception then
`client.events.error` is called.

#### Default event

```py
@NekoBot.commands
async def default_event(client, message):
    lowercase_content = message.content.lower()
    
    if lowercase_content in ('owo', 'uwu', '0w0'):
        await client.message_create(message.channel, lowercase_content)
    
    elif lowercase_content.startswith('ayy'):
        await client.message_create(message.channel, 'lmao')
```

The advantage of using `default_event` over adding a new `message_create` event handler that at this point bot 
authors/developers (as message authors) and channels where the bot cannot reply are already filtered out 
(those messages will not trigger `default_event`).
To see the actual flow of the command handler and when the default_event will trigger see [here](https://github.com/HuyaneMatsu/hata/blob/master/hata/ext/commands/command.py#L2951)
