import vampytest

from ....bases import Icon, IconType
from ....guild import Guild
from ....user import AvatarDecoration, NameStyle, NameStyleFont
from ....utils import image_to_base64

from ...client import Client

from .helpers import IMAGE_DATA, TestDiscordApiClient


async def test__Client__guild_profile_edit__stuffed():
    """
    Tests whether ``Client.guild_profile_edit`` works as intended.
    
    Case: stuffed.
    
    This function is a coroutine.
    """
    client_id = 202604200002
    guild_id = 202604200004
    reason = 'Mokou'
    
    mock_client_guild_profile_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    
    avatar_data = IMAGE_DATA
    avatar = Icon(IconType.static, 2)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202604200003)
    banner_data = IMAGE_DATA
    banner = Icon(IconType.static, 2)
    bio = 'Get caved'
    name_style = NameStyle(
        font = NameStyleFont.sakura,
    )
    nick = 'keine'
    
    expected_role_data = {
        'avatar': image_to_base64(avatar_data),
        'avatar_decoration_data': avatar_decoration.to_data(defaults = True),
        'banner': image_to_base64(banner_data),
        'bio': bio,
        'display_name_styles': name_style.to_data(defaults = True),
        'nick': nick,
    }
    
    output_role_data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'banner': banner.as_base_16_hash,
        'bio': bio,
        'display_name_styles': name_style.to_data(),
        'nick': nick,
    }
    
    
    async def mock_client_guild_profile_edit(input_guild_id, input_role_data, input_reason):
        nonlocal mock_client_guild_profile_edit_called
        nonlocal expected_role_data
        nonlocal output_role_data
        nonlocal guild_id
        nonlocal reason
        mock_client_guild_profile_edit_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(expected_role_data, input_role_data)
        vampytest.assert_eq(reason, input_reason)
        return output_role_data
    
    api.client_guild_profile_edit = mock_client_guild_profile_edit
        
    try:
        output = await client.guild_profile_edit(
            guild,
            reason = reason,
            avatar = avatar_data,
            avatar_decoration = avatar_decoration,
            banner = banner_data,
            bio = bio,
            name_style = name_style,
            nick = nick,
        )
        vampytest.assert_true(mock_client_guild_profile_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
