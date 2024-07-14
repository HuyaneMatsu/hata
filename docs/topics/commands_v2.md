# Introduction

Hata commands_v2 extension lets you easily assign python functions as commands. The user then can call the commands
from the chat using a prefix, familiarly as a you would call the python function.

> The [slash](slash.md) command and old style command share different extensions.

For example this is a command definition:

```py3
@client.commands
async def ping():
    return 'pong'
```

If you set the prefix for example to `!`, you could call the command as `!ping`.

You can setup the commands extension by passing `extensions = 'commands_v2'` to the client constructor. The extension
also required a `prefix`, so pass that as well.

> Naming your bots might be important when using multiple ones, so in the examples it will be called `NekoBot` from
> now.

```py3
from hata import Client

TOKEN = ''
NekoBot = Client(TOKEN,
    extensions = 'commands_v2',
    prefix = '!',
)

@client.commands
async def NekoBot():
    return 'pong'
```

The other way to add the extension is to use the `setup_ext_commands` function on the same way

```py3
from hata import Client
from hata.ext.commands import setup_ext_commands

TOKEN = ''
NekoBot = Client(TOKEN)
setup_ext_commands(NekoBot, prefix = '!')
```

# Command Parameters

You may use internal parameters to get context about command invocation, or outer ones, which are required to be
passed by the user invoking the user. Parameter types are detected based on annotation, name and position.

## Internal parameters

### No parameters

You may use no internal parameters in command definition, since every `return`-ed and `yield`-ed value will be
forwarded as a response to the client.

### Old style

You may use the old style (from commands v1) `client` and `message` parameter combination as the first 2 parameters
of the command.

### Context

You can define any parameter annotated as ``CommandContext``, or named as `context` (`ctx` works as well of course).
This parameter gives you access to information about the command's invocation and implements many related functions,
like `.send(...)`, `.message`, `.channel`, `.client`, `.prefix` to make your life easier.

## Outer / Discord parameters

Outer or Discord parameters can be required or optionally passable by the caller user on Discord.

You can define them as any other parameter with annotation added. String annotations representing a type
(or a converter) are accepted as well. They may be defined as any of the following:


- `ChannelBase`
    - `ChannelCategory`
    - `ChannelDirectory`
    - `ChannelGroup`
    - `ChannelPrivate`
    - `ChannelGuildBase`
    - `ChannelStage`
    - `ChannelStore`
    - `ChannelText`
    - `ChannelTextBase`
    - `ChannelVoice`
    - `ChannelVoiceBase`
- `Client`
- `Color`
- `Emoji`
- `Guild`
- `Invite`
- `Message`
- `Role`
- `Sticker`
- `User` *(`UserBase`)*
- `bool`
- `int`
- `relativedelta` *(requires `dateutil` package)*
- `str`
- `timedelta`

```py3
@NekoBot.commands
async def repeat(ctx, to_repeat: str):
    await ctx.reply(to_repeat, allowed_mentions = None)
```

The command will accept one word as parameter, and then reply it back. You may use `"..."` to pass multiple words.

> `.reply` replies on the invoking message, meanwhile `allowed_mentions = None` blocks all the outgoing mentions.
> Using these is a great way with dealing random user inputs.

## Default values


By using default values you can make parameters optional, like as in python.

```py3
@NekoBot.commands
async def repeat(ctx, to_repeat: str = None):
    if to_repeat is None:
        to_repeat = '*nothing to repeat*'
    
    await ctx.reply(to_repeat, allowed_mentions = None)
```

## Keyword only parameters

You may use keyword only parameters inside of commands.

```py3
@NekoBot.commands
async def repeat(ctx, to_repeat: str = None, *, upper = False):
    if to_repeat is None:
        to_repeat = '*nothing to repeat*'
    elif upper:
        to_repeat = to_repeat.upper()
    
    await ctx.reply(to_repeat, allowed_mentions = None)
```

Keyword only parameter can be passed using the parameter's name followed by a colon, a space character and then the
parameter's value, as: `!repeat cakes upper: true`.

## Multi variable parameters

You can use `*args` to allowing the user to pass multiple variables, on the same way as you do it in python.

```py3
@NekoBot.commands
async def separate(*args: str):
    if args:
        return ', '. join(args)
    
    return 'Nothing to separate'
```

## Dynamic keyword parameters

When using `**kwargs`, you allow the user to pass any keyword parameters

```py3
@NekoBot.commands
async def keywords(**kwargs):
    if kwargs:
        return ', '.join(f'{key!r}: {value!r}' for key, value in kwargs)
    
    return 'No keyword received.'
```

A downside of using `kwargs` may be, that you cannot annotate it, so no auto-conversion will take place, like at the
case of `*args`.

## Multi-type parameters

You can use a set to define multi-type parameters.

```py3
@NekoBot.commands
async def keywords(user: {'User', 'str'}):
    if isinstance(user, str):
        return f'I have no clue who {user} is'
    
    return 'Oh, my old friend {user:f}!'
```

## Not annotated parameters

Each not annotated parameter is auto annotated to `str`. However if a command's last not annotated parameter is
positional, it will capture the rest of the respective message's content instead.

```py3
from hata import Embed

@NekoBot.commands
async def pat(ctx, user, message):
    embed = Embed(f'{ctx.author} pats {user:f}')
    
    if message:
        embed.add_field('Message:', message)
    
    return embed
```

You can also use default values for the cases if no additional content is given.

```py3
from hata import Embed

@NekoBot.commands
async def pat(ctx, user, message = None):
    embed = Embed(f'{ctx.author} pats {user:f}')
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    return embed
```

## Parameter separators & assigner

You can overwrite the default parameter separator `('"', '"')` and assigner `':'` by passing as keyword parameters to
the `.commands` decorator. Overwriting these can be a great tool to make your bot unique.

### Parameter separators

Separators might be defined as encapsulators, where you define where a group starts and ends, or as a standalone
separator to break up the input text.

```py3
@NekoBot.commands(separator=',')
async def separate(*args):
    if not args:
        return 'Nothing to separate'
    
    return ', '. join(args)
```

| Input	                                            | Output                                                                |
|---------------------------------------------------|-----------------------------------------------------------------------|
| `'Reach for the Moon, Immortal Smoke'`	        | `'Reach for the Moon'`,`'Immortal Smoke'`                             |

```py3
@NekoBot.commands(separator=('[', ']'))
async def separate(*args):
    if not args:
        return 'Nothing to separate'
    
    return ', '. join(args)
```

| Input	                                            | Output                                                                |
|---------------------------------------------------|-----------------------------------------------------------------------|
| `'[Touhou vocal] Lost Emotion'`                   | `'[Touhou vocal]'`, `'Lost'`, `'Emotion'`                             |


```py3
@NekoBot.commands(separator=('*', '*'))
async def separate(*args):
    if not args:
        return 'Nothing to separate'
    
    return ', '. join(args)
```

| Input	                                            | Output                                                                |
|---------------------------------------------------|-----------------------------------------------------------------------|
| `'Legacy of Lunatic Kingdom *Pandemonic Planet*'` | `'Legacy'`, `'of'`, `'Lunatic'`, `'Kingdom'`, `'Pandemonic Planet'`   |

### Assigner

Assigners modify the assigner used at keyword parameters.

```py3
@NekoBot.commands(assigner='=')
async def keywords(**kwargs):
    if kwargs:
        return ', '.join(f'{key!r}: {value!r}' for key, value in kwargs.items())
    
    return 'No keyword received.'
```

## Configure parameters

Each entity parameter converter has converter flags., which define the was how the converter tries to convert a field.
Like by default `User` converter wont allow you to access out-of-guild users. But by using `configure_converter
you can modify this behaviour.

```py3
from hata.ext.commands_v2 import configure_converter

@NekoBot.commands
@configure_converter('user', everywhere = True)
async def avatar(ctx, user: 'User' = None):
    if user is None:
        user = ctx.author
    
    return user.avatar_url_as(size = 4096)
```

The default flags are the following:

| Entity    | Included flags                            |
|-----------|-------------------------------------------|
| user      | mention, name, id                         |
| client    | mention, name, id                         |
| role      | mention, name, id                         |
| channel   | mention, name, id                         |
| emoji     | mention, name, id                         |
| guild     | id                                        |
| message   | url, id                                   |
| invite    | url, id                                   |
| default   | name, id                                  |

Meanwhile these are all the applicable ones:

| Entity    | Included flags                            |
|-----------|-------------------------------------------|
| user      | mention, name, id, everywhere, profile    |
| client    | mention, name, id, everywhere             |
| role      | mention, name, id, everywhere             |
| channel   | mention, name, id, everywhere             |
| emoji     | mention, name, id, everywhere             |
| guild     | id, everywhere                            |
| message   | url, id, everywhere                       |
| invite    | url, id                                   |
| sticker   | name, id, everywhere                      |

# Categories

Categories can be used to group up commands. Can be used for help commands, checks and for error handling.

## Creating categories

Categories can be created on the fly, by using the `category` keyword inside of the `.commands` decorator.

```py3
from hata.ext.commands_v2 import configure_converter

@NekoBot.commands(category='utility')
@configure_converter('user', everywhere = True)
async def avatar(ctx, user: 'User' = None):
    if user is None:
        user = ctx.author
    
    return user.avatar_url_as(size = 4096)
```

Although usually you want to create the category first to apply [checks](#checks) or description to it. If you have a
created category, you can pass it directly to the `.commands` decorator instead of the category's name.

```py3
from hata.ext.commands_v2 import configure_converter

UTILITY_CATEGORY = NekoBot.command_processor.create_category('utility')

@NekoBot.commands(category = UTILITY_CATEGORY)
@configure_converter('user', everywhere = True)
async def avatar(ctx, user: 'user' = None):
    if user is None:
        user = ctx.author
    
    return user.avatar_url_as(size = 4096)
```

As on command processor, `.commands` works on categories as well.


```py3
from hata.ext.commands_v2 import configure_converter

UTILITY_CATEGORY = NekoBot.command_processor.create_category('utility')

@UTILITY_CATEGORY.commands
@configure_converter('user', everywhere = True)
async def avatar(ctx, user: 'user' = None):
    if user is None:
        user = ctx.author
    
    return user.avatar_url_as(size = 4096)
```

## Default category

When no category is passed to a command, they will be added to the command processor's default category. Default 
category name can be set when initializing the extension on the client, with the `default_category_name` parameter.

```py3
from hata import Client

TOKEN = ''
NekoBot = Client(TOKEN,
    extensions = 'commands_v2',
    prefix = '!',
    default_category_name = 'generic commands',
)
```

Default category can be get by using the `client.command_processor.get_default_category()` method later.

# Checks

Checks can be applied to commands and to categories to check whether the user has permission to invoke the user.

```py3
import os
from hata.ext.commands_v2 import checks

@NekoBot.commands
@checks.owner_only()
async def shutdown():
    yield 'shutting down'
    os._exit()
```

An other way to apply checks it to pass them to `.commands` decorator.

```py3
import os
from hata.ext.commands_v2 import checks

@NekoBot.commands(checks = checks.owner_only())
async def shutdown():
    yield 'shutting down'
    os._exit()
```

The following checks are implemented:

| Name                           | Extra parameter          | Description                                                                                               |
|--------------------------------|--------------------------|-----------------------------------------------------------------------------------------------------------|
| announcement_channel_only      | N/A                      | Whether the message's channel is an announcement channel.                                                 |
| booster_only                   | N/A                      | Whether the user boosts the respective guild.                                                             |
| bot_account_only               | N/A                      | Whether the message's author is a bot account.                                                            |
| client_only                    | N/A                      | Whether the message was sent by a ``Client``.                                                             |
| custom                         | function                 | Custom checks, to wrap a given `function`. (Can be async.)                                                |
| guild_only                     | N/A                      | Whether the message was sent to a guild channel.                                                          |
| guild_owner_only               | N/A                      | Whether the message's author is the guild's owner. (Fails in private channels.)                           |
| has_any_role                   | *roles                   | Whether the message's author has any of the given roles.                                                  |
| has_client_guild_permissions   | permissions, **kwargs    | Whether the client has the given permissions at the guild. (Fails in private channels.)                   |
| has_client_permissions         | permissions, **kwargs    | Whether the client has the given permissions at the channel.                                              |
| has_guild_permissions          | permissions, **kwargs    | Whether the message's author has the given permissions at the guild. (Fails in private channels.)         |
| has_permissions                | permissions, **kwargs    | Whether the message's author has the given permissions at the channel.                                    |
| has_role                       | role                     | Whether the message's author has the given role.                                                          |
| is_any_category                | *categories              | Whether the message was sent into a channel, what's category is any of the specified ones.                |
| is_any_channel                 | *channels                | Whether the message was sent to any of the given channels.                                                |
| is_any_guild                   | *guilds                  | Whether the message was sent to any of the given guilds.                                                  |
| is_category                    | category                 | Whether the message was sent into a channel, what's category is the specified one.                        |
| is_channel                     | channel                  | Whether the message's channel is the given one.                                                           |
| is_guild                       | guild                    | Whether the message guild is the given one.                                                               |
| is_in_voice                    | N/A                      | Whether the user is in a voice channel in the respective guild.                                           |
| release_at                     | release_at, *roles       | Whether the command is already released. Users with the given roles and the bot owners bypass the check.  |
| nsfw_channel_only              | N/A                      | Whether the message's channel is nsfw.                                                                    |
| owner_only                     | N/A                      | Whether the message's author is an owner of the client.                                                   |
| owner_or_guild_owner_only      | N/A                      | `owner_only`, `guild_owner` (Fails in private channels.)                                                  |
| owner_or_has_any_role          | *roles                   | `owner_only`, `has_any_role`                                                                              |
| owner_or_has_guild_permissions | permissions, **kwargs    | `owner_only`, `has_guild_permissions` (Fails in private channels.)                                        |
| owner_or_has_permissions       | permissions, **kwargs    | `owner_only`, `has_permissions`                                                                           |
| owner_or_has_role              | role                     | `owner_only`, `has_role`                                                                                  |
| private_only                   | N/A                      | Whether the message's channel is a private channel.                                                       |
| user_account_only              | N/A                      | Whether the message's author is a user account.                                                           |
| user_account_or_client_only    | N/A                      | Whether the message's author is a user account or a ``Client``.                                           |


## Category checks

Checks can be applied to categories at creation or later as well.

```py3
# At creation
UTILITY_CATEGORY = NekoBot.command_processor.create_category('utility', checks = checks.owner_only())

# Apply checks later
NekoBot.command_processor.get_default_category().checks = checks.owner_only()
```

# Precheck

Command processor's precheck runs when a message is received. It decides, whether the received message should be
processed as a command.

The default precheck filters out bot message authors, and the channels, where the client cannot create a message.

To change the command processor's precheck, use the `.command_processor.precheck` decorator.

```py3
@NekoBot.command_processor.precheck
def filter_only_bots(client, message):
    return (not message.author.bot)
```

>  Pre-checks cannot be async. `client` and `message` parameters are always passed to them.

# Error handling

Exception handlers can be registered to the command processor, to categories and to commands as well. The first
exception handler, returning `True` will stop the rest of being called, marking the exception as handled.

Use the `.error` decorator to register exception handlers.

```py3
from hata.ext.commands_v2 import checks, CommandCheckError

# Will catch every failed `checks.owner_only()` check.

@NekoBot.command_processor.error
async def handle_owner_only_error(ctx, exception):
    if isinstance(exception, CommandCheckError) and (type(exception.check) is checks.CheckIsOwner):
        await ctx.send('Lacked owner permission')
        return True
    
    return False
```

```py3
from hata.ext.commands_v2 import checks, CommandParameterParsingError

# Returns a role's identifier. If the role cannot be identified, an error message will be dropped to the user.

@NekoBot.commands
async def about_role(role: 'Role'):
    """Returns the role's identifier."""
    return role.id

@about_role.error
async def about_role_error_handler(ctx, exception):
    if isinstance(exception, CommandParameterParsingError):
        await ctx.send(f'{exception.content_parser_parameter.name} is required.')
        return True
    
    return False
```


# Cooldowns

Cooldowns can be applied to commands by using the `cooldown` decorator. They can be either per `'user'`, `'channel'`
or `'guild'`.

```py3
from hata.ext.commands_v2 import CommandCooldownError, cooldown

EMOJI_CAKE = BUILTIN_EMOJIS['cake']

@NekoBot.commands
@cooldown('user', 30.0)
async def cake():
    return emoji.as_emoji

@cake.error
async def handle_cooldown_error(command_context, exception):
    if isinstance(exception, CommandCooldownError):
        await command_context.send(f'You are on cooldown. Try again after {exception.expires_after:.2f} seconds.')
        return True
    
    return False
```

# Sub commands

Sub commands can be registered under other commands on the same way as they are registered to the client.

```py3
@NekoBot.commands
async def upper():
    """Upper command."""
    return 'I am an upper command.'

@upper.commands
async def sub():
    """Sub command."""
    return 'This is a sub command.'
```

# Unknown command

If command prefix and command name is found, but the command's name do not refers to any command,
`.command_processor.unknown_command` is called.

Not like as generic commands, to `unknown_command` always set parameters are passed. `return`-ed and `yield`-ed values
are not forwarded, and if exception occurs, error handlers are not called either.

```py3
@NekoBot.command_processor.unknown_command
async def command_processor(client, message, command_name):
    await client.message_create(message.channel, f'Could not find command named : {command_name!r}')
```
