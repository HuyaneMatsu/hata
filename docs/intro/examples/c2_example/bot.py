import re, random

from hata import Client, start_clients, User, Embed
from hata.ext.commands import setup_extension, Converter, ConverterFlag, checks

from cute_commands import cute_commands

OWO_RP = re.compile('owo|uwu|0w0', re.I)
AYY_RP = re.compile('ay+', re.I)

TOKEN = ''
NekoBot = Client(TOKEN)

setup_extension(NekoBot, 'n!')

NekoBot.commands.extend(cute_commands)

@NekoBot.commands
async def pat(client, message):
    await client.message_create(message.channel, 'Puurs !')


@NekoBot.commands
async def say(client, message, content):
    if content:
        await client.message_create(message.channel, content)


@NekoBot.commands
async def hug(client, message, user:User=None):
    if user is None:
        user = message.author
    
    await client.message_create(message.channel, f'Hugs {user:m} !')


@NekoBot.commands
async def separate(client, message, *args):
    if not args:
        result = 'Nothing to separate'
    else:
        result = '\n'. join(args)
    await client.message_create(message.channel, result) 


@NekoBot.commands
async def avatar(client, message, user : Converter('user', flags=ConverterFlag.user_default.update_by_keys(everywhere=True), default_code='message.author')):
    color = user.avatar_hash&0xffffff
    if not color:
        color = user.default_avatar.color
    
    url=user.avatar_url_as(size=4096)
    embed=Embed(f'{user:f}\'s avatar', color=color, url=url)
    embed.add_image(url)
    
    await client.message_create(message.channel, embed=embed)


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

async def owner_only_handler(client, message, command, check):
    await client.message_create(message.channel, f'You must be the owner of the bot to use the `{command}` command.')

@NekoBot.commands(checks=[checks.owner_only(handler=owner_only_handler)])
async def owner(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')


@NekoBot.commands(aliases=['pong'])
async def ping(client, message):
    await client.message_create(message.channel, f'{client.gateway.latency*1000.:.0f} ms')


@NekoBot.commands
async def default_event(client, message):
    if message.author.is_bot:
        return
    
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


start_clients()
