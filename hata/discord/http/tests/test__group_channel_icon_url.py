import vampytest

from ...bases import Icon, IconType
from ...channel import Channel, ChannelType

from ..urls import CDN_ENDPOINT, channel_group_icon_url


def _iter_options():
    channel_id = 202504160130
    yield (
        channel_id,
        None,
        None,
    )
    
    channel_id = 202504160131
    yield (
        channel_id,
        Icon(IconType.static, 2),
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/00000000000000000000000000000002.png',
    )
    
    channel_id = 202504160132
    yield (
        channel_id,
        Icon(IconType.animated, 3),
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/a_00000000000000000000000000000003.gif',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__channel_group_icon_url(channel_id, icon):
    """
    Tests whether ``channel_group_icon_url`` works as intended.
    
    Parameters
    ----------
    channel_id : `int`
        Channel identifier to create channel for.
    
    icon : `None | Icon`
        Icon to use as the channel's icon.
    
    Returns
    -------
    output : `None | str`
    """
    channel = Channel.precreate(channel_id, channel_type = ChannelType.private_group, icon = icon)
    output = channel_group_icon_url(channel)
    vampytest.assert_instance(output, str, nullable = True)
    return output
