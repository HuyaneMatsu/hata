import vampytest

from ...media_item import MediaItem

from ..fields import parse_items


def _iter_items():
    item_0 = MediaItem('https://orindance.party/')
    item_1 = MediaItem('https://www.astil.dev/')
    
    yield ({}, None)
    yield ({'items': None}, None)
    yield ({'items': []}, None)
    yield ({'items': [item_0.to_data()]}, (item_0, ))
    yield ({'items': [item_0.to_data(), item_1.to_data()]}, (item_0, item_1))


@vampytest._(vampytest.call_from(_iter_items()).returning_last())
def test__parse_items(input_data):
    """
    Tests whether ``parse_items`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<MediaItem>`
    """
    return parse_items(input_data)
