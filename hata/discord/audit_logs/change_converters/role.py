__all__ = ()

from ....env import API_VERSION

from ...emoji import create_unicode_emoji
from ...role import RoleFlag

from ..audit_log_change import AuditLogChange

from .shared import convert_color, convert_deprecated, convert_icon, convert_nothing, convert_permission


def convert_channel_flags(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = RoleFlag(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = RoleFlag(after)
    
    return AuditLogChange('flags', before, after)


def convert_bool__separated(name, data):
    return convert_nothing('separated', data)


def convert_unicode_emoji(name, data):
    before = data.get('old_value', None)
    if (before is None):
        before = None
    else:
        before = create_unicode_emoji(before)
    
    after = data.get('new_value', None)
    if (after is None):
        after = None
    else:
        after = create_unicode_emoji(after)
    
    return AuditLogChange(name, before, after)


ROLE_CONVERTERS = {
    'color': convert_color,
    'flags': convert_channel_flags,
    'hoist': convert_bool__separated,
    'icon_hash': convert_icon,
    'permissions': convert_deprecated if API_VERSION in (6, 7) else convert_permission,
    'permissions_new': convert_permission if API_VERSION in (6, 7) else convert_deprecated,
    'mentionable': convert_nothing,
    'name': convert_nothing,
    'position': convert_nothing,
    'unicode_emoji': convert_unicode_emoji,
}
