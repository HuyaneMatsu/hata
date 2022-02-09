# Introduction

When it comes to interactions, slash commands and components are a great first step, but for longer inputs they are
not intuitive enough. This is when multi-field forms / model interactions come into the picture.

## Building Forms

Forms are standalone components, with sub-components as fields.

For now forms are limited to 5 sub-components. And the only accepted sub-components are `TextInput`-s (basically rows
of text inputs, but rows are inserted automatically if not defined.)

## Limitations

- Up to `5` rows in each form.

### Text input limitations

- Up to `1` text input can be in a row.

# Form commands

To send a form response to the user just return the form from a slash or a component command, or use the
`Client.interaction_form_send` method.

```py
from hata.ext.slash import Form, TextInput, TextInputStyle

INTRODUCTION_FORM = Form(
    'Introduce yourself',
    [
        TextInput(
            'What is your name?',
            min_length = 2,
            max_length = 128,
            custom_id = 'name',
        ),
        TextInput(
            'Something about you?',
            style = TextInputStyle.paragraph,
            min_length = 64,
            max_length = 1024,
            custom_id = 'bio',
        ),
    ],
    custom_id = 'introduction',
)
 
@Nitori.interactions(guild=TEST_GUILD)
def introduce_myself():
    """Creates an introduction embed after filling a form."""
    return INTRODUCTION_FORM
```

Defining `custom_id` for each component is not required, but its highly recommended since each received field is matched by
its `custom_id`.

You may add form commands to slasher by specifying what forms they should capture based on their `custom_id`. Also, you can
specify that you want to match forms submit interaction and not component interactions by passing `target=` either as
`'form'` / `'form_submit'`.


```py
from hata import Embed

@Nitori.interactions(custom_id='introduction', target='form')
async def introduction_form_submit(event, *, name, bio):
    return Embed(
        f'Hi, my name is {name}',
    ).add_field(
        'About me',
        bio,
    ).add_thumbnail(
        event.user.avatar_url,
    )
```

## Parameters

Positional parameters of form submit commands work in the same way as component commands'. This means single and 
multiple regex `custom_id`-s are both supported.

Additionally, form submit commands support keyword parameters as well. These are matched from the fields of the
submitted form.

```py
import re
from hata import DiscordException, ERROR_CODES, Embed
from hata.ext.slash import abort

ADD_ROLE_FORM = Form(
    'Add role', # Any dummie title does it
    [
        TextInput(
            'Additional message to send?',
            style = TextInputStyle.paragraph,
            max_length = 512,
            custom_id = 'message',
        ),
    ],
)


@Nitori.interactions(guild=TEST_GUILD)
def add_role(
    user: ('user', 'User to add role to'),
    role: ('role', 'The role to give'),
):
    """Add role to a user."""
    # Check for permissions
    if not event.user_permissions.can_manage_roles:
        abort('You need `manage roles` permission to invoke this command.')
    
    if not event.guild.cached_permissions_for(client).can_manage_roles:
        abort('I need `manage roles` permission to execute this command.')
    
    if not event.user.has_higher_role_than(role):
        abort('You must have higher role than the role you are trying to give.')
    
    if not client.has_higher_role_than(role):
        abort('I must have higher role than the role you are trying to give.')
    
    # Using `.copy_to` on forms works as well.
    return ADD_ROLE_FORM.copy_with(
        title = f'Add role {role.name} to {user.full_name}',
        custom_id = f'add_role.{user.id}.{role.id}',
    )


@Nitori.interactions(custom_id=re.compile('add_role\.(\d+)\.(\d+)'), target='form')
async def add_role(client, event, user_id, role_id, *, message):
    user_id = int(user_id)
    role_id = int(role_id)
    
    yield # acknowledge the even
    
    await client.role_add(user, (event.guild_id, role_id), reason=message)
    
    # Try to send DM to the poor being.
    channel = await channel_private_create(user_id)
    
    guild = event.guild
    role = guild.roles[role_id]
    
    embed = Embed(
        description = 'You have received role {role.name} in {guild.name}.',
    )
    
    # Since message doesn't have `required` nor `min_length` passed it can be `None`.
    if (message is not None):
        embed.add_field(
            'Message',
            message,
        )

    try:
        await client.message_create(channel, embed=embed) 
    except DiscordException as err:
        # Ignore the exception if the user has dm-s disabled.
        if err.code != ERROR_CODES.cannot_message_user: # user has dm-s disabled
            raise
    
    # Note: The user might not be cached at this point. Request it. If you have user caching enabled + intent, it will
    # do nothing.
    user = await client.user_get(user_id)
    
    embed = Embed(
        description = 'You gave {role.name} to {user.full_name}',
    )
    
    if (message is not None):
        embed.add_field(
            'Message',
            message,
        )
    
    yield embed
```

By annotating keyword parameters with string or with regex, you can customize what `custom_id`-s they are matching.
If the annotation is neither string nor regex pattern, it is ignored.

> Annotating a parameter with "regular" regex is pretty pointless. Could be good when updating old code
> and you want to support multiple `custom_id`-s.

```py
import re
from hata import Embed
from hata.ext.slash import Form, TextInput, TextInputStyle, abort

# Define constants

WAIFUS = {}

CUSTOM_ID_WAIFU_FORM = 'waifu.form'
CUSTOM_ID_WAIFU_AGE = 'waifu.age'
CUSTOM_ID_WAIFU_BIO = 'waifu.bio'
CUSTOM_ID_WAIFU_HAIR = 'waifu.hair'
CUSTOM_ID_WAIFU_NAME = 'waifu.name'

CUSTOM_ID_WAIFU_BIO_REGEX = re.compile('waifu\.(?:description|bio)')

class Waifu:
    __slots__ = ('age', 'bio', 'hair', 'name', 'user')
    
    def __init__(self, age, bio, hair, name, user):
        self.age = age
        self.bio = bio
        self.hair = hair
        self.name = name
        self.user = user
    
    @property
    def embed(self):
        return Embed(
            self.name,
            self.description,
        ).add_field(
            'age',
            self.age,
            inline = True,
        ).add_field(
            'hair',
            self.hair,
            inline = True,
        ).add_footer(
            f'Added by: {self.user:f}'
        )


# We will need these 3 in an example later

TEXT_INPUT_WAIFU_BIO = TextInput(
    'Bio',
    style = TextInputStyle.bio,
    min_length = 64,
    max_length = 1024,
    custom_id = CUSTOM_ID_WAIFU_BIO,
)

TEXT_INPUT_WAIFU_AGE = TextInput(
    'Age',
    min_length = 1,
    max_length = 1024,
    custom_id = CUSTOM_ID_WAIFU_AGE,
)

TEXT_INPUT_WAIFU_HAIR = TextInput(
    'hair',
    min_length = 1,
    max_length = 1024,
    custom_id = CUSTOM_ID_WAIFU_HAIR,
)

WAIFU_FORM = Form(
    'Describe your waifu',
    [
        TextInput(
            'Name',
            min_length = 2,
            max_length = 64,
            custom_id = CUSTOM_ID_WAIFU_NAME,
        ),
        TEXT_INPUT_WAIFU_BIO,
        TEXT_INPUT_WAIFU_AGE,
        TEXT_INPUT_WAIFU_HAIR,
    ],
    custom_id = CUSTOM_ID_WAIFU_FORM,
)
 
# Add command

@Nitori.interactions(guild=TEST_GUILD)
def add_waifu():
    """Add a new waifu to the database!"""
    return WAIFU_FORM


@Nitori.interactions(custom_id=CUSTOM_ID_WAIFU_FORM, target='form')
async def waifu_add_form_submit(
    event,
    *,
    age: CUSTOM_ID_WAIFU_AGE,
    bio: CUSTOM_ID_WAIFU_BIO_REGEX,
    hair: CUSTOM_ID_WAIFU_HAIR,
    name: CUSTOM_ID_WAIFU_NAME,
):
    key = name.casefold()
    if key in WAIFUS:
        abort('A waifu with the given name is already added.')
    
    WAIFUS[key] = waifu = Waifu(age, bio, hair, name, event.user)
    
    return waifu.embed

# Get command

@Nitori.interactions(guild=TEST_GUILD)
def get_waifu(
    name: ('str', 'Their name?')
):
    """Returns an added waifu."""
    try:
        waifu = WAIFUS[name.casefold()]
    except KeyError:
        abort(f'There is no waifu named like: {name}.')
    
    return waifu.embed


@get_waifu.autocomplete('name')
async def autocomplete_waifu_name(value):
    if (value is None):
        # Return the 20 oldest
        return [waifu.name for waifu, _ in zip(WAIFUS.values(), range(20))]
    
    value = value.casefold()
    return [waifu.name for key, waifu in WAIFUS.items() if value in key]
```

When using capturing groups or named capturing groups, you will get the captured values back as well. This can be
useful when dynamically generating form fields.

```py
CUSTOM_ID_WAIFU_EDIT_BASE = 'waifu.edit.'
CUSTOM_ID_WAIFU_EDIT_REGEX = 'waifu\.edit\.(.*)'
CUSTOM_ID_WAIFU_FIELD_ALL = 'waifu\.(?P<field>age|bio|hair)'

FIELD_TO_TEXT_INPUT = {
    'age': TEXT_INPUT_WAIFU_AGE,
    'bio': TEXT_INPUT_WAIFU_BIO,
    'hair': TEXT_INPUT_WAIFU_HAIR,
}

FIELD_TO_ATTRIBUTE = {
    'age': Waifu.age,
    'bio': Waifu.bio,
    'hair': Waifu.hair,
}

@Nitori.interactions(guild=TEST_GUILD)
async def edit_waifu(
    event,
    name: ('str', 'Their name?'),
    field : (['age', 'bio', 'hair'], 'Which field to edit?'),
):
    """Edits a waifu. | You must own her."""
    key = name.casefold()
    try:
        waifu = WAIFUS[key]
    except KeyError:
        abort(f'There is no waifu named like: {name}.')
    
    if waifu.user is not event.user:
        abort('You can only edit waifus added by yourself.')
    
    text_input = FIELD_TO_TEXT_INPUT[field]
    
    # We autofill the current value
    text_input = text_input.copy_with(value=FIELD_TO_ATTRIBUTE[field].__get__(waifu, Waifu))
    
    return Form(
        f'Editing {waifu.name}'
        [text_input],
        custom_id = f'{CUSTOM_ID_WAIFU_EDIT_BASE}{key}',
    )

@edit_waifu.autocomplete('name')
async def autocomplete_waifu_name(event, value):
    user = event.user
    
    if (value is None):
        # Return the 20 newest oldest
        return [waifu.name for waifu, _ in zip((waifu for waifu in WAIFUS.values() if waifu.user is user), range(20))]
    
    value = value.casefold()
    return [waifu.name for key, waifu in WAIFUS.items() if value in key and waifu.user is user]


@Nitori.interactions(custom_id=CUSTOM_ID_WAIFU_EDIT_REGEX, target='form')
async def waifu_edit_form_submit(
    key,
    *,
    edited_field: CUSTOM_ID_WAIFU_FIELD_ALL,
):
    # Both `group_dict` and `value` might be `None` at cases, so check them if you are not sure.
    group_dict, value = edited_field
    field = group_dict['field']
    
    waifu = WAIFUS[key]
    FIELD_TO_ATTRIBUTE[field].__set__(waifu, value)
    
    return waifu.embed
```

To capture multiple fields in one parameter you can use `*args`.

When using capturing groups in regex, each element will be a tuple, similar to the keyword parameters above.

```py
import re
from hata import Embed, BUILTIN_EMOJIS
from hata.ext.slash import Form, TextInput, TextInputStyle

EMOJI_CAKE = BUILTIN_EMOJIS['cake']

CUSTOM_ID_RATE_CAKE = 'rate_cake'
CUSTOM_ID_RATE_CAKE_FIELD = 'rate_cake.field'


CAKE_NAMES = ['butter', 'pound', 'sponge', 'genoise', 'biscuit', 'angel food', 'chiffon', 'baked flourless',
    'unbaked flourless', 'carrot', 'red velvet', ]

@Nitori.interactions(guild=TEST_GUILD)
async def rate_cakes(
    cake_1: ('str', 'Please rate this cake'),
    cake_2: ('str', 'Please rate this cake') = None,
    cake_3: ('str', 'Please rate this cake') = None,
    cake_4: ('str', 'Please rate this cake') = None,
    cake_5: ('str', 'Please rate this cake') = None,
):
    """Rate cakes."""
    # Filter 
    cakes = {cake for cake in (cake_1, cake_2, cake_3, cake_4, cake_5) if (cake is not None)}
    
    return Form(
        'Rate your cakes',
        [
            TextInput(
                f'Please rate {cake}',
                min_length = 2,
                max_length = 128,
                custom_id = f'{CUSTOM_ID_RATE_CAKE_FIELD}[{cake}]',
            ) for cake in cakes
        ],
        custom_id = CUSTOM_ID_RATE_CAKE,
    )

@cake_love.autocomplete('cake-1', 'cake-2', 'cake-3', 'cake-4', 'cake-5')
async def autocomplete_cake_type(value):
    if value is None:
        return CAKE_NAMES[:20]
    
    value = value.casefold()
    return [cake_name for cake_name in CAKE_NAMES if (value in cake_name)]


@Nitori.interactions(custom_id=CUSTOM_ID_RATE_CAKE, target='form')
async def rate_cake_form_submit(
    event,
    *cakes: re.compile(f'{CUSTOM_ID_RATE_CAKE_FIELD}\[(\w+)\]'),
):
    user = event.user
    embed = Embed(f'{user:f}\'s cake ratings').add_thumbnail(user.avatar_url)
    
    for (cake, ), rating in cakes:
        embed.add_field(cake, rating)
    
    return embed
```
