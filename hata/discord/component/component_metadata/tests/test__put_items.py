import vampytest

from ...media_item import MediaItem

from ..fields import put_items


def _iter_items():
    item_0 = MediaItem('https://orindance.party/')
    item_1 = MediaItem('https://www.astil.dev/')

    yield (None, False, {'items': []})
    yield (None, True, {'items': []})
    yield (
        (item_0, item_1),
        False,
        {'items': [item_0.to_data(), item_1.to_data()]},
    )
    yield (
        (item_0, item_1),
        True,
        {'items': [item_0.to_data(defaults = True), item_1.to_data(defaults = True)]},
    )


@vampytest._(vampytest.call_from(_iter_items()).returning_last())
def test__put_items(input_value, defaults):
    """
    Tests whether ``put_items`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<MediaItem>`
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_items(input_value, {}, defaults)
