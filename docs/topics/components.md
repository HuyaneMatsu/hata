# Components

### Introduction

Message components, mainly known as components, are interactive gui elements which might get included with a message.
Your application or bot can send and interact with them. They are customizable and easy to use.

Hata supports components with native ways as well. This topic is a continuation of the [slash](slash.md) one, so if you
did not read that yet please go ahead.

Writing component based interactions is usually three times longer than generic ones. So if writing some extra code
is not your bread I do not recommend using components, although I never said they are more complicated.

## Component Structures

Components can be passed to `InteractionResponse` and to many client methods as well:

- `.message_create`
- `.message_edit`
- `.webhook_message_create`
- `.webhook_message_edit`
- `.interaction_response_message_create`
- `.interaction_response_message_edit`
- `.interaction_followup_message_create`
- `.interaction_followup_message_edit`
- `.interaction_component_message_edit`

Three component types are supported: `Row`, `Button` and `Select`. However select is not yet released (not really
useful either), so we will ignore it for now.

`components` parameters can be passed either as the component itself, list of components, or as a nested list of
components. Some examples might clarify it more.

Below are 3 examples on how to make 1 row have 3 buttons:

```py
# The component itself
components = Row(Button(...), Button(...), Button(...))

# List of components.
components = [
    Row(Button(...), Button(...), Button(...)),
]

# Nested list of components.
components = [
    [Button(...), Button(...), Button(...)],
]
```

Below are 3 examples on how to make 3 rows each having 1 button:

```py

# List of components
components = [
    Row(Button(...)),
    Row(Button(...)),
    Row(Button(...)),
]

# List of components with skipping rows.
components = [
    Button(...),
    Button(...),
    Button(...),
]

# Nested list of  components
components = [
    [Button(...)],
    [Button(...)],
    [Button(...)],
]
```

## Limitations

- Row limit is `5`.
- Up to `5` buttons can be in a row.
- Component `label` can be `80` characters long.
- `custom_id` can be `100` character long.

###### Select limitations

- Up to `1` select can be in a row.
- A select can have `25` choices.
- A select can have choices in range `[1:25]`.
- Select `min_values` can be in range `[1:15]`.
- Select `max_values` can be in range `[1:25]`.

## Component commands

You may add component commands to a slashers which are called when a component with the specified `custom_id` is
used.

Similarly to slash commands they are registered with the `client.interactions` decorator. The difference is that now
you will use only the `custom_id` parameter.

Take a look at the following ping-pong command:

```py
from random import random
from hata import BUILTIN_EMOJIS
from hata.ext.slash import Button, ButtonStyle, InteractionResponse


EMOJI_PING_PONG = BUILTIN_EMOJIS['ping_pong']

CUSTOM_ID_PING = 'ping_pong.ping'
CUSTOM_ID_PONG = 'ping_pong.pong'

BUTTON_PING = Button('ping', EMOJI_PING_PONG, custom_id=CUSTOM_ID_PING, style=ButtonStyle.green)
BUTTON_PONG = Button('pong', EMOJI_PING_PONG, custom_id=CUSTOM_ID_PONG, style=ButtonStyle.violet)


@Nitori.interactions(guild=TEST_GUILD)
async def ping_pong():
    if random() < 0.5:
        button = BUTTON_PING
    else:
        button = BUTTON_PONG
    
    return InteractionResponse(f'**ping {EMOJI_PING_PONG:e} pong**', components=button)


@Nitori.interactions(custom_id=CUSTOM_ID_PING)
async def ping_pong_ping():
    return InteractionResponse(components=BUTTON_PONG)

@Nitori.interactions(custom_id=CUSTOM_ID_PONG)
async def ping_pong_pong():
    return InteractionResponse(components=BUTTON_PING)
```

Usually you can separate component commands implementation in 3 parts: defining static variables, defining the
command and defining the component interaction. Stick to this pattern, and you can't go wrong.


```py
from hata import BUILTIN_EMOJIS, Emoji
from hata.ext.slash import Button, ButtonStyle, InteractionResponse


# Static variables
CAT_FEEDER_CAT_EMOJI = Emoji.precreate(853998730071638056)
CAT_FEEDER_FOOD_EMOJI = BUILTIN_EMOJIS['fish']
CAT_FEEDER_CUSTOM_ID = 'cat_feeder.click'


# Command
@Nitori.interactions(guild=TEST_GUILD)
async def cat_feeder():
    """Hungry cat feeder!"""
    return InteractionResponse(
        f'Please feed my cat {CAT_FEEDER_CAT_EMOJI:e}, she is hungry.',
        components=Button('Feed cat', CAT_FEEDER_FOOD_EMOJI, custom_id=CAT_FEEDER_CUSTOM_ID, style=ButtonStyle.green)
    )


# Component interaction
@Nitori.interactions(custom_id=CAT_FEEDER_CUSTOM_ID)
async def cat_fed(event):
    return (
        f'Please feed my cat {CAT_FEEDER_CAT_EMOJI:e}, she is hungry.\n'
        f'\n'
        f'Thanks, {event.user:f} for feeding my cat.'
    )
```

#### Using regex

You can pass regex as `custom_id` for component commands to match. It can be used to store specific states or button
positions and then get the data back when clicked. Here is a short example for giving roles on button click.

```py
import re
from hata import Role
from hata.ext.slash import Button, Row, set_permission, abort, InteractionResponse


ROLE_OWNER = Role.precreate(403581319139033090)

ROLE_NSFW_ACCESS = Role.precreate(828576094776590377)
ROLE_ANNOUNCEMENTS = Role.precreate(538397994421190657)

BUTTON_NSFW_ACCESS = Button('Nsfw access', custom_id=f'role_claimer.{ROLE_NSFW_ACCESS.id}')
BUTTON_ANNOUNCEMENTS = Button('Announcements', custom_id=f'role_claimer.{ROLE_ANNOUNCEMENTS.id}')

ROLE_CLAIMER_COMPONENTS = Row(BUTTON_NSFW_ACCESS, BUTTON_ANNOUNCEMENTS)

ROLE_CLAIMER_ROLES = {
    ROLE_NSFW_ACCESS.id: ROLE_NSFW_ACCESS,
    ROLE_ANNOUNCEMENTS.id: ROLE_ANNOUNCEMENTS,
}


@Nitori.interactions(guild=TEST_GUILD, allow_by_default=False)
@set_permission(TEST_GUILD, ROLE_OWNER, True)
async def role_claimer(event):
    """Role claimer message. (Owner only)"""
    
    # Double check.
    if not event.user.has_role(ROLE_OWNER):
        abort('Owner only')
    
    return InteractionResponse('Claim role by clicking on it', components=ROLE_CLAIMER_COMPONENTS)


@Nitori.interactions(custom_id=re.compile('role_claimer\.(\d+)'))
async def give_role(client, event, role_id):
    role_id = int(role_id)
    
    role = ROLE_CLAIMER_ROLES.get(role_id, None)
    if (role is not None) and (not event.user.has_role(role)):
        await client.user_role_add(event.user, role)

```

#### Using multiple custom id

Using multiple strings or regex `custom_id`-s work as well. Here is a simple poison chooser example for multiple string.
This example could have been done with regex as well, but an advantage of strings is that their lookup time is `O(1)`,
meanwhile regex ones are `O(n)`.

```py
from hata import Embed, BUILTIN_EMOJIS
from hata.ext.slash import InteractionResponse, Button, Row, ButtonStyle


CUSTOM_ID_CAKE = 'choose_your_poison.cake'
CUSTOM_ID_CAT = 'choose_your_poison.cat'
CUSTOM_ID_SNAKE = 'choose_your_poison.snake'
CUSTOM_ID_EGGPLANT = 'choose_your_poison.eggplant'

EMOJI_CAKE = BUILTIN_EMOJIS['cake']
EMOJI_CAT = BUILTIN_EMOJIS['cat']
EMOJI_SNAKE = BUILTIN_EMOJIS['snake']
EMOJI_EGGPLANT = BUILTIN_EMOJIS['eggplant']

CHOOSE_YOUR_POISON_ROW = Row(
    Button('cake', custom_id=CUSTOM_ID_CAKE, style=ButtonStyle.violet),
    Button('cat', custom_id=CUSTOM_ID_CAT, style=ButtonStyle.gray),
    Button('snake', custom_id=CUSTOM_ID_SNAKE, style=ButtonStyle.green),
    Button('eggplant', custom_id=CUSTOM_ID_EGGPLANT, style=ButtonStyle.red),
)

CHOOSE_YOUR_POISON_CUSTOM_ID_TO_EMOJI = {
    CUSTOM_ID_CAKE: EMOJI_CAKE,
    CUSTOM_ID_CAT: EMOJI_CAT,
    CUSTOM_ID_SNAKE: EMOJI_SNAKE,
    CUSTOM_ID_EGGPLANT: EMOJI_EGGPLANT,
}


@Nitori.interactions(guild=TEST_GUILD)
async def choose_your_poison():
    """What is your weakness?"""
    return InteractionResponse(embed=Embed('Choose your poison'), components=CHOOSE_YOUR_POISON_ROW)


@Nitori.interactions(custom_id=[CUSTOM_ID_CAKE, CUSTOM_ID_CAT, CUSTOM_ID_SNAKE, CUSTOM_ID_EGGPLANT])
async def poison_edit_cake(event):
    emoji = CHOOSE_YOUR_POISON_CUSTOM_ID_TO_EMOJI.get(event.interaction.custom_id, None)
    if (emoji is not None):
        return emoji.as_emoji
```


## Waiting for component interaction

You can wait for component interaction on a message by using the `wait_for_component_interaction` coroutine function.

```py
import functools
from hata import parse_emoji, Embed
from hata.ext.slash import abort, Button, Row, InteractionResponse, ButtonStyle, wait_for_component_interaction


ADD_EMOJI_BUTTON_ADD = Button('Add!', style=ButtonStyle.green)
ADD_EMOJI_BUTTON_CANCEL = Button('Nah.', style=ButtonStyle.red)

ADD_EMOJI_COMPONENTS = Row(ADD_EMOJI_BUTTON_ADD, ADD_EMOJI_BUTTON_CANCEL)

def check_is_user_same(user, event):
    return (user is event.user)


@Nitori.interactions(guild=TEST_GUILD)
async def add_emoji(client, event,
        emoji: ('str', 'The emoji to add.'),
        name: ('str', 'Custom name to add the emoji with.') = None
            ):
    """Adds an emoji to the guild."""
    if not client.is_owner(event.user):
        abort('Owner only!')
    
    emoji = parse_emoji(emoji)
    if emoji is None:
        abort('That\'s not an emoji.')
    
    if emoji.is_unicode_emoji():
        abort('Cannot add unicode emojis')
    
    if name is None:
        name = emoji.name
    else:
        if len(name) > 32:
            abort('Name length can be max 32.')
    
    embed = Embed('Are you sure to add this emoji?').add_field('Name:', name).add_image(emoji.url)
    
    message = yield InteractionResponse(embed=embed, components=ADD_EMOJI_COMPONENTS)
    
    try:
        component_interaction = await wait_for_component_interaction(message, timeout=300.0,
            check=functools.partial(check_is_user_same, event.user))
    
    except TimeoutError:
        component_interaction = None
        cancelled = True
    else:
        if component_interaction.interaction == ADD_EMOJI_BUTTON_CANCEL:
            cancelled = True
        else:
            cancelled = False
    
    if cancelled:
        embed.title = 'Adding emoji has been cancelled.'
    else:
        embed.title = 'Emoji has been added!'
        
        async with client.http.get(emoji.url) as response:
            emoji_data = await response.read()
        
        await client.emoji_create(event.guild, name, emoji_data)
    
    yield InteractionResponse(embed=embed, components=None, message=message, event=component_interaction)
```

> By passing `event` to `InteractionResponse`, you can change the interact event to respond to. When passing it
> as a component interaction event, it will acknowledge it and/or edit the source message.
>
> When passing the `event` parameter as `None` it will default back to the default interaction event. Since the
> default one is an application command event, it will create a new message by default, but we can make it edit a
> message by using the `message` parameter.
>
> Component interaction events always ignore the message parameter.


### Waiting for multiple component interaction

In the same way as `wait_for_component_interaction` returns on the first sufficient interaction,
`iter_component_interactions` can be used to (async) iterate over multiple ones.

```py
import functools
from hata.ext.slash import Button, InteractionResponse, iter_component_interactions


BUTTON_ATTEND = Button('Attend', style=ButtonStyle.green)

def check_is_user_unique(users, event):
    return (event.user not in users)

def render_joined_users(users):
    content_parts = ['I will pick who I like the most from the attenders.\n\nAttenders:']
    for user in users:
        content_parts.append('\n')
        content_parts.append(user.mention)
    
    return ''.join(content_parts)

def get_liking(client_id, user_id):
    if user_id > client_id:
        liking = user_id-client_id
    else:
        liking = client_id-user_id
    
    return liking

def pick_most_liked(client, users):
    client_id = client.id
    
    most_liked = users[0]
    most_liking = get_liking(client_id, most_liked.id)
    
    for user in users[1:]:
        liking = get_liking(client_id, user.id)
        if liking < most_liking:
            most_liking = liking
            most_liked = user
    
    return most_liked


@Nitori.interactions(guild=TEST_GUILD)
async def pick(client, event):
    """Picks who I like the most from the attenders."""
    users = [event.user]
    message = yield InteractionResponse(render_joined_users(users), allowed_mentions=None, components=BUTTON_ATTEND)
    
    try:
        async for component_interaction in iter_component_interactions(message, timeout=60.0,
                check=functools.partial(check_is_user_unique, users)):
            users.append(component_interaction.user)
            
            # limit the amount of users to 10.
            if len(users) == 10:
                break
            
            yield InteractionResponse(render_joined_users(users), allowed_mentions=None,
                event=component_interaction)
    
    except TimeoutError:
        component_interaction = None
    
    most_liked = pick_most_liked(client, users)
    
    content_parts = ['From:']
    for user in users:
        content_parts.append('\n')
        content_parts.append(user.mention)
    
    content_parts.append('\n\nI like ')
    content_parts.append(most_liked.mention)
    content_parts.append(' the most.')
    
    content = ''.join(content_parts)
    
    yield InteractionResponse(content, allowed_mentions=most_liked, components=None, message=message,
        event=component_interaction)
```
