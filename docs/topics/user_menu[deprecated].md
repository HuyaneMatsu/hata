# Introduction

User menu allows you to create `Pagination` like mini-apps, where you wait for reactions and then respond.
The user menu-runner executes the middle layer which deals with waiting, timeouts and race conditions.

> This is an experimental feature.

## Special methods & attributes

User menu factorizes the wrapped classes, picking up special methods and other attributes.

### close_emoji

Emoji used to close the menu. Can be either `None`, `Emoji` instance. If the user reacts with it, the
`.close(CancelledError()` will be called.

> Defaults to `None`.

### emojis

The emojis which are added on the respective message.

> Defaults to `None`.

### allow_third_party_emojis

Whether third party emojis should trigger the menu as well. Note that these emojis are not removed.

> Defaults to `False`.

### timeout

The timeout after which the menu will expire.

Defining timeout is optional, but recommended. If it's undefined or negative then no timeout will be applied.

> Defaults to `0.0`.

### check

Check is an optional **non-async** function that check whether the reaction add or delete emoji should be further
processed.

The following parameters will be passed to it:

| Name      | Type                                              |
|-----------|---------------------------------------------------|
| event     | ``ReactionAddEvent``, ``ReactionDeleteEvent``     |

It will return the following values:

| Name              | Type      |
|-------------------|-----------|
| should_process    | `bool`    |

> Defaults to `None`.

### initial_invoke

A required **async** function to return the default content of the menu to display.

Function takes no parameters and will return the following values:

| Name      | Type                          |
|-----------|-------------------------------|
| content   | `str`, `EmbedBase`, `None`    |

If it returns `None` then the menu will be instantly closed. Note that at this point `menu.close()` can also be called
to not add any reactions on the menu and leave.

### invoke

A required **async** function called when the menu is invoked with a reaction. Not called if the emoji is
`close_emoji`.

The following parameters will be passed to it:

| Name      | Type                                              |
|-----------|---------------------------------------------------|
| event     | ``ReactionAddEvent``, ``ReactionDeleteEvent``     |

It will return the following values:

| Name      | Type                          |
|-----------|-------------------------------|
| content   | `str`, `EmbedBase`, `None`    |

If non-`None` value is returned the respective message will be edited and the timeout will be reset.

### cancel

Called when the menu is closed, timeouted or when any exception occurs.

The following parameters will be passed to it:

| Name      | Type                      |
|-----------|---------------------------|
| exception | `None`, `BaseException`   |

The exceptions value depends on how the menu was closed:
- `None` : The factorized class called `menu.close()` without passing any exception.
- `TimeoutError` : The menu timed-out.
- `CancelledError` : The menu was closed with `close_emoji`.
- `PermissionError` : The client has no permissions to add reactions on the menu (can be ignored).
- `ConnectionError` : No internet connection (can be ignored).
- `DiscordException` : Exception raised by Discord (can be ignored but if important can be ensured with
    `client.events.error`)

Other exception will not trigger it.

## Parameters

User menu has 3 parameters from which 2 are required. Any extra positional and keyword parameters of the
menu runner instance will be passed to the factorized class constructor.

### client

The client who executes the menu.

### channel

The channel to send the message to.

Can also be given as `Message` or as `InteractionEvent`.

### message

A message to re-use inside the menu. Optional keyword only.

## Examples

### Feed the cat

```py
from hata.emoji import BUILTIN_EMOJIS
from hata.ext.command_utils import UserMenuFactory

@UserMenuFactory
class CatFeeder:
    
    cat = BUILTIN_EMOJIS['cat']
    eggplant = BUILTIN_EMOJIS['eggplant']
    
    emojis = (cat, )
    timeout = 300.0
    
    allow_third_party_emojis = True
    
    # The user menu runner is always passed.
    def __init__(self, menu):
        self.menu = menu
        self.reacted = set()
    
    
    async def initial_invoke(self):
        return f'Please react with {self.cat} to feed her!\n' \
               f'If no new person reacts for 5 minutes the cat will be sad.'
    
    
    async def invoke(self, event):
        emoji = event.emoji
        user = event.user
        reacted = self.reacted
        if emoji is self.cat:
            
            if user in reacted:
                return None
            
            reacted.add(user)
            
            return f'Please react with {self.cat} to feed her!\n' \
                   f'If no no new unique person reacts for 5 minutes the cat will be sad.\n' \
                   f'\n' \
                   f'{len(reacted)} people gave the cat a slice of cake!'
        
        if emoji is self.eggplant:
            return f'Please react with {self.cat} to feed her!\n' \
                   f'If no no new unique person reacts for 5 minutes the cat will be sad.\n' \
                   f'\n' \
                   f'{len(reacted)} people gave the cat a slice of cake!\n' \
                   f'\n' \
                   f'{user:m} you wot mate?'
        
        return None
    
    async def close(self, exception):
        if exception is None:
            return
        
        if isinstance(exception, TimeoutError):
            menu = self.menu
            
            content = f'The {self.cat}has been fed by {len(self.reacted)} people.'
            await menu.client.message_edit(menu.message, content)
            
            if menu.channel.cached_permissions_for(menu.client).can_manage_messages:
                await menu.client.reaction_clear(menu.message)


@Nitori.interactions(guild=TEST_GUILD)
async def cat_feeder(client, event):
    """Feed the cat!"""
    await CatFeeder(client, event)
```

### Zeref's pagination

There is a `Pagination`-like class which you can subclass included just for this purpose.

```py
from hata.emoji import BUILTIN_EMOJIS
from hata.ext.command_utils import UserMenuFactory, UserPagination

@UserMenuFactory
class ZerefPagination(UserPagination):
    
    cake = BUILTIN_EMOJIS['cake']
    emojis = (*UserPagination.emojis[:-1], cake, *UserPagination.emojis[-1:])
    
    __slots__ = ('user',)
    
    def __init__(self, menu, pages, user):
        UserPagination.__init__(self, menu, pages)
        self.user = user
    
    def check(self, event):
        return (self.user is event.user)
    
    async def invoke(self, event):
        if event.emoji is self.cake:
            menu = self.menu
            await menu.client.message_create(menu.channel, menu.message.content)
            return None
        
        return await UserPagination.invoke(self, event)

@Nitori.interactions(guild=TEST_GUILD)
async def zeref_pagination(client, event):
    """Zeref's cake paginator."""
    await ZerefPagination(client, event, ['hi', 'hello'], event.user)
```
