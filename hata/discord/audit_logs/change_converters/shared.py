__all__ = ()

from ...bases import Icon
from ...color import Color
from ...permission import Permission
from ...utils import timestamp_to_datetime

from ..audit_log_change import AuditLogChange


def _convert_preinstanced(name, data, preinstanced_type):
    before = data.get('old_value', None)
    if (before is not None):
        before = preinstanced_type.get(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = preinstanced_type.get(after)
    
    return AuditLogChange(name, before, after)


def convert_color(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = Color(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = Color(after)
    
    return AuditLogChange('color', before, after)


def convert_deprecated(name, data):
    return None


def convert_icon(name, data):
    if name == 'splash_hash':
        name = 'invite_splash'
    elif name.endswith('hash'):
        name = name[:-5]
    
    before = Icon.from_base16_hash(data.get('old_value', None))
    
    after = Icon.from_base16_hash(data.get('new_value', None))
    
    return AuditLogChange(name, before, after)


def convert_nothing(name, data):
    before = data.get('old_value', None)
    after = data.get('new_value', None)
    return AuditLogChange(name, before, after)


def convert_permission(name, data):
    if name.endswith('_new'):
        name = name[:-4]
    
    before = data.get('old_value', None)
    if (before is not None):
        before = Permission(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = Permission(after)
    
    return AuditLogChange(name, before, after)


def convert_snowflake(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        before = int(before)
    
    after = data.get('new_value', None)
    if (after is not None):
        after = int(after)
    
    return AuditLogChange(name, before, after)


def convert_timestamp(name, data):
    before = data.get('old_value', None)
    if (before is None):
        before = None
    else:
        before = timestamp_to_datetime(before)
    
    after = data.get('new_value', None)
    if (after is None):
        after = None
    else:
        after = timestamp_to_datetime(after)
    
    return AuditLogChange(name, before, after)


def convert_snowflake_array(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        if before:
            before = (*(int(sub_value) for sub_value in before),)
        else:
            before = None
    
    after = data.get('new_value', None)
    if (after is not None):
        if after:
            after = (*(int(sub_value) for sub_value in after),)
        else:
            after = None
    
    return AuditLogChange(name, before, after)
