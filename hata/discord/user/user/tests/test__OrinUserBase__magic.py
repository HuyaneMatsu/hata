import vampytest

from ....bases import Icon, IconType
from ....color import Color

from ...avatar_decoration import AvatarDecoration

from ..flags import UserFlag
from ..orin_user_base import OrinUserBase


def test__OrinUserBase__repr():
    """
    Tests whether ``OrinUserBase.__repr__`` works as intended.
    """
    user_id = 202302040016
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160034)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    
    user = OrinUserBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
    )
    vampytest.assert_instance(repr(user), str)


def test__OrinUserBase__hash():
    """
    Tests whether ``OrinUserBase.__hash__`` works as intended.
    """
    user_id = 202302040017
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160035)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    
    user = OrinUserBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
    )
    vampytest.assert_instance(repr(user), str)


def test__OrinUserBase__eq():
    """
    Tests whether ``OrinUserBase.__eq__`` works as intended.
    """
    user_id = 202302040018
    
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160036)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    
    keyword_parameters = {
        'avatar': avatar,
        'avatar_decoration': avatar_decoration,
        'banner': banner,
        'banner_color': banner_color,
        'discriminator': discriminator,
        'display_name': display_name,
        'flags': flags,
        'name': name,
    }
    
    user = OrinUserBase(**keyword_parameters)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())

    test_user = OrinUserBase._create_empty(user_id)
    vampytest.assert_eq(test_user, test_user)
    vampytest.assert_ne(user, test_user)
    
    for field_name, field_value in (
        ('avatar', None),
        ('avatar_decoration', None),
        ('banner', None),
        ('banner_color', None),
        ('discriminator', 0),
        ('display_name', None),
        ('flags', UserFlag(0)),
        ('name', 'okuu'),
    ):
        test_user = OrinUserBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(user, test_user)


def test__OrinUserBase__format():
    """
    Tests whether ``OrinUserBase.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160037)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    
    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
    )
    
    vampytest.assert_instance(format(user, ''), str)


def test__OrinUserBase__sort():
    """
    Tests whether sorting ``OrinUserBase` works as intended.
    """
    user_id_0 = 202302040019
    user_id_1 = 202302040020
    user_id_2 = 202302040021
    
    user_0 = OrinUserBase._create_empty(user_id_0)
    user_1 = OrinUserBase._create_empty(user_id_1)
    user_2 = OrinUserBase._create_empty(user_id_2)
    
    to_sort = [
        user_1,
        user_2,
        user_0,
    ]
    
    expected_output = [
        user_0,
        user_1,
        user_2,
    ]
    
    vampytest.assert_eq(sorted(to_sort), expected_output)
