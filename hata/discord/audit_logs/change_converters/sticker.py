__all__ = ()

from ...sticker import StickerFormat, StickerType

from ..audit_log_change import AuditLogChange

from .shared import _convert_preinstanced, convert_deprecated, convert_nothing, convert_snowflake


def convert_sticker_format(name, data):
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


def convert_sticker_type(name, data):
    return _convert_preinstanced('type', data, StickerType)


STICKER_CONVERTERS = {
    'asset': convert_deprecated,
    'available': convert_nothing,
    'description': convert_nothing,
    'format_type': convert_sticker_format,
    'guild_id': convert_snowflake,
    'id': convert_snowflake,
    'name': convert_nothing,
    'tags': convert_tags,
    'type': convert_sticker_type,
}
