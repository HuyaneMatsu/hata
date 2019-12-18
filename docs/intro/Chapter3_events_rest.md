# Events (rest)

This chapter will superficially drive you trough other predefined tools
at using `CommandProcesser` and other events.

Context:
- [ContentParser](#ContentParser)
- [Reaction events](#Reaction events)
- [Pagination](#Pagination)
- [Waiting for reaction and message](#Waiting for reaction and message)
- [Cooldown](#Cooldown)

## ContentParser

One of the indispensable tool of a discord api wrapper is probably a
content parser. This wrapper's content parser can parse users,
roles, channels and much more from the message's content.

This tool creates a function then compiles it. So it has no extra overhead
at runtime. 

```py
from hata import Client, start_clients
from hata.events import CommandProcesser
from hata.events_compiler import ContentParser

client=Client(TOKEN)

on_command = client.events(events.CommandProcesser('e!')).shortcut

@on_command
@ContentParser('user, flags=mna, default="message.author"')
async def rate(client,message,target):
    if target is client:
        result=10
    else:
        result=target.id%11
    # nickname check
    await client.message_create(message.channel,
        f'I rate {target.name_at(message.guild)} {result}/10')
    
start_clients()
```

> [ContentParser reference](https://github.com/HuyaneMatsu/hata/blob/master/docs/ref/ContentParser.md)

## Reaction events

There are 2 predefined reaction events which implement only basic `waitfor`
protocol (so only the `append` and the `remove` method).

```py
# lets import and add them
from hata.events import ReactionAddWaitfor, ReactionDeleteWaitfor

client.events(ReactionAddWaitfor)
client.events(ReactionDeleteWaitfor)
```

These are familiar to the `CommandProcesser` showed at the previous chapter,
but as said, these implement only the `waitfor` part. Each other tool later
at this chapter, which uses reactions, requires these events to be added or
they should throw exceptions (`AttributeError`-s and such).

## Pagination

An option to display paginated messages, which allows moving between the
pages with arrows. This class allows modifications and closing for every user.
Also works in private channels.

```py
# lets import the extra
from hata import Embed
from hata.events import Pagination

@on_command
async def pagination_example(client,message,content):
    pages = [
        Embed('page 1'),
        Embed('page 2'),
        Embed('page 3'),
            ]
    
    await Pagination(client,message.channel,pages)

# a more usefull example
@on_command
async def bans(client,message,content):
    guild=message.guild
    if guild is None:
        return
    if not guild.cached_permissions_for(client).can_ban_user:
        return await client.message_create(message.channel,
            embed=Embed(description='I have no permissions to check it.'))
                                 
    ban_data = await client.guild_bans(guild)

    if not ban_data:
        await client.message_create(message.channel,'None')
        return

    embeds=[]
    maintext=f'Guild bans for {guild.name} {guild.id}:'
    limit=len(ban_data)
    index=0

    while True:
        field_count=0
        embed_length=len(maintext)
        embed=Embed(title=maintext)
        embeds.append(embed)
        while True:
            user,reason=ban_data[index]
            if reason is None:
                reason='Not defined.'
            name=f'{user:f} {user.id}'
            embed_length+=len(reason)+len(name)
            if embed_length>7900:
                break
            embed.add_field(name,reason)
            field_count+=1
            if field_count==25:
                break
            index+=1
            if index==limit:
                break
        if index==limit:
            break
    
    index=0
    field_count=0
    embed_ln=len(embeds)
    result=[]
    while True:
        embed=embeds[index]
        index+=1
        embed.add_footer(f'Page: {index}/{embed_ln}. Bans {field_count+1}-{field_count+len(embed.fields)}/{limit}')
        field_count+=len(embed.fields)
        
        result.append(embed)
        
        if index==embed_ln:
            break
    
    await Pagination(client,message.channel,result)
```

The pagination expires after 240 seconds by default but it can be changed
when created. Also each action on the pagination will delay it's expiration.

At a lot of cases you will probably want different pagination classes but
this class gives a nice starting point to implement one.

> [Pagination reference](https://github.com/HuyaneMatsu/hata/blob/master/docs/ref/Pagination.md)

## Waiting for reaction and message

There are two pretty simple waiters defined at 
[events.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events.py).

### `wait_for_reaction(client,message,case,timeout)`

Waits for a reaction on the given message.

The `case` argument should be a function which accepts two arguments,
`emoji` and `user`. It should return either `True` or `False` or any `object`.
If it returned `True` then the `wait_for_reaction` will return the `emoji`
and the `user`. If `case` returns `False` nothing will happen. If the `case`
returns anything else then it will return that value as well.

The `timeout` argument is in seconds. If the timeout occurs before the `case`
yields anything that is not `False` then the `wait_for_reaction` will raise
`TimeoutError`.

```py
from hata import BUILTIN_EMOJIS
from hata.events import wait_for_reaction
import re

EMOJI_ANGER=BUILTIN_EMOJIS['anger']

class check_reacter_and_anger():
    __slots__ = ('user',)
    def __init__(self,user):
        self.user=user
    def __call__(self,emoji,user):
        return (emoji is EMOJI_ANGER and user is self.user)
    
@on_command
async def bully(client,message,content):
    if not message.channel.cached_permissions_for(client).can_add_reactions:
        return # just to make sure
    
    message = await client.message_create(message.channel,'YES BULLY!')
    await client.reaction_add(message,EMOJI_ANGER)
    
    try:
        await wait_for_reaction(client,message,check_reacter_and_anger(message.author),60.)
    except TimeoutError:
        return
    finally:
        try:
            await client.reaction_delete_own(message,EMOJI_ANGER)
        except DiscordException:
            pass
            
    await client.message_edit(message,'NO BULLY!')
    @on_command

class check_reacter():
    __slots__ = ('user',)
    def __init__(self,user):
        self.user=user
    def __call__(self,emoji,user):
        return user is self.user:

@on_command
async def waitreaction(client,message,content):
    if not message.channel.cached_permissions_for(client).can_add_reactions:
        return # just to make sure
        
    await client.message_create(message.channel,'Please react on this message')
    
    try:
        emoji,user = await wait_for_reaction(client,message,check_reacter(message.author),300.)
    except TimeoutError:
        return
            
    await client.message_create(message.channel,emoji.as_emoji*5)
    
class check_reacter_and_skin_tone():
    PATTERN=re.compile('.*?_skin_tone_(\d)')
    __slots__ = ('user',)
    def __init__(self,user):
        self.user=user
    def __call__(self,emoji,user):
        if user is not self.user:
            return False
        if emoji.is_custom_emoji:
            return None
        parsed=self.PATTERN.fullmatch(emoji.name)
        if parsed is None:
            return None
        return parsed.group(1)

@on_command
async def check_skin_tone(client,message,content):
    await client.message_create(message.channel,'Please react on this message')
    
    try:
        _,_,skin_tone = await wait_for_reaction(client,message,check_reacter_and_skin_tone(message.author),300.)
    except TimeoutError:
        return
    
    if skin_tone is None:
        text = 'Thats an emoji without skin tone'
    else:
        text = f'skin tone : {skin_tone}'
    await client.message_create(message.channel,text)
```

### `wait_for_message(client,channel,case,timeout)`

Waits for a message at the given channel. Acts same as `wait_for_reaction`
but its `case` gets only 1 argument passed - the `message`.

```py
from hata import parse_emoji
from hata.events import wait_for_message

def check_message_for_emoji(message):
    parsed=parse_emoji(message.content)
    if parsed is None:
        return False
    return parsed
    
@on_command
async def waitemoji(client,message,content):
    channel=message.channel
    
    message_to_delete = await client.message_create(channel,'Waiting!')
    
    try:
        _,emoji = await wait_for_message(client,channel,check_message_for_emoji,240.)
    except TimeoutError:
        return
    finally:
        await client.message_delete(message_to_delete)
    
    await client.message_create(channel,emoji.as_emoji*5)
        
```

## Cooldown

You can define cooldown for a command. It allows you to choose how many times
a user can execute a command or how many times the command can be executed in
a guild or in a channel.

```py
from hata.events import Cooldown
from hata.events_compiler import ContentParser
from hata import Embed

@on_command
@Cooldown('user',60.,limit=2)
@ContentParser('user, flags=mna, default="message.author"')
async def avatar(client, message, user):
    url=user.avatar_url_as(size=4096)
    embed=Embed(f'{user:f}\'s avatar', url=url)
    embed.add_image(url)
    await client.message_create(message.channel, embed=embed)
```

Cooldowns can be shared between commands with different weight. A handler can
be added as well too, to define what happens when a command is on cooldown.

> [Cooldown reference](https://github.com/HuyaneMatsu/hata/blob/master/docs/ref/Cooldown.md)
