import vampytest

from ...sticker import Sticker

from ..fields import parse_stickers


def _iter_options():
    sticker_0 = Sticker.precreate(202301050014, name = 'just')
    sticker_1 = Sticker.precreate(202301050015, name = 'flowering')
    
    yield (
        {},
        None,
    )
     
    yield (
        {'stickers': None},
        None,
    )
    
    yield (
        {'stickers': []},
        None,
    )
    
    yield (
        {'stickers': [sticker_0.to_data(include_internals = True), sticker_1.to_data(include_internals = True)]},
        frozenset((sticker_0, sticker_1)),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_stickers(input_data):
    """
    Tests whether ``parse_stickers`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    stickers : `None | frozenset<Sticker>`
    """
    output = parse_stickers(input_data)
    vampytest.assert_instance(output, frozenset, nullable = True)
    return output
