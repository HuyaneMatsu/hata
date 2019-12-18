# class `ContentParser`

A content parser command wrapper to save time at creating content parsers.

- source : [events_compiler.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events_compiler.py)

###### Example

```py
@on_command
@ContentParser('user, flags=mna, default="message.author"')
async def rate(client, message, target):
    if target is client:
        result=10
    else:
        result=target.id%11
    # nickname check
    await client.message_create(message.channel, f'I rate {target.name_at(message.guild)} {result}/10')
```

The content parser always takes 3 arguments, `client`, `message` and `content`.
If the parsing succeeds, then it is going to always pass the `client` and the
`message` as well and each parsed value.

The content parser's syntax is pretty easy. The content parser accepts
lines of strings, and an optional keyword argument as well.

```py
async def no_permission(client,message,*args):
    # Guild is passed before checking the permissions, so
    # if len(args)==0, then the command was not called from a guild.
    # At that case we dont want to send the no permission message.
    if args:
        await client.message_create(message.channel,
            'You do not have permission to use this command!')
        
@on_command
@ContentParser('guild',
                'condition, flags=r, default="not guild.permissions_for(message.author).can_kick_users"',
                'user, flags=mni, default=None',
                'rest',
                on_failure=no_permission)
async def kick(client,message,guild,user,rest):
    # If user is not passed, lets write a general help message out.
    if user is None:
        await client.message_create(message.channel,
            'Call the command with a user's name, mention or id to kick it '
            'from the guild.')
        return
    
    # Check our permissions. If there are many roles, using cached permissions
    # can save a lot of time.
    if not guild.cached_permissions_for(client).can_kick_users:
        await client.message_create(message.channel,
            'I do not have permissions here to invoke this command')
        return
    
    # If reason is not set lets create one.
    if not rest:
        rest=f'Invoked by {message.author:f}.'
    
    await client.guild_user_delete(guild, user, reason=rest)
    await client.message_create(message.channel, f'{user:f} kicked')
```

Each line builds up from a [name](#Names), what tells the parser what to do.
These can be normal to-parse names, like `user` or, names, which do not
require parsing, like `guild`, or some have special purpose, `condition`.
And every other part of the strings are keyword arguments:
- [`mode`](#Modes)
- [`flags`](#Flags)
- [`default`](#Default)
- [`passit`](#Passit)

The keyword arguments should be separated with `,` as expected. If the passed
value is not just a simple word, it should be be put in `"` (or in `'`). If
you want to use still `'`-s, then those can be still used as `\'`. Examples:

```
'user, default=None'
'user, default="message.author"'
'user, default="\'noone\'"
```

The [`on_failure`](#on_failure) keyword argument can be used, if you want to
call a function, when the parsing fails. The other keyword argument is
[`is_method`](#is_method), what should be passed as `True`, whenever a
`method` is wrapped by the [`ContentParser`](ContentParser.md).

The parser works linearly and wont skip any word. So if parsing fails on any
word and it has [`default`](#default) set, then the next parser will work with
it. Lets say we wanna parse: `'user, default=None', 'str'`. At this case the
parser will yield:

| input           | output                  |
|-----------------|-------------------------|
| user1, user2    | user1, str (from user2) |
| str, user       | None, str               |
| user, str       | user, str               |
| str1, str2      | None, str1              |
| user            | parsing fails           |
| str             | None, str1              |
|                 | parsing fails           |

Everything passed within `"` counts as a single word. So if we use a parser
like :  `'str, mode="1+"'`, will yield:

| input                             | output                                    |
|-----------------------------------|-------------------------------------------|
| 'Nekos are cute and fluffy.'      | 'Nekos', 'are', 'cute', 'and', 'fluffy.'  |
| 'Nekos are "cute and fluffy."'    | 'Nekos', 'are', 'cute and fluffy.'        |
| '"Nekos are cute and fluffy."'    | 'Nekos are cute and fluffy.'              |

There are two more keyword arguments, which can be passed. They are 
`case` and `func`.

If `case` is passed, then it will be used, when adding the
[ContentParser](ContentParser.md) as a command instead of it's function's
autodetected name.

```py
@on_command
@ContentParser('emoji', case='se')
async def show_emoji(client, message, emoji):
    if emoji.is_custom_emoji:
        await client.message_create(message.channel, f'**Name:** {emoji:e} **Link:** {emoji.url}')
```

If `func` is passed, the [ContentParser](ContentParser.md) wrpa the function
instantly and will not act like a decorator.

```py
async def show_emoji(client, message, emoji):
    if emoji.is_custom_emoji:
        await client.message_create(message.channel, f'**Name:** {emoji:e} **Link:** {emoji.url}')
        
on_command(ContentParser('emoji', case='se', func=show_emoji))
```

### Names

There are different names, what the parsers accepts:

- [`user`](#user)
- [`role`](#role)
- [`channel`](#channel)
- [`guild`](#channel)
- [`message`](#message)
- [`emoji`](#emoji)
- [`content`](#content)
- [`rest`](#rest)
- [`condition`](#condition)
- [`str`](#str)
- [`int`](#int)
- [`ensure`](#ensure)
- [`rdelta`](#rdleta)
- [`tdelta`](#tdelta)

#### user

Using the `user` parses a [`User`](User.md) (/[`Client`](Client.md)) as it says.

If no [flags](#Flags) are passed, then it will be compiled with `mni` flags.
There 6 [flags](#Flags) for this name:

| flag  | description                                                                                                       |
|-------|-------------------------------------------------------------------------------------------------------------------|
| g     | Marks the whole parser as guild only.                                                                             |
| m     | Checks for user at the message's mentions.                                                                        |
| n     | Checks for users by name (/nick) at the message's local user scope.                                               |
| i     | Looks up if there is a user with the given id at the local scope.                                                 |
| a     | Checks all the user with the given id. Might even request it.                                                     |
| p     | If user caching is disabled it can be used to ensure, that the user got by id will have guild profile as well.    |

> If the message is sent in a private (/group) channel, then the `local scope`
will be the channel, but if the mesage is sent in a guild channel, then the
`local scope` means the whole guild.

> The `n` flag is not for full name check, it checks if the user's name
(/nick) starts with the given string. Also it is not casesensitive. If the
passed text is under 2 characters this check will be ignored.

> Flag `i` is a sub flag of `a`, so if `a` is set `i` is ignored.

#### role

`role` parses for [`Role`](Role.md) at the message.

If no [flags](#Flags) are passed it will use the default flags, which are:
`gmni`.
Parsing role is a guild only operation, so even if g flag is not passed,
it will extend itself with it.

| flag  | description                                               |
|-------|-----------------------------------------------------------|
| g     | Marks the whole parser as guild only.                     |
| m     | Checks for roles at the message's mentions.               |
| n     | Checks for role by name at the message's guild.           |
| i     | Looks up the guild's roles for a role with the given id.  |

> The `n` flag at this case not like at the case of [user](#user) stands for
full role name match.

#### channel

Parses a [channel](CHANNEL_TYPES.md).

If no [flags](#Flags) are passed, it will use the default `gmni` flags.
Parsing a channel is possible only in a guild, so even if `g` flag is not
passed, it will auto extend itself with it.

| flag  | description                                                   |
|-------|---------------------------------------------------------------|
| g     | Marks the whole parser as guild only.                         |
| m     | Checks for the channels at the message's mentions.            |
| n     | Checks for the channel at the guild by it's name.             |
| i     | Tries to get the channel from the guild with the given id.    |

> The `n` flag 1st checks the channel's display name for full match, then
it's normal name at the guild. A channel's display name is how it is
Displayed by Discord, like a category channel's name is always full upper
case, meanwhile it does not needs to be stored on the way.

#### guild

Just simply passes the message's guild. Also it marks the command as guild
only.

> Ignores `mode` and `default`.

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

#### message

Message is passed by default, so it is ignored.

> Ignores `mode`, `default` and `passit`.

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

#### emoji

Used to parse an [`Emoji`](Emoji.md). It can yield builtin (unicode) and
custom emoji as well.

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

#### content

Used to pass the content received on call. If `default` is set and the content
is empty, then it will pass the `default` instead of the original `content`
variable.

> Ignores `mode`.

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

#### rest

Passes all the non parsed leftover [content](#content). If default is set and
there is no leftover content, it will pass the default.

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

> Ignores `mode`.

#### condition

Uses it's expression and if the result equates to True, then calls the wrapped
command with the already parsed variables. If `r` flag is used, then instead
of calling the command will exit the parser with failure.

| flag  | description                                   |
|-------|-----------------------------------------------|
| g     | Marks the whole parser as guild only.         |
| r     | Reverses the condition from success to fail.  |

> Ignores `mode`. `default` is a must.

#### str

Just passes the next word.

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

#### int

Passes the next word as `int`.

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

#### ensure

Makes sure that there is an another word to parse from. If there is no more
word at the content, it will use an empty string, or it's default if set.

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

> Ignores `mode`.

### rdleta

Parses a `dateutil.relativedelta`. Can parse `'years'`, `'months'`, `'weeks'`,
`'days'`, `'hours'`, `'minutes'`, `'seconds'` and `'microseconds'`. Accepts
short versions of each and it will use the first matched unit. For
example `3m` will be 3 months. But it will match units in order from highest
to lower, so `3h2m` will be 3 hours and 2 minutes (not month).

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

### tdelta

Parses a `datetime.timedelta`. Familar to `rdleta`. Can parse `'weeks'`,
`'days'`, `'hours'`, `'minutes'`, `'seconds'` and `'microseconds'`.
(So not years and months.)

| flag  | description                           |
|-------|---------------------------------------|
| g     | Marks the whole parser as guild only. |

### Modes

There are different modes, which can be set to parse in loops.

```py
@on_command
@ContentParser('user, mode="1+"') #parse at least 1
async def i_love(client, message, users):
    for user in users:
        await client.message_create(message.channel, f'{user:m} I love u!')

@on_command
@ContentParser('user, mode="2"') #parse 2
async def i_love(client, message, users):
    for user in users:
        await client.message_create(message.channel, f'{user:m} I love u!')
        
@on_command
@ContentParser('user, mode="2-"') #parse max 2
async def i_love(client, message, users):
    for user in users:
        await client.message_create(message.channel,f'{user:m} I love u!')
        
@on_command
@ContentParser('user, mode="2-4"') #parse between 2 and 4
async def i_love(client, message, users):
    for user in users:
        await client.message_create(message.channel, f'{user:m} I love u!')
        
@on_command
@ContentParser('user, mode="*2"') #parse 2 and pass separately
async def i_love(client, message, user1, user2):
    await client.message_create(message.channel, f'{user1:m} I love u!')
    await client.message_create(message.channel, f'{user2:m} I love u!')

@on_command
@ContentParser('user, mode="*1+"') #parse at least 1 and pass separately
async def i_love(client, message, user, *users):
    await client.message_create(message.channel, f'{user:m} I love u!')
    for user in users:
        await client.message_create(message.channel, f'{user:m} I love u!')
```

This is the whole story, what can i say.

### Flags

Each [name](#Names) has it's own flags. These flags modify where and how the
parsers going to search.

```py
@on_command
@ContentParser('user, flags=mna, default="message.author"')
async def avatar(client, message, user):
    url=user.avatar_url_as(size=4096)
    embed=Embed(f'{user:f}\'s avatar', url=url)
    embed.add_image(url)
    await client.message_create(message.channel, embed=embed)
```

### Default

The `default` keyword argument is a single line expression, what is used if
the parsing fails. The variable will be equal to expression's result.
Not all case of the [names](#Names) is used for parsing, so at those cases
`default` has a special purpose.

Expressions use local variables from the parser and they are tested to a 
limit. Simple expressions should not break anything, and they should 
force the content parser to raise an error when compiling.

### Passit

The `passit` default keyword argument can be added as `True` or `False`.

```py
@on_command
@ContentParser('user, flags=m, passit=False')
async def didiping(client, message):
    await client.message_create(message.channel, 'Sadly')
```

By default passit is `True`. If it is set to `False`, the parser just simply
will not pass the parsed value.

### `on_failure`

The `on_failure` keyword argument can be a normal and an `async` function too.
It is checked to be async on the same ways, as events and commands are. So
there is more option to work with it (or to break it).

`on_failure` is called with the already parsed arguments, so using it `*args`
or with default values is recommended. Checking the amount of passed arguments
can be usefull to know at which step the parser failed.

### `is_method`

Whenever the [`ContentParser`](ContentParser.md) wraps a method, the
`is_method` keyword argument should be passed as `True`. `is_method` is
compiled into the parser, so it should not be changed after. If the keyword
is passed within a bad usecase, a `TypeError` might pop up later.

##### `is_method` examples

Default example on wrapping a `__call__` method in content parser:

```py
@on_command
@ContentParser('user, flags=mni')
class userlist(object):
    def __init__(self):
        self.users = [None for _ in range(10)]
        self.position = 0
    
    async def __call__(self, client, message, user):
        position = self.position
        
        users = self.users
        users[position] = user
        
        if position==9:
            position = 0
        else:
            position = position + 1
        self.position = position

        names = []
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel, text)
```

Wrapping a `__call__` from inside:

```py
@on_command
class userlist(object):
    def __init__(self):
        self.users = [None for _ in range(10)]
        self.position = 0

    @ContentParser('user, flags=mni', is_method=True)
    async def __call__(self, client, message, user):
        position = self.position
        
        users = self.users
        users[position] = user
        
        if position==9:
            position = 0
        else:
            position = position + 1
        self.position=position

        names = []
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text = ', '.join(names)
        
        await client.message_create(message.channel, text)
```

Wrapping a classmethod:

```py
class UserList(object):
    users = [None for _ in range(10)]
    position = 0

    @ContentParser('user, flags=mni', is_method=True)
    async def userlist(cls, client, message, user):
        position = cls.position
        
        users = cls.users
        users[position] = user
        
        if position==9:
            position = 0
        else:
            position = position + 1
        cls.position = position

        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel, text)

on_command(UserList.userlist)
```

Sadly we can not add a classmethod command meanwhile class creation.
But an advantage of it, that we can add more classmethods as command
from a class.

```py
class UserList(object):
    users = [None for _ in range(10)]
    position = 0

    @ContentParser('user, flags=mni',is_method=True)
    async def userlist(cls, client, message, user):
        position = cls.position
        
        users = cls.users
        users[position]=user
        
        if position==9:
            position = 0
        else:
            position = position + 1
        cls.position = position

        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel, text)

    @ContentParser('user, flags=mni', is_method=True)
    async def userclear(cls, client, message, user):
        users = cls.users
        count = 0
        for index in reversed(range(len(users))):
            user_ = users[index]
            if user_ is user:
                del users[index]
                users.append(None)
                count += 1
        
        await client.message_create(message.channel, f'{user:f} removed {count} times.')

    @classmethod
    async def usershow(cls, client, message, content):
        users = cls.users
        names = []
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        if names:
            text=', '.join(names)
        else:
            text='No users are added yet.'
        
        await client.message_create(message.channel, text)
    
on_command(UserList.userlist)
on_command(UserList.userclear)
on_command(UserList.usershow)
```

The last advantage is, when using subcommands:

```py

@on_command
class userlist:
    def __init__(self):
        self.users = [None for _ in range(10)]
        self.position = 0

    @ContentParser('str, default="\'\'"', 'rest', is_method=True)
    async def __call__(self, client, message, subcommand, rest):
        subcommand = subcommand.lower()
        
        if subcommand=='add':
            await self.add(client, message, rest)
            return
        
        if subcommand=='clear':
            await self.clear(client, message, rest)
            return

        if subcommand=='show':
            await self.show(client, message)
            return

        await self.help(client, message)

    @ContentParser('user, flags=mni', is_method=True)
    async def add(self, client, message, user):
        position = self.position
        
        users = self.users
        users[position] = user
        
        if position==9:
            position = 0
        else:
            position = position + 1
        self.position = position

        names = []
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel, text)

    @ContentParser('user, flags=mni', is_method=True)
    async def clear(self, client, message, user):
        users = self.users
        count = 0
        for index in reversed(range(len(users))):
            user_ = users[index]
            if user_ is user:
                del users[index]
                users.append(None)
                count += 1
        
        await client.message_create(message.channel, f'{user:f} removed {count} times.')

    async def show(self,client,message):
        users = self.users
        names = []
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        if names:
            text=', '.join(names)
        else:
            text='No users are added yet.'
        
        await client.message_create(message.channel, text)

    async def help(self, client, message):
        prefix=client.events.message_create.prefix(message)
        text = (
            f'Use `{prefix}userlist add *user*` to add a user to the list.\n'
            f'Use `{prefix}userlist clear *user*` to clear a user from the list.\n'
            f'Use `{prefix}userlist show` to show up the list of the user.'
                )
        await client.message_create(message.channel, text)
```

Same is possible without instancing a class, if you use
`async __new__` instead of `__init__` and `async __call__`.

## Settings

There are 2 available settings for [`ContentParser`](ContentParsermd)
at the moment.

### `REQUEST_OVER`

- default : `1000`

A class attribute, what defines over how much user we will request users from
Discord instead of searching them by name.

> If user caching is disabled, requesting is the default search method.

### `INT_CONVERSION_LIMIT`

- default : `100`

A class attribute, what tells the parser, the maximum length of strings, what
it should try to convert to `int`.
