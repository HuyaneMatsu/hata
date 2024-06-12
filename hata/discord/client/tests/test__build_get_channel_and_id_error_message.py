import vampytest

from ...channel import Channel, ChannelType

from ..request_helpers import build_get_channel_and_id_error_message


def _iter_options():
    yield (
        None,
        None, 
        f'`channel` can be `{Channel.__name__}`, `int`, got NoneType; None.',
    )
    
    channel = Channel.precreate(202406020000, channel_type = ChannelType.guild_text, name = 'pudding')
    
    yield (
        channel,
        Channel.is_guild_category,
        (
            f'`channel` can be `{Channel.__name__}`, `int`, '
            f'passing the `{Channel.is_guild_category.__name__}` check, '
            f'got {Channel.__name__}; {channel!r}.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_get_channel_and_id_error_message(channel, type_checker):
    """
    Tests whether ``build_get_channel_and_id_error_message`` works as intended.
    
    Parameters
    ----------
    channel : `object`
        The object that was passed as `channel`.
    type_checker : `None | FunctionType`
        Type checker for `channel`.
    
    Returns
    -------
    output : `str`
    """
    output = build_get_channel_and_id_error_message(channel, type_checker)
    vampytest.assert_instance(output, str)
    return output
