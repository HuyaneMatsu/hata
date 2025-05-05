import vampytest

from ...media_info import MediaInfo

from ..fields import put_media__attachment_only


def _iter_options():
    media = MediaInfo.precreate(
        height = 55,
        proxy_url = 'https://orindance.party/proxy',
        url = 'https://orindance.party',
        width = 56,
    )
    
    yield (
        media,
        False,
        False,
        {
            'file': media.to_data(defaults = False, include_internals = False),
        },
    )
    
    yield (
        media,
        True,
        False,
        {
            'file': media.to_data(defaults = True, include_internals = False),
        },
    )
    
    yield (
        media,
        False,
        True,
        {
            'file': media.to_data(defaults = False, include_internals = True),
        },
    )
    
    yield (
        media,
        True,
        True,
        {
            'file': media.to_data(defaults = True, include_internals = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_media__attachment_only(input_value, defaults, include_internals):
    """
    Tests whether ``put_media__attachment_only`` is working as intended.
    
    Parameters
    ----------
    input_value : ``MediaInfo``
        The value to serialize.
    
    defaults : `bool`
        Whether fields with as their default should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_media__attachment_only(input_value, {}, defaults, include_internals = include_internals)
