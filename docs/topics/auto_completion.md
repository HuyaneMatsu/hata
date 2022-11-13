# Introduction

Auto-completion is a great tool to improve command usability as it provides dynamic options for the user to select
from.

Do you know how the 'choice' parameter only has up to 25 options? An auto completed parameter can only **display**
up to `25` options as well, however based on user input you can change those displayed options, theoretically
allowing you to have infinite amount of options.

> A parameter cannot have choices and be auto completed at the same time. 
> Both of these support same types, which are: string based, integers and floats

## Decorator

You can register auto-complete function with the `.autocomplete(...)` decorator after adding the command.

```py3
from hata import BUILTIN_EMOJIS


CAKE_NAMES = [
    'butter', 'pound', 'sponge', 'genoise', 'biscuit', 'angel food', 'chiffon', 'baked flourless', 'unbaked flourless',
    'carrot', 'red velvet'
]

EMOJI_CAKE = BUILTIN_EMOJIS['cake']


@Nitori.interactions(guild = TEST_GUILD)
async def cake_love(
    cake_name: ('str', 'Please pick a cake.')
):
    """Do I love the cake or nah?"""
    return f'Hmmm, yes, I love {cake_name} {EMOJI_CAKE} as well.'


@cake_love.autocomplete('cake_name') # Define which parameter we want to auto-complete.
async def autocomplete_cake_name(value):
    if value is None:
        return CAKE_NAMES[:25]
    
    value = value.casefold()
    return [cake_name for cake_name in CAKE_NAMES if (value in cake_name)]
```

![](assets/auto_completion_0000.gif)

Autocomplete functions support **1 additional parameter** outside the client and event, which is the value the user
already typed. This value defaults to `None` if the user didn't type anything yet.

### Dependent auto completion

Sometimes you'll want your auto-complete parameters to directly depend on each other.
For example (as in below code) if you have food product (categories), and you want only types for **that** food category.

The main disadvantage of implementing such a system is that the user might break up parameter order or just give bad
parameters. For example, in the discord client, the user can select type before he selects category of food.
You have to handle these cases yourself (in below code example these are appropriately handled).

In the below example we use the `event.interaction.get_value_of(*option_names)` method which returns the parameter
values for the given **option stack**. This means that if you're dealing with sub-commands you will need to mention
the sub-command name before the parameter.

```py3
from hata.ext.slash import abort

PRODUCT_TYPES = {
    'pudding': ['choco', 'dark choco', 'strawberry', 'vanilla'],
    'croissant': ['choco', 'cherry', 'hazelnut', 'strawberry', 'vanilla'],
}


def get_option_like(options, name):
    name = name.casefold()
    
    for option in options:
        if name in option:
            return option


def get_options_like(options, name):
    name = name.casefold()
    
    return [option for option in options if name in option]


@Nitori.interactions(guild = TEST_GUILD)
async def shop(
    product: ([*PRODUCT_TYPES], 'Select a product to buy.'),
    type_: ('str', 'Select a type'),
):
    """Buy some sweets."""
    type_ = get_option_like(PRODUCT_TYPES[product], type_)
    if type_ is None:
        abort('Invalid product type.')
    
    return f'You just bought a {type_} {product}'


@shop.autocomplete('type_')
async def autocomplete_product_type(event, value):
    product = event.interaction.get_value_of('product')
    if product is None:
        return
    
    options = PRODUCT_TYPES[product]
    
    if value is None:
        return options[:25]
    
    return get_options_like(options, value)
```

![](assets/auto_completion_0001.gif)

### Dependent exclusive auto completion

Sometimes your auto-completed parameters might rely on each other in a way that you want to exclude some of them from
showing in auto-completion if they were previously selected.
A common case is when you have multiple similar parameters.

> If doing multiple filterings then having a `get_one_like` and `get_multiple_like` functions might be handy.

In the below example we use the `event.interaction.get_non_focused_values()` method which returns a dictionary of
`parameter-name` - `value` pairs. Using it can be great help when you want to get **all** the parameters which the user
already filled out (so you can do something with them, in this case exclude them).
This also includes parameters filled out with *null* value (so values can be `None`).

```py3
from random import choice

from hata.ext.slash import abort


CAKE_NAMES = [
    'butter', 'pound', 'sponge', 'genoise', 'biscuit', 'angel food', 'chiffon', 'baked flourless', 'unbaked flourless',
    'carrot', 'red velvet'
]

def get_cake_name_like(name):
    name = name.casefold()
    
    for cake_name in CAKE_NAMES:
        if name in cake_name:
            return cake_name


def get_cake_names_like(name):
    name = name.casefold()
    
    return [cake_name for cake_name in CAKE_NAMES if (name in cake_name)]


@Nitori.interactions(guild = TEST_GUILD)
async def pick_cake(
    cake_name_1: ('str', 'Select a cake!'),
    cake_name_2: ('str', 'Another one.'),
    cake_name_3: ('str', 'Another one.') = None,
    cake_name_4: ('str', 'Another one.') = None,
    cake_name_5: ('str', 'Another one.') = None,
):
    """Picks a cake."""
    cakes = []
    
    for cake_name in (cake_name_1, cake_name_2, cake_name_3, cake_name_4, cake_name_5):
        if cake_name is not None:
            cake_name = get_cake_name_like(cake_name)
            if cake_name is not None:
                cakes.append(cake_name)
    
    if not cakes:
        abort('No valid choices provided.')
    
    return f'I choose: {choice(cakes)}'


@pick_cake.autocomplete('cake_name_1', 'cake_name_2', 'cake_name_3', 'cake_name_4', 'cake_name_5')
async def exclusive_autocomplete_cake_name(event, actual_cake_name):
    excluded_cake_names = set()
    
    for cake_name in event.interaction.get_non_focused_values().values():
        if cake_name is not None:
            cake_name = get_cake_name_like(cake_name)
            if cake_name is not None:
                excluded_cake_names.add(cake_name)
    
    
    if actual_cake_name is None:
        if excluded_cake_names:
            return [cake_name for cake_name in CAKE_NAMES if cake_name not in excluded_cake_names]
        
        else:
            return CAKE_NAMES[:25]
    
    else:
        cake_names = get_cake_names_like(actual_cake_name)
        if excluded_cake_names:
            return [cake_name for cake_name in cake_names if cake_name not in excluded_cake_names]
        
        else:
            return cake_names
```

![](assets/auto_completion_0002.gif)

## Sharing auto-completer

You may add the same auto-completer to multiple commands, with using multiple decorators.

```py3
from hata.ext.slash import abort


SPELLS = [
    'ankle snare', 'blade of wind', 'blast', 'blessing', 'bottomless swamp', 'break spell', 'burning flash',
    'control of weather', 'create earth', 'create earth golem', 'create water', 'crystal prison', 'cursed lighting',
    'detonation', 'earthshaker', 'energy ignition', 'exorcism', 'explosion', 'fireball', 'flash', 'force fire',
    'freeze', 'freeze bind', 'freeze gust', 'heal', 'inferno', 'light of reflection', 'light of saber', 'lighting',
    'lightning strike', 'lock', 'magic canceller', 'paralyze', 'powered', 'puppet', 'purification', 'reflect',
    'resurrection', 'sacred shell', 'silent', 'sleep', 'teleport', 'tinder', 'tornado', 'turn undead', 'unlock',
    'versatile actor', 'wind breath', 'wind curtain'
]


def get_spell_or_abort(name):
    name = name.casefold()
    
    for spell in SPELLS:
        if name in spell:
            break
    
    else:
        abort('Unknown spell.')
    
    return name


def get_spells_like(name):
    name = name.casefold()
    
    return [spell for spell in SPELLS if name in spell]



SPELL_COMMANDS = Nitori.interactions(
    None,
    name = 'spell',
    description = 'Magic!',
    guild = TEST_GUILD,
)


@SPELL_COMMANDS.interactions
async def cast(
    event,
    spell: ('str', 'select a spell'),
):
    """Uses the selected spell"""
    spell = get_spell_or_abort(spell)
    
    return f'{event.user:f} just used {spell}; It is super effective!'


@SPELL_COMMANDS.interactions
async def upgrade(
    event,
    spell: ('str', 'select a spell'),
):
    """Uses the selected spell"""
    spell = get_spell_or_abort(spell)
    
    return f'{event.user:f} just upgraded their {spell}; It was a *next* level move!'


@cast.autocomplete('spell')
@upgrade.autocomplete('spell')
async def auto_complete_spell_name(value):
    if value is None:
        return SPELLS[:25]
    
    return get_spells_like(value)
```

![](assets/auto_completion_0003.gif)

### Sharing within command root

```py3
@SPELL_COMMANDS.autocomplete('spell')
async def auto_complete_spell_name(value):
    ...
```
In this case it would be applied to **every** sub-command parameter, which has the given parameter name.

### Sharing globally

You may also register an auto-completer directly to the interaction handler:

```py3
@Nitori.slasher.autocomplete(...):
async def ...
```

This might be dangerous and could cause happy accidents (accidentally overwriting handler,
setting handler and forgetting about it then wondering from where your commands pull their arguments etc.)


## Keyword parameter

When defining a bigger command you might consider splitting the code into multiple files.

When the auto-completer is split, you might want to consider adding it inside the parameter definition and not
within a decorator.
This is completely optional, and you can choose either decorator or keyword parameter depending on your preference.

```py3
from hata.ext.slash import P, abort


async def autocomplete_sticker_name(event, value):
    guild = event.guild
    if guild is None:
        return None
    
    
    if value is None:
        return sorted(sticker.name for sticker in guild.stickers.values())
    
    return sorted(sticker.name for sticker in guild.get_stickers_like(value))


@Nitori.interactions(guild = TEST_GUILD)
async def get_sticker_id(
    event,
    sticker: P('str', 'Sticker\'s name', autocomplete=autocomplete_sticker_name),
):
    guild = event.guild
    if guild is None:
        abort('Please use the command inside of a guild')
    
    sticker = guild.get_sticker_like(sticker)
    if sticker is None:
        abort('Unknown sticker')
    
    return f'{sticker.name}\'s id: `{sticker.id}`'
```

![](assets/auto_completion_0004.gif)

----

<p align="left">
    <a href="./slash.md">Previously: Slash & Context commands</a>
</p>

<p align="right">
    <a href="./components.md">Next up: Components</a>
</p>
