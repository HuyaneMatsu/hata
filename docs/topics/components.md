# Components

### Introduction

Components, mainly known as buttons are interactive gui elements, which might be included with messages.

Hata supports components on native ways as well, but this topic is a continuation of the [slash](slash.md) one.

## Component Structures

Components can be passed to `InteractionResponse` and to many client methods as well:

- `.message_create`
- `.message_edit`
- `.interaction_response_message_create`
- `.interaction_response_message_edit`
- `.interaction_followup_message_create`
- `.interaction_followup_message_edit`
- `.interaction_component_message_edit`

3 component types are supported, `Row`, `Button` and `Select`. However select is not yet released (not really useful
either), so we will ignore it for now.

`components` parameters can be either as the component itself, list of components, or as a nested list of components.
Some examples might clarify it more.

First start with the 1 row, 3 buttons next to each other cases.

```py
# The component itself
components = Row(Button(...), Button(...), Button(...))

# List of components.
components = [
    Row(Button(...), Button(...), Button(...)),
]

# Nexted list of components.
components = [
    [Button(...), Button(...), Button(...)],
]
```

Then, 3 row, 1 button in each example:

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

## Waiting for component interaction

You can wait for component interaction on a message or on an interaction with a message by using
`wait_for_component_interaction`.

###### TODO

```py
import functools
from hata import parse_emoji, Embed
from hata.ext.slash import abort, Button, Row, InteractionResponse, ButtonStyle

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

###### TODO
