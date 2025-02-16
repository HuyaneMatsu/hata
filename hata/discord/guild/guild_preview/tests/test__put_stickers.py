import vampytest

from ....sticker import Sticker

from ..fields import put_stickers


def _iter_options():
    sticker = Sticker.precreate(202301080010, name = 'Koishi')
    
    yield {}, False, {'stickers': []}
    yield {}, True, {'stickers': []}
    
    yield {sticker.id: sticker}, False, {'stickers': [sticker.to_data(defaults = False, include_internals = True)]}
    yield {sticker.id: sticker}, True, {'stickers': [sticker.to_data(defaults = True, include_internals = True)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_stickers(input_value, defaults):
    """
    Tests whether ``put_stickers`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<int, Sticker>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_stickers(input_value, {}, defaults)
