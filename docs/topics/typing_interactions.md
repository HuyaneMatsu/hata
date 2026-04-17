# Introduction

If you want to type your slash commands with the [pep 484](https://peps.python.org/pep-0484/) way,
there are two ways of doing it.

## configure_parameter

The `configure_parameter` decorator allows you to configure a *slash* command parameter. To do so, pass the respective
parameter name as the first parameter in `configure_parameter`. 

```py3
from hata import parse_emoji
from hata.ext.slash import abort, configure_parameter

@Nitori.interactions(guild = TEST_GUILD)
@configure_parameter('emoji_name', 'str', 'Yes?', 'emoji')
async def show_emoji(
    emoji_name: str
):
    """Shows the given custom emoji."""
    emoji = parse_emoji(emoji_name)
    if emoji is None:
        abort('Please give an emoji')
    
    if emoji.is_unicode_emoji():
        abort('Cannot link unicode emojis.')
    
    return f'**Name:** {emoji} **Link:** {emoji.url}'
```

![](assets/typing_interactions_0000.gif)

`configure_parameter` supports every parameter that `SlashParameter` (`P`) does.

```py3
from hata import ChannelType, Channel
from hata.ext.slash import P

@Nitori.interactions(guild = TEST_GUILD)
@configure_parameter('channel', 'channel', 'Select a text channel', channel_types = [ChannelType.guild_text])
async def text_channel_name_length(
    channel: Channel
):
    """Returns the selected text channel name length."""
    return len(channel.name)
```

![](assets/typing_interactions_0001.gif)

## Annotated

`Annotated` is a new typing feature introduced in python 3.9 by [pep 593](https://peps.python.org/pep-0593/).
It allows you to extend [pep 484](https://peps.python.org/pep-0484/) annotations with arbitrary metadata.

The interaction parameter parser only uses the added metadata, enabling you to use both systems with maximum
potential.

> Since hata does *"structure"* checking, you could port it to lower python versions as well if required.

```py3
from typing import Annotated

from hata import Embed
from hata.ext.slash import P


@Nitori.interactions(guild = TEST_GUILD)
async def grocery_bag(
    cucumber: Annotated[int, P('int', 'How much cucumbers to buy?', min_value = 0, max_value = 1000)] = 0,
    strawberry: Annotated[int, P('int', 'How much oranges to buy?', min_value = 0, max_value = 1000)] = 0,
    orange: Annotated[int, P('int', 'How much oranges to buy?', min_value = 0, max_value = 1000)] = 0,
    watermelon: Annotated[int, P('int', 'How much watermelons to buy?', min_value = 0, max_value = 1000)] = 0,
):
    in_bag = []
    
    for count, name in zip(
        (cucumber, strawberry, orange, watermelon),
        ('cucumber', 'strawberry', 'orange', 'watermelon'),
    ):
        if count:
            in_bag.append(f'{name}: {count}')
    
    if in_bag:
        description = '\n'.join(in_bag)
    else:
        description = '*nothing*'
    
    return Embed(
        'In bag',
        description,
    )
```

![](assets/typing_interactions_0002.gif)

You can also spread out annotation to multiple metadata fields.

```py3
from typing import Annotated

@Nitori.interactions(guild = TEST_GUILD)
async def set_difficulty(
    difficulty: Annotated[str, ['easy', 'lunatic'], 'difficulty'],
):
    if difficulty == 'easy':
        return 'Only kids play on easy mode.\nHow lame!'
    
    return 'Crazy moon rabbit mode activated!'
```

![](assets/typing_interactions_0003.gif)

----

<p align="left">
    <a href="./embedded_activity_launch.md">Previously: Launching embedded activities</a>
</p>
