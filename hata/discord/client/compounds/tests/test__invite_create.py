import vampytest
from scarletio import to_json
from scarletio.web_common import FormData

from ....application import Application
from ....invite import Invite, InviteTargetType
from ....channel import Channel, ChannelType
from ....core import INVITES
from ....role import Role
from ....user import User

from ...client import Client

from .helpers import TestDiscordApiClient


async def test__Client__invite_create__stuffed__no_allowed_user_ids():
    """
    Tests whether ``Client.invite_create`` works as intended.
    
    Case: stuffed invite; no allowed user ids.
    
    This function is a coroutine.
    """
    client_id = 202604090004
    channel_id = 202604090005
    role_id_0 = 202604090006
    role_id_1 = 202604090007
    target_application_id = 202604090008
    target_user_id = 202604090009
    invite_code = 'satori'
    reason = 'howling moon'
    
    mock_api_invite_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text)
    role_0 = Role.precreate(role_id_0, name = 'kagerou')
    role_1 = Role.precreate(role_id_1, name = 'wakasagihime')
    application = Application.precreate(target_application_id, name = 'hatate')
    user = User.precreate(target_user_id, name = 'sekibanki')
    
    max_age = 72000
    max_uses = 6666
    role_ids = [role_id_0, role_id_1]
    target_type = InviteTargetType.embedded_application
    temporary = True
    unique = True
    
    expected_invite_data = {
        'max_age': max_age,
        'max_uses': max_uses,
        'role_ids': [str(role_id) for role_id in role_ids],
        'target_application_id': str(target_application_id),
        'target_type': target_type.value,
        'target_user_id': str(target_user_id),
        'temporary': temporary,
        'unique': unique,
    }
    
    output_invite_data = {
        'code': invite_code,
        'max_age': max_age,
        'max_uses': max_uses,
        'roles': [
            role_0.to_data(include_internals = True),
            role_1.to_data(include_internals = True),
        ],
        'target_application': application.to_data_invite(include_internals = True),
        'target_type': target_type.value,
        'target_user': user.to_data(include_internals = True),
        'temporary': temporary,
        'unique': unique,
    }
    
    
    async def mock_api_invite_create(input_channel_id, input_invite_data, input_reason):
        nonlocal mock_api_invite_create_called
        nonlocal channel_id
        nonlocal expected_invite_data
        nonlocal output_invite_data
        nonlocal reason
        mock_api_invite_create_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(expected_invite_data, input_invite_data)
        vampytest.assert_eq(reason, input_reason)
        return output_invite_data
    
    api.invite_create = mock_api_invite_create
        
    try:
        output = await client.invite_create(
            channel,
            reason = reason,
            max_age = max_age,
            max_uses = max_uses,
            role_ids = role_ids,
            target_application_id = target_application_id,
            target_type = target_type,
            target_user_id = target_user_id,
            temporary = temporary,
            unique = unique,
        )
        vampytest.assert_true(mock_api_invite_create_called)
        
        vampytest.assert_instance(output, Invite)
        vampytest.assert_eq(output.code, invite_code)
        vampytest.assert_eq(output.max_age, max_age)
        vampytest.assert_eq(output.max_uses, max_uses)
        vampytest.assert_eq(output.roles, (role_0, role_1))
        vampytest.assert_eq(output.target_application_id, target_application_id)
        vampytest.assert_eq(output.target_type, target_type)
        vampytest.assert_eq(output.target_user_id, target_user_id)
        vampytest.assert_eq(output.temporary, temporary)
        
        # It should not be registered, just returned
        vampytest.assert_is(INVITES.get(invite_code, None), output)
    finally:
        client._delete()
        client = None


async def test__Client__invite_create__bland__with_allowed_user_ids():
    """
    Tests whether ``Client.invite_create`` works as intended.
    
    Case: bland invite; with allowed user ids.
    
    This function is a coroutine.
    """
    client_id = 202604090000
    channel_id = 202604090001
    user_id_0 = 202604090006
    user_id_1 = 202604090007
    invite_code = 'satori'
    reason = 'howling moon'
    
    mock_api_invite_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text)
    
    unique = True
    allowed_user_ids = [
        user_id_0,
        user_id_1,
    ]
    
    expected_invite_data = FormData()
    expected_invite_data.add_field('unique', to_json(True))
    expected_invite_data.add_field(
        'target_users_file',
        '\n'.join([str(user_id) for user_id in allowed_user_ids]),
        content_type = 'text/csv',
        file_name = f'file.csv',
    )
    
    output_invite_data = {
        'code': invite_code,
        'unique': unique,
    }
    
    
    async def mock_api_invite_create(input_channel_id, input_invite_data, input_reason):
        nonlocal mock_api_invite_create_called
        nonlocal channel_id
        nonlocal expected_invite_data
        nonlocal output_invite_data
        nonlocal reason
        mock_api_invite_create_called = True
        vampytest.assert_eq(channel_id, input_channel_id)
        vampytest.assert_eq(expected_invite_data, input_invite_data)
        vampytest.assert_eq(reason, input_reason)
        return output_invite_data
    
    api.invite_create = mock_api_invite_create
        
    try:
        output = await client.invite_create(
            channel,
            reason = reason,
            allowed_user_ids = allowed_user_ids,
            unique = unique,
        )
        vampytest.assert_true(mock_api_invite_create_called)
        
        vampytest.assert_instance(output, Invite)
        vampytest.assert_eq(output.code, invite_code)
        
        # It should not be registered, just returned
        vampytest.assert_is(INVITES.get(invite_code, None), output)
    finally:
        client._delete()
        client = None
