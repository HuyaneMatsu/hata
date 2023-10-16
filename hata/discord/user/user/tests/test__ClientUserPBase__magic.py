import vampytest

from ....activity import Activity, ActivityType
from ....bases import Icon, IconType
from ....color import Color

from ...avatar_decoration import AvatarDecoration

from ..flags import UserFlag
from ..client_user_presence_base import ClientUserPBase
from ..preinstanced import Status


def test__ClientUserPBase__repr():
    """
    Tests whether ``ClientUserPBase.__repr__`` works as intended.
    """
    user_id = 202302060001
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160058)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    activities = [Activity('orin dance', activity_type = ActivityType.game)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    user = ClientUserPBase._create_empty(user_id)
    vampytest.assert_instance(repr(user), str)

    user = ClientUserPBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        bot = bot,
        activities = activities,
        status = status,
        statuses = statuses,
    )
    vampytest.assert_instance(repr(user), str)


def test__ClientUserPBase__hash():
    """
    Tests whether ``ClientUserPBase.__hash__`` works as intended.
    """
    user_id = 202302060002
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160059)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    activities = [Activity('orin dance', activity_type = ActivityType.game)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    user = ClientUserPBase._create_empty(user_id)
    vampytest.assert_instance(hash(user), int)
    
    user = ClientUserPBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        bot = bot,
        activities = activities,
        status = status,
        statuses = statuses,
    )
    vampytest.assert_instance(hash(user), int)


def test__ClientUserPBase__eq():
    """
    Tests whether ``ClientUserPBase.__eq__`` works as intended.
    """
    user_id = 202302060003
    
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160060)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    activities = [Activity('orin dance', activity_type = ActivityType.game)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    keyword_parameters = {
        'avatar': avatar,
        'avatar_decoration': avatar_decoration,
        'banner': banner,
        'banner_color': banner_color,
        'discriminator': discriminator,
        'display_name': display_name,
        'flags': flags,
        'name': name,
        'bot': bot,
        'activities': activities,
        'status': status,
        'statuses': statuses,
    }
    
    user = ClientUserPBase(**keyword_parameters)
    vampytest.assert_eq(user, user)
    vampytest.assert_ne(user, object())

    test_user = ClientUserPBase._create_empty(user_id)
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
        ('bot', False),
        ('activities', None),
        ('status', Status.idle),
        ('statuses', None),
    ):
        test_user = ClientUserPBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(user, test_user)


def test__ClientUserPBase__format():
    """
    Tests whether ``ClientUserPBase.__format__`` works as intended.
    
    Case: Shallow.
    """
    avatar = Icon(IconType.static, 14)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160061)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'orin'
    bot = True
    activities = [Activity('orin dance', activity_type = ActivityType.game)]
    status = Status.online
    statuses = {'mobile': Status.online.value}
    
    user = ClientUserPBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        bot = bot,
        activities = activities,
        status = status,
        statuses = statuses,
    )
    
    vampytest.assert_instance(format(user, ''), str)


def test__ClientUserPBase__sort():
    """
    Tests whether sorting ``ClientUserPBase` works as intended.
    """
    user_id_0 = 202302080005
    user_id_1 = 202302080006
    user_id_2 = 202302080007
    
    user_0 = ClientUserPBase._create_empty(user_id_0)
    user_1 = ClientUserPBase._create_empty(user_id_1)
    user_2 = ClientUserPBase._create_empty(user_id_2)
    
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
