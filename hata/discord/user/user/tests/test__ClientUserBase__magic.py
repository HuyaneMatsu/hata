import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....guild import GuildBadge

from ...avatar_decoration import AvatarDecoration

from ..flags import UserFlag
from ..client_user_base import ClientUserBase


def test__ClientUserBase__repr():
    """
    Tests whether ``ClientUserBase.__repr__`` works as intended.
    """
    user_id = 202302060001
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160031)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    primary_guild_badge = GuildBadge(guild_id = 202405180035, tag = 'miau')
    bot = True
    
    user = ClientUserBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = ClientUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        primary_guild_badge = primary_guild_badge,
        bot = bot,
    )
    vampytest.assert_instance(repr(user), str)


def test__ClientUserBase__hash():
    """
    Tests whether ``ClientUserBase.__hash__`` works as intended.
    """
    user_id = 202302060002
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160032)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    primary_guild_badge = GuildBadge(guild_id = 202405180036, tag = 'miau')
    bot = True
    
    user = ClientUserBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = ClientUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        primary_guild_badge = primary_guild_badge,
        bot = bot,
    )
    vampytest.assert_instance(repr(user), str)


def test__ClientUserBase__eq__non_partial_and_different_object():
    """
    Tests whether ``ClientUserBase.__eq__`` works as intended.
    
    Case: non partial and non user object.
    """
    user_id = 202504260012
    
    name = 'Orin'
    
    user = ClientUserBase(name = name)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())
    
    test_user = ClientUserBase._create_empty(user_id)
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
    primary_guild_badge = GuildBadge(guild_id = 202405180009, tag = 'miau')
    bot = True
    
    keyword_parameters = {
        'avatar': avatar,
        'name': name,
        'avatar_decoration': avatar_decoration,
        'banner': banner,
        'banner_color': banner_color,
        'discriminator': discriminator,
        'display_name': display_name,
        'flags': flags,
        'primary_guild_badge': primary_guild_badge,
        'bot': bot,
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
            'name': 'okuu',
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
            'primary_guild_badge': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'bot': False,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ClientUserBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ClientUserBase.__eq__`` works as intended.
    
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
    instance_0 = ClientUserBase(**keyword_parameters_0)
    instance_1 = ClientUserBase(**keyword_parameters_1)
    
    output = instance_0 == instance_1
    vampytest.assert_instance(output, bool)
    return output


def test__ClientUserBase__format():
    """
    Tests whether ``ClientUserBase.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160051)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    primary_guild_badge = GuildBadge(guild_id = 202405180038, tag = 'miau')
    bot = True
    
    user = ClientUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        primary_guild_badge = primary_guild_badge,
        bot = bot,
    )
    
    vampytest.assert_instance(format(user, ''), str)


def test__ClientUserBase__sort():
    """
    Tests whether sorting ``ClientUserBase` works as intended.
    """
    user_id_0 = 202302060004
    user_id_1 = 202302060005
    user_id_2 = 202302060006
    
    user_0 = ClientUserBase._create_empty(user_id_0)
    user_1 = ClientUserBase._create_empty(user_id_1)
    user_2 = ClientUserBase._create_empty(user_id_2)
    
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
