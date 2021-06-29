# User menu

### Introduction

User menu allows you to create `Pagination` like mini-apps, where you wait for reactions and then respond. The user
menu's runner executes the middle layer, which deals with waiting, timeout and race conditions.

> This is an experimental feature.

## Special methods & attributes

User menu factorizes the wrapped classes, picking up special methods and other attributes.

##### close_emoji

Emoji used to close the menu. Can be either `None` or `Emoji` instance. If the user reacts with it, the
`.close(CancelledError()` will be called.

> Defaults to `None`.

##### emojis

The emojis which are added on the respective message.

> Defaults to `None`.

##### allow_third_party_emojis

Whether third party emojis should trigger the menu as well. Note, that these emojis are not removed.

> Defaults to `False`.

##### timeout

The timeout after the menu will expire.

Defining timeout is optional, but recommended. When not defining or when defining it as negative, the menu will have no
timeout applied.

> Defaults to `0.0`.

##### check

Check is an optional **non-async** function to check whether the reaction add or delete emoji should be further
processed.

The following parameters are passed to it:

| Name      | Type                                              |
|-----------|---------------------------------------------------|
| event     | ``ReactionAddEvent`` or ``ReactionDeleteEvent``   |

And should return the following values:

| Name              | Type      |
|-------------------|-----------|
| should_process    | `bool`    |

> Defaults to `None`.

##### initial_invoke

A required **async** function to return the default content of the menu to display.

No parameter is passed to it and should return the following values:

| Name      | Type                          |
|-----------|-------------------------------|
| content   | `str`, `EmbedBase`, `None`    |

If returns `None`, the menu is instantly closed. Note, that `menu.close()` can also be called at this point to not add
any reactions on the menu and leave.

##### invoke

A required **async** function called when the menu is invoked with a reaction. Not called if the emoji is
`close_emoji`.

The following parameters are passed to it:

| Name      | Type                                              |
|-----------|---------------------------------------------------|
| event     | ``ReactionAddEvent`` or ``ReactionDeleteEvent``   |

And should return the following values:

| Name      | Type                          |
|-----------|-------------------------------|
| content   | `str`, `EmbedBase`, `None`    |

If non-`None` value is returned the respective message will be edited and the timeout will be reset.

##### cancel

Called when the menu is closed, timeouted, or when any exception occurs.

The following parameters are passed to iti:

| Name      | Type                      |
|-----------|---------------------------|
| exception | `None` or `BaseException` |

The exception's value depends how the menu was closed:
- `None` : The factorized class called `menu.close()` without passing any exception.
- `TimeoutError` : The menu timed out.
- `CancelledError` : The menu was closed with `close_emoji`.
- `PermissionError` : The client has no permissions to add reactions on the menu. (Can be ignored)
- `ConnectionError` : No internet connection. (Can be ignored)
- `DiscordException` : Exception raised by Discord. (Can be ignored, if important, is ensured with
    `client.events.error`)

Other exception should not be triggered.

## Parameters

User menu has 3 parameters, from which 2 is required. Every extra positional and keyword parameter with the created
menu runner instance is passed to the factorized class's constructor.

##### client

The client who executes the menu.

##### channel

The channel to send the message to.

Also can be given as `Message` to reply or as `InteractionEvent` as well.


##### message

A message to reuse inside of the menu. Optional keyword only.

## Examples

##### Feed the cat

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
        return f'Please react with {self.cat:e} to feed her!\n' \
               f'If no new person reacts for 5 minutes the cat will be sad.'
    
    
    async def invoke(self, event):
        emoji = event.emoji
        user = event.user
        reacted = self.reacted
        if emoji is self.cat:
            
            if user in reacted:
                return None
            
            reacted.add(user)
            
            return f'Please react with {self.cat:e} to feed her!\n' \
                   f'If no no new unique person reacts for 5 minutes the cat will be sad.\n' \
                   f'\n' \
                   f'{len(reacted)} people gave the cat a slice of cake!'
        
        if emoji is self.eggplant:
            return f'Please react with {self.cat:e} to feed her!\n' \
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
            
            content = f'The {self.cat:e}has been fed by {len(self.reacted)} people.'
            await menu.client.message_edit(menu.message, content)
            
            if menu.channel.cached_permissions_for(menu.client).can_manage_messages:
                await menu.client.reaction_clear(menu.message)


@Nitori.interactions(guild=TEST_GUILD)
async def cat_feeder(client, event):
    """Feed the cat!"""
    await CatFeeder(client, event)
```

##### Zeref's pagination

There is a `Pagination` like subclassable class included just for this purpose.

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
