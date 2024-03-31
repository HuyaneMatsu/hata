import vampytest

from ....emoji import Emoji

from ..fields import parse_emojis
from ..guild import Guild


def _iter_options():
    emoji_id = 202306090000
    emoji_name = 'Koishi'
    
    
    emoji = Emoji.precreate(
        emoji_id,
        name = emoji_name,
    )
    
    yield {}, {}
    yield {'emojis': []}, {}
    yield (
        {'emojis': [emoji.to_data(defaults = True, include_internals = True)]},
        {emoji_id: emoji},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_emojis(input_value):
    """
    Tests whether ``parse_emojis`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    
    Returns
    -------
    output : `dict<int, Emoji>`
    """
    guild_id = 202306090001
    guild = Guild.precreate(guild_id)
    
    return parse_emojis(input_value, guild.emojis, guild_id)
