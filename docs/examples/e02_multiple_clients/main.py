from hata import Client, start_clients, ClientWrapper

TOKEN_1 = ''
TOKEN_2 = ''
TOKEN_3 = ''

Sakuya = Client(TOKEN_1)
Remilia = Client(TOKEN_2)
Flandre = Client(TOKEN_3)

# With `ClientWrapper` you can add event handlers to all clients...
ALL = ClientWrapper()

# ...or to just the specified ones.
ONLY_SAKUYA_AND_REMILIA = ClientWrapper(Sakuya, Remilia)


@ALL.events
async def ready(client):
    # This event is registered for all (currently 3) clients
    print(f'{client:f} is connected!')


@ONLY_SAKUYA_AND_REMILIA.events
async def message_create(client, message):
    # This event is registered only to Sakuya and Remilia
    # When either of them sees a message that is '!basement' they will reply with 'nope'
    if message.content == '!basement':
        await client.message_create(message.channel, 'nope')


# Don't forget that you can always explicitly specify client to register an event for
# (ClientWrapper is just a shortcut and makes it easy to register events for multiple clients at the same time)
@Flandre.events
async def message_create(client, message):
    # This event is registered only to Flandre
    # When she sees a message that is '!basement' she will reply with 'of course!'
    if message.content == '!basement':
        await client.message_create(message.channel, 'of course!')


# Since we have multiple clients we call start_clients which is a helper method to start all clients properly.
start_clients()
