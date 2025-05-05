import vampytest

from ...media_info import MediaInfo

from ..fields import parse_media__attachment_only


def _iter_options():
    media = MediaInfo.precreate(
        height = 55,
        proxy_url = 'https://orindance.party/proxy',
        url = 'https://orindance.party',
        width = 56,
    )
    
    yield (
        {},
        MediaInfo._create_empty(),
    )
    
    yield (
        {
            'file': None,
        },
        MediaInfo._create_empty(),
    )
    
    yield (
        {
            'file': media.to_data(include_internals = True),
        },
        media,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_media__attachment_only(input_data):
    """
    Tests whether ``parse_media__attachment_only`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``MediaInfo``
    """
    output = parse_media__attachment_only(input_data)
    vampytest.assert_instance(output, MediaInfo)
    return output
