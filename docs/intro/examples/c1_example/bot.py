import re

from hata import Client, start_clients

OWO_RP = re.compile('owo|uwu|0w0', re.I)
AYY_RP = re.compile('ay+', re.I)

TOKEN = ''
NekoBot = Client(TOKEN)

@NekoBot.events
async def ready(client):
    print(f'{client:f} ({client.id}) logged in')


@NekoBot.events
async def message_create(client, message):
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
