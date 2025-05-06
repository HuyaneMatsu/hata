import vampytest

from ...media_item import MediaItem

from ..fields import validate_items


def _iter_items__passing():
    item_0 = MediaItem('https://orindance.party/')
    item_1 = MediaItem('https://www.astil.dev/')
    
    yield None, None
    yield [], None
    yield [item_0], (item_0,)
    yield [item_0, item_1], (item_0, item_1,)
    yield [item_0.url], (item_0,)


def _iter_items__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_items__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_items__type_error()).raising(TypeError))
def test__validate_items(input_value):
    """
    Tests whether ``validate_items`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | tuple<MediaItem>``
    
    Raises
    ------
    TypeError
    """
    return validate_items(input_value)
