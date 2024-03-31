import vampytest

from ....sticker import Sticker

from ..guild import Guild

from ..fields import parse_stickers


def _iter_options():
    sticker_id = 202306140002
    sticker_name = 'Koishi'
    
    
    sticker = Sticker.precreate(
        sticker_id,
        name = sticker_name,
    )
    
    yield {}, {}
    yield {'stickers': []}, {}
    yield (
        {'stickers': [sticker.to_data(defaults = True, include_internals = True)]},
        {sticker_id: sticker},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_stickers(input_value):
    """
    Tests whether ``parse_stickers`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to pass.
    
    Returns
    -------
    output : `dict<int, Sticker>`
    """
    guild_id = 202306140003
    guild = Guild.precreate(guild_id)
    
    return parse_stickers(input_value, guild.stickers)
