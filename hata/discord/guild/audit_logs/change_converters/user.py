__all__ = ()

from ..audit_log_change import AuditLogChange
from ..audit_log_role import AuditLogRole

from .shared import convert_icon, convert_nothing, convert_timestamp


def convert_roles(name, data):
    roles = tuple(AuditLogRole(role_data) for role_data in data['new_value'])
    
    if name == '$add':
        before = None
        after = roles
    else:
        before = roles
        after = None
    
    return AuditLogChange('roles', before, after)


def convert_timestamp__timed_out_until(name, data):
    return convert_timestamp('timed_out_until', data)


USER_CONVERTERS = {
    '$add': convert_roles,
    '$remove': convert_roles,
    'avatar_hash': convert_icon,
    'communication_disabled_until': convert_timestamp__timed_out_until,
    'deaf': convert_nothing,
    'mute': convert_nothing,
    'nick': convert_nothing,
    'pending': convert_nothing,
}
