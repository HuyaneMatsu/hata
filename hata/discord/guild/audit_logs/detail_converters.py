__all__ = ()

from ...auto_moderation import AutoModerationRuleTriggerType
from ...channel import PermissionOverwriteTargetType


def detail_converter_channel_id(key, value):
    return 'channel_id', int(value)


def detail_converter_amount(key, value):
    return 'amount', int(value)


def detail_converter_delete_message_days_as_duration(key, value):
    return 'delete_message_duration', int(value) * 24 * 60 * 60


def detail_converter_delete_message_duration(key, value):
    return 'delete_message_duration', int(value)


def detail_converter_users_removed(key, value):
    return 'users_removed', int(value)


def detail_converter_message(key, value):
    return 'message_id', int(value)


def detail_converter_permission_overwrite_target_id(key, value):
    return 'target_id', int(value)


def detail_converter_permission_overwrite_target_type(key, value):
    if PermissionOverwriteTargetType.VALUE_TYPE is int:
        value = int(value)
    
    return 'target_type', PermissionOverwriteTargetType.get(value)


def detail_converter_auto_moderation_rule_trigger_type(key, value):
    return key, AutoModerationRuleTriggerType.get(value)


def detail_converter_nothing(key, value):
    return key, value


DETAIL_CONVERTERS = {
    'auto_moderation_rule_name': detail_converter_nothing,
    'auto_moderation_rule_trigger_type': detail_converter_auto_moderation_rule_trigger_type,
    'channel_id': detail_converter_channel_id,
    'count': detail_converter_amount,
    'delete_message_days': detail_converter_delete_message_days_as_duration,
    'delete_message_seconds': detail_converter_delete_message_duration,
    'id': detail_converter_permission_overwrite_target_id,
    'members_removed': detail_converter_users_removed,
    'message_id': detail_converter_message,
    'role_name': detail_converter_nothing,
    'type': detail_converter_permission_overwrite_target_type,
}
