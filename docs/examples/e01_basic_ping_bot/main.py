from hata import Client

# Replace this with your bot token, see topics/getting_started.md to see how you can get one
TOKEN = ''

# Create your client instance by using your bot token
Sakuya = Client(TOKEN)


# Register event handler for message create event. When a message is received the decorated function will be called.
#
# Events are dispatched asynchronously so multiple events can be handled in parallel.
@Sakuya.events
async def message_create(client, message):
    if message.content == '!ping':
        # Sending message can fail due to network error or by lack of permissions.
        #
        # If exception is not explicitly caught it will be logged to stderr and ignored.
        await client.message_create(message.channel, 'pong')


# Register handler for the `ready` event. Ready is called when the client shards are all booted up.
@Sakuya.events
async def ready(client):
    # Hata has various format codes for Discord entities
    #
    # In this case `f` stands for `.full_name` property.
    print(f'{client:f} is connected!')


Sakuya.start()
