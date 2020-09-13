# Events (extension)

The last chapter was all about basic event handling and some example cases,
but at this chapter we will look into one of Hata extension, the `commands` extension.
It is a high-level modular command framework that allows you to easily create commands.
 
All features of the extension can be setup with the `setup_ext_commands` function.

After the client is created and `setup_ext_commands` is called on it you can register commands
on said client using its new `.commands` attribute as a decorator:

```py
from hata import Client, start_clients
from hata.ext.commands import setup_ext_commands

TOKEN = ''
NekoBot = Client(TOKEN)

setup_ext_commands(NekoBot, 'n!')


@NekoBot.commands
async def pat(client, message):
    await client.message_create(message.channel, 'Puurs !')

start_clients()

```

`setup_ext_commands` function accepts more arguments:

| name                  | type                                                      | default       | description                                                                                           |
|-----------------------|-----------------------------------------------------------|---------------|-------------------------------------------------------------------------------------------------------|
| client                | `[Client`](../ref/discord/Client.md)                      | *required*    | The client on which the extension will be setup.                                                      |
| prefix                | `str`, `iterable` of `str` or `callable` returning `str`  | *required*    | The prefix used for by the client's [CommandProcesser](../ref/ext/commands/CommandProcesser.md)       |
| ignorecase            | `bool`                                                    | `True`        | Whether the prefix case should be ignored.                                                            |
| mention_prefix        | `bool`                                                    | `True`        | Whether the client should accept its mention at the start of the messages as an alternative prefix.   |
| default_category_name | `NoneType` / `str`                                        | `None`        | The CommandProcesser default [Category](../ref/ext/commands/Category.md) name.                        |



Every command must accept at least 2 arguments, `client` and `message`, but you
can have additional arguments that can be parsed to certain types and they each can have default values.
More on these in the next section.

## Command argument parser

Commands can take additional arguments instead of the default `client` and `message`.

If the command accepts 3 arguments (client and message by default + 3d additional argument) and that 3d argument 
has no annotation nor default value, then the message content will be passed to that third argument (until newline).

Example for the above case:
```py
@NekoBot.commands
async def test(client, message, third):
    print(third)
```
If we call command test with `n!test abc 123 zzz` this will print `third` which would be a string with value `abc 123 zzz`

However if we call it with newline `n!test abc 123 zzz\nnewline` the newline(s) will be ignored and `third` would still
be a string with value `abc 123 zzz`

...

Sometimes we want to deal with certain types inside our command, for example let's say we want a command that hugs a user:
```py
@NekoBot.commands
async def hug(client, message, user):
    ...
```
Let's say we call the above command with `n!hug @some_member_mention`, it would be easier for us if argument `user` was
already a `User` object that we can use right away inside that function instead of string which we would then need to 
additionally convert to user object inside our command.

If the command's arguments are more complicated, as the default 2 argument,
or the extended 3 argument case, then a parser function is generated for it.

```
from hata import User

@NekoBot.commands
async def hug(client, message, user:User=None):
    if user is None:
        user = message.author
    
    await client.message_create(message.channel, f'Hugs {user:m} !')
```
Like this piece of code generates a parser, what tries to parse out a user
from mention, name and id of the next word of the content. With using a
default value, we can make sure, that the command will be called even if
the parsing fails.

Just some built-in and hata types are supported:

| type          | description                                                                                                   |
|---------------|---------------------------------------------------------------------------------------------------------------|
| str           | Parses the next word.                                                                                         |
| int           | Converts the next word to int. The maximal length of converted ints is 100 by default, but can be changed.    |
| timedelta     |                                                                                                               |
| relativedelta | You must have deateutil installed.                                                                            |
| User          |                                                                                                               |
| Emoji         |                                                                                                               |
| ChannelBase   | Guild only for getting any channel of it.                                                                     |
| Role          | Guild only for getting any role of it.                                                                        |

The last argument without annotation will always mean the rest of the content
and every other argument before that will be interpretered as `str` annotation.
If you want to you can also use `*args` to receive undfined amount of parsed
arguments.
```
@NekoBot.commands
async def separate(client, message, *args):
    if not args:
        result = 'Nothing to separate'
    else:
        result = ', '. join(args)
    await client.message_create(message.channel, result)
```
The parser everything within quote will interpreter as one word, for cases,
when you want to pass more words separated with space.

| input	                            | output                                        |
|-----------------------------------|-----------------------------------------------|
| 'Nekos are cute and fluffy.'	    | ('Nekos', 'are', 'cute', 'and', 'fluffy.')    |
| 'Nekos are "cute and fluffy."'	| ('Nekos', 'are', 'cute and fluffy.')          |
| '"Nekos are cute and fluffy."'	| ('Nekos are cute and fluffy.')                |

You can also specify the generated parser, with using the `Converter` object.
```py
from hata import Embed
from hata.ext.commands import Converter, ConverterFlag

@NekoBot.commands
async def avatar(client, message, user : Converter('user', flags=ConverterFlag.user_default.update_by_keys(everywhere=True), default_code='message.author')):
    color = user.avatar_hash&0xffffff
    if not color:
        color = user.default_avatar.color
    
    url=user.avatar_url_as(size=4096)
    embed=Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)
```
By default `user` search is by searching by `mention` / `id` / `name` at the
respective guild, or private channel, but they can be disabled, or some
more option can be enabled with passing a moified converter flag. When
looking up a `user`, with using the `everywere` flag as well, will generate
a parser what will request the user by `id` if not found locally.

Converter also allows to pass `default` or `default_code` mutually exclusive
arguments, which allows you for more control over the default value.
```py
import random

@NekoBot.commands
async def choose(client, message, emojis : Converter('emoji', amount=2)):
    emoji = random.choice(emojis)
    await client.message_create(message.channel, f'I choose {emoji:e} !')
```
`amount` is also a valid argument, which allows you to define how much object
you want to get. Passing amount as a `tuple` with as `(start, end)` is also
supported. (`end` can be passd as `0` as well, then it will go for as much as
it can.)

Each type has it's name at the parser and also 2 more value is supported
`content` and `rest` as well.

| type          | name          |
|---------------|---------------|
| str           | 'str'         |
| int           | 'int'         |
| timedelta     | 'tdelta'      |
| relativedelta | 'rdelta'      |
| User          | 'user         |
| Emoji         | 'emoji'       |
| ChannelBase   | 'channel'     |
| Role          | 'role'        |
| -             | 'content'     |
| -             | 'rest'        |

When you add a command, you can also specify it's parameters by calling the decorator and using keyword arguments.
Like this is how you can add a command with a different name:

```py
@NekoBot(name='print')
async def print_(client, message, content):
    await client.message_create(message.channel, content)
```

Or add checks for the command:

```py
from hata.ext.commands import checks

@NekoBot.commands(checks=[checks.owner_only()])
async def owner(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')
```

If you want to run a specified code when a check fails, you can also add a handler to it:

```
async def owner_only_handler(client, message, command, check):
    await client.message_create(message.channel, f'You must be the owner of the bot to use the `{command}` command.')

@NekoBot.commands(checks=[checks.owner_only(handler=owner_only_handler)])
async def owner(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')
```

If a command uses an argument parser, then `parser_failure_handler` might be called, what can be also defined:

```py
async def on_parse_fail(client, message, command, content, args):
    emojis = args[0]
    if len(emojis)==1:
        result = 'Please pass 1 more emoji.'
    else:
        result = 'Please pass 2 emojis after the command\'s name.'
    
    await client.message_create(message.channel, result)

@NekoBot.commands(parser_failure_handler=on_parse_fail)
async def choose(client, message, emojis : Converter('emoji', amount=2)):
    emoji = random.choice(emojis)
    await client.message_create(message.channel, f'I choose {emoji:e} !')
```

```py
@NekoBot.commands(aliases=['pong'])
async def ping(client, message):
    await client.message_create(message.channel, f'{client.gateway.latency*1000.:.0f} ms')
```
Adding a command with more names is not impossible either, just use `alises`.

There are also some special command names, which have special role. These are:
- [invalid_command](#invalid_command)
- [command_error](#command_error)
- [default_event](#default_event)

###### invalid_command

Ensured when a user the bot's prefix but typed a not existing command.
It can be added as any other command. It's specific name is `invalid_command`.

```py
@NekoBot.commands
async def invalid_command(client, message, command, content):
    pass
```

> If a command returns an `int` instance, what evaulates to `True`, then the
> command processer will act, like the command was not found.

###### command_error

Ensured, when an exception occures at a command.

```py
@NekoBot.commands
async def command_error(client, message, command, content, exception):
    pass
```

> If `command_error` returns an `int` instance, what evaulates to `True`, then
> the client's default error handler will be used.

#### default_event

Same as the normal `message_create`, but called only if nothing else picks up
the message.

```py
import re

OWO_RP = re.compile('owo|uwu|0w0', re.I)
AYY_RP = re.compile('ay+', re.I)

@NekoBot.commands
async def default_event(client, message):
    content = message.content
    
    matched = OWO_RP.fullmatch(content)
    if (matched is not None):
        result = f'{content[0].upper()}{content[1].lower()}{content[2].upper()}'
        await client.message_create(message.channel, result)
        return
    
    matched = AYY_RP.fullmatch(content)
    if (matched is not None):
        result = 'lmao'
        await client.message_create(message.channel, result)
        return
```

The advantage of using `default_event` over adding a new `message_create` event
is that the command parser checks that the message's author is not bot and the
client has permission to send message as well.

> For making it clear, adding more handlers under one event is supported.

### Loading commands from other files

Hata has a builtin type for collecting handlers in a container, then adding them
later, but this also works with commands as well.

###### cute_commands.py
```py
from hata import eventlist, BUILTIN_EMOJIS

CAKE = BUILTIN_EMOJIS['cake']

cute_commands = eventlist()

@cute_commands
async def cake(client, message):
    await client.message_create(message.channel, CAKE.as_emoji)

@cute_commands(name='love')
async def send_love(client, message):
    channel = await client.channel_private_create(message.author)
    await client.message_create(channel, 'I love you :3')
```

Now lets continue the main file:
```py
from cute_commands import cute_commands

NekoBot.commands.extend(cute_commands)
```

The passed function, arguments and the annotations will be checked only
when `.commands` are extened with the `eventist`'s content, so errors
might not show up initially.

`.commands` not only supports `.extend`, but also `.remove` and `.unextend`
operations. These 3 base operations are supported by the `eventlist` type
as well.
