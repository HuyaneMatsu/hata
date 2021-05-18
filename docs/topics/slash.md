# Slash

### Introduction

Slash refers to slash commands as probably known by the users or by interactions as mentioned by the api.

You can also find Discord's API documentation
[here](https://github.com/discord/discord-api-docs/blob/master/docs/interactions/Slash_Commands.md).

Hata supports interactions with many methods and classes, but this topic is not about their raw usage, but about the
inherent slash extension.

Not like regular commands, slash commands' format is limited by the Discord API itself, what we cannot overpass.

## Limitations

Discord sets the following limitations:

- Parameter count to `[0:25]`.
- Command name length to `[1:32]`.
- Command description length to `[2:100]`.
- Choice amount to `[1:25]`.
- Choice name length to `[1:100]`.
- Parameter name length to `[1:32]`.
- Parameter description length to `[1:32]`.
- A command can have `25` sub-commands or sub-categories.
- A sub-category can have `25` sub-commands.
- A sub-category cannot have sub-category under itself.
- Global commands are updated only after `1` hour.
- Acknowledging must be done within `3` seconds.
- Followup messages can be sent within 15 minutes after acknowledging.
- Custom emojis only show up correctly in interaction responses when `@everyone` role has `use_external_emojis`
    permission.

The parameter types can be the following:

| Name              | Requires bot  | Discord field | String representation | Type representation   | Output type               |
|-------------------|---------------|---------------|-----------------------|-----------------------|---------------------------|
| channel           | Depends       | channel       | `'channel'`           | `ChannelBase`         | `ChannelBase`             |
| channel_id        | No            | channel       | `'channel_id'`        | N/A                   | `int`                     |
| boolean           | No            | boolean       | `'bool'`              | `bool`                | `bool`                    |
| integer           | No            | string        | `'int'`               | `int`                 | `int`                     |
| mentionable       | Depends       | mentionable   | `'mentionable'`       | N/A                   | `ClientUserBase`, `Role`  |
| mentionable_id    | No            | mentionable   | `'mentionable_id'`    | N/A                   | `int`                     |
| number            | No            | integer       | `'number'`            | N/A                   | `int`                     |
| role              | Depends       | role          | `'role'`              | `Role`                | `Role`                    |
| role_id           | No            | role          | `'role_id'`           | N/A                   | `int`                     |
| string            | No            | string        | `'str'`               | `str`                 | `str`                     |
| user              | No            | user          | `'user'`              | `User`, `UserBase`    | `ClientUserBase`          |
| user_id           | No            | user          | `'user_id'`           | N/A                   | `int`                     |


##### Parameter notes

`user`, `channel` and `role` data may not be included within the interaction. However users can be requested from
Discord, but channels and roles can not be. It means `role` and `channel` conversions can fail and the command wont be
called. To avoid this case, you may use `role_id` or `channel_id` parameter types instead.

`mentionable` field stands for `user` + `role`.

In hata there is 2 numeric input option available, one is `int` and the other one is `number`. Both has it's pros and
cons. `int` field is converted to `string` by the extension, then when receiving an interaction is converted back to
`int`. It means, when the user not gives a valid integer, the payload validation will fail and the interaction command 
might wont be called. On other hand `number` field is inaccurate. Discord uses javascript `number` type
(that's from the name comes from as well), what equals to float64. It means integers over 53 bit will lose from their
precision.

There are also choice parameters, but lets talk about those only later.

### Internal parameters

`client` (`c`) and `event` (`e`, `interaction_event`) parameters are picked up as internal parameters.

> They can be also linted as `Client` or `InteractionEvent`.

Internal parameters are not propagated towards discord, instead they are auto-fulfilled internally. They can be used
to access information about the command's context if required.

## Required oauth2 scopes

When using slash commands, adding your bot to a guild with just the regular `bot` scope is not enough. Make sure you
authorize it with `applications.commands` oauth2 scope as well. Just fill out your bot's application's id in the
`<APPLICATION_ID>` part and add the bot to your guild;
`https://discord.com/api/oauth2/authorize?client_id=<APPLICATION_ID>&scope=bot+applications.commands`.

If this error pops ups as you launched your bot: `DiscordException Forbidden (403), code=50001: Missing access`
Do not worry, you probably just need to authorize your bot with the `applications.commands` oauth2 scope.

## Setup

To setup the extension you just pass `'slash'` into the client's `extensions` parameter, or use the `setup_ext_slash`
function.

```py
from hata import Client

Nitori = Client(TOKEN, extensions='slash')
```
or
```py
from hata import Client
from hata.ext.slash import setup_ext_slash

Nitori = Client(TOKEN)
setup_ext_slash(Nitori)
```

#### delete_commands_on_unload

Optional parameter for the slasher.

Tells to the slasher whether it should delete the commands from Discord when they are removed. Defaults to `False` in
favor of working with extensions.

When unloading an extension, all of it's commands are deleted from Discord as well if set as `True`. This might be
painful when reloading global commands, because it would need 1 hour for the changes to take place.

## Adding commands & responding

After the extension is setuped, commands can be added using the `client.interaction` decorator.

> Global commands are only updated after 1 hour, meanwhile guild commands immediately, so when using test commands
> make sure to use only guild bound commands. The examples will show only guild commands, tho of course global
> commands will be mentioned as well.

```py
from hata import Embed

@Nitori.interactions(guild=TEST_GUILD)
async def perms(event):
    """Shows your permissions."""
    user_permissions = event.user_permissions
    if user_permissions:
        description = '\n'.join(permission_name.replace('_', '-') for permission_name in user_permissions)
    else:
        description = '*none*'
    
    user = event.user
    return Embed('Permissions', description).add_author(user.avatar_url, user.full_name)
```

Every `return`-ed or `yield`-ed string or embed (list or tuple of embeds as well) from a slash command will be
propagated to be sent as a response to the user, but you can also send responses manually with the
`Client.interaction_response_message_create` or with the `Client.interaction_followup_message_create` methods. There
are also other interaction related client methods, which are mentioned [later](#manual-responding).

> New commands might not show up till you restart your client (not the bot). This is **always** the case for the first
> command.

## Command Parameters

An interaction event has the following top level attributes, which you may use up to produce a proper response:

| Name              | Type                              | Notes                                                                     |
|-------------------|-----------------------------------|---------------------------------------------------------------------------|
| channel           | `ChannelText` or `ChannelPrivate` | The channel from where the interaction was called. Might be a partial.    |
| guild             | `None` or `Guild`                 | The channel's guild. Might be partial or `None`                           |
| user              | `Client` or `User`                | The user who called the interaction.                                      |
| user_permissions  | `Permission`                      | The user's permissions in the respective channel.                         |

> The rest of the attributes should be ignored if you are **not** writing your own interaction handler.

> If a command is called from a private channel, it's `.guild` is always `None`.


The possible parameter types are listed above in the [Limitations](#Limitations) section, tho it is a little bit more
complicated as might look for first time. All parameter has 3 fields what we need to fulfill; `name`, `type` and
`description`. Their definition is expected in the following format: `name : (type, descritpion)`.

```py
from hata import Embed

@Nitori.interactions(guild=TEST_GUILD)
async def cookie(event,
        user : ('user', 'To who?'),
            ):
    """Gifts a cookie!"""
    return Embed(description=f'{event.user:f} just gifted a cookie to {user:f} !')
```

#### configure_parameter

If you do not like the annotation design, you can use the `configure_parameter` decorator. Since the main design is
more intuitive, the rest of the examples will follow that one.

```py
from hata import parse_emoji
from hata.ext.slash import configure_parameter

@Nitori.interactions(guild=TEST_GUILD)
@configure_parameter('emoji', str, 'Yes?')
async def show_emoji(emoji):
    """Shows the given custom emoji."""
    emoji = parse_emoji(emoji)
    if emoji is None:
        return 'That\'s not an emoji.'
    
    if emoji.is_unicode_emoji():
        return 'That\' an unicode emoji, cannot link it.'
    
    return f'**Name:** {emoji:e} **Link:** {emoji.url}'
```

### Choice parameters

Slash commands support choice parameters, for string and integer types. Each choice has a `name` and a
`value` field. All values must be the same type, either `str` or `int` as mentioned above.

Choice parameters go to the "annotation type field" and they can be either:
- Dictionary of `name - value` items.
- List of tuple `name - value` pairs.
- Set of tuple `name - value` pairs.
- List of `value`-s.
- Set of `value`-s.
- Iterables of `name - value` pairs.
- Iterables of `value`-s.

> Dictionary and set choices are sorted alphabetically, so if order matters for you, use list.
>
> Formatting choices into a table-like appearance might help, but it is up to you.

```py
from hata import Embed

@Nitori.interactions(guild=TEST_GUILD)
async def guild_icon(event,
        choice: ({
            'Icon'             : 'icon'             ,
            'Banner'           : 'banner'           ,
            'Discovery-splash' : 'discovery_splash' ,
            'Invite-splash'    : 'invite_splash'    ,
        }, 'Which icon of the guild?' ) = 'icon',
            ):
    """Shows the guild's icon or it's selected splash."""
    guild = event.guild
    if (guild is None) or guild.partial:
        return Embed('Error', 'The command unavailable in guilds, where the application\'s bot is not in.')
    
    if choice == 'icon':
        name = 'icon'
        url = guild.icon_url_as(size=4096)
        hash_value = guild.icon_hash
    elif choice == 'banner':
        name = 'banner'
        url = guild.banner_url_as(size=4096)
        hash_value = guild.banner_hash
    elif choice == 'discovery_splash':
        name = 'discovery splash'
        url = guild.discovery_splash_url_as(size=4096)
        hash_value = guild.discovery_splash_hash
    else:
        name = 'invite splash'
        url = guild.invite_splash_url_as(size=4096)
        hash_value = guild.invite_splash_hash
    
    if url is None:
        color = (event.id>>22)&0xFFFFFF
        return Embed(f'{guild.name} has no {name}', color=color)
    
    color = hash_value&0xFFFFFF
    return Embed(f'{guild.name}\'s {name}', color=color, url=url).add_image(url)
```

If you find defining choice parameters inside of the "function parameter definition" too confusing, consider creating
a variable and annotate that instead.

```py
GUILD_ICON_CHOICES = {
    'Icon'             : 'icon'             ,
    'Banner'           : 'banner'           ,
    'Discovery-splash' : 'discovery_splash' ,
    'Invite-splash'    : 'invite_splash'    ,
}

@Nitori.interactions(guild=TEST_GUILD)
async def guild_icon(
        choice: (GUILD_ICON_CHOICES, 'Which icon of the guild?' ) = 'icon',
            ):
    """Shows the guild's icon."""
    # Code goes brr..
```

Same as list:

```py
GUILD_ICON_CHOICES = [
    ('Icon'             , 'icon'             ),
    ('Banner'           , 'banner'           ),
    ('Discovery-splash' , 'discovery_splash' ),
    ('Invite-splash'    , 'invite_splash'    ),
]
```

When defining annotations only as `value`-s, the `name`-s will set as `str(value)`.

```py
from random import random

@Nitori.interactions(guild=TEST_GUILD)
async def roll(
        dice_count: (range(1, 7), 'With how much dice do you wanna roll?') = 1,
            ):
    """Rolls with dices."""
    amount = 0
    for _ in range(dice_count):
        amount += round(1.+(random()*5.))
    
    return str(amount)
```

### Required & not required parameters

Whether a command parameter is required or not, is defined whether you assign default value to it.

Examples are the  `cookie` command above for required and the `guild-icon` command for not required one.

> Do not forget that in python default-value parameters always follows non-default-value parameters.

Lets improve the `cookie` command to not require user!

```py
from hata import Embed

@Nitori.interactions(guild=TEST_GUILD)
async def cookie(client, event,
        user : ('user', 'To who?') = None,
            ):
    """Gifts a cookie!"""
    if user is None:
        source_user = client
        target_user = event.user
    else:
        source_user = event.user
        target_user = user
    
    return Embed(description=f'{source_user:f} just gifted a cookie to {target_user:f} !')
```

### Decorator parameters

`client.interactions` has no requires parameters, so can be used just as `@client.interactions` decorator, however in
most of the cases of slash commands, you want to also pass additional parameters.

##### guild

The `guild` parameter is already mentioned above, it defines in which guild(s) the command is available. Can be given
either as `Guild` or `guild_id` or as a `list` of `set` of them as well.

##### is_global

Defines whether the command is a global command. Accepts either `True` of `False`.

Mutually exclusive with the `guild` parameter. If neither `guild` not `is_global` parameter is given, the command will
become "non-global". More about them in the [Non-global](#non-global-commands) section.

##### show_for_invoking_user_only

Whether the source message should be shown only for the invoker user. Defaults to `False`.

This is a perfect time to change up our `/perms` command. Discord ignores everything except `content`, so we need to
change up the command as well, to return just a simple string.

```py
from hata import Embed

@Nitori.interactions(guild=TEST_GUILD, show_for_invoking_user_only=True)
async def perms(event):
    """Shows your permissions."""
    user_permissions = event.user_permissions
    if user_permissions:
        content = '\n'.join(permission_name.replace('_', '-') for permission_name in user_permissions)
    else:
        content = '*none*'
    
    return content
```

##### name

The most important feature, changing the name! By default a command's name will be it's function's name.

An important note might be, that the command's name might be displayed differently by Discord, so the extension will
do the prettification for you internally.

As an example: an already used function's name has conflict with the command's.

```py
from hata import id_to_time, DATETIME_FORMAT_CODE, elapsed_time

@Nitro.interactions(guild=TEST_GUILD, name='id-to-time')
async def idtotime(
        snowflake : ('int', 'Id please!'),
            ):
    """Converts the given Discord snowflake id to time."""
    time = id_to_time(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'
```

You can resolve name conflicts in an other way as well. Trailing `_` characters are ignored.

```py
from hata import id_to_time, DATETIME_FORMAT_CODE, elapsed_time

@Nitro.interactions(guild=TEST_GUILD)
async def id_to_time_(
        snowflake : ('int', 'Id please!'),
            ):
    """Converts the given Discord snowflake id to time."""
    time = id_to_time(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'
```

##### description

Description can be passed instead of defining as docstring. As an example this feature can be used when auto-generating
commands, like:

```py
class Action:
    __slots__ = ('action_name', 'embed_color', )
    def __init__(self, action_name, embed_color):
        self.action_name = action_name
        self.embed_color = embed_color
    
    async def __call__(self, client, event,
            user : ('user', 'Who?') = None,
                ):
        if user is None:
            source_user = client
            target_user = event.user
        else:
            source_user = event.user
            target_user = user
        
        return Embed(description=f'{source_user:f} {self.action_name}s {target_user:f} !', color=self.embed_color)

for action_name, embed_color in (('pat', 0x325b34), ('hug', 0xa4b51b), ('lick', 0x7840c3), ('slap', 0xdff1dc),):
    Nitori.interactions(Action(action_name, embed_color),
        name = action_name,
        description = f'Do you want some {action_name}s, or to {action_name} someone?',
        guild = TEST_GUILD,
    )

# Cleanup
del action_name, embed_color
```

##### delete_on_unload

Command specific setting, to overwrite the parent slasher's [delete_commands_on_unload](#delete_commands_on_unload).

##### allow_by_default

Whether the command should be allowed by default for everyone. Defaults to `True` of course. Not allowed commands
in the GUI are not hidden, they show up as gray.

Command permission overwrites can be set manually or with the [set_permissions](#Set command permissions) decorator.
If a command inside of the guild has permission set with the `set_permissions` decorator, then all other command's
manually set permission overwrites will be wiped out there, so make sure you either want manual or pre-set overwrites.

> Permission overwrites are buggy from Discord side, I take no responsibility if they do not work as expected.

## Tricks and Tips

##### Sending rich response

With `return` and `yield` statements, you can only send either `content` or `embed` fields. Using these statements is
still way more comfy than typing out the whole client method, so there is a middle way, called `SlashResponse`.

```py
@Marisa.interactions(guild=GUILD__NEKO_DUNGEON)
async def repeat(
        text : ('str', 'The content to repeat')
            ):
    """What should I exactly repeat?"""
    if not text:
        text = 'nothing to repeat'
    
    return SlashResponse(text, allowed_mentions=None)
```

##### Responding multiple times

Sometimes you might wanna respond multiple times on an event. At this case use `yield` instead of `return`.

```py
from random import random, choice
from hata import sleep

IMPROVISATION_CHOICES = [
    'Did Marisa really adopt Reimu?',
    'Yuuka beat Goku.',
    'Marisa! You know what you did!',
    'Thick cucumber Nitori',
    'Nitori Kappashiro',
    'Suwako\'s secret family technique is so lovely.',
    'Reimu\'s armpits, yeeaaa...',
    'Have you heard of Izaoyi love-shop?',
    'Marisa's underskirt shrooms are poggers'
]

@Nitori.interactions(guild=TEST_GUILD)
async def improvise():
    """Imrpovises some derpage"""
    yield '*Thinks*'
    await sleep(1.0+random()*4.0)
    yield choose(IMPROVISATION_CHOICES)
```

> Python limitation, you cannot `return` any value if you use `yield` inside of an `async def`.

##### Acknowledge the interaction event

The first response can be also empty just to acknowledge the event.

```py
@Nitori.interactions(guild=TEST_GUILD)
async def ping():
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'
```

Acknowledging can be useful if you do an additional request to an other site, because the event need to be acknowledged
within 3 seconds to send followup messages. If the event is acknowledged, followup messages can be sent within an
additional 15 minutes!

##### Capturing messages & exceptions

Acknowledging will never return a message object (Discord side), so it cannot be captured either, but followup messages
will do. So can do the following with them:

```py
message = yield content
```

Exceptions can be captured on the same way as well.

```py
try:
    yield content
except BaseException as err:
    # Do things.
```

After an interaction event is acknowledged with empty content, the second `yield` will edit the source message,
causing no `Message` object to be retrieved. This is why `SlashResponse` supports a `force_new_message` parameter,
which will force a new message causing a `Message` object to be retrieved.

```py
from hata import sleep
from hata.ext.slash import SlashResponse

@Nitori.interactions(guild=TEST_GUILD)
async def collect_reactions():
    """Collects reactions"""
    message = yield SlashResponse('Collecting reactions for 1 minute!', force_new_message=True)
    await sleep(60.0)
    
    reactions = message.reactions
    if reactions:
        emojis = list(reactions)
        # Limit reactions to 16 to avoid error from Discord
        del emojis[16:]
        
        yield ' '.join(emoji.as_emoji for emoji in emojis)
    else:
        yield 'No reactions were collected.'
```

##### Giving away control flow

Sometimes you have more commands calling the same coroutine function, which executes shared code among more commands.
This is all good, till the function is not a coroutine generator function. As we know you can yield from a generator
inside of one, but this is not exactly true at the case of coroutine generators.

```py
NEKO_LIFE = 'https://nekos.life/api/v2'

async def get_neko_life(client, keyword):
    yield
    url = f'{NEKO_LIFE}/{keyword}'
    
    async with client.http.get(url) as response:
        if response.status == 200:
            data = await response.json()
            content = data[keyword]
        else:
            content = 'Couldn\'t contact the API right now... OwO'
    
    yield content


@Nitori.interactions(guild=TEST_GUILD)
async def text_cat(client):
    """I will send text cats :3"""
    async for content in get_neko_life(client, 'cat')
        yield content

@Nitori.interactions(guild=TEST_GUILD)
async def why(client):
    """why are you using this commands?"""
    async for content in get_neko_life(client, 'why')
        yield content
```

Python misses asynchronous version of `yield from`, so you need to write out a full `async for` loop, making your code
loop derpy, or `yield` or `return` it, because having regard to this case, it is allowed to `yield` and `return`
`coroutine generator` object as well.

```py
@Nitori.interactions(guild=TEST_GUILD)
async def text_cat(client):
    """I will send text cats :3"""
    return get_neko_life(client, 'cat')

@Nitori.interactions(guild=TEST_GUILD)
async def why(client):
    """why are you using this commands?"""
    yield get_neko_life(client, 'why')
```

Both works completely fine.

##### Aborting command

Commands may be aborted using the `abort` function. It leaves from the command's execution and sends the passed
content familiarly to `SlashResponse`. The one difference is, that abort should be mainly used to send end-command
error message, so if only string `content` is passed to abort, it will show up only for the invoking user.

```py
from hata import DiscordException, ERROR_CODES, Embed
from hata.ext.slash import abort

@Nitori.interactions(guild=TEST_GUILD)
async def is_banned(client, event,
        user: ('user', 'Who should I check?')
            ):
    """Checks whether the user is banned."""
    if not event.user_permissions.can_ban_users:
        abort('You need to have `ban users` permissions to do this.')
    
    if not event.channel.cached_permissions_for(client).can_ban_users:
        abort('I need to have `ban users` permissions to do this.')
    
    yield # Acknowledge the event.
    
    try:
        ban_entry = await client.guild_ban_get(event.guild, user)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_ban:
            ban_entry = None
        else:
            raise
    
    embed = Embed(f'Ban entry for {user:f}').add_thumbnail(user.avatar_url)
    
    if ban_entry is None:
        embed.description = 'The user **NOT YET** banned.'
    
    else:
        embed.description = 'The user is banned.'
        
        reason = ban_entry.reason
        if reason is None:
            reason = '*No reason was specified.*'
        
        embed.add_field('Reason:', reason)
    
    yield embed
```

##### Changing parameter name

Familiarly to the `name` interaction parameter mentioned [above](#name), the tailing `_` characters are removed from
parameter names as well, but at some cases it is not enough. For this cases, you can add an extra third element to your
annotation tuple.

```py
@Nitori.interactions(guild=TEST_GUILD)
async def user_id(event,
        user_id: ('user_id', 'Get the id of an other user?', 'user') = None,
            ):
    """Shows your or the selected user's id."""
    if user_id is None:
        user_id = event.user.id
    
    return str(user_id)
```

##### Set command permissions

Default command permissions can be set with the `allow_by_default` command parameter and they can be overwritten with
the `set_permission` decorator. With `set_permission` you can set 1 overwrite, but with using more you can set
permission overwrite for up to 10 users or roles in each guild!

The decorator accepts 3 parameters:

| Name              | Type                                                          | Description                                                   |
|-------------------|---------------------------------------------------------------|---------------------------------------------------------------|
| guild             | `Guild`  or `int`                                             | The guild where the overwrite is applied in.                  |
| target            | `User`, `Role`, `Client`, `tuple` (`str` or `type`, `int`)    | The target entity. Can be either role or user.                |
| allow             | `bool`                                                        | Whether the command should be allowed for the target entity.  |

The `target` parameter can be given in many ways to allow relaxing definitions:

| Description                                                       | Example                   |
|-------------------------------------------------------------------|---------------------------|
| The entity itself.                                                | `Role.precreate(role_id)` |
| A `tuple` of the entity's type and of it's identifier.            | `(Role, role_id)`         |
| A `tuple` of the entity's type's name and of it's identifier.     | `('role', role_id)`       |

The most important thing about it, is of course an example!

```py
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from hata import Role, Embed, elapsed_time, DATETIME_FORMAT_CODE
from hata.ext.slash import SlashResponse, set_permission

MODERATOR_ROLE = Role.precreate(MODERATOR_ROLE_ID)

@Nitori.interactions(guild=TEST_GUILD, allow_by_default=False)
@set_permission(TEST_GUILD, MODERATOR_ROLE, True)
async def latest_users(event):
    """Shows the new users of the guild."""
    date_limit = datetime.now() - timedelta(days=7)
    
    users = []
    guild = event.guild
    for user in guild.users.values():
        # `joined_at` might be set as `None` if the user is a lurker.
        # We can ignore lurkers, so use `created_at` which defaults to Discord epoch.
        created_at = user.guild_profiles[guild].created_at
        if created_at > date_limit:
            users.append((created_at, user))
    
    users.sort(reverse=True)
    del users[10:]
    
    embed = Embed('Recently joined users')
    if users:
        for index, (joined_at, user) in enumerate(users, 1):
            created_at = user.created_at
            embed.add_field(
                f'{index}. {user.full_name}',
                f'Id: {user.id}\n'
                f'Mention: {user.mention}\n'
                '\n'
                f'Joined : {joined_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(joined_at)} ago*]\n'
                f'Created : {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
                f'Difference : {elapsed_time(relativedelta(created_at, joined_at))}',
            )
    
    else:
        embed.description = '*none*'
    
    return SlashResponse(embed=embed, allowed_mentions=None)
```

## Non-global commands

The slash extension supports non-global commands, which are neither global nor normal guild bound commands. These
commands are not added automatically, but matched with guild commands on the fly.

> You can specify that a command is non-global by not specifying neither that it is guild-bound nor a global one.

Their main purpose is, that you can add or remove these commands from guilds manually without modifying the source code.

Here is an example how to do it:

```py
from time import perf_counter
from hata import Embed
from hata.ext.slash import abort

@Nitori.interactions
async def ping(event):
    """HTTP ping-pong."""
    start = perf_counter()
    yield
    delay = (perf_counter()-start)*1000.0
    
    yield f'{delay:.0f} ms'


@Nitori.interactions(is_global=True)
async def enable_ping(client, event,
        allow: ('bool', 'Enable?')=True,
            ):
    """Enables the ping command in your guild."""
    guild = event.guild
    if guild is None:
        abort('Guild only command.')
    
    if not event.user_permissions.can_administrator:
        abort('You must have administrator permission to use this command.')
    
    application_commands = await client.application_command_guild_get_all(guild)
    for application_command in application_commands:
        # If you are not working with overlapping names, a name check should be enough.
        if application_command.name == ping.name:
            command_present = True
            break
    else:
        command_present = False
    
    if allow:
        if command_present:
            content = 'The command is already present.'
        else:
            await client.application_command_guild_create(guild, ping.get_schema())
            content = 'The command has been added.'
    else:
        if command_present:
            await client.application_command_guild_delete(guild, application_command)
            content = 'The command has been disabled.'
        else:
            content = 'The command is not present.'
    
    return Embed('Success', content)
```

If you have a guild bound ping command and a non-global one, always the guild bound will be matched first. However if
you added your ping as guild bound, then modified it to non-global, then the non-global one will match the old guild
bound one.

> If you are using `ClientWrapper` to add commands to more clients you will get back a command router instead of
> the command, so you wont be able to use `.name` or `.get_schema()` on it.

## Categories

It is possible to create a "category" command by creating a command with giving function as `None`. If you do not pass
a function, then name and description can not be auto-detected, so you will need to pass those manually as well.

```py
from random import choice
from bs4 import BeautifulSoup 
# `bs4` requires `lxml` library or you will get an error.

# You might wanna add `-tag`-s to surely avoid nsfw pictures
SAFE_BOORU = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='

# Use a cache to avoid repeated requests.
# Booru also might ban ban you for a time if you do too much requests.
IMAGE_URL_CACHE = {}

async def get_image_embed(client, tags, name, color):
    image_urls = IMAGE_URL_CACHE.get(tags, None)
    if image_urls is None:
        
        # Request image information
        async with client.http.get(SAFE_BOORU+tags) as response:
            if response.status != 200:
                return Embed('Error', 'Safe-booru unavailable', color=color)
            
            result = await response.read()
        
        # Read response and get image urls.
        soup = BeautifulSoup(result, 'lxml')
        image_urls = [post['file_url'] for post in soup.find_all('post')]
        
        if not image_urls:
            return Embed('Error', 'No images found.\nPlease try again later.', color=color)
        
        # If we received image urls, cache them
        IMAGE_URL_CACHE[tags] = image_urls
    
    image_url = choice(image_urls)
    return Embed(name, color=color, url=image_url).add_image(image_url)


SCARLET = Nitori.interactions(None, name='scarlet', description='Scarlet?', guild=TEST_GUILD)

@SCARLET.interactions
async def flandre(client):
    """Flandre!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'flandre_scarlet', 'Scarlet Flandre', 0xdc143c)

@SCARLET.interactions
async def remilia(client):
    """Remilia!"""
    yield # Yield one to acknowledge the interaction
    yield await get_image_embed(client, 'remilia_scarlet', 'Scarlet Remilia', 0x9400d3)
```

## Manual Responding

Sometimes the auto-responding feature just cannot do it. For these cases there are the questionably long named
`Client` interaction methods. This section just mentions these methods, please check their docs for more info.

The first response message can be sent only with `Client.interaction_response_message_create`. The `3` second
acknowledge time still stands.

```py
@Nitori.interactions(guild=TEST_GUILD)
async def repeat(client, event,
        text: ('str', 'Uhum?')
            ):
    """What should I exactly repeat?"""
    await client.interaction_response_message_create(event, text, allowed_mentions=None)
```

Not like `Client.message_create`, this endpoint can be called without any content to still acknowledge the
interaction event. This method also wont return a ``Message`` object (thank to Discord), but at least
`.interaction_followup_message_create` will.

The followup message methods are the following:
- `Client.interaction_followup_message_create`
- `Client.interaction_followup_message_edit`
- `Client.interaction_followup_message_delete`

An example using pure client methods:

```py
from hata import sleep

@Nitori.interactions(guild=TEST_GUILD)
async def kaboom(client, event):
    """Kabooom!!"""
    await client.interaction_response_message_create(event)
    
    messages = []
    for x in reversed(range(1, 4)):
        message = await client.interaction_followup_message_create(event, x)
        messages.append(message)
        await sleep(1.0)
    
    await client.interaction_followup_message_create(event, 'KABOOM!!')
    
    for message in messages:
        await sleep(1.0)
        await client.interaction_followup_message_delete(event, message)
```

An example using mixed `yield` and `Client` methods:

```py
from hata import sleep

@Nitori.interactions(guild=TEST_GUILD)
async def kaboom_mixed(client, event):
    """Kabooom!!"""
    yield
    
    messages = []
    for x in reversed(range(1, 4)):
        message = yield str(x)
        messages.append(message)
        await sleep(1.0)
    
    yield 'KABOOM!!'
    
    for message in messages:
        await sleep(1.0)
        await client.interaction_followup_message_delete(event, message)
```

## FAQ

#### Commands not show up

Slash commands might not show up after you launched your bot with them. This can be caused by many reasons:

-  Lazy caching

    When your Discord app (browser, desktop or mobile) is launched, the application commands are cached by it
    correctly, but the commands meanwhile might not show up correctly.

-  Global command sync time

    Global commands have a shocking **1** hour sync time. This is applied after creating, updating and when removing
    them as well.

- Command is not global neither guild bound
    
    You may have forgot to specify that your command is either global or guild bound.
    
    > Note, that specifying whether the command is global or guild bound to a sub-commands does nothing.

#### Commands are not removed

Removed slash commands may not disappear after they are removed. This can have many reasons.

- Guild bound command syncing
    
    Hata syncs global commands every time, but this is not true for guild bound commands.
    
    Only those guilds are synced initially, which have any command added bound them. The rest of the guilds are synced
    only when the first interaction is received from them. This means, when you remove all the guild bound commands
    from a guild, you need to call any of those commands to remove them from Discord as well. This behaviour is also
    true for non-global commands, which are matched runtime.

- Modifying command type
    
    When modifying a command's type from guild bound to non-global or from non-global to guild bound, the command wont
    disappear, because the other command type will be able to still match the source command. This is not applicable
    for guilds, which not have the command bound.

- Unloading extension
    
    By default commands wont disappear when their extension is unloaded on favor to avoid 1 hour global command sync
    time when reloading an extension. This behaviour can be altered (mentioned later).

- Global command sync time & Lazy caching
