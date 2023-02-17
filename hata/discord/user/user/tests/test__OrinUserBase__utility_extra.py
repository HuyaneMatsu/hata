import vampytest

from ....bases import Icon, IconType
from ....utils import is_url

from ..orin_user_base import OrinUserBase


def test__OrinUserBase__banner_url():
    """
    Tests whether ``OrinUserBase.banner_url`` work as intended.
    """
    banner = Icon(IconType.static, 23)
    
    user = OrinUserBase(
        banner = banner,
    )
    
    banner_url = user.banner_url
    
    vampytest.assert_instance(banner_url, str)
    vampytest.assert_true(is_url(banner_url))


def test__OrinUserBase__banner_url_as():
    """
    Tests whether ``OrinUserBase.banner_url_as`` work as intended.
    """
    banner = Icon(IconType.static, 23)
    
    user = OrinUserBase(
        banner = banner,
    )
    
    banner_url = user.banner_url_as(ext = 'jpg', size = 4096)
    
    vampytest.assert_instance(banner_url, str)
    if (banner_url is not None):
        vampytest.assert_true(is_url(banner_url))


def test__OrinUserBase__avatar_decoration_url():
    """
    Tests whether ``OrinUserBase.avatar_decoration_url`` work as intended.
    """
    avatar_decoration = Icon(IconType.static, 23)
    
    user = OrinUserBase(
        avatar_decoration = avatar_decoration,
    )
    
    avatar_decoration_url = user.avatar_decoration_url
    
    vampytest.assert_instance(avatar_decoration_url, str)
    vampytest.assert_true(is_url(avatar_decoration_url))


def test__OrinUserBase__avatar_decoration_url_as():
    """
    Tests whether ``OrinUserBase.avatar_decoration_url_as`` work as intended.
    """
    avatar_decoration = Icon(IconType.static, 23)
    
    user = OrinUserBase(
        avatar_decoration = avatar_decoration,
    )
    
    avatar_decoration_url = user.avatar_decoration_url_as(ext = 'png', size = 4096)
    
    vampytest.assert_instance(avatar_decoration_url, str)
    vampytest.assert_true(is_url(avatar_decoration_url))
