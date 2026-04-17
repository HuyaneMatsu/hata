import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji
from ....guild import Guild, GuildBadge
from ....localization import Locale
from ....message import Message
from ....role import Role

from ...avatar_decoration import AvatarDecoration
from ...name_plate import NamePlate
from ...status_by_platform import SessionPlatformType, Status, StatusByPlatform

from ..flags import UserFlag
from ..preinstanced import DefaultAvatar, PremiumType
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
    vampytest.assert_instance(user.bot, bool)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.display_name, str, nullable = True)
    vampytest.assert_instance(user.email, str, nullable = True)
    vampytest.assert_instance(user.email_verified, bool)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.guild_profiles, dict)
    vampytest.assert_instance(user.locale, Locale)
    vampytest.assert_instance(user.mfa_enabled, bool)
    vampytest.assert_instance(user.name_plate, NamePlate, nullable = True)
    vampytest.assert_instance(user.premium_type, PremiumType)
    vampytest.assert_instance(user.primary_guild_badge, GuildBadge, nullable = True)
    vampytest.assert_instance(user.status, Status)
    vampytest.assert_instance(user.status_by_platform, StatusByPlatform, nullable = True)
    vampytest.assert_instance(user.thread_profiles, dict, nullable = True)


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
    vampytest.assert_instance(output, SessionPlatformType)
    vampytest.assert_is(output, SessionPlatformType.none)


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


def test__UserBase__can_use_emoji__unicode():
    """
    Tests whether ``Userbase.can_use_emoji`` works as intended.
    
    Case: unicode.
    """
    emoji = BUILTIN_EMOJIS['heart']
    
    user = UserBase()
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__UserBase__can_use_emoji__custom():
    """
    Tests whether ``Userbase.can_use_emoji`` works as intended.
    
    Case: custom.
    """
    emoji = Emoji.precreate(202510010020)
    
    user = UserBase()
    
    output = user.can_use_emoji(emoji)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


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
    
    output = user.get_status_by_platform(SessionPlatformType.desktop)
    
    vampytest.assert_instance(output, Status)
    vampytest.assert_is(output, Status.offline)


def _iter_options__avatar_decoration_url():
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__avatar_decoration_url()).returning_last())
def test__UserBase__avatar_decoration_url(avatar_decoration):
    """
    Tests whether ``UserBase.avatar_decoration_url`` work as intended.
    
    Parameters
    ----------
    avatar_decoration : ``None | AvatarDecoration``
        Avatar decoration to create the user with.
    
    Returns
    -------
    has_avatar_decoration_url : `bool`
    """
    assert avatar_decoration is None
    user = UserBase()
    output = user.avatar_decoration_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__avatar_decoration_url_as():
    yield None, {'ext': 'jpg', 'size': 128}, False


@vampytest._(vampytest.call_from(_iter_options__avatar_decoration_url_as()).returning_last())
def test__UserBase__avatar_decoration_url_as(avatar_decoration, keyword_parameters):
    """
    Tests whether ``UserBase.avatar_decoration_url_as`` work as intended.
    
    Parameters
    ----------
    avatar_decoration : ``None | AvatarDecoration``
        Avatar decoration to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Keyword parameters to use.
    
    Returns
    -------
    has_avatar_decoration_url : `bool`
    """
    assert avatar_decoration is None
    user = UserBase()
    output = user.avatar_decoration_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__default_avatar_url():
    yield 202506010038 << 22, 0, True
    yield 202506010039 << 22, 0, True
    yield 202506010040 << 22, 0, True
    yield 202506010041 << 22, 0, True
    yield 202506010042 << 22, 0, True
    yield 202506010043 << 22, 0, True


@vampytest._(vampytest.call_from(_iter_options__default_avatar_url()).returning_last())
def test__UserBase__default_avatar_url(user_id, discriminator):
    """
    Tests whether ``Userbase.default_avatar_url`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create user with.
    
    discriminator : `int`
        Discriminator to create user with.
    
    Returns
    -------
    has_default_avatar_url : `int`
    """
    assert discriminator == 0
    
    user = UserBase()
    user.id = user_id
    
    output = user.default_avatar_url
    vampytest.assert_instance(output, str)
    return True


def _iter_options__default_avatar():
    yield 202506010044 << 22, 0, DefaultAvatar.blue
    yield 202506010045 << 22, 0, DefaultAvatar.gray
    yield 202506010046 << 22, 0, DefaultAvatar.green
    yield 202506010047 << 22, 0, DefaultAvatar.orange
    yield 202506010048 << 22, 0, DefaultAvatar.red
    yield 202506010049 << 22, 0, DefaultAvatar.pink


@vampytest._(vampytest.call_from(_iter_options__default_avatar()).returning_last())
def test__UserBase__default_avatar(user_id, discriminator):
    """
    Tests whether ``Userbase.default_avatar`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create user with.
    
    discriminator : `int`
        Discriminator to create user with.
    
    Returns
    -------
    default_avatar : ``DefaultAvatar``
    """
    assert discriminator == 0
    
    user = UserBase()
    user.id = user_id
    
    output = user.default_avatar
    vampytest.assert_instance(output, DefaultAvatar)
    return output


def _iter_options__avatar_url():
    yield 202506010064, None, True
    yield 202506010065, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__avatar_url()).returning_last())
def test__UserBase__avatar_url(user_id, icon):
    """
    Tests whether ``UserBase.avatar_url`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_avatar_url : `bool`
    """
    user = UserBase(
        avatar = icon,
    )
    user.id = user_id
    
    output = user.avatar_url
    vampytest.assert_instance(output, str)
    return True


def _iter_options__avatar_url_as():
    yield 202506010062, None, {'ext': 'webp', 'size': 128}, True
    yield 202506010063, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__avatar_url_as()).returning_last())
def test__UserBase__avatar_url_as(user_id, icon, keyword_parameters):
    """
    Tests whether ``UserBase.avatar_url_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_avatar_url : `bool`
    """
    user = UserBase(
        avatar = icon,
    )
    user.id = user_id
    
    output = user.avatar_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str)
    return True


def _iter_options__avatar_url_for():
    yield 202506020000, 0, None, False


@vampytest._(vampytest.call_from(_iter_options__avatar_url_for()).returning_last())
def test__UserBase__avatar_url_for(user_id, guild_id, icon):
    """
    Tests whether ``UserBase.avatar_url_for`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    guild_id : `int`
        Guild identifier to add guild profile for.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_avatar_url_for : `bool`
    """
    assert guild_id == 0
    assert icon is None
    
    user = UserBase()
    user.id = user_id
    
    output = user.avatar_url_for(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__avatar_url_for_as():
    yield 202506020001, 0, None, {'ext': 'webp', 'size': 128}, False


@vampytest._(vampytest.call_from(_iter_options__avatar_url_for_as()).returning_last())
def test__UserBase__avatar_url_for_as(user_id, guild_id, icon, keyword_parameters):
    """
    Tests whether ``UserBase.avatar_url_for_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    guild_id : `int`
        Guild identifier to add guild profile for.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_avatar_url_for : `bool`
    """
    assert guild_id == 0
    assert icon is None
    
    user = UserBase()
    user.id = user_id
    
    output = user.avatar_url_for_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__avatar_url_at():
    yield 202506020003, None, 0, None, True
    yield 202506020004, Icon(IconType.animated, 3), 0, None, True


@vampytest._(vampytest.call_from(_iter_options__avatar_url_at()).returning_last())
def test__UserBase__avatar_url_at(user_id, global_icon, guild_id, local_icon):
    """
    Tests whether ``UserBase.avatar_url_at`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    global_icon : ``None | Icon``
        Icon to create the user with.
    
    guild_id : `int`
        Guild identifier to add guild profile at.
    
    local_icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_avatar_url_at : `bool`
    """
    assert guild_id == 0
    assert local_icon is None
    
    user = UserBase(
        avatar = global_icon
    )
    user.id = user_id
    
    output = user.avatar_url_at(guild_id)
    vampytest.assert_instance(output, str)
    return True


def _iter_options__avatar_url_at_as():
    yield 202506020005, None, 0, None, {'ext': 'webp', 'size': 128}, True
    yield 202506020006, Icon(IconType.animated, 3), 0, None, {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__avatar_url_at_as()).returning_last())
def test__UserBase__avatar_url_at_as(user_id, global_icon, guild_id, local_icon, keyword_parameters):
    """
    Tests whether ``UserBase.avatar_url_at_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    global_icon : ``None | Icon``
        Icon to create the user with.
    
    guild_id : `int`
        Guild identifier to add guild profile at.
    
    local_icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_avatar_url_at : `bool`
    """
    assert guild_id == 0
    assert local_icon is None
    
    user = UserBase(
        avatar = global_icon
    )
    user.id = user_id
    
    output = user.avatar_url_at_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str)
    return True


def _iter_options__banner_url():
    yield 202506020057, None, False


@vampytest._(vampytest.call_from(_iter_options__banner_url()).returning_last())
def test__UserBase__banner_url(user_id, icon):
    """
    Tests whether ``UserBase.banner_url`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_banner_url : `bool`
    """
    assert icon is None
    
    user = UserBase()
    user.id = user_id
    
    output = user.banner_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_as():
    yield 202506020059, None, {'ext': 'webp', 'size': 128}, False


@vampytest._(vampytest.call_from(_iter_options__banner_url_as()).returning_last())
def test__UserBase__banner_url_as(user_id, icon, keyword_parameters):
    """
    Tests whether ``UserBase.banner_url_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_banner_url : `bool`
    """
    assert icon is None
    
    user = UserBase()
    user.id = user_id
    
    output = user.banner_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_for():
    yield 202506020061, 0, None, False


@vampytest._(vampytest.call_from(_iter_options__banner_url_for()).returning_last())
def test__UserBase__banner_url_for(user_id, guild_id, icon):
    """
    Tests whether ``UserBase.banner_url_for`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    guild_id : `int`
        Guild identifier to add guild profile for.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_banner_url_for : `bool`
    """
    assert guild_id == 0
    assert icon is None
    
    user = UserBase()
    user.id = user_id
    
    output = user.banner_url_for(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_for_as():
    yield 202506020062, 0, None, {'ext': 'webp', 'size': 128}, False


@vampytest._(vampytest.call_from(_iter_options__banner_url_for_as()).returning_last())
def test__UserBase__banner_url_for_as(user_id, guild_id, icon, keyword_parameters):
    """
    Tests whether ``UserBase.banner_url_for_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    guild_id : `int`
        Guild identifier to add guild profile for.
    
    icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_banner_url_for : `bool`
    """
    assert guild_id == 0
    assert icon is None
    
    user = UserBase()
    user.id = user_id
    
    output = user.banner_url_for_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_at():
    yield 202506020063, None, 0, None, False


@vampytest._(vampytest.call_from(_iter_options__banner_url_at()).returning_last())
def test__UserBase__banner_url_at(user_id, global_icon, guild_id, local_icon):
    """
    Tests whether ``UserBase.banner_url_at`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    global_icon : ``None | Icon``
        Icon to create the user with.
    
    guild_id : `int`
        Guild identifier to add guild profile at.
    
    local_icon : ``None | Icon``
        Icon to create the user with.
    
    Returns
    -------
    has_banner_url_at : `bool`
    """
    assert guild_id == 0
    assert local_icon is None
    assert global_icon is None
    
    user = UserBase()
    user.id = user_id
    
    output = user.banner_url_at(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_at_as():
    yield 202506020064, None, 0, None, {'ext': 'webp', 'size': 128}, False


@vampytest._(vampytest.call_from(_iter_options__banner_url_at_as()).returning_last())
def test__UserBase__banner_url_at_as(user_id, global_icon, guild_id, local_icon, keyword_parameters):
    """
    Tests whether ``UserBase.banner_url_at_as`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        Identifier to create user with.
    
    global_icon : ``None | Icon``
        Icon to create the user with.
    
    guild_id : `int`
        Guild identifier to add guild profile at.
    
    local_icon : ``None | Icon``
        Icon to create the user with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_banner_url_at : `bool`
    """
    assert guild_id == 0
    assert local_icon is None
    assert global_icon is None
    
    user = UserBase()
    user.id = user_id
    
    output = user.banner_url_at_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__name_plate_url():
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__name_plate_url()).returning_last())
def test__UserBase__name_plate_url(name_plate):
    """
    Tests whether ``UserBase.name_plate_url`` work as intended.
    
    Parameters
    ----------
    name_plate : ``None | NamePlate``
        Avatar decoration to create the user with.
    
    Returns
    -------
    has_name_plate_url : `bool`
    """
    assert name_plate is None
    user = UserBase()
    output = user.name_plate_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
