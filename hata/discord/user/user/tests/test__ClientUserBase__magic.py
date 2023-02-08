import vampytest

from ....bases import Icon, IconType
from ....color import Color

from ..flags import UserFlag
from ..client_user_base import ClientUserBase


def test__ClientUserBase__repr():
    """
    Tests whether ``ClientUserBase.__repr__`` works as intended.
    """
    user_id = 202302060001
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    
    user = ClientUserBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = ClientUserBase(
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        bot = bot,
    )
    vampytest.assert_instance(repr(user), str)


def test__ClientUserBase__hash():
    """
    Tests whether ``ClientUserBase.__hash__`` works as intended.
    """
    user_id = 202302060002
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    
    user = ClientUserBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = ClientUserBase(
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
        bot = bot,
    )
    vampytest.assert_instance(repr(user), str)


def test__ClientUserBase__eq():
    """
    Tests whether ``ClientUserBase.__eq__`` works as intended.
    """
    user_id = 202302060003
    
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    
    keyword_parameters = {
        'avatar': avatar,
        'banner': banner,
        'banner_color': banner_color,
        'discriminator': discriminator,
        'flags': flags,
        'name': name,
        'bot': bot,
    }
    
    user = ClientUserBase(**keyword_parameters)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())

    test_user = ClientUserBase._create_empty(user_id)
    vampytest.assert_eq(test_user, test_user)
    vampytest.assert_ne(user, test_user)
    
    for field_name, field_value in (
        ('avatar', None),
        ('banner', None),
        ('banner_color', None),
        ('discriminator', 0),
        ('flags', UserFlag(0)),
        ('name', 'okuu'),
        ('bot', False),
    ):
        test_user = ClientUserBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(user, test_user)


def test__ClientUserBase__format():
    """
    Tests whether ``ClientUserBase.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    
    user = ClientUserBase(
        avatar = avatar,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
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
