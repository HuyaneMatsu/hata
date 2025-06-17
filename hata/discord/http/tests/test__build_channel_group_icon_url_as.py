import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_channel_group_icon_url_as


def _iter_options():
    channel_id = 202405170140
    yield (
        channel_id,
        IconType.none,
        0,
        None,
        None,
        None,
    )
    
    channel_id = 202405170141
    yield (
        channel_id,
        IconType.static,
        2,
        None,
        1024,
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    channel_id = 202405170142
    yield (
        channel_id,
        IconType.animated,
        3,
        None,
        None,
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/a_00000000000000000000000000000003.gif',
    )
    
    channel_id = 202405170143
    yield (
        channel_id,
        IconType.animated,
        3,
        'png',
        None,
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_channel_group_icon_url_as(channel_id, icon_type, icon_hash, ext, size):
    """
    Tests whether ``build_channel_group_icon_url_as`` works as intended.
    
    Parameters
    ----------
    channel_id : `int`
        Channel identifier to test with.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    ext : `None | str`
        The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
    
    size : `None | int`
        The preferred minimal size of the image's url.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_channel_group_icon_url_as(channel_id, icon_type, icon_hash, ext, size)
    vampytest.assert_instance(output, str, nullable = True)
    return output
