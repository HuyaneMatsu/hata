import vampytest

from ...sticker import Sticker

from ..fields import put_stickers


def _iter_options():
    sticker_0 = Sticker.precreate(202301050016, name = 'just')
    sticker_1 = Sticker.precreate(202301050017, name = 'flowering')
    
    yield (
        None,
        False,
        {'stickers': []},
    )    
    yield (
        None,
        True,
        {'stickers': []},
    )
    
    yield (
        frozenset((sticker_0, sticker_1)),
        False,
        {'stickers': [sticker_0.to_data(include_internals = True), sticker_1.to_data(include_internals = True)]},
    )
    yield (
        frozenset((sticker_0, sticker_1)),
        True,
        {
            'stickers': [
                sticker_0.to_data(defaults = True, include_internals = True),
                sticker_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_stickers(input_value, defaults):
    """
    Tests whether ``put_stickers`` works as intended.
    
    Parameters
    ----------
    input_value : `None | frozenset<Sticker>`
        Input value to serialise.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_stickers(input_value, {}, defaults)
