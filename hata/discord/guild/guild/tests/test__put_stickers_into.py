import vampytest

from ....sticker import Sticker

from ..fields import put_stickers_into


def _iter_options():
    sticker_id = 202306140001
    sticker_name = 'Koishi'
    
    sticker = Sticker.precreate(
        sticker_id,
        name = sticker_name,
    )
    
    yield {}, True, {'stickers': []}
    yield {sticker_id: sticker}, True, {'stickers': [sticker.to_data(defaults = True, include_internals = True)]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_stickers_into(input_value, defaults):
    """
    Tests whether ``put_stickers_into`` works as intended.
    
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
    return put_stickers_into(input_value, {}, defaults)
