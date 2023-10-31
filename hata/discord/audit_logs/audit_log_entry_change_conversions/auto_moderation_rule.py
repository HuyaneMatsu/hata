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

from ..audit_log_change.flags import FLAG_IS_ADDITION, FLAG_IS_MODIFICATION, FLAG_IS_REMOVAL
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import (
    get_converter_id, get_converter_ids, get_converter_name, get_converter_string_array, put_converter_id,
    put_converter_ids, put_converter_name, put_converter_string_array
)


# ---- action ----

ACTIONS_CONVERSION = AuditLogEntryChangeConversion(
    'actions',
    'actions',
    FLAG_IS_MODIFICATION,
    validator = validate_actions,
)


@ACTIONS_CONVERSION.set_get_converter
def actions_get_converter(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*(AutoModerationAction.from_data(data) for data in value),)
    return value


@ACTIONS_CONVERSION.set_put_converter
def actions_put_converter(value):
    if value is None:
        value = []
    else:
        value = [action.to_data(defaults = True) for action in value]
    return value


# ---- creator_id ----

CREATOR_ID_CONVERSION = AuditLogEntryChangeConversion(
    'creator_id',
    'creator_id',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_id,
    put_converter = put_converter_id,
    validator = validate_creator_id,
)


# ---- enabled ----

ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    'enabled',
    'enabled',
    FLAG_IS_MODIFICATION,
    validator = validate_enabled,
)


@ENABLED_CONVERSION.set_get_converter
def enabled_get_converter(value):
    if value is None:
        value = True
    return value


# ---- excluded_keywords ----

EXCLUDED_KEYWORDS_CONVERSION__ADDITION = AuditLogEntryChangeConversion(
    '$add_allow_list',
    'excluded_keywords',
    FLAG_IS_ADDITION,
    get_converter = get_converter_string_array,
    put_converter = put_converter_string_array,
    validator = validate_excluded_keywords,
)


EXCLUDED_KEYWORDS_CONVERSION__REMOVAL = AuditLogEntryChangeConversion(
    '$remove_allow_list',
    'excluded_keywords',
    FLAG_IS_REMOVAL,
    get_converter = get_converter_string_array,
    put_converter = put_converter_string_array,
    validator = validate_excluded_keywords,
)

# ---- event_type ----

EVENT_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    'event_type',
    'event_type',
    FLAG_IS_MODIFICATION,
    validator = validate_event_type,
)


@EVENT_TYPE_CONVERSION.set_get_converter
def event_type_get_converter(value):
    return AutoModerationEventType.get(value)


@EVENT_TYPE_CONVERSION.set_put_converter
def event_type_put_converter(value):
    return value.value


# ---- excluded_channel_ids ----

EXCLUDED_CHANNEL_IDS_CONVERSION = AuditLogEntryChangeConversion(
    'exempt_channels',
    'excluded_channel_ids',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_ids,
    put_converter = put_converter_ids,
    validator = validate_excluded_channel_ids,
)


# ---- excluded_role_ids ----

EXCLUDED_ROLE_IDS_CONVERSION = AuditLogEntryChangeConversion(
    'exempt_roles',
    'excluded_role_ids',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_ids,
    put_converter = put_converter_ids,
    validator = validate_excluded_role_ids,
)


# ---- keywords ---

KEYWORDS_CONVERSION__ADDITION = AuditLogEntryChangeConversion(
    '$add_keyword_filter',
    'keywords',
    FLAG_IS_ADDITION,
    get_converter = get_converter_string_array,
    put_converter = put_converter_string_array,
    validator = validate_keywords,
)


KEYWORDS_CONVERSION__REMOVAL = AuditLogEntryChangeConversion(
    '$remove_keyword_filter',
    'keywords',
    FLAG_IS_REMOVAL,
    get_converter = get_converter_string_array,
    put_converter = put_converter_string_array,
    validator = validate_keywords,
)

# ---- mention_limit ----

MENTION_LIMIT_CONVERSION = AuditLogEntryChangeConversion(
    'mention_total_limit',
    'mention_limit',
    FLAG_IS_MODIFICATION,
    validator = validate_mention_limit,
)


@MENTION_LIMIT_CONVERSION.set_get_converter
def mention_limit_get_converter(value):
    if value is None:
        value = AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'name',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- raid_protection ----

RAID_PROTECTION_CONVERSION = AuditLogEntryChangeConversion(
    'mention_raid_protection_enabled',
    'raid_protection',
    FLAG_IS_MODIFICATION,
    validator = validate_raid_protection,
)


@RAID_PROTECTION_CONVERSION.set_get_converter
def raid_protection_get_converter(value):
    if value is None:
        value = False
    return value


# ---- regex_patterns ---

REGEX_PATTERNS_CONVERSION__ADDITION = AuditLogEntryChangeConversion(
    '$add_regex_patterns',
    'regex_patterns',
    FLAG_IS_ADDITION,
    get_converter = get_converter_string_array,
    put_converter = put_converter_string_array,
    validator = validate_regex_patterns,
)


REGEX_PATTERNS_CONVERSION__REMOVAL = AuditLogEntryChangeConversion(
    '$remove_regex_patterns',
    'regex_patterns',
    FLAG_IS_REMOVAL,
    get_converter = get_converter_string_array,
    put_converter = put_converter_string_array,
    validator = validate_regex_patterns,
)


# ---- trigger_metadata ----

TRIGGER_METADATA_CONVERSION = AuditLogEntryChangeConversion(
    'trigger_metadata',
    'trigger_metadata',
    FLAG_IS_MODIFICATION,
)

@TRIGGER_METADATA_CONVERSION.set_get_converter
def trigger_metadata_get_converter(value):
    if value is not None:
        metadata_type = try_get_auto_moderation_trigger_metadata_type_from_data(value)
        if metadata_type is None:
            value = None
        else:
            value = metadata_type.from_data(value)
    
    return value


@TRIGGER_METADATA_CONVERSION.set_put_converter
def trigger_metadata_put_converter(value):
    if value is not None:
        value = value.to_data(defaults = True)
    return value


@TRIGGER_METADATA_CONVERSION.set_validator
def trigger_metadata_validator(value):
    if value is None or isinstance(value, AutoModerationRuleTriggerMetadataBase):
        return value
    
    raise TypeError(
        f'`trigger_metadata` can be `None`, `{AutoModerationRuleTriggerMetadataBase.__name__}`, '
        f'got {type(value).__name__}; {value!r}.'
    )


# ---- trigger_type ----

TRIGGER_TYPE_CONVERSION = AuditLogEntryChangeConversion(
    'trigger_type',
    'trigger_type',
    FLAG_IS_MODIFICATION,
    validator = validate_trigger_type,
)


@TRIGGER_TYPE_CONVERSION.set_get_converter
def trigger_type_get_converter(value):
    return AutoModerationRuleTriggerType.get(value)


@TRIGGER_TYPE_CONVERSION.set_put_converter
def trigger_type_put_converter(value):
    return value.value


# ---- Construct ----

AUTO_MODERATION_RULE_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    ACTIONS_CONVERSION,
    CREATOR_ID_CONVERSION,
    ENABLED_CONVERSION,
    EXCLUDED_KEYWORDS_CONVERSION__ADDITION,
    EXCLUDED_KEYWORDS_CONVERSION__REMOVAL,
    EVENT_TYPE_CONVERSION,
    EXCLUDED_CHANNEL_IDS_CONVERSION,
    EXCLUDED_ROLE_IDS_CONVERSION,
    KEYWORDS_CONVERSION__ADDITION,
    KEYWORDS_CONVERSION__REMOVAL,
    MENTION_LIMIT_CONVERSION,
    NAME_CONVERSION,
    RAID_PROTECTION_CONVERSION,
    REGEX_PATTERNS_CONVERSION__ADDITION,
    REGEX_PATTERNS_CONVERSION__REMOVAL,
    TRIGGER_METADATA_CONVERSION,
    TRIGGER_TYPE_CONVERSION,
)
