import re, random

from hata import Client, start_clients, User, Embed, UserBase, ChannelBase
from hata.ext.commands import setup_extension, Converter, ConverterFlag, checks, FlaggedAnnotation

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


@NekoBot.commands(name='print', alises=['say'])
async def print_(client, message, content):
    if content:
        await client.message_create(message.channel, content)


@NekoBot.commands
async def hug(client, message, user: User = None):
    if user is None:
        user = message.author
    
    await client.message_create(message.channel, f'Hugs {user:m} !')


@NekoBot.commands
async def separate(client, message, *args):
    if not args:
        result = 'Nothing to separate'
    else:
        result = ', '. join(args)
    await client.message_create(message.channel, result)


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


async def owner_only_handler(client, message, command, check):
    await client.message_create(message.channel, f'You must be the owner of the bot to use the `{command}` command.')

@NekoBot.commands(checks=[checks.owner_only(handler=owner_only_handler)])
async def owner(client, message):
    await client.message_create(message.channel, f'My masuta is {client.owner:f} !')


start_clients()
