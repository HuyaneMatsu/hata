from hata import Client, start_clients

TOKEN = ''
NekoBot = Client(TOKEN)


@NekoBot.events
async def ready(client):
    print(f'{client.full_name} ({client.id}) logged in')


@NekoBot.events
async def message_create(client, message):
    """Simple reply functionality based on message content."""
    if message.author.is_bot:
        return  # We will ignore messages from bot accounts
    
    content = message.content
    if (content is None):
        return
    
    content = content.lower()

    if content in ('owo', 'uwu', '0w0'):
        await client.message_create(message.channel, content)

    elif content.startswith('ayy'):
        await client.message_create(message.channel, 'lmao')


start_clients()
