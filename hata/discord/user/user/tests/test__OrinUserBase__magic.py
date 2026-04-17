import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....guild import GuildBadge

from ...avatar_decoration import AvatarDecoration
from ...name_plate import NamePlate

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
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030008,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180007, tag = 'miau')
    
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
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
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
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030008,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180008, tag = 'miau')
    
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
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
    )
    vampytest.assert_instance(repr(user), str)


def test__OrinUserBase__eq__non_partial_and_different_object():
    """
    Tests whether ``OrinUserBase.__eq__`` works as intended.
    
    Case: non partial and non user object.
    """
    user_id = 202504260011
    
    name = 'Orin'
    
    user = OrinUserBase(name = name)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())
    
    test_user = OrinUserBase._create_empty(user_id)
    vampytest.assert_eq(test_user, test_user)
    vampytest.assert_ne(user, test_user)


def _iter_options__eq():
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160036)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030009,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180009, tag = 'miau')
    
    keyword_parameters = {
        'avatar': avatar,
        'name': name,
        'avatar_decoration': avatar_decoration,
        'banner': banner,
        'banner_color': banner_color,
        'discriminator': discriminator,
        'display_name': display_name,
        'flags': flags,
        'name_plate': name_plate,
        'primary_guild_badge': primary_guild_badge,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'avatar': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'avatar_decoration': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'banner': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'banner_color': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'discriminator': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'display_name': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': UserFlag(0),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'okuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name_plate': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'primary_guild_badge': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__OrinUserBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``OrinUserBase.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    instance_0 = OrinUserBase(**keyword_parameters_0)
    instance_1 = OrinUserBase(**keyword_parameters_1)
    
    output = instance_0 == instance_1
    vampytest.assert_instance(output, bool)
    return output


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
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030010,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180010, tag = 'miau')
    
    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
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
