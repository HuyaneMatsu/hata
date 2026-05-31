import vampytest

from ....channel import ChannelType

from ..fields import put_channel_type


def _iter_options():
    yield (
        ChannelType.unknown,
        False,
        {},
    )
    
    yield (
        ChannelType.unknown,
        True,
        {
            'channel_type': ChannelType.unknown.value,
        },
    )
    
    yield (
        ChannelType.guild_text,
        False,
        {
            'channel_type': ChannelType.guild_text.value,
        },
    )
    
    yield (
        ChannelType.guild_text,
        True,
        {
            'channel_type': ChannelType.guild_text.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_channel_type(input_value, defaults):
    """
    Tests whether ``put_channel_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ChannelType``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_channel_type(input_value, {}, defaults)
