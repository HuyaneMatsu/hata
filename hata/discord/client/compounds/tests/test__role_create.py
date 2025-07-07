import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....role import Role, RoleColorConfiguration, RoleFlag
from ....guild import Guild
from ....permission import Permission
from ....utils import image_to_base64

from ...client import Client

from .helpers import IMAGE_DATA, TestDiscordApiClient


async def test__Client__role_create__stuffed():
    """
    Tests whether ``Client.role_create`` works as intended.
    
    Case: stuffed role.
    
    This function is a coroutine.
    """
    client_id = 202506190000
    guild_id = 202506190001
    role_id = 202506190002
    reason = 'howling moon'
    
    mock_api_role_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    
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
    
    
    async def mock_api_role_create(input_guild_id, input_role_data, input_reason):
        nonlocal mock_api_role_create_called
        nonlocal guild_id
        nonlocal expected_role_data
        nonlocal output_role_data
        nonlocal reason
        mock_api_role_create_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(expected_role_data, input_role_data)
        vampytest.assert_eq(reason, input_reason)
        return output_role_data
    
    api.role_create = mock_api_role_create
        
    try:
        output = await client.role_create(
            guild,
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
        vampytest.assert_true(mock_api_role_create_called)
        
        vampytest.assert_instance(output, Role)
        vampytest.assert_eq(output.id, role_id)
        vampytest.assert_eq(output.color, color)
        vampytest.assert_eq(output.color_configuration, color_configuration)
        vampytest.assert_eq(output.flags, flags)
        vampytest.assert_eq(output.icon, icon)
        vampytest.assert_eq(output.mentionable, mentionable)
        vampytest.assert_eq(output.name, name)
        vampytest.assert_eq(output.permissions, permissions)
        vampytest.assert_eq(output.position, position)
        vampytest.assert_eq(output.separated, separated)
        
        # It should not be registered, just returned
        vampytest.assert_is(guild.roles.get(role_id, None), output)
    finally:
        client._delete()
        client = None
