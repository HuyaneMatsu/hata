import vampytest

from ....bases import Icon, IconType

from ...avatar_decoration import AvatarDecoration
from ...name_plate import NamePlate

from ..orin_user_base import OrinUserBase
from ..preinstanced import DefaultAvatar


def _iter_options__avatar_decoration_url():
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160097)
    
    yield None, False
    yield avatar_decoration, True


@vampytest._(vampytest.call_from(_iter_options__avatar_decoration_url()).returning_last())
def test__OrinUserBase__avatar_decoration_url(avatar_decoration):
    """
    Tests whether ``OrinUserBase.avatar_decoration_url`` work as intended.
    
    Parameters
    ----------
    avatar_decoration : ``None | AvatarDecoration``
        Avatar decoration to create the user with.
    
    Returns
    -------
    has_avatar_decoration_url : `bool`
    """
    user = OrinUserBase(avatar_decoration = avatar_decoration)
    output = user.avatar_decoration_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__avatar_decoration_url_as():
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160098)
    
    yield None, {'ext': 'jpg', 'size': 128}, False
    yield avatar_decoration, {'ext': 'jpg', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__avatar_decoration_url_as()).returning_last())
def test__OrinUserBase__avatar_decoration_url_as(avatar_decoration, keyword_parameters):
    """
    Tests whether ``OrinUserBase.avatar_decoration_url_as`` work as intended.
    
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
    user = OrinUserBase(avatar_decoration = avatar_decoration)
    output = user.avatar_decoration_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__default_avatar_url():
    yield 202506010050 << 22, 0, True
    yield 202506010051 << 22, 0, True
    yield 202506010052 << 22, 0, True
    yield 202506010053 << 22, 0, True
    yield 202506010054 << 22, 0, True
    yield 202506010055 << 22, 0, True
    
    yield 202506010100 << 22, 6, True
    yield 202506010101 << 22, 1, True
    yield 202506010102 << 22, 2, True
    yield 202506010103 << 22, 3, True
    yield 202506010104 << 22, 4, True
    yield 202506010105 << 22, 5, True


@vampytest._(vampytest.call_from(_iter_options__default_avatar_url()).returning_last())
def test__OrinUserBase__default_avatar_url(user_id, discriminator):
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
    user = OrinUserBase(discriminator = discriminator)
    user.id = user_id
    
    output = user.default_avatar_url
    vampytest.assert_instance(output, str)
    return True


def _iter_options__default_avatar():
    yield 202506010056 << 22, 0, DefaultAvatar.blue
    yield 202506010057 << 22, 0, DefaultAvatar.gray
    yield 202506010058 << 22, 0, DefaultAvatar.green
    yield 202506010059 << 22, 0, DefaultAvatar.orange
    yield 202506010060 << 22, 0, DefaultAvatar.red
    yield 202506010061 << 22, 0, DefaultAvatar.pink
    
    yield 202506010106 << 22, 6, DefaultAvatar.blue
    yield 202506010107 << 22, 1, DefaultAvatar.gray
    yield 202506010108 << 22, 2, DefaultAvatar.green
    yield 202506010109 << 22, 3, DefaultAvatar.orange
    yield 202506010110 << 22, 4, DefaultAvatar.red
    yield 202506010111 << 22, 5, DefaultAvatar.pink


@vampytest._(vampytest.call_from(_iter_options__default_avatar()).returning_last())
def test__OrinUserBase__default_avatar(user_id, discriminator):
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
    user = OrinUserBase(discriminator = discriminator)
    user.id = user_id
    
    output = user.default_avatar
    vampytest.assert_instance(output, DefaultAvatar)
    return output


def _iter_options__banner_url():
    yield 202506020047, None, False
    yield 202506020048, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__banner_url()).returning_last())
def test__OrinUserBase__banner_url(user_id, icon):
    """
    Tests whether ``OrinUserBase.banner_url`` works as intended.
    
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
    user = OrinUserBase(
        banner = icon,
    )
    user.id = user_id
    
    output = user.banner_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_as():
    yield 202506020049, None, {'ext': 'webp', 'size': 128}, False
    yield 202506020050, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__banner_url_as()).returning_last())
def test__OrinUserBase__banner_url_as(user_id, icon, keyword_parameters):
    """
    Tests whether ``OrinUserBase.banner_url_as`` works as intended.
    
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
    user = OrinUserBase(
        banner = icon,
    )
    user.id = user_id
    
    output = user.banner_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_for():
    yield 202506020051, 0, None, False


@vampytest._(vampytest.call_from(_iter_options__banner_url_for()).returning_last())
def test__OrinUserBase__banner_url_for(user_id, guild_id, icon):
    """
    Tests whether ``OrinUserBase.banner_url_for`` works as intended.
    
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
    
    user = OrinUserBase()
    user.id = user_id
    
    output = user.banner_url_for(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_for_as():
    yield 202506020052, 0, None, {'ext': 'webp', 'size': 128}, False


@vampytest._(vampytest.call_from(_iter_options__banner_url_for_as()).returning_last())
def test__OrinUserBase__banner_url_for_as(user_id, guild_id, icon, keyword_parameters):
    """
    Tests whether ``OrinUserBase.banner_url_for_as`` works as intended.
    
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
    
    user = OrinUserBase()
    user.id = user_id
    
    output = user.banner_url_for_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_at():
    yield 202506020053, None, 0, None, False
    yield 202506020054, Icon(IconType.animated, 3), 0, None, True


@vampytest._(vampytest.call_from(_iter_options__banner_url_at()).returning_last())
def test__OrinUserBase__banner_url_at(user_id, global_icon, guild_id, local_icon):
    """
    Tests whether ``OrinUserBase.banner_url_at`` works as intended.
    
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
    
    user = OrinUserBase(
        banner = global_icon
    )
    user.id = user_id
    
    output = user.banner_url_at(guild_id)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__banner_url_at_as():
    yield 202506020055, None, 0, None, {'ext': 'webp', 'size': 128}, False
    yield 202506020056, Icon(IconType.animated, 3), 0, None, {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__banner_url_at_as()).returning_last())
def test__OrinUserBase__banner_url_at_as(user_id, global_icon, guild_id, local_icon, keyword_parameters):
    """
    Tests whether ``OrinUserBase.banner_url_at_as`` works as intended.
    
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
    
    user = OrinUserBase(
        banner = global_icon
    )
    user.id = user_id
    
    output = user.banner_url_at_as(guild_id, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__name_plate_url():
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030015,
    )
    
    yield None, False
    yield name_plate, True


@vampytest._(vampytest.call_from(_iter_options__name_plate_url()).returning_last())
def test__OrinUserBase__name_plate_url(name_plate):
    """
    Tests whether ``OrinUserBase.name_plate_url`` work as intended.
    
    Parameters
    ----------
    name_plate : ``None | NamePlate``
        Avatar decoration to create the user with.
    
    Returns
    -------
    has_name_plate_url : `bool`
    """
    user = OrinUserBase(
        name_plate = name_plate,
    )
    output = user.name_plate_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
