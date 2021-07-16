from hata import Client

TOKEN = ''

# Configure your client with it's token.
Sakuya = Client(TOKEN)

# Set event handler for message create event. When a message is received, the added function will ba called.
#
# Events are dispatched asynchronously, so multiple events can be handled parallelly.
@Sakuya.events
async def message_create(client, message):
    if message.content == '!ping':
        # Sending a message can fail due to network error, or by lack of permissions.
        #
        # Un-retrieved exceptions are logged to stderr, at the next garbage collection cycle.
        await client.message_create(message.channel, 'pong')


# Set handler to the `ready` event. Ready is called when the client's shards are all booted up.
@Sakuya.events
async def ready(client):
    # Many Discord entities support various format codes.
    #
    # `f` stands for `.full_name` property.
    print(f'{client:f} is connected!')


Sakuya.start()
