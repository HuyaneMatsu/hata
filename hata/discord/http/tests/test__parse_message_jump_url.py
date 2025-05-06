import vampytest

from ..urls import DISCORD_ENDPOINT, parse_message_jump_url


def _iter_options():
    guild_id = 202504160010
    channel_id = 202504160011
    
    message_id = 202504160012
    yield (
        f'{DISCORD_ENDPOINT}/channels/{guild_id}/{channel_id}/{message_id}',
        (guild_id, channel_id, message_id),
    )
    
    message_id = 202504160013
    yield (
        f'{DISCORD_ENDPOINT}/channels/@me/{channel_id}/{message_id}',
        (0, channel_id, message_id),
    )
    
    message_id = 202504160014
    yield (
        f'{DISCORD_ENDPOINT}/chaaaaannels/@me/{channel_id}/{message_id}',
        (0, 0, 0),
    )
    
    message_id = 202504160014
    yield (
        f'',
        (0, 0, 0),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_message_jump_url(message_jump_url):
    """
    Tests whether ``parse_message_jump_url`` works as intended.
    
    Parameters
    ----------
    message_jump_url : `str`
        Message jump url to input.
    
    Returns
    -------
    output : `(int, int, int)`
    """
    output = parse_message_jump_url(message_jump_url)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 3)
    
    vampytest.assert_instance(output[0], int)
    vampytest.assert_instance(output[1], int)
    vampytest.assert_instance(output[2], int)
    
    return output
