import vampytest

from ...bases import IconType

from ..urls import CDN_ENDPOINT, build_channel_group_icon_url


def _iter_options():
    channel_id = 202504160130
    yield (
        channel_id,
        IconType.none,
        0,
        None,
    )
    
    channel_id = 202504160131
    yield (
        channel_id,
        IconType.static,
        2,
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/00000000000000000000000000000002.png',
    )
    
    channel_id = 202504160132
    yield (
        channel_id,
        IconType.animated,
        3,
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_channel_group_icon_url(channel_id, icon_type, icon_hash):
    """
    Tests whether ``build_channel_group_icon_url`` works as intended.
    
    Parameters
    ----------
    channel_id : `int`
        Channel identifier to test with.
    
    icon_type : ``IconType``
        The icon's type.
    
    icon_hash : `int`
        The icon's hash (uint128).
    
    Returns
    -------
    output : `None | str`
    """
    output = build_channel_group_icon_url(channel_id, icon_type, icon_hash)
    vampytest.assert_instance(output, str, nullable = True)
    return output
