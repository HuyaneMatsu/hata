import vampytest

from ....channel import Channel, ChannelType

from ..fields import put_channel


def _iter_options():
    yield None, {
        'channel': None,
        'channel_id': None,
    }
    
    channel_id = 202307290003
    guild_id = 202307290004
    name = 'Remilia'
    channel_type = ChannelType.guild_text
    
    channel = Channel.precreate(
        channel_id,
        guild_id = guild_id,
        name = name,
        channel_type = channel_type,
    )
    
    expected_output = {
        'channel': {
            'id': str(channel_id),
            'guild_id': str(guild_id),
            'name': name,
            'type': channel_type.value,
        },
        'channel_id': str(channel_id),
    }

    yield channel, expected_output


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channel(channel):
    """
    Tests whether ``put_channel`` works as intended.
    
    Parameters
    ----------
    channel : ``None | Channel``
        The channel to serialise.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_channel(channel, {}, True)
