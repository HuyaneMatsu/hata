import vampytest

from ...media_item import MediaItem

from ..fields import put_items


def _iter_items():
    item_0 = MediaItem('https://orindance.party/')
    item_1 = MediaItem('https://www.astil.dev/')

    yield (
        None,
        False,
        False,
        {
            'items': [],
        },
    )
    
    yield (
        None,
        True,
        False,
        {
            'items': [],
        },
    )
    
    yield (
        None,
        False,
        True,
        {
            'items': [],
        },
    )
    
    yield (
        None,
        True,
        True,
        {
            'items': [],
        },
    )
    
    yield (
        (item_0, item_1),
        False,
        False,
        {
            'items': [
                item_0.to_data(defaults = False, include_internals = False),
                item_1.to_data(defaults = False, include_internals = False),
            ],
        },
    )
    
    yield (
        (item_0, item_1),
        True,
        False,
        {
            'items': [
                item_0.to_data(defaults = True, include_internals = False),
                item_1.to_data(defaults = True, include_internals = False),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_items()).returning_last())
def test__put_items(input_value, defaults, include_internals):
    """
    Tests whether ``put_items`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<MediaItem>``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    include_internals : `bool`
        Whether internal fields should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_items(input_value, {}, defaults, include_internals = include_internals)
