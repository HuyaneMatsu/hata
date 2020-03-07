# class `Cooldown`

A helper wrapper class to implement cooldowns.

- Source : [events.py](https://github.com/HuyaneMatsu/hata/blob/master/hata/events.py)

## Wrapping a command in cooldown

```py
from hata.events import Cooldown

@on_command
@Cooldown('user', 30.,)
async def ping(client, message, content):
    await client.message_create(message.channel, f'{client.gateway.latency.:.0f} ms')
    
```

### `Cooldown(for_, reset, limit=1, weight=1, handler=_default_handler, name=None, func=None)`

##### `for_`

The `for_` argument stands for for what the cooldown is meant for. It can be
passed as `'user'`, `'channel'` or `'guild'` (`'u'`, `'c'` and `'g'` works as
well). If invalid value is passed, then `ValueError` will be raised. 

##### `reset`

The time after the cooldown resets. Should be float.

##### `limit`

The limit how much times the command can be called by the user at the specific
channel or guild before getting limited. Should be `int`, default is `1`.

##### `weight`

The amount how much this command counts to acquiring the `limit`.
Should be `int`, the default is `1`.

##### `handler`

A specific coroutine function (any callable object is fine, what returns
an awaitable), what is awaited, when the command is on cooldown and a
user calls it.

It always calls the function with 4 variables:

| name      | description                                       |
|-----------|---------------------------------------------------|
| client    | The client who's command triggered the cooldown.  |
| message   | The message what triggered the cooldown.          |
| command   | The command's name what triggered the cooldown.   |
| time_left | The time left till reset.                         |

> If `for_` is set to `guild`, and the command was called from a
[private](ChannelPrivate.md) / [group](ChannelGroup.md) channel, then
`time_left` will be always `-1.0` at those cases.


```pys
from hata import DiscordException, CancelledError, sleep
from hata.events import Cooldown

class CooldownHandler:
    __slots__=('cache',)
    
    def __init__(self):
        self.cache = {}
    
    async def __call__(self, client, message, command, time_left):
        user_id = message.author.id
        try:
            notification, waiter = self.cache[user_id]
        except KeyError:
            pass
        else:
            if notification.channel is message.channel:
                try:
                    await client.message_edit(notification,
                        f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
                except DiscordException:
                    pass
                return

            waiter.cancel()

        try:
            notification = await client.message_create(message.channel,
                f'**{message.author:f}** please cool down, {time_left:.0f} seconds left!')
        except DiscordException:
            return

        waiter = client.loop.create_task(self.waiter(client,user_id,notification)
        self.cache[user_id] = (notification, waiter)

    async def waiter(self, client, user_id, notification):
        try:
            await sleep(30., client.loop)
        except CancelledError:
            pass
        del self.cache[user_id]
        try:
            await client.message_delete(notification)
        except DiscordException:
            pass

@on_command
@Cooldown('user', 30., handler=CooldownHandler())
async def ping(client, message, content):
    await client.message_create(message.channel, f'{client.gateway.latency.:.0f} ms')
```

##### `name`

Same as passing `name` when adding a command at
[CommandProcesser](CommandProcesser.md). Instead of trying to get the name of
the command by checking different kind of attributes of it, it will use the
passes string instead.

##### `func`

When `func` is passed it will instantly wrap the function and return itself.
But if `func` is not passed, then it will act like a decorator.

```py
from hata.events import Cooldown

@on_command
@Cooldown('user', 30.,) # func not passed -> decorator
async def ping(client, message, content):
    await client.message_create(message.channel, f'{client.gateway.latency.:.0f} ms')


async def pong(client, message, content):
    await client.message_create(message.channel, f'{client.gateway.latency.:.0f} ms')
    
on_command(Cooldown('user',30.,func=pong)) # func passed -> wraps instantly

```

## Sharing cooldowns between commands

Using an already created [Cooldown](Cooldown.md)'s `.shared` method allows
to share cooldows between commands. The new cooldown object inherits the
source's `for_`, `reset`, `limit` and `handler`.

```py
from hata.events import ContentParser
from hata import Embed

@on_command
@Cooldown('user', 60., limit=3, weight=2, handler=CooldownHandler())
@ContentParser('user, flags=mna, default="message.author"')
async def avatar(client, message, user):
    url = user.avatar_url_as(size=4096)
    embed = Embed(f'{user:f}\'s avatar', url=url)
    embed.add_image(url)
    await client.message_create(message.channel, embed=embed)

@on_command
@avatar.shared(weight=1)
async def myavatar(client, message, content):
    url = message.author.avatar_url_as(size=4096)
    embed = Embed('Your avatar', url=url)
    embed.add_image(url)
    await client.message_create(message.channel, embed=embed)
```

### `cooldown_instance.shared(weight=0., name=None, func=None)`

Acts familiarly as `Cooldown()` itself. 

If weight is not set, the new [cooldown](Cooldown.md) will inherit the source
cooldown's `weight`.

If `func` is passed, then the it will be wrapped instantly. If not, then the
cooldown will act as a decorator.
