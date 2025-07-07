import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....role import Role, RoleColorConfiguration, RoleFlag
from ....permission import Permission
from ....utils import image_to_base64

from ...client import Client

from .helpers import IMAGE_DATA, TestDiscordApiClient


async def test__Client__role_edit__stuffed():
    """
    Tests whether ``Client.role_edit`` works as intended.
    
    Case: stuffed role.
    
    This function is a coroutine.
    """
    client_id = 202506190003
    guild_id = 202506190004
    role_id = 202506190005
    reason = 'howling moon'
    
    mock_api_role_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    role = Role.precreate(role_id, guild_id = guild_id)
    
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    flags = RoleFlag(12)
    icon_data = IMAGE_DATA
    icon = Icon(IconType.static, 2)
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    
    expected_role_data = {
        'color': int(color),
        'colors': color_configuration.to_data(),
        'flags': int(flags),
        'icon': image_to_base64(icon_data),
        'mentionable': mentionable,
        'name': name,
        'permissions': format(permissions, 'd'),
        'position': position,
        'hoist': separated,
    }
    
    output_role_data = {
        'id': str(role_id),
        'color': int(color),
        'colors': color_configuration.to_data(),
        'flags': int(flags),
        'icon': icon.as_base_16_hash,
        'mentionable': mentionable,
        'name': name,
        'permissions': format(permissions, 'd'),
        'position': position,
        'hoist': separated,
    }
    
    
    async def mock_api_role_edit(input_guild_id, input_role_id, input_role_data, input_reason):
        nonlocal mock_api_role_edit_called
        nonlocal guild_id
        nonlocal expected_role_data
        nonlocal output_role_data
        nonlocal reason
        nonlocal role_id
        mock_api_role_edit_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(role_id, input_role_id)
        vampytest.assert_eq(expected_role_data, input_role_data)
        vampytest.assert_eq(reason, input_reason)
        return output_role_data
    
    api.role_edit = mock_api_role_edit
        
    try:
        output = await client.role_edit(
            role,
            reason = reason,
            color = color,
            color_configuration = color_configuration,
            flags = flags,
            icon = icon_data,
            mentionable = mentionable,
            name = name,
            permissions = permissions,
            position = position,
            separated = separated,
        )
        vampytest.assert_true(mock_api_role_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
