import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....permission import Permission

from ...role_color_configuration import RoleColorConfiguration
from ...role_manager_metadata import RoleManagerMetadataBot

from ..flags import RoleFlag
from ..role import Role
from ..preinstanced import RoleManagerType


def test__Role__hash():
    """
    Tests whether ``Role.__hash__`` works as intended.
    """
    role_id = 202211040016
    
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(333),
        color_secondary = Color(334),
        color_tertiary = Color(335),
    )
    flags = RoleFlag(12)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBot(bot_id = 202211040017)
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    keyword_parameters = {
        'color': color,
        'color_configuration': color_configuration,
        'flags': flags,
        'icon': icon,
        'manager': (manager_type, manager_metadata),
        'mentionable': mentionable,
        'name': name,
        'permissions': permissions,
        'position': position,
        'separated': separated,
        'unicode_emoji': unicode_emoji,
    }
    
    role = Role(**keyword_parameters)
    vampytest.assert_instance(hash(role), int)
    
    role = Role.precreate(role_id, **keyword_parameters)
    vampytest.assert_instance(hash(role), int)


def test__Role__repr():
    """
    Tests whether ``Role.__repr__`` works as intended.
    """
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(333),
        color_secondary = Color(334),
        color_tertiary = Color(335),
    )
    flags = RoleFlag(12)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBot(bot_id = 202211040019)
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    role = Role(
        color = color,
        color_configuration = color_configuration,
        flags = flags,
        icon = icon,
        manager = (manager_type, manager_metadata),
        mentionable = mentionable,
        name = name,
        permissions = permissions,
        position = position,
        separated = separated,
        unicode_emoji = unicode_emoji,
    )
    
    vampytest.assert_instance(repr(role), str)


def _iter_options__eq():
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(333),
        color_secondary = Color(334),
        color_tertiary = Color(335),
    )
    flags = RoleFlag(12)
    icon = None
    manager_metadata = RoleManagerMetadataBot(bot_id = 202211040021)
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    keyword_parameters = {
        'color': color,
        'color_configuration': color_configuration,
        'flags': flags,
        'icon': icon,
        'manager': (manager_type, manager_metadata),
        'mentionable': mentionable,
        'name': name,
        'permissions': permissions,
        'position': position,
        'separated': separated,
        'unicode_emoji': unicode_emoji,
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
            'color': Color(666),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'color_configuration': RoleColorConfiguration(
                color_primary = Color(433),
                color_secondary = Color(434),
                color_tertiary = Color(345),
            ),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': RoleFlag(11),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'icon': Icon(IconType.animated, 12),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'manager': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'mentionable': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'alive',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'permissions': Permission(554),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'position': 7,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'separated': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'unicode_emoji': BUILTIN_EMOJIS['heart'],
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Role__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Role.__eq__`` works as intended.
    
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
    role_0 = Role(**keyword_parameters_0)
    role_1 = Role(**keyword_parameters_1)
    
    output = role_0 == role_1
    vampytest.assert_instance(output, bool)
    return output


def test__Role__format():
    """
    Tests whether ``Role.__format__`` works as intended.
    """
    role_id = 202211040022
    
    color = Color(123)
    color_configuration = RoleColorConfiguration(
        color_primary = Color(333),
        color_secondary = Color(334),
        color_tertiary = Color(335),
    )
    flags = RoleFlag(12)
    icon = Icon(IconType.static, 2)
    manager_metadata = RoleManagerMetadataBot(bot_id = 202211040023)
    manager_type = RoleManagerType.bot
    mentionable = True
    name = 'holo'
    permissions = Permission(555)
    position = 6
    separated = True
    unicode_emoji = None
    
    keyword_parameters = {
        'color': color,
        'color_configuration': color_configuration,
        'flags': flags,
        'icon': icon,
        'manager': (manager_type, manager_metadata),
        'mentionable': mentionable,
        'name': name,
        'permissions': permissions,
        'position': position,
        'separated': separated,
        'unicode_emoji': unicode_emoji,
    }
    
    role = Role.precreate(role_id, **keyword_parameters)
    
    vampytest.assert_eq(format(role, ''), role.name)
    vampytest.assert_eq(format(role, 'm'), role.mention)
    vampytest.assert_instance(format(role, 'c'), str)
    
    with vampytest.assert_raises(ValueError):
        format(role, 'owo')


def _iter_options__sort():
    role_0 = Role.precreate(202211040024, position = 6)
    role_1 = Role.precreate(202211040025, position = 12)
    role_2 = Role.precreate(202211040026, position = 6)
    
    yield (
        [role_0, role_1],
        [role_0, role_1],
    )
    
    yield (
        [role_1, role_2],
        [role_2, role_1],
    )
    
    yield (
        [role_2, role_0],
        [role_0, role_2],
    )


@vampytest._(vampytest.call_from(_iter_options__sort()).returning_last())
def test__Role__sort(roles):
    """
    Tests whether ``Role`` sorting works as intended.
    
    Parameters
    ----------
    roles : ``list<Role>>``
        Roles to sort.
    
    Returns
    -------
    output : ``list<Role>``
        The roles sorted.
    """
    return sorted(roles)
