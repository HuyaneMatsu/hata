import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....localization import Locale
from ....guild import GuildBadge
from ....user import AvatarDecoration, PremiumType, UserFlag

from ..oauth2_user import Oauth2User


def test__Oauth2User__repr():
    """
    Tests whether ``Oauth2User.__repr__`` works as intended.
    """
    user_id = 202302040024
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160043)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    primary_guild_badge = GuildBadge(guild_id = 202405180021, tag = 'miau')
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        primary_guild_badge = primary_guild_badge,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa_enabled = mfa_enabled,
        premium_type = premium_type,
    )
    vampytest.assert_instance(repr(user), str)


def test__Oauth2User__hash():
    """
    Tests whether ``Oauth2User.__hash__`` works as intended.
    """
    user_id = 202302040025
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160044)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    primary_guild_badge = GuildBadge(guild_id = 202405180022, tag = 'miau')
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        primary_guild_badge = primary_guild_badge,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa_enabled = mfa_enabled,
        premium_type = premium_type,
    )
    vampytest.assert_instance(repr(user), str)


def test__Oauth2User__eq__non_partial_and_different_object():
    """
    Tests whether ``Oauth2User.__eq__`` works as intended.
    
    Case: non partial and non user object.
    """
    user_id = 202504260014
    
    name = 'Orin'
    
    user = Oauth2User(name = name)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())
    
    test_user = Oauth2User._create_empty(user_id)
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
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro
    
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
        'email': email,
        'email_verified': email_verified,
        'locale': locale,
        'mfa_enabled': mfa_enabled,
        'premium_type': premium_type,
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
            'email': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'email_verified': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'locale': Locale.dutch,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mfa_enabled': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'premium_type': PremiumType.none,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Oauth2User__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Oauth2User.__eq__`` works as intended.
    
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
    instance_0 = Oauth2User(**keyword_parameters_0)
    instance_1 = Oauth2User(**keyword_parameters_1)
    
    output = instance_0 == instance_1
    vampytest.assert_instance(output, bool)
    return output


def test__Oauth2User__format():
    """
    Tests whether ``Oauth2User.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160046)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    primary_guild_badge = GuildBadge(guild_id = 202405180024, tag = 'miau')
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        primary_guild_badge = primary_guild_badge,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa_enabled = mfa_enabled,
        premium_type = premium_type,
    )
    
    vampytest.assert_instance(format(user, ''), str)


def test__Oauth2User__sort():
    """
    Tests whether sorting ``Oauth2User` works as intended.
    """
    user_id_0 = 202302040027
    user_id_1 = 202302040028
    user_id_2 = 202302040029
    
    user_0 = Oauth2User._create_empty(user_id_0)
    user_1 = Oauth2User._create_empty(user_id_1)
    user_2 = Oauth2User._create_empty(user_id_2)
    
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
