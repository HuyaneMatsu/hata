import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....localization import Locale
from ....guild import GuildBadge
from ....user import AvatarDecoration, PremiumType, UserFlag

from ...oauth2_access import Oauth2Access

from ..oauth2_user import Oauth2User


def _assert_fields_set(user):
    """
    Asserts whether every fields of the given user are set.
    
    Parameters
    ----------
    user : ``User``
        The user to check.
    """
    vampytest.assert_instance(user, Oauth2User)
    vampytest.assert_instance(user.access, Oauth2Access)
    vampytest.assert_instance(user.avatar, Icon)
    vampytest.assert_instance(user.avatar_decoration, AvatarDecoration, nullable = True)
    vampytest.assert_instance(user.banner, Icon)
    vampytest.assert_instance(user.banner_color, Color, nullable = True)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.display_name, str, nullable = True)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.id, int)
    vampytest.assert_instance(user.name, str)
    vampytest.assert_instance(user.primary_guild_badge, GuildBadge, nullable = True)
    vampytest.assert_instance(user.email, str, nullable = True)
    vampytest.assert_instance(user.email_verified, bool)
    vampytest.assert_instance(user.locale, Locale)
    vampytest.assert_instance(user.mfa_enabled, bool)
    vampytest.assert_instance(user.premium_type, PremiumType)


def test__Oauth2User__new__no_fields():
    """
    Tests whether ``Oauth2User.__new__`` works as intended.
    
    Case: No fields given.
    """
    user = Oauth2User()
    _assert_fields_set(user)


def test__Oauth2User__new__all_fields():
    """
    Tests whether ``Oauth2User.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160038)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    primary_guild_badge = GuildBadge(guild_id = 202405180015, tag = 'miau')
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
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.primary_guild_badge, primary_guild_badge)
    vampytest.assert_eq(user.email, email)
    vampytest.assert_eq(user.email_verified, email_verified)
    vampytest.assert_is(user.locale, locale)
    vampytest.assert_eq(user.mfa_enabled, mfa_enabled)
    vampytest.assert_is(user.premium_type, premium_type)


def test__Oauth2User__create_empty():
    """
    Tests whether ``Oauth2User._create_empty`` works as intended.
    """
    user_id = 202302040022
    user = Oauth2User._create_empty(user_id)
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.id, user_id)
