import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji
from ....guild import Guild
from ....localization import Locale
from ....message import Message
from ....role import Role
from ....utils import is_url

from ...avatar_decoration import AvatarDecoration
from ...user_clan import UserClan

from ..flags import UserFlag
from ..preinstanced import DefaultAvatar, PremiumType, Status
from ..user_base import UserBase


def test__UserBase__placeholders():
    """
    Tests whether ``UserBase``'s placeholders work as intended.
    """
    user = UserBase()
    vampytest.assert_instance(user.activities, list, nullable = True)
    vampytest.assert_instance(user.avatar_decoration, AvatarDecoration, nullable = True)
    vampytest.assert_instance(user.banner, Icon)
    vampytest.assert_instance(user.banner_color, Color, nullable = True)
    vampytest.assert_instance(user.banner_hash, int)
    vampytest.assert_instance(user.banner_type, IconType)
    vampytest.assert_instance(user.clan, UserClan, nullable = True)
    vampytest.assert_instance(user.bot, bool)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.display_name, str, nullable = True)
    vampytest.assert_instance(user.email, str, nullable = True)
    vampytest.assert_instance(user.email_verified, bool)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.guild_profiles, dict)
    vampytest.assert_instance(user.locale, Locale)
    vampytest.assert_instance(user.mfa_enabled, bool)
    vampytest.assert_instance(user.premium_type, PremiumType)
    vampytest.assert_instance(user.status, Status)
    vampytest.assert_instance(user.statuses, dict, nullable = True)
    vampytest.assert_instance(user.thread_profiles, dict, nullable = True)


def test__UserBase__banner_url():
    """
    Tests whether ``UserBase.banner_url`` work as intended.
    """
    user = UserBase()
    banner_url = user.banner_url
    
    vampytest.assert_instance(banner_url, str, nullable = True)
    if (banner_url is not None):
        vampytest.assert_true(is_url(banner_url))


def test__UserBase__banner_url_as():
    """
    Tests whether ``UserBase.banner_url_as`` work as intended.
    """
    user = UserBase()
    banner_url = user.banner_url_as(ext = 'jpg', size = 4096)
    
    vampytest.assert_instance(banner_url, str, nullable = True)
    if (banner_url is not None):
        vampytest.assert_true(is_url(banner_url))


def test__UserBase__avatar_decoration_url():
    """
    Tests whether ``UserBase.avatar_decoration_url`` work as intended.
    """
    user = UserBase()
    avatar_decoration_url = user.avatar_decoration_url
    
    vampytest.assert_instance(avatar_decoration_url, str, nullable = True)
    if (avatar_decoration_url is not None):
        vampytest.assert_true(is_url(avatar_decoration_url))


def test__UserBase__avatar_decoration_url_as():
    """
    Tests whether ``UserBase.avatar_decoration_url_as`` work as intended.
    """
    user = UserBase()
    avatar_decoration_url = user.avatar_decoration_url_as(ext = 'png', size = 4096)
    
    vampytest.assert_instance(avatar_decoration_url, str, nullable = True)
    if (avatar_decoration_url is not None):
        vampytest.assert_true(is_url(avatar_decoration_url))


def test__UserBase__full_name():
    """
    Tests whether ``Userbase.full_name`` works as intended.
    """
    user = UserBase()
    vampytest.assert_instance(user.full_name, str)


def test__UserBase__mention():
    """
    Tests whether ``Userbase.mention`` works as intended.
    """
    user = UserBase()
    vampytest.assert_instance(user.mention, str)


def test__UserBase__mention_nick():
    """
    Tests whether ``Userbase.mention_nick`` works as intended.
    """
    user = UserBase()
    vampytest.assert_instance(user.mention_nick, str)


def test__UserBase__default_avatar_url():
    """
    Tests whether ``Userbase.default_avatar_url`` works as intended.
    """
    user = UserBase()
    default_avatar_url = user.default_avatar_url
    
    vampytest.assert_instance(default_avatar_url, str)
    vampytest.assert_true(is_url(default_avatar_url))


def test__UserBase__default_avatar():
    """
    Tests whether ``Userbase.default_avatar`` works as intended.
    """
    user = UserBase()
    vampytest.assert_instance(user.default_avatar, DefaultAvatar)


def test__UserBase__iter_activities():
    """
    Tests whether ``Userbase.iter_activities`` works as intended.
    """
    user = UserBase()
    vampytest.assert_eq([*user.iter_activities()], [])


def test__UserBase__partial():
    """
    Tests whether ``Userbase.partial`` works as intended.
    """
    user = UserBase()
    vampytest.assert_eq(user.partial, True)


def test__UserBase__activity():
    """
    Tests whether ``Userbase.activity`` works as intended.
    """
    user = UserBase()
    vampytest.assert_is(user.activity, None)


def test__UserBase__custom_activity():
    """
    Tests whether ``Userbase.custom_activity`` works as intended.
    """
    user = UserBase()
    vampytest.assert_is(user.custom_activity, None)


def test__UserBase__platform():
    """
    Tests whether ``Userbase.platform`` works as intended.
    """
    user = UserBase()
    output = user.platform
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, '')


def test__UserBase__color_at():
    """
    Tests whether ``Userbase.color_at`` works as intended.
    """
    user = UserBase()
    guild_id = 202302040000
    output = user.color_at(guild_id)
    vampytest.assert_instance(output, Color)
    vampytest.assert_eq(output, 0)


def test__UserBase__name_at():
    """
    Tests whether ``Userbase.name_at`` works as intended.
    """
    user = UserBase()
    guild_id = 202302040001
    output = user.name_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, '')


def test__UserBase__has_name_like():
    """
    Tests whether ``Userbase.has_name_like`` works as intended.
    """
    name = 'orin'
    user_id = 202302040002
    user = UserBase(
        name = name,
    )
    user.id = user_id
    
    for input_value, expected_output in (
        ('Orin', True),
        ('Okuu', False),
        ('@orin', True),
        ('@okuu', False),
        ('orin#0000', True),
        ('okuu#0000', False),
        ('orin#0010', False),
        ('rin', True),
    ):
        vampytest.assert_eq(user.has_name_like(input_value), expected_output)


def test__UserBase__has_name_like_at():
    """
    Tests whether ``Userbase.has_name_like_at`` works as intended.
    """
    name = 'orin'
    user_id = 202302040003
    user = UserBase(
        name = name,
    )
    user.id = user_id
    
    guild_id = 202302040004
    
    for input_value, expected_output in (
        ('Orin', True),
        ('Okuu', False),
        ('@orin', True),
        ('@okuu', False),
        ('orin#0000', True),
        ('okuu#0000', False),
        ('orin#0010', False),
        ('rin', True),
    ):
        vampytest.assert_eq(user.has_name_like_at(input_value, guild_id), expected_output)


def test__UserBase__mentioned_in():
    """
    Tests whether ``Userbase.mentioned_in`` works as intended.
    """
    user = UserBase()
    
    for message, expected_output in (
        (Message.precreate(202302040005, mentioned_everyone = True), True),
        (Message.precreate(202302040006), False),
        # (Message.precreate(202302040007, mentioned_users = [user]), True),
    ):
        vampytest.assert_eq(user.mentioned_in(message), expected_output)


def test__UserBase__has_role():
    """
    Tests whether ``Userbase.has_role`` works as intended.
    """
    user = UserBase()
    
    guild_id = 202302040008
    role_id_0 = 202302040009
    
    role_0 = Role.precreate(role_id_0, guild_id = guild_id)
    

    vampytest.assert_eq(user.has_role(role_0), False)


def test__UserBase__top_role_at():
    """
    Tests whether ``Userbase.top_role_at`` works as intended.
    """
    user = UserBase()
    guild_id = 202302040010
    default = object()

    vampytest.assert_is(user.top_role_at(guild_id, default = default), default)


def test__UserBase__can_use_emoji():
    """
    Tests whether ``Userbase.can_use_emoji`` works as intended.
    """
    user = UserBase()
    
    emoji_0 = BUILTIN_EMOJIS['x']
    emoji_1 = Emoji.precreate(202302040011)
    
    vampytest.assert_true(user.can_use_emoji(emoji_0))
    vampytest.assert_false(user.can_use_emoji(emoji_1))


def test__UserBase__has_higher_role_than():
    """
    Tests whether ``Userbase.has_higher_role_than`` works as intended.
    """
    user = UserBase()
    
    
    guild_id = 2023020400012
    role_id_0 = 202302040013
    
    role_0 = Role.precreate(role_id_0, guild_id = guild_id)
    
    vampytest.assert_false(user.has_higher_role_than(role_0))


def test__UserBase__has_higher_role_than_at():
    """
    Tests whether ``Userbase.has_higher_role_than_at`` works as intended.
    """
    user_0 = UserBase()
    user_1 = UserBase()
    
    guild_id = 2023020400014
    
    vampytest.assert_false(user_0.has_higher_role_than_at(user_1, guild_id))


def test__UserBase__get_guild_profile_for():
    """
    Tests whether ``Userbase.get_guild_profile_for`` works as intended.
    """
    user = UserBase()
    
    guild_id = 2023020400015
    
    vampytest.assert_is(user.get_guild_profile_for(guild_id), None)


def test__UserBase__iter_guilds_and_profiles():
    """
    Tests whether ``Userbase.iter_guilds_and_profiles`` works as intended.
    """
    user = UserBase()
    
    vampytest.assert_eq([*user.iter_guilds_and_profiles()], [])


def test__UserBase__iter_guilds():
    """
    Tests whether ``Userbase.iter_guilds`` works as intended.
    """
    user = UserBase()
    
    vampytest.assert_eq([*user.iter_guilds()], [])


def test__UserBase__is_boosting():
    """
    Tests whether ``Userbase.is_boosting`` works as intended.
    """
    user = UserBase()
    
    guild_id = 2023020400016
    
    vampytest.assert_eq(user.is_boosting(guild_id), False)


def test__UserBase__avatar_url_for():
    """
    Tests whether ``Userbase.avatar_url_for`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    user = UserBase(
        avatar = avatar,
    )
    
    guild_id = 2023020400016
    
    output = user.avatar_url_for(guild_id)
    vampytest.assert_is(output, None)



def test__UserBase__avatar_url_for_as():
    """
    Tests whether ``Userbase.avatar_url_for_as`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    user = UserBase(
        avatar = avatar,
    )
    
    guild_id = 2023020400017
    
    output = user.avatar_url_for_as(guild_id)
    vampytest.assert_is(output, None)


def test__UserBase__avatar_url_at():
    """
    Tests whether ``Userbase.avatar_url_at`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    user = UserBase(
        avatar = avatar,
    )
    
    guild_id = 2023020400018
    
    output = user.avatar_url_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_true(is_url(output))


def test__UserBase__avatar_url_at_as():
    """
    Tests whether ``Userbase.avatar_url_at_as`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    user = UserBase(
        avatar = avatar,
    )
    
    guild_id = 2023020400019
    
    output = user.avatar_url_at_as(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_true(is_url(output))


def test__UserBase__delete():
    """
    Tests whether ``Userbase._delete`` works as intended.
    """
    user = UserBase()
    user._delete()


def test__UserBase__difference_update_presence():
    """
    Tests whether ``Userbase._difference_update_presence`` works as intended.
    """
    user = UserBase()
    
    data = {}
    
    output = user._difference_update_presence(data)
    
    vampytest.assert_eq(output, {})


def test__UserBase__update_presence():
    """
    Tests whether ``Userbase._update_presence`` works as intended.
    """
    user = UserBase()
    
    data = {}
    
    user._update_presence(data)


def test__UserBase__from_data_and_update_profile():
    """
    Tests whether ``Userbase._from_data_and_update_profile`` works as intended.
    """
    guild_id = 2023020400020
    guild = Guild.precreate(guild_id)
    
    data = {}
    
    with vampytest.assert_raises(NotImplementedError):
        UserBase._from_data_and_update_profile(data, guild)


def test__UserBase__from_data_and_difference_update_profile():
    """
    Tests whether ``Userbase._from_data_and_difference_update_profile`` works as intended.
    """
    guild_id = 2023020400021
    guild = Guild.precreate(guild_id)
    
    data = {}
    
    with vampytest.assert_raises(NotImplementedError):
        UserBase._from_data_and_difference_update_profile(data, guild)


def test__UserBase__update_profile():
    """
    Tests whether ``Userbase._update_profile`` works as intended.
    """
    user = UserBase()
    guild_id = 202312060000
    guild = Guild.precreate(guild_id)
    
    data = {}
    
    with vampytest.assert_raises(NotImplementedError):
        user._update_profile(data, guild)


def test__UserBase__difference_update_profile():
    """
    Tests whether ``Userbase._difference_update_profile`` works as intended.
    """
    user = UserBase()
    guild_id = 202312060001
    guild = Guild.precreate(guild_id)
    
    data = {}
    
    with vampytest.assert_raises(NotImplementedError):
        user._difference_update_profile(data, guild)


def test__UserBase__get_status_by_platform():
    """
    Tests whether ``UserBase.get_status_by_platform`` works as intended.
    """
    user = UserBase()
    
    output = user.get_status_by_platform('')
    
    vampytest.assert_instance(output, Status)
    vampytest.assert_is(output, Status.offline)
