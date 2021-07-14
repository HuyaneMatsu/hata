from hata import Client

TOKEN = ''

Sakuya = Client(TOKEN)

@Sakuya.events
async def message_create(client, message):
    if message.content == '!messageme':
        # Client class has many useful high level methods implemented, so you do not need to deal with low level "rest"
        # calls. Usually each high level `Client` method has a low level http method as well. Lets take
        # `Client.message_create(...)` and it's low level `Client.http.message_create(...)` methods as examples.
        #
        # You cannot call api methods on simple `User` instances, since if you have multiple clients, I believe, it
        # should not decide which one to use instead of you.
        channel = await client.channel_private_create(message.author)
        
        await client.message_create(channel, 'Hello!')

@Sakuya.events
async def ready(client):
    print(f'{client:f} is connected!')


Sakuya.start()
