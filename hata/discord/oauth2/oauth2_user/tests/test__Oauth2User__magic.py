import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....localization import Locale
from ....user import PremiumType, UserFlag

from ..oauth2_user import Oauth2User


def test__Oauth2User__repr():
    """
    Tests whether ``Oauth2User.__repr__`` works as intended.
    """
    user_id = 202302040024
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = Oauth2User(
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa = mfa,
        premium_type = premium_type,
    )
    vampytest.assert_instance(repr(user), str)


def test__Oauth2User__hash():
    """
    Tests whether ``Oauth2User.__hash__`` works as intended.
    """
    user_id = 202302040025
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = Oauth2User(
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa = mfa,
        premium_type = premium_type,
    )
    vampytest.assert_instance(repr(user), str)


def test__Oauth2User__eq():
    """
    Tests whether ``Oauth2User.__eq__`` works as intended.
    """
    user_id = 202302040026
    
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa = True
    premium_type = PremiumType.nitro
    
    keyword_parameters = {
        'avatar': avatar,
        'banner': banner,
        'banner_color': banner_color,
        'discriminator': discriminator,
        'flags': flags,
        'name': name,
        'email': email,
        'email_verified': email_verified,
        'locale': locale,
        'mfa': mfa,
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
        ('banner', None),
        ('banner_color', None),
        ('discriminator', 0),
        ('flags', UserFlag(0)),
        ('name', 'okuu'),
        ('email', None),
        ('email_verified', False),
        ('locale', Locale.dutch),
        ('mfa', False),
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
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    email = 'rin@orindance.party'
    email_verified = True
    locale = Locale.greek
    mfa = True
    premium_type = PremiumType.nitro
    
    user = Oauth2User(
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        email = email,
        email_verified = email_verified,
        locale = locale,
        mfa = mfa,
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
