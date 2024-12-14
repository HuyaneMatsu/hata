import vampytest

from ....embedded_activity import EmbeddedActivity, EmbeddedActivityLocation, EmbeddedActivityLocationType

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__embedded_activity_get__stuffed():
    """
    Tests whether ``Client.embedded_activity_get`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202409040060
    guild_id = 202409040061
    embedded_activity_id = 202409040062
    channel_id = 202409040063
    launch_id = 202409040064
    application_id = 202409040065
    
    mock_api_embedded_activity_get_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, application_id = application_id, client_id = client_id)
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id, application_id = application_id, guild_id = guild_id
    )
    
    location = EmbeddedActivityLocation(
        channel_id = channel_id, guild_id = guild_id, location_type = EmbeddedActivityLocationType.guild_channel
    )
    
    output_embedded_activity_data = {
        'instance_id': str(embedded_activity_id),
        'launch_id': str(launch_id),
        'application_id': application_id,
        'guild_id': str(guild_id),
        'location': location.to_data(),
    }
    
    async def mock_api_embedded_activity_get(input_application_id, input_embedded_activity_id):
        nonlocal mock_api_embedded_activity_get_called
        nonlocal application_id
        nonlocal embedded_activity_id
        nonlocal output_embedded_activity_data
        mock_api_embedded_activity_get_called = True
        vampytest.assert_eq(application_id, input_application_id)
        vampytest.assert_eq(embedded_activity_id, input_embedded_activity_id)
        return output_embedded_activity_data
    
    api.embedded_activity_get = mock_api_embedded_activity_get
        
    try:
        output = await client.embedded_activity_get(
            embedded_activity,
            force_update = True,
        )
        vampytest.assert_true(mock_api_embedded_activity_get_called)
        
        vampytest.assert_instance(output, EmbeddedActivity)
        vampytest.assert_eq(output.id, embedded_activity_id)
        vampytest.assert_eq(output.guild_id, guild_id)
        vampytest.assert_eq(output.launch_id, launch_id)
        vampytest.assert_eq(output.application_id, application_id)
        vampytest.assert_eq(output.location, location)
    finally:
        client._delete()
        client = None
