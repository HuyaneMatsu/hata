# Forms \[Work in progress\]

> Forms are implemented on wrapper side, but waiting for Discord release

### Introduction

When it comes to interactions, slash commands and components are a great first step, but for longer inputs they are
not intuitive enough. This is when multi-field forms / model interactions come into the picture.

## Building Forms

Forms are standalone components, with sub-components as fields.

For now, forms are limited to 5 sub-components. And the only accepted sub-component are `TextInput`-s. (Basically rows
of text inputs, but rows are inserted automatically if not defined.)

## Limitations

- Up to `5` rows in each form.

###### Text input limitations

- Up to `1` text input can be in a row.

## Form commands

To send a form response to the user, just return the form from a slash or a component command, or use the
`Client.interaction_form_send` method.

```py
from hata.ext.slash import Form, TextInput, TextInputStyle

INRTODUCTION_FORM = Form(
    'Introduce yourself'
    [
        TextInput(
            'What is your name?',
            custom_id = 'name',
        ),
        TextInput(
            'Something about you?'
            style = TextInputStyle.paragraph,
            min_length = 64,
            max_length = 1024,
            custom_id = 'bio',
        ),
    ],
    custom_id = 'introduction',
)
 
@Nitori.interactions(guild=TEST_GUILD):
def introduce_myself():
    return INRTODUCTION_FORM
```

Defining `custom_id` to each component is not required, but highly recommended, since each received field is matched by
it's `custom_id`.

You may add form commands to slasher by specifying what forms they should capture based on their `custom_id`. Also
specify that you want to match forms submit interaction and not component interactions by passing `target=` either as
`'form'` or `'form_submit'`.


```py
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

### Parameters

Positional parameters of form submit commands work on the same way as component commands'. This means regex
`custom_id`-s, as multiple `custom_id`-s are both supported.

Additionally form submit commands support keyword parameters as well. These are matched from the fields of the
submitted form.

```py
import re

from hata import DiscordException, ERROR_CODES, Embed
from hata.ext.slash import abort

ADD_ROLE_FORM = Form(
    'Add role', # Any dummie title does it
    [
        TextInput(
            'Additional message to send?'
            style = TextInputStyle.paragraph,
            max_length = 512,
            custom_id = 'message',
        ),
    ],
)


@Nitori.interactions(guild=TEST_GUILD):
def add_role(
    user: ('user', 'User to add role to'),
    role :('role', 'The role to give'),
):
    # Check for permissions
    if not event.user_permissions.can_manage_roles:
        abort('You need `manage roles` permission to invoke this command.')
    
    if not event.guild.cached_permissions_for(client).can_manage_roles:
        abort('I need `manage roles` permission to execute this command.')
    
    if not event.user.has_higher_role_than(role):
        abort('You must have higher role than the role to be given.')
    
    if not client.has_higher_role_than(role):
        abort('I must have higher role than the role to be given.')
    
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
    channel = await.channel_private_create(user_id)
    
    guild = event.guild
    role = guild.roles[role_id]
    
    try:
        await client.message_create(
            channel,
            embed = Embed(
                description = 'You have received role {role.name} in {guild.name}.'
            ).add_field(
                'Message',
                message,
            )
        )
    except DiscordException as err:
        # Ignore the exception if the user has dm-s disabled.
        if err.code != ERROR_CODES.cannot_message_user: # user has dm-s disallowed
            raise
    
    # Note: The user might not be cached at this point. Request it. If you have user caching enabled + intent, it will
    do nothing.
    user = await client.user_get(user_id)
    
    yield Embed(
        description = 'You gave {role.name} to {user.full_name}',
    ).add_field(
        'Message',
        message,
    )
```

By annotating keyword parameters with string or with regex, you can customize what `custom_id`-s they are matching.
If the annotation is neither string nor regex pattern, it is ignored.

> Annotating a parameter with "regular" regex is pretty pointless. Could be good when updating old code,
> and you want to support multiple `custom_id`-s.

```py
import re
from hata import Embed
from hata.ext.slash import Form, TextInput, TextInputStyle, abort

# Define constants

WAIFUS = {}

CUSTOM_ID_WAIFU_FORM = 'waifu.form'
CUSTOM_ID_WAIFU_NAME = 'waifu.name'
CUSTOM_ID_WAIFU_DESCRIPTION = 'waifu.description'

CUSTOM_ID_WAIFU_DESCRIPTION_REGEX = re.compile('waifu\.description(?:\.long)')

WAIFU_FORM = Form(
    'Describe your waifu'
    [
        TextInput(
            'What is their name?',
            min_length = 2,
            max_length = 128,
            custom_id = CUSTOM_ID_WAIFU_NAME,
        ),
        TextInput(
            'Describe them!'
            style = TextInputStyle.paragraph,
            min_length = 64,
            max_length = 1024,
            custom_id = CUSTOM_ID_DESCRIPTION,
        ),
    ],
    custom_id = CUSTOM_ID_WAIFU_FORM,
)
 
# Add command

@Nitori.interactions(guild=TEST_GUILD):
def add_waifu():
    return WAIFU_FORM

@Nitori.interactions(custom_id=CUSTOM_ID_WAIFU_FORM, target='form')
async def waifu_add_form_submit(
    event,
    *,
    name : CUSTOM_ID_WAIFU_NAME,
    desciption : CUSTOM_ID_WAIFU_DESCRIPTION_REGEX,
):
    key = name.casefold()
    if key in WAIFUS:
        abort(
            Embed(
               description = (
                    'There is already a waifu named: {name!r}.\n'
                    'Try again with a difefernt name.'
                ),
            ).add_field(
                'Description given',
                description,
            )
        )
    
    WAIFUS[key] = (name, desciption, event.user)
    
    return Embed(name, description).add_footer('Great success !!!')

# Get command

@Nitori.interactions(guild=TEST_GUILD):
def get_waifu(
    name: ('str', 'Their name?')
):
    try:
        name, description, adder = WAIFUS[name.casefold()]
    except KeyError:
        abort('There is no waifu named like: {name}.')
    
    return Embed(name, description).add_footer(f'Added by: {user:f}')


@get_waifu.autocomplete('name')
async def autocomplete_waifu_name(value):
    if (value is None):
        # Return the 20 newest waifu
        return [waifu[0] for waifu, _ in zip(WAIFUS.values(), range(20))]
    
    value = value.casefold()
    return [waifu[0] for key, waifu in WAIFUS.items() if value in key]
```

# TODO
