from hata import Client, start_clients, ClientWrapper

TOKEN_1 = ''
TOKEN_2 = ''

Sakuya = Client(TOKEN_1)
Remilia = Client(TOKEN_2)

# With `ClientWrapper` you can add event handlers to all or just to the passed clients.
ALL = ClientWrapper()

@ALL.events
async def message_create(client, message):
    if message.content == '!ping':
        await client.message_create(message.channel, 'pong')


@ALL.events
async def ready(client):
    print(f'{client:f} is connected!')


# Not like `Client.start()`, `start_clients()` starts each offline client parallelly
start_clients()
