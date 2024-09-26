import vampytest

from ....sticker import Sticker

from ..fields import parse_stickers


def _iter_options():
    sticker_0 = Sticker.precreate(202301080008, name = 'rose')
    sticker_1 = Sticker.precreate(202301080009, name = 'slayer')
    
    yield (
        {},
        {},
        {},
    )
    yield (
        {'stickers': None},
        {},
        {},
    )
    yield (
        {'stickers': []},
        {},
        {},
    )
    yield (
        {'stickers': [sticker_0.to_data(defaults = True, include_internals = True)]},
        {},
        {sticker_0.id: sticker_0},
    )
    yield (
        {'stickers': [sticker_1.to_data(defaults = True, include_internals = True)]},
        {sticker_0.id: sticker_0},
        {sticker_1.id: sticker_1},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_stickers(input_data, input_entities):
    """
    Tests whether ``parse_stickers`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    input_entities : `dict<int, Sticker>`
        Old entities.
    
    Returns
    -------
    output : `dict<int, Sticker>`
    """
    return parse_stickers(input_data, input_entities)
