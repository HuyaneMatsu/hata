# Introduction

Auto completion is a great tool to improve command usability as it provides dynamic options for the user to select
from.

Do you know how the choice parameter only has up to 25 options? An auto completed parameter can only **display**
up to `25` options as well, however based on user input you can change the displayed options, theoretically
allowing you to have infinite amount of options.

> A parameter cannot have choices and be auto completed at the same time. The same types of parameters can have
> choices & auto completion, so string based, number and float ones.

#### Decorator

You may register auto completion function with the `.autocomplete(...)` decorator after adding the command.

```py3
from hata import BUILTIN_EMOJIS

EMOJI_CAKE = BUILTIN_EMOJIS['cake']

CAKE_NAMES = [
    'butter', 'pound', 'sponge', 'genoise', 'biscuit', 'angel food', 'chiffon', 'baked flourless', 'unbaked flourless',
    'carrot', 'red velvet'
]


@Nitori.interactions(guild=TEST_GUILD)
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

Autocomplete functions support **1 additional parameter** outside of client and event, which is the value what the user
already typed. This value defaults to `None` if the user didn't yet type anything.

#### Exclusive auto completion

Sometimes your auto completed parameters might rely on each other. A common case is when you have multiple of the same
parameter.

> When doing multiple filtering having a `get_one_like` and a `get_multiple_like` function might be handy.

This example showcases the `event.interaction.get_non_focused_values()` method, which returns a dictionary of
`parameter-name` - `value` pairs. Using it can be great help when you want to get **all** the parameter which the user
already filled out. This also includes the parameters filled out with *null* value (so values can be `None`).

```py3
from random import choice

from hata.ext.slash import abort


CAKE_NAMES = [
    'butter', 'pound', 'sponge', 'genoise', 'biscuit', 'angel food', 'chiffon', 'baked flourless', 'unbaked flourless',
    'carrot', 'red velvet'
]

# Define `get_one_like˙ function
def get_cake_name_like(name):
    name = name.casefold()
    
    for cake_name in CAKE_NAMES:
        if name in cake_name:
            return cake_name


# Define `get_multiple_like` function
def get_cake_names_like(name):
    name = name.casefold()
    
    return [cake_name for cake_name in CAKE_NAMES if (name in cake_name)]


@Nitori.interactions(guild=TEST_GUILD)
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

#### Dependent auto completion

At cases you might want to have an auto completion, where parameters depend on each other. The main disadvantage of
implementing such a system, that the use might break up parameter order, or just give bad parameters ruining the whole
idea.

This example showcases the usage of `event.interaction.get_value_of(*option_names)` which returns the parameter's
value for the given **option stack**. This means when dealing with sub-commands, you will need to mention their name
before the parameter's.

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


@Nitori.interactions(guild=TEST_GUILD)
async def shop(
    product: ([*PRODUCT_TYPES], 'Select a product to buy.'),
    type_: ('str', 'Select a type'),
):
    """Buy some sweets."""
    type_ = get_option_like(PRODUCT_TYPES[product], type_),
    if type_ is None:
        abort('Invalid product type.')
    
    return f'You just bought a {type_} {product}'


@shop.autocomplete('type_')
async def autocomplete_product_type(event, value):
    product = event.intearction.get_value_of('product')
    if product is None:
        return
    
    options = PRODUCT_TYPES[product]
    
    if value is None:
        return options[:25]
    
    return get_options_like(options, value)
```

#### Sharing auto completers

You may add the same auto completer to multiple commands, with using multiple decorators.

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

##### Sharing within command root

```py3
@SPELL_COMMANDS.autocomple('spell')
async def auto_complete_spell_name(value):
    ...
```
At this case it would be applied to **every** sub-command's parameter, which has the given name.

##### Sharing globally

You may also register an auto completer directly to the interaction handler:

```py3
@Nitori.slasher.autocomplete(...):
async def ...
```

This might be dangerous and could cause happy accidents.


#### Autocompleted parameter definition

When defining a bigger command you might consider splitting the code into multiple files.

When the auto completer is split down, you might want to consider adding it inside of the parameter definition and not
wth a decorator.

```py3
from hata.ext.slash import P, abort


async def autocomplete_sticker_name(event, value):
    guild = event.guild
    if guild is None:
        return None
    
    
    if value is None:
        return sorted(sticker.name for sticker in guild.stickers.values())
    
    return sorted(sticker.name for sticker in guild.get_stickers_like(value))


@Nitori.interactions(guild=TEST_GUILD)
async def get_sticker_id(
    event,
    sticker: P('str', 'Sticker\'s name', autocomplete=autocomplete_sticker_name),
):
    guild = event.guild
    if guild is None:
        abort('Please use the command inside of a guild')
    
    sticker = guild.get_sticker_like(sticker)
    if sticker:
        abort('Unknown sticker')
    
    return f'{sticker.name}\'s id: `{sticker.id}`'
```

----

<p align="right">
    <a href="./components.md">Next up: Components</a>
</p>
