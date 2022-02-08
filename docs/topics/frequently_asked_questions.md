### Where can I find usage examples?

Examples can be found in the [examples folder](https://github.com/HuyaneMatsu/hata/tree/master/docs/examples) of the
repository.

### How do I set activity?

When creating a client, you may pass an `ActivityRich` instance to the `activity` parameter.

```py
from hata import ActivityRich, Client

client = Client(
    'token',
    activity = ActivityRich('Eating'),
)
```

To change the type of the activity, use the `type_` parameter of `ActivityRich`.

```py
from hata import ACTIVITY_TYPES, ActivityRich, Client

client = Client(
    'token',
    activity = ActivityRich('Eating', type_=ACTIVITY_TYPES.competing),
)
```

### How do I send a message to a specific channel?

If you have a channel entity

```py
await client.message_create(channel, 'content')
```

If you don't passing just the `id` is fine too.

```py
await client.message_create(123456789123456789, 'content')
```

### How do I send a direct message?

First you get / create the bot's direct message channel with the user.

If you have the user entity:

```py
channel = await client.channel_private_create(user)
```

If you have just it's id:

```py
channel = await client.channel_private_create(8899898989898989898)
```

### How do I get the ID of a sent message?

`Client.message_create` returns the created message (if you create a non empty one of course).
You can access it's id like `messsage.id`.

```py
message = await client.message_create(channel, 'content')
message_id = message.id
```

### How do I upload an image?

To upload a file to Discord, you will need to use a file-like object, or it's data.

To upload a file from your file system, we recommend to use `scarletio.ReuAsyncIO`. It is which is an async file-like
object which also handles retrying requests.

```py
from scarletio import ReuAsyncIO

with (await ReuAsyncIO('flan.png')) as file:
    await client.message_create(channel, file=file)
```

To upload multiple files, use a list.

```py
from scarletio import ReuAsyncIO

with (await ReuAsyncIO('flan.png')) as file_1, (await ReuAsyncIO('remi.png')) as file_2:
    await client.message_create(channel, file=[file_1, file_2])
```

To send a file with a different name, pass a `name` - `file` pair.

```py
from scarletio import ReuAsyncIO

with (await ReuAsyncIO('flan.png')) as file:
    await client.message_create(channel, file=('vampy.png', file))
```

If you want to upload something from an url, you will have to request it first. To request anything, you can create
a new http session, but it is recommended just to use the client's preexisting one.

```py
async with client.http.get(file_url) as response:
    if response.status == 200:
        data = await response.read()
    else:
        data = None

if data is None:
    await client.message_create(channel, 'something went wrong')
else:
    await client.message_create(channel, file=('file_name', data))
```

Since a `bytes` object has no name, it is highly recommended to define one when sending it.

### How can I add a reaction to a message?

To add a reaction on a message, use the `client.reaction_add` method.

```py
await client.reaction_add(message, emoji)
```

To get an builtin / unicode emoji, you can use the `BUILTIN_EMOJIS` dictionary.

```py
from hata import BUILTIN_EMOJIS

emoji = BUILTIN_EMOJIS['thumbsup']
```

If you are using constant emojis, it is recommended to create references to them. At the case of custom emojis it can
be acquired `Emoji.precreate`

```py
from hata import Emoji

emoji = Emoji.precreate(704392145330634812)
```

### How do I get a specific entity?

When using constant entities, it is recommended to create them with the respective type's `.precreate` method.
It creates a reference to the entity, which is picked up and updated when the entity is received from Discord.

```py
from hata import User

user = User.precreate(24343344487441449444)
```

It is possible to get entities dynamically from cache, with rich functionality methods, and at a few cases with client
api methods as well.

```py
from hata import USERS

# from cache
user = USERS.get(user_id)

# rich functionality methods
user = channel.get_user(user_id)
user = guild.get_user(user_id)

# client api method
user = await client.get_user(user_id)
```

### How do I make a web request?

To make a web request you should use a non-blocking library. Hata already requires one, since it is necessary to
communicate with Discord.

```py
from scarletio import HTTPClient, get_event_loop

session = HTTPClient(get_event_loop())

async with session.get('https://nekos.life/api/v2/cat') as response:
    if response.status == 200:
        data = await response.json()
    else:
        data = None
```

Since web resources are cached per sessions it is recommended to reuse the same one. For this reason using the client's
http session is the preferred way of doing web requests.

```py
async with client.http.get('https://nekos.life/api/v2/cat') as response:
    if response.status == 200:
        data = await response.json()
    else:
        data = None
```

### How do I use a local image file for an embed image?

A special case is, when using an uploaded attachment within an embed. To do it, pass your file as usual, then in the
embed instead of defining the image's url, do `attachment://image.png`, where `image.png` is the name of the file you
send.

```py
from hata import Embed, ReuAsyncIO

with (await ReuAsyncIO('some_file_path')) as file:
    await client.message_create(
        channel,
        embed = Embed().add_image('attachment://image.png'),
        file = ('image.png', file),
    )
```
