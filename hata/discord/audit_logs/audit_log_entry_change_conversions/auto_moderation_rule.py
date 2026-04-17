__all__ = ()

from ...auto_moderation import (
    AutoModerationAction, AutoModerationEventType, AutoModerationRuleTriggerMetadataBase, AutoModerationRuleTriggerType
)
from ...auto_moderation.rule.fields import (
    validate_actions, validate_creator_id, validate_enabled, validate_event_type, validate_excluded_channel_ids,
    validate_excluded_role_ids, validate_name, validate_trigger_type
)
from ...auto_moderation.trigger_metadata.constants import AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
from ...auto_moderation.trigger_metadata.fields import (
    validate_excluded_keywords, validate_keywords, validate_mention_limit, validate_raid_protection,
    validate_regex_patterns
)
from ...auto_moderation.trigger_metadata.utils import try_get_auto_moderation_trigger_metadata_type_from_data

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..audit_log_entry_change_conversion.change_deserializers import change_deserializer_addition_and_removal
from ..audit_log_entry_change_conversion.change_serializers import change_serializer_addition_and_removal
from ..audit_log_entry_change_conversion.value_mergers import value_merger_sorted_array
from ..conversion_helpers.converters import (
    value_deserializer_id, value_deserializer_ids, value_deserializer_name, value_deserializer_string_array,
    value_serializer_id, value_serializer_ids, value_serializer_name, value_serializer_string_array
)


# ---- action ----

ACTIONS_CONVERSION = AuditLogEntryChangeConversion(
    ('actions',),
    'actions',
    value_validator = validate_actions,
)


@ACTIONS_CONVERSION.set_value_deserializer
def actions_value_deserializer(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*(AutoModerationAction.from_data(data) for data in value),)
    return value


@ACTIONS_CONVERSION.set_value_serializer
def actions_value_serializer(value):
    if value is None:
        value = []
    else:
        value = [action.to_data(defaults = True) for action in value]
    return value


# ---- creator_id ----

CREATOR_ID_CONVERSION = AuditLogEntryChangeConversion(
    ('creator_id',),
    'creator_id',
    value_deserializer = value_deserializer_id,
    value_serializer = value_serializer_id,
    value_validator = validate_creator_id,
)


# ---- enabled ----

ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    ('enabled',),
    'enabled',
    value_validator = validate_enabled,
)


@ENABLED_CONVERSION.set_value_deserializer
def enabled_value_deserializer(value):
    if value is None:
        value = True
    return value


# ---- excluded_keywords ----

EXCLUDED_KEYWORDS_CONVERSION = AuditLogEntryChangeConversion(
    ('$remove_allow_list', '$add_allow_list'),
    'excluded_keywords',
    change_deserializer = change_deserializer_addition_and_removal,
    change_serializer = change_serializer_addition_and_removal,
    value_merger = value_merger_sorted_array,
    value_deserializer = value_deserializer_string_array,
    value_serializer = value_serializer_string_array,
    value_validator = validate_excluded_keywords,
)

# ---- event_type ----

EVENT_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('event_type',),
    'event_type',
    value_validator = validate_event_type,
)


@EVENT_TYPE_CONVERSION.set_value_deserializer
def event_type_value_deserializer(value):
    return AutoModerationEventType(value)


@EVENT_TYPE_CONVERSION.set_value_serializer
def event_type_value_serializer(value):
    return value.value


# ---- excluded_channel_ids ----

EXCLUDED_CHANNEL_IDS_CONVERSION = AuditLogEntryChangeConversion(
    ('exempt_channels',),
    'excluded_channel_ids',
    value_deserializer = value_deserializer_ids,
    value_serializer = value_serializer_ids,
    value_validator = validate_excluded_channel_ids,
)


# ---- excluded_role_ids ----

EXCLUDED_ROLE_IDS_CONVERSION = AuditLogEntryChangeConversion(
    ('exempt_roles',),
    'excluded_role_ids',
    value_deserializer = value_deserializer_ids,
    value_serializer = value_serializer_ids,
    value_validator = validate_excluded_role_ids,
)


# ---- keywords ---

KEYWORDS_CONVERSION = AuditLogEntryChangeConversion(
    ('$remove_keyword_filter', '$add_keyword_filter'),
    'keywords',
    change_deserializer = change_deserializer_addition_and_removal,
    change_serializer = change_serializer_addition_and_removal,
    value_merger = value_merger_sorted_array,
    value_deserializer = value_deserializer_string_array,
    value_serializer = value_serializer_string_array,
    value_validator = validate_keywords,
)

# ---- mention_limit ----

MENTION_LIMIT_CONVERSION = AuditLogEntryChangeConversion(
    ('mention_total_limit',),
    'mention_limit',
    value_validator = validate_mention_limit,
)


@MENTION_LIMIT_CONVERSION.set_value_deserializer
def mention_limit_value_deserializer(value):
    if value is None:
        value = AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('name',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- raid_protection ----

RAID_PROTECTION_CONVERSION = AuditLogEntryChangeConversion(
    ('mention_raid_protection_enabled',),
    'raid_protection',
    value_validator = validate_raid_protection,
)


@RAID_PROTECTION_CONVERSION.set_value_deserializer
def raid_protection_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- regex_patterns ---

REGEX_PATTERNS_CONVERSION = AuditLogEntryChangeConversion(
    ('$remove_regex_patterns', '$add_regex_patterns'),
    'regex_patterns',
    change_deserializer = change_deserializer_addition_and_removal,
    change_serializer = change_serializer_addition_and_removal,
    value_merger = value_merger_sorted_array,
    value_deserializer = value_deserializer_string_array,
    value_serializer = value_serializer_string_array,
    value_validator = validate_regex_patterns,
)


# ---- trigger_metadata ----

TRIGGER_METADATA_CONVERSION = AuditLogEntryChangeConversion(
    ('trigger_metadata',),
    'trigger_metadata',
)

@TRIGGER_METADATA_CONVERSION.set_value_deserializer
def trigger_metadata_value_deserializer(value):
    if value is not None:
        metadata_type = try_get_auto_moderation_trigger_metadata_type_from_data(value)
        if metadata_type is None:
            value = None
        else:
            value = metadata_type.from_data(value)
    
    return value


@TRIGGER_METADATA_CONVERSION.set_value_serializer
def trigger_metadata_value_serializer(value):
    if value is not None:
        value = value.to_data(defaults = True)
    return value


@TRIGGER_METADATA_CONVERSION.set_value_validator
def trigger_metadata_value_validator(value):
    if value is None or isinstance(value, AutoModerationRuleTriggerMetadataBase):
        return value
    
    raise TypeError(
        f'`trigger_metadata` can be `None`, `{AutoModerationRuleTriggerMetadataBase.__name__}`, '
        f'got {type(value).__name__}; {value!r}.'
    )


# ---- trigger_type ----

TRIGGER_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('trigger_type',),
    'trigger_type',
    value_validator = validate_trigger_type,
)


@TRIGGER_TYPE_CONVERSION.set_value_deserializer
def trigger_type_value_deserializer(value):
    return AutoModerationRuleTriggerType(value)


@TRIGGER_TYPE_CONVERSION.set_value_serializer
def trigger_type_value_serializer(value):
    return value.value


# ---- Construct ----

AUTO_MODERATION_RULE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    ACTIONS_CONVERSION,
    CREATOR_ID_CONVERSION,
    ENABLED_CONVERSION,
    EXCLUDED_KEYWORDS_CONVERSION,
    EVENT_TYPE_CONVERSION,
    EXCLUDED_CHANNEL_IDS_CONVERSION,
    EXCLUDED_ROLE_IDS_CONVERSION,
    KEYWORDS_CONVERSION,
    MENTION_LIMIT_CONVERSION,
    NAME_CONVERSION,
    RAID_PROTECTION_CONVERSION,
    REGEX_PATTERNS_CONVERSION,
    TRIGGER_METADATA_CONVERSION,
    TRIGGER_TYPE_CONVERSION,
)
