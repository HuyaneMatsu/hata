import vampytest

from ...bases import Icon, IconType
from ...channel import Channel, ChannelType

from ..urls import CDN_ENDPOINT, channel_group_icon_url_as


def _iter_options():
    channel_id = 202405170140
    yield (
        channel_id,
        None,
        {},
        None,
    )
    
    channel_id = 202405170141
    yield (
        channel_id,
        Icon(IconType.static, 2),
        {'size': 1024},
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/00000000000000000000000000000002.png?size=1024',
    )
    
    channel_id = 202405170142
    yield (
        channel_id,
        Icon(IconType.animated, 3),
        {},
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/a_00000000000000000000000000000003.gif',
    )
    
    channel_id = 202405170143
    yield (
        channel_id,
        Icon(IconType.animated, 3),
        {'ext': 'png'},
        f'{CDN_ENDPOINT}/channel-icons/{channel_id}/a_00000000000000000000000000000003.png',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__channel_group_icon_url_as(channel_id, icon, keyword_parameters):
    """
    Tests whether ``channel_group_icon_url_as`` works as intended.
    
    Parameters
    ----------
    channel_id : `int`
        Channel identifier to create channel for.
    
    icon : `None | Icon`
        Icon to use as the channel's icon.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    output : `None | str`
    """
    channel = Channel.precreate(channel_id, channel_type = ChannelType.private_group, icon = icon)
    output = channel_group_icon_url_as(channel, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return output
