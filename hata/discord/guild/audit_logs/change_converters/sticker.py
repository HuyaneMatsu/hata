__all__ = ()

from ....sticker import StickerFormat

from ..audit_log_change import AuditLogChange

from .shared import _convert_preinstanced, convert_nothing, convert_snowflake


def convert_format(name, data):
    return _convert_preinstanced('format', data, StickerFormat)


def convert_tags(name, data):
    before = data.get('old_value', None)
    if (before is None) or (not before):
        before = None
    else:
        before = frozenset(before.split(', '))
    
    after = data.get('new_value', None)
    if (after is None) or (not after):
        after = None
    else:
        after = frozenset(after.split(', '))
    
    return AuditLogChange('tags', before, after)


STICKER_CONVERTERS = {
    'available': convert_nothing,
    'description': convert_nothing,
    'format_type': convert_format,
    'guild_id': convert_snowflake,
    'name': convert_nothing,
    'tags': convert_tags,
}
