import vampytest

from ..urls import parse_message_jump_url


@vampytest.call_with(
    'https://discord.com/channels/@me/931534110002481173/1109217121273567569',
    0,
    931534110002481173,
    1109217121273567569,
)
@vampytest.call_with(
    'https://discord.com/channels/388267636661611178/931534110002481173/1109217121273567569',
    388267636661611178,
    931534110002481173,
    1109217121273567569,
)

@vampytest.call_with(
    'https://discord.com/chaaannels/388267636661611178/931534110002481173/1109217121273567569',
    0,
    0,
    0,
)
@vampytest.call_with(
    '',
    0,
    0,
    0,
)
def test__parse_message_jump_url(message_jump_url, expected_guild_id, expected_channel_id, expected_message_id):
    """
    Tests whether ``parse_message_jump_url`` works as intended.
    
    Parameters
    ----------
    message_jump_url : `str`
        Message jump url to input.
    expected_guild_id : `int`
        The expected guild identifier as output.
    expected_channel_id : `int`
        The expected channel identifier as output.
    expected_message_id : `int`
        The expected message identifier as output.
    """
    output = parse_message_jump_url(message_jump_url)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 3)
    
    vampytest.assert_eq(output[0], expected_guild_id)
    vampytest.assert_eq(output[1], expected_channel_id)
    vampytest.assert_eq(output[2], expected_message_id)
