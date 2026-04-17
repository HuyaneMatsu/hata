import vampytest

from ...component import Component, ComponentType
from ...media_info import MediaInfo

from ..fields import put_thumbnail


def _iter_options():
    thumbnail = Component(
        ComponentType.thumbnail_media,
        media = MediaInfo.precreate(
            height = 55,
            proxy_url = 'https://orindance.party/proxy',
            url = 'https://orindance.party',
            width = 56,
        ),
    )
    
    yield (
        None,
        False,
        False,
        {},
    )
    
    yield (
        None,
        True,
        False,
        {
            'accessory': None,
        },
    )
    
    yield (
        thumbnail,
        False,
        False,
        {
            'accessory': thumbnail.to_data(defaults = False, include_internals = False),
        },
    )
    
    yield (
        thumbnail,
        True,
        False,
        {
            'accessory': thumbnail.to_data(defaults = True, include_internals = False),
        },
    )
    
    yield (
        thumbnail,
        False,
        True,
        {
            'accessory': thumbnail.to_data(defaults = False, include_internals = True),
        },
    )
    
    yield (
        thumbnail,
        True,
        True,
        {
            'accessory': thumbnail.to_data(defaults = True, include_internals = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_thumbnail(input_value, defaults, include_internals):
    """
    tests whether ``put_thumbnail`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | Component``
        value to serialize.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    include_internals : `bool`
        Whether internal fields should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_thumbnail(input_value, {}, defaults, include_internals = include_internals)
