import vampytest

from ....channel import ChannelType

from ..fields import parse_channel_type


def _iter_options():
    yield (
        {},
        ChannelType.unknown,
    )
    
    yield (
        {
            'channel_type': None,
        },
        ChannelType.guild_text,
    )
    
    yield (
        {
            'channel_type': ChannelType.guild_text.value,
        },
        ChannelType.guild_text,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_channel_type(input_data):
    """
    Tests whether ``parse_channel_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ChannelType``
    """
    output = parse_channel_type(input_data)
    vampytest.assert_instance(output, ChannelType)
    return output
