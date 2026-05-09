import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....user import AvatarDecoration, NameStyle, NameStyleFont
from ....utils import image_to_base64

from ...client import Client

from .helpers import IMAGE_DATA, TestDiscordApiClient


async def test__Client__edit__stuffed():
    """
    Tests whether ``Client.edit`` works as intended.
    
    Case: stuffed.
    
    This function is a coroutine.
    """
    client_id = 202604200000
    
    mock_client_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    avatar_data = IMAGE_DATA
    avatar = Icon(IconType.static, 2)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202604200001)
    banner_data = IMAGE_DATA
    banner = Icon(IconType.static, 2)
    banner_color = Color(123)
    display_name = 'EX Keine'
    name = 'keine'
    name_style = NameStyle(
        font = NameStyleFont.sakura,
    )
    
    expected_role_data = {
        'avatar': image_to_base64(avatar_data),
        'avatar_decoration_data': avatar_decoration.to_data(defaults = True),
        'banner': image_to_base64(banner_data),
        'accent_color': int(banner_color),
        'global_name': display_name,
        'username': name,
        'display_name_styles': name_style.to_data(defaults = True),
    }
    
    output_role_data = {
        'id': str(client.id),
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'banner': banner.as_base_16_hash,
        'accent_color': int(banner_color),
        'global_name': display_name,
        'username': name,
        'display_name_styles': name_style.to_data(),
    }
    
    
    async def mock_client_edit(input_role_data):
        nonlocal mock_client_edit_called
        nonlocal expected_role_data
        nonlocal output_role_data
        mock_client_edit_called = True
        vampytest.assert_eq(expected_role_data, input_role_data)
        return output_role_data
    
    api.client_edit = mock_client_edit
        
    try:
        output = await client.edit(
            avatar = avatar_data,
            avatar_decoration = avatar_decoration,
            banner = banner_data,
            banner_color = banner_color,
            display_name = display_name,
            name = name,
            name_style = name_style,
        )
        vampytest.assert_true(mock_client_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
