import vampytest

from ..media_item import MediaItem


def test__MediaItem__repr():
    """
    Tests whether ``MediaItem.__repr__`` works as intended.
    """
    description = 'orin'
    spoiler = True
    url = 'https://orindance.party/'
    
    media_item = MediaItem(
        description = description,
        spoiler = spoiler,
        url = url,
    )
    vampytest.assert_instance(repr(media_item), str)


def test__MediaItem__hash():
    """
    Tests whether ``MediaItem.__hash__`` works as intended.
    """
    description = 'orin'
    spoiler = True
    url = 'https://orindance.party/'
    
    media_item = MediaItem(
        description = description,
        spoiler = spoiler,
        url = url,
    )
    vampytest.assert_instance(hash(media_item), int)


def _iter_options__eq__same_type():
    description = 'orin'
    spoiler = True
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'description': description,
        'spoiler': spoiler,
        'url': url,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'rin',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'spoiler': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'url': 'https://www.astil.dev/',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__MediaItem__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MediaItem.__eq__`` works as intended.
    
    Case: Same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    media_item_0 = MediaItem(**keyword_parameters_0)
    media_item_1 = MediaItem(**keyword_parameters_1)
    
    output = media_item_0 == media_item_1
    vampytest.assert_instance(output, bool)
    return output
