import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....localization import Locale
from ....user import AvatarDecoration, PremiumType, UserClan, UserFlag

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
    clan = UserClan(guild_id = 202405180021, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
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
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
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
    clan = UserClan(guild_id = 202405180022, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
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
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa_enabled = mfa_enabled,
        premium_type = premium_type,
    )
    vampytest.assert_instance(repr(user), str)


def test__Oauth2User__eq():
    """
    Tests whether ``Oauth2User.__eq__`` works as intended.
    """
    user_id = 202302040026
    
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160045)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    clan = UserClan(guild_id = 202405180023, tag = 'miau')
    discriminator = 2222
    display_name = 'far'
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa_enabled = True
    premium_type = PremiumType.nitro
    
    keyword_parameters = {
        'avatar': avatar,
        'avatar_decoration': avatar_decoration,
        'banner': banner,
        'banner_color': banner_color,
        'clan': clan,
        'discriminator': discriminator,
        'display_name': display_name,
        'flags': flags,
        'name': name,
        'email': email,
        'email_verified': email_verified,
        'locale': locale,
        'mfa_enabled': mfa_enabled,
        'premium_type': premium_type,
    }
    
    user = Oauth2User(**keyword_parameters)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())

    test_user = Oauth2User._create_empty(user_id)
    vampytest.assert_eq(test_user, test_user)
    vampytest.assert_ne(user, test_user)
    
    for field_name, field_value in (
        ('avatar', None),
        ('avatar_decoration', None),
        ('banner', None),
        ('banner_color', None),
        ('clan', None),
        ('discriminator', 0),
        ('display_name', None),
        ('flags', UserFlag(0)),
        ('name', 'okuu'),
        ('email', None),
        ('email_verified', False),
        ('locale', Locale.dutch),
        ('mfa_enabled', False),
        ('premium_type', PremiumType.none),
    ):
        test_user = Oauth2User(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(user, test_user)


def test__Oauth2User__format():
    """
    Tests whether ``Oauth2User.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160046)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    clan = UserClan(guild_id = 202405180024, tag = 'miau')
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
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
        clan = clan,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
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
