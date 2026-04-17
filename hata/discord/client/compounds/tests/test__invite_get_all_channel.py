import vampytest

from ....invite import Invite
from ....channel import Channel, ChannelType

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_get_all_channel():
    """
    Tests whether ``Client.invite_get_all_channel`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202604110005
    invite_code_0 = 'satori'
    invite_code_1 = 'eye'
    channel_id = 202604110006
    
    mock_api_invite_get_all_channel_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text)
    channel.clients.append(client)
    
    invite_0 = Invite.precreate(
        invite_code_0, channel = channel, uses = 13
    )
    invite_1 = Invite.precreate(
        invite_code_1, channel = channel, uses = 14
    )
    response_data = [
        invite_0.to_data(include_internals = True),
        invite_1.to_data(include_internals = True),
    ]
    
    async def mock_api_invite_get_all_channel(input_channel_id):
        nonlocal mock_api_invite_get_all_channel_called
        nonlocal channel_id
        nonlocal response_data
        
        mock_api_invite_get_all_channel_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        
        return response_data
    
    
    api.invite_get_all_channel = mock_api_invite_get_all_channel
        
    try:
        output = await client.invite_get_all_channel(channel)
        vampytest.assert_true(mock_api_invite_get_all_channel_called)
        
        vampytest.assert_eq(output, [invite_0, invite_1])
    finally:
        client._delete()
        client = None
