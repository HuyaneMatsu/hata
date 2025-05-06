import vampytest

from ...component import Component, ComponentType
from ...media_info import MediaInfo

from ..fields import parse_thumbnail


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
        {},
        None,
    )
    
    yield (
        {
            'accessory': None,
        },
        None,
    )
    
    yield (
        {
            'accessory': thumbnail.to_data(include_internals = True),
        },
        thumbnail,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_thumbnail(input_data):
    """
    tests whether ``parse_thumbnail`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | Component``
    """
    output = parse_thumbnail(input_data)
    vampytest.assert_instance(output, Component, nullable = True)
    return output
