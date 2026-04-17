import vampytest

from ....sticker import Sticker

from ..guild import Guild

from ..fields import parse_stickers


def _iter_options():
    sticker_0 = Sticker.precreate(202306140002, name = 'Koishi')
    sticker_1 = Sticker.precreate(202409200000, name = 'Satori')
    
    yield {}, {}
    yield {'stickers': []}, {}
    yield (
        {
            'stickers': [
                sticker_0.to_data(defaults = True, include_internals = True),
                sticker_1.to_data(defaults = True, include_internals = True),
            ],
        },
        {
            sticker_0.id: sticker_0,
            sticker_1.id: sticker_1,
        },
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
