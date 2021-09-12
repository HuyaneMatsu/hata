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

Three component types are supported: `Row`, `Button` and `Select`.

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

- A message can have up to `5` rows.
- `custom_id` can be `100` character long.

###### Button limitations

- Up to `5` buttons can be in a row.
- Component `label` can be `80` characters long.

###### Select limitations

- Up to `1` select can be in a row.
- A select can have `25` choices.
- A select can have choices in range `[1:25]`.
- Select `min_values` can be in range `[0:15]`.
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

#### Deleting the component's message

The source message can be deleted, by first acknowledging it, then using the
`.interaction_response_message_delete` client method.

```py
from hata import BUILTIN_EMOJIS, Embed, DATETIME_FORMAT_CODE, elapsed_time
from hata.ext.slash import Button, InteractionResponse

CUSTOM_ID_USER_INFO_CLOSE = 'user_info.close'
EMOJI_X = BUILTIN_EMOJIS['x']

BUTTON_USER_INFO_CLOSE = Button(
    emoji = EMOJI_X,
    custom_id = CUSTOM_ID_USER_INFO_CLOSE,
)

@Nitori.interactions(guild=TEST_GUILD)
async def user_info(client, event,
        user: ('user', 'Check out someone other user?') = None,
            ):
    if user is None:
        user = event.user
    
    embed = Embed(
        user.full_name,
    ).add_thumbnail(
        user.avatar_url,
    )
    
    created_at = user.created_at
    embed.add_field(
        'User Information',
        (
            f'Created: {created_at:{DATETIME_FORMAT_CODE}} [*{elapsed_time(created_at)} ago*]\n'
            f'Profile: {user:m}\n'
            f'ID: {user.id}'
        ),
    )
    
    # We ignore guild specific information to keep it short.
    
    return InteractionResponse(
        embed = embed,
        components = BUTTON_USER_INFO_CLOSE,
    )

@Nitori.interactions(custom_id=CUSTOM_ID_USER_INFO_CLOSE)
async def close_user_info(client, event):
    # Allow closing for the source user
    if event.user is not event.message.interaction.user:
        return
    
    # We can use `yield` as well for acknowledging it.
    await client.interaction_component_acknowledge(event)
    await client.interaction_response_message_delete(event)
```

#### Sending notification

Sometimes you do not want to edit the source message, but want to notify the user, about anything in general. You
can do it by first acknowledging the event, then creating a followup message.


```py
from random import choice
from hata import Emoji, Embed
from hata.ext.slash import Button, ButtonStyle, InteractionResponse

CUSTOM_ID_ORIN_DANCE = 'orin_dance_please'
EMOJI_ORIN_DANCE = Emoji.precreate(704392145330634812)

BUTTON_ORIN_DANCE = Button(
    emoji = EMOJI_ORIN_DANCE,
    custom_id = CUSTOM_ID_ORIN_DANCE,
    style = ButtonStyle.green,
)

@Nitori.interactions(guild=TEST_GUILD)
async def orindance():
    return InteractionResponse(
        embed = Embed('Party!', url='https://orindance.party/').add_image(choice(ORIN_DANCE_IMAGES)),
        components = BUTTON_ORIN_DANCE,
    )

@Nitori.interactions(custom_id=TEST_GUILD)
async def party(client, event):
    if event.user is event.message.interaction.user:
        
        old_url = event.message.embed.image.url
        orin_dance_images = ORIN_DANCE_IMAGES.copy()
        try:
            orin_dance_images.remove(old_url)
        except ValueError:
            pass
        
        return Embed('Party!', url='https://orindance.party/').add_image(choice(orin_dance_images))
    
    # Notify the user; we also could use `yield` to acknowledging it.
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(
        event,
        'Please start your own party to dance!',
        show_for_invoking_user_only = True,
    )
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

## Using select

Selects are not as useful as buttons in practice, since lacking form functionality means, they are just a dynamic
slash command choice parameter.

```py
from import Embed
from hata.ext.slash import Select, Option, InteractionResponse


WAIFU_API_BASE_URL = 'https://api.waifu.pics'

WAIFU_API_HEADERS = {
    'Content-Type': 'application/json',
}
WAIFU_API_REQUEST_DATA = b'{}'


WAIFU_CUSTOM_ID = 'waifu_api'

WAIFU_TYPES = [
    'waifu',
    'neko',
    'shinobu',
    'megumin',
]

# We will cache responses
WAIFU_CACHE_BY_KEY = {waifu_type: [] for waifu_type in WAIFU_TYPES}


@Nitori.interactions(guild=TEST_GUILD)
async def waifu():
    """Ships waifus!"""
    embed = Embed('Please select a waifu type to ship.')
    select = Select(
        [Option(waifu_type, waifu_type) for waifu_type in WAIFU_TYPES],
        custom_id = WAIFU_CUSTOM_ID,
    )
    
    return InteractionResponse(embed=embed, components=select)


@Nitori.interactions(custom_id=WAIFU_CUSTOM_ID)
async def handle_waifu_select(client, event):
    # We filter out 3rd party users based on original and current invoking user.
    if event.message.interaction.user is not event.user:
        return
    
    # Second we filter out incorrect selected values.
    # You can change the command over time and the can return bad option as well.
    selected_waifu_types = event.interaction.options
    if (selected_waifu_types is None):
        return
    
    selected_waifu_type = selected_waifu_types[0]
    if (selected_waifu_type not in WAIFU_TYPES):
        return
    
    # Try to get url from cache
    cache = WAIFU_CACHE_BY_KEY[selected_waifu_type]
    if cache:
        url = cache.pop()
    else:
        # We could not get url from cache
        
        # Do 1 yield to acknowledge the event.
        yield
        
        # We could use a Lock to avoid parallel requests, but that would expose us to other edge cases.
        async with client.http.post(
            f'{WAIFU_API_BASE_URL}/many/sfw/{selected_waifu_type}',
            headers = WAIFU_API_HEADERS,
            data = WAIFU_API_REQUEST_DATA,
        ) as response:
            
            if response.status == 200:
                data = await response.json()
            else:
                data = None
        
        url = None
        
        if (data is not None):
            try:
                files = data['files']
            except KeyError:
                pass
            else:
                cache.extend(files)
                
                if cache:
                    url = cache.pop()
    
    # Url defaults to `None`, so passing it to `url` field is fine.
    embed = Embed('Please select a waifu type to ship.', url=url)
    
    if url is None:
        embed.description = (
            f'*Could not find any free {selected_waifu_type} now.\n'
            f'Please try again later.*'
        )
    else:
        embed.add_image(url)
    
    # We re-build the select again with one difference, we mark the used one as default.
    select = Select(
        [Option(waifu_type, waifu_type, default=(waifu_type == selected_waifu_type)) for waifu_type in WAIFU_TYPES],
        custom_id = WAIFU_CUSTOM_ID,
    )
    
    yield InteractionResponse(embed=embed, components=select)
```

And advantage of select over generic choices might be, that you cna allow the user to select non, or multiple options.

```py
import functools
from hata import BUILTIN_EMOJIS
from hata.ext.slash import InteractionResponse, Select, Option, wait_for_component_interaction

EMOJI_ELEPHANT = BUILTIN_EMOJIS['elephant']
LABEL_ELEPHANT = 'elephant'
DESCRIPTION_ELEPHANT = (
    f'Visiting big elephants.\n'
    f'{EMOJI_ELEPHANT:e} sugoi {EMOJI_ELEPHANT:e}'
)

EMOJI_LION = BUILTIN_EMOJIS['lion']
LABEL_LION = 'lion'
DESCRIPTION_LION = (
    f'Peeking at scary lions.\n'
    f'(I love cats {EMOJI_LION:e})'
)

EMOJI_ZEBRA = BUILTIN_EMOJIS['zebra']
LABEL_ZEBRA = 'zebra'
DESCRIPTION_ZEBRA = (
    f'Watching prison horses be like.\n'
    f'{EMOJI_ZEBRA:e} are cute!'
)


ANIMAL_IDENTIFIER_TO_DESCRIPTION = {
    LABEL_ELEPHANT: DESCRIPTION_ELEPHANT,
    LABEL_LION: DESCRIPTION_LION,
    LABEL_ZEBRA: DESCRIPTION_ZEBRA,
}

ZOO_SELECT = Select(
    [
        Option(LABEL_ELEPHANT, LABEL_ELEPHANT, emoji=EMOJI_ELEPHANT),
        Option(LABEL_LION, LABEL_LION, emoji=EMOJI_LION),
        Option(LABEL_ZEBRA, LABEL_ZEBRA, emoji=EMOJI_ZEBRA),
        
    ],
    placeholder = 'Select animals!',
    min_values = 0,
    max_values = 3,
)

def check_is_user_same(user, event):
    return (user is event.user)


@Nitori.interactions(guild=TEST_GUILD)
async def zoo(event):
    """Visiting zoo!"""
    
    message = yield InteractionResponse('Please select animals to visit!', components=ZOO_SELECT)

    try:
        component_interaction = await wait_for_component_interaction(message, timeout=300.0,
            check=functools.partial(check_is_user_same, event.user))
    
    except TimeoutError:
        content = 'You didn\'t decide which animals to visit and the zoo closed, see ya tomorrow!'
        component_interaction = None
    else:
        selected_animals = component_interaction.interaction.options
        if selected_animals is None:
            content = 'Going to zoo only to buy icecream?'
        else:
            content_parts = ['Visiting animals in the zoo!']
            
            for selected_animal in selected_animals:
                try:
                    description = ANIMAL_IDENTIFIER_TO_DESCRIPTION[selected_animal]
                except KeyError:
                    continue
                
                content_parts.append(description)
            
            content = '\n\n'.join(content_parts)
    
    yield InteractionResponse(content, components=None, message=message, event=component_interaction)
```
