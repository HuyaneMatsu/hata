import vampytest

from ....auto_moderation import (
    AutoModerationAction, AutoModerationEventType, AutoModerationRuleTriggerMetadataMentionSpam,
    AutoModerationRuleTriggerType
)
from ....auto_moderation.rule.fields import (
    validate_actions, validate_creator_id, validate_enabled, validate_event_type, validate_excluded_channel_ids,
    validate_excluded_role_ids, validate_name, validate_trigger_type
)
from ....auto_moderation.trigger_metadata.constants import AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
from ....auto_moderation.trigger_metadata.fields import (
    validate_excluded_keywords, validate_keywords, validate_mention_limit, validate_raid_protection,
    validate_regex_patterns
)

from ...audit_log_entry_change_conversion.change_deserializers import change_deserializer_addition_and_removal
from ...audit_log_entry_change_conversion.change_serializers import change_serializer_addition_and_removal
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...audit_log_entry_change_conversion.value_mergers import value_merger_sorted_array
from ...conversion_helpers.converters import (
    value_deserializer_id, value_deserializer_ids, value_deserializer_name, value_deserializer_string_array,
    value_serializer_id, value_serializer_ids, value_serializer_name, value_serializer_string_array
)

from ..auto_moderation_rule import (
    ACTIONS_CONVERSION, AUTO_MODERATION_RULE_CONVERSIONS, CREATOR_ID_CONVERSION, ENABLED_CONVERSION,
    EVENT_TYPE_CONVERSION, EXCLUDED_CHANNEL_IDS_CONVERSION, EXCLUDED_KEYWORDS_CONVERSION, EXCLUDED_ROLE_IDS_CONVERSION,
    KEYWORDS_CONVERSION, MENTION_LIMIT_CONVERSION, NAME_CONVERSION, RAID_PROTECTION_CONVERSION,
    REGEX_PATTERNS_CONVERSION, TRIGGER_METADATA_CONVERSION, TRIGGER_TYPE_CONVERSION
)


def test__AUTO_MODERATION_RULE_CONVERSIONS():
    """
    Tests whether `AUTO_MODERATION_RULE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(AUTO_MODERATION_RULE_CONVERSIONS)
    vampytest.assert_eq(
        {*AUTO_MODERATION_RULE_CONVERSIONS.iter_field_keys()},
        {
            'actions', 'creator_id', 'enabled', '$add_allow_list', '$remove_allow_list', 'event_type',
            'exempt_channels', 'exempt_roles', '$add_keyword_filter', '$remove_keyword_filter',
            'mention_raid_protection_enabled', 'mention_total_limit', 'name', '$add_regex_patterns',
            '$remove_regex_patterns', 'trigger_metadata', 'trigger_type',
        },
    )


# ---- actions ----

def test__ACTIONS_CONVERSION__generic():
    """
    Tests whether ``ACTIONS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ACTIONS_CONVERSION)
    vampytest.assert_is(ACTIONS_CONVERSION.value_validator, validate_actions)
    

def _iter_options__actions__value_deserializer():
    action_0 = AutoModerationAction(duration = 69)
    action_1 = AutoModerationAction(channel_id = 202310250000)
    
    yield None, None
    yield [], None
    yield [action_0.to_data(defaults = True), action_1.to_data(defaults = True)], (action_0, action_1)


@vampytest._(vampytest.call_from(_iter_options__actions__value_deserializer()).returning_last())
def test__ACTIONS_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `ACTIONS_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | tuple<AutoModerationAction>`
    """
    return ACTIONS_CONVERSION.value_deserializer(input_value)


def _iter_options__actions__value_serializer():
    action_0 = AutoModerationAction(duration = 69)
    action_1 = AutoModerationAction(channel_id = 202310250001)
    
    yield None, []
    yield (action_0, action_1), [action_0.to_data(defaults = True), action_1.to_data(defaults = True)]


@vampytest._(vampytest.call_from(_iter_options__actions__value_serializer()).returning_last())
def test__ACTIONS_CONVERSION__value_serializer(input_value):
    """
    Tests whether `ACTIONS_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<AutoModerationAction>`
        Processed value.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return ACTIONS_CONVERSION.value_serializer(input_value)


# ---- creator_id ----

def test__CREATOR_ID_CONVERSION__generic():
    """
    Tests whether ``CREATOR_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CREATOR_ID_CONVERSION)
    vampytest.assert_is(CREATOR_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(CREATOR_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(CREATOR_ID_CONVERSION.value_validator, validate_creator_id)


# ---- enabled ----

def test__ENABLED_CONVERSION__generic():
    """
    Tests whether ``ENABLED_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ENABLED_CONVERSION)
    vampytest.assert_is(ENABLED_CONVERSION.value_serializer, None)
    vampytest.assert_is(ENABLED_CONVERSION.value_validator, validate_enabled)


def _iter_options__enabled__value_deserializer():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__enabled__value_deserializer()).returning_last())
def test__ENABLED_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `ENABLED_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return ENABLED_CONVERSION.value_deserializer(input_value)


# ---- excluded_keywords ----

def test__EXCLUDED_KEYWORDS_CONVERSION__generic():
    """
    Tests whether ``EXCLUDED_KEYWORDS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(EXCLUDED_KEYWORDS_CONVERSION)
    vampytest.assert_is(EXCLUDED_KEYWORDS_CONVERSION.value_deserializer, value_deserializer_string_array)
    vampytest.assert_is(EXCLUDED_KEYWORDS_CONVERSION.value_serializer, value_serializer_string_array)
    vampytest.assert_is(EXCLUDED_KEYWORDS_CONVERSION.value_validator, validate_excluded_keywords)
    
    vampytest.assert_is(EXCLUDED_KEYWORDS_CONVERSION.value_merger, value_merger_sorted_array)
    vampytest.assert_is(EXCLUDED_KEYWORDS_CONVERSION.change_deserializer, change_deserializer_addition_and_removal)
    vampytest.assert_is(EXCLUDED_KEYWORDS_CONVERSION.change_serializer, change_serializer_addition_and_removal)
    vampytest.assert_instance(EXCLUDED_KEYWORDS_CONVERSION.field_keys, tuple)
    vampytest.assert_eq(len(EXCLUDED_KEYWORDS_CONVERSION.field_keys), 2)


# ---- event_type ----

def test__EVENT_TYPE_CONVERSION__generic():
    """
    Tests whether ``EVENT_TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(EVENT_TYPE_CONVERSION)
    vampytest.assert_is(EVENT_TYPE_CONVERSION.value_validator, validate_event_type)


def _iter_options__event_type__value_deserializer():
    yield None, AutoModerationEventType.none
    yield AutoModerationEventType.message_send.value, AutoModerationEventType.message_send


@vampytest._(vampytest.call_from(_iter_options__event_type__value_deserializer()).returning_last())
def test__EVENT_TYPE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `EVENT_TYPE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``AutoModerationEventType``
    """
    return EVENT_TYPE_CONVERSION.value_deserializer(input_value)


def _iter_options__event_type__value_serializer():
    yield AutoModerationEventType.none, AutoModerationEventType.none.value
    yield AutoModerationEventType.message_send, AutoModerationEventType.message_send.value


@vampytest._(vampytest.call_from(_iter_options__event_type__value_serializer()).returning_last())
def test__EVENT_TYPE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `EVENT_TYPE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``AutoModerationEventType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return EVENT_TYPE_CONVERSION.value_serializer(input_value)


# ---- excluded_channel_ids ----

def test__EXCLUDED_CHANNEL_IDS_CONVERSION__generic():
    """
    Tests whether ``EXCLUDED_CHANNEL_IDS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(EXCLUDED_CHANNEL_IDS_CONVERSION)
    vampytest.assert_is(EXCLUDED_CHANNEL_IDS_CONVERSION.value_deserializer, value_deserializer_ids)
    vampytest.assert_is(EXCLUDED_CHANNEL_IDS_CONVERSION.value_serializer, value_serializer_ids)
    vampytest.assert_is(EXCLUDED_CHANNEL_IDS_CONVERSION.value_validator, validate_excluded_channel_ids)


# ---- excluded_role_ids ----

def test__EXCLUDED_ROLE_IDS_CONVERSION__generic():
    """
    Tests whether ``EXCLUDED_ROLE_IDS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(EXCLUDED_ROLE_IDS_CONVERSION)
    vampytest.assert_is(EXCLUDED_ROLE_IDS_CONVERSION.value_deserializer, value_deserializer_ids)
    vampytest.assert_is(EXCLUDED_ROLE_IDS_CONVERSION.value_serializer, value_serializer_ids)
    vampytest.assert_is(EXCLUDED_ROLE_IDS_CONVERSION.value_validator, validate_excluded_role_ids)


# ---- keywords ----

def test__KEYWORDS_CONVERSION__generic():
    """
    Tests whether ``KEYWORDS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(KEYWORDS_CONVERSION)
    vampytest.assert_is(KEYWORDS_CONVERSION.value_deserializer, value_deserializer_string_array)
    vampytest.assert_is(KEYWORDS_CONVERSION.value_serializer, value_serializer_string_array)
    vampytest.assert_is(KEYWORDS_CONVERSION.value_validator, validate_keywords)

    vampytest.assert_is(KEYWORDS_CONVERSION.value_merger, value_merger_sorted_array)
    vampytest.assert_is(KEYWORDS_CONVERSION.change_deserializer, change_deserializer_addition_and_removal)
    vampytest.assert_is(KEYWORDS_CONVERSION.change_serializer, change_serializer_addition_and_removal)
    vampytest.assert_instance(KEYWORDS_CONVERSION.field_keys, tuple)
    vampytest.assert_eq(len(KEYWORDS_CONVERSION.field_keys), 2)


# ---- mention_limit ----

def test__MENTION_LIMIT_CONVERSION__generic():
    """
    Tests whether ``MENTION_LIMIT_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MENTION_LIMIT_CONVERSION)
    vampytest.assert_is(MENTION_LIMIT_CONVERSION.value_serializer, None)
    vampytest.assert_is(MENTION_LIMIT_CONVERSION.value_validator, validate_mention_limit)


def _iter_options__mention_limit__value_deserializer():
    yield 1, 1
    yield None, AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX


@vampytest._(vampytest.call_from(_iter_options__mention_limit__value_deserializer()).returning_last())
def test__MENTION_LIMIT_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `MENTION_LIMIT_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return MENTION_LIMIT_CONVERSION.value_deserializer(input_value)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_validator, validate_name)


# ---- raid_protection ----

def test__RAID_PROTECTION_CONVERSION__generic():
    """
    Tests whether ``RAID_PROTECTION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(RAID_PROTECTION_CONVERSION)
    vampytest.assert_is(RAID_PROTECTION_CONVERSION.value_serializer, None)
    vampytest.assert_is(RAID_PROTECTION_CONVERSION.value_validator, validate_raid_protection)


def _iter_options__raid_protection__value_deserializer():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__raid_protection__value_deserializer()).returning_last())
def test__RAID_PROTECTION_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `RAID_PROTECTION_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return RAID_PROTECTION_CONVERSION.value_deserializer(input_value)


# ---- regex_patterns ----

def test__REGEX_PATTERNS_CONVERSION__generic():
    """
    Tests whether ``REGEX_PATTERNS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(REGEX_PATTERNS_CONVERSION)
    vampytest.assert_is(REGEX_PATTERNS_CONVERSION.value_deserializer, value_deserializer_string_array)
    vampytest.assert_is(REGEX_PATTERNS_CONVERSION.value_serializer, value_serializer_string_array)
    vampytest.assert_is(REGEX_PATTERNS_CONVERSION.value_validator, validate_regex_patterns)

    vampytest.assert_is(REGEX_PATTERNS_CONVERSION.value_merger, value_merger_sorted_array)
    vampytest.assert_is(REGEX_PATTERNS_CONVERSION.change_deserializer, change_deserializer_addition_and_removal)
    vampytest.assert_is(REGEX_PATTERNS_CONVERSION.change_serializer, change_serializer_addition_and_removal)
    vampytest.assert_instance(REGEX_PATTERNS_CONVERSION.field_keys, tuple)
    vampytest.assert_eq(len(REGEX_PATTERNS_CONVERSION.field_keys), 2)


# ---- trigger_metadata ----

def test__TRIGGER_METADATA_CONVERSION__generic():
    """
    Tests whether ``TRIGGER_METADATA_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TRIGGER_METADATA_CONVERSION)


def _iter_options__trigger_metadata__value_deserializer():
    yield None, None
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = 6)
    yield metadata.to_data(defaults = True), metadata


@vampytest._(vampytest.call_from(_iter_options__trigger_metadata__value_deserializer()).returning_last())
def test__TRIGGER_METADATA_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `TRIGGER_METADATA_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | AutoModerationRuleTriggerMetadataBase`
    """
    return TRIGGER_METADATA_CONVERSION.value_deserializer(input_value)


def _iter_options__trigger_metadata__value_serializer():
    yield None, None
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = 6)
    yield metadata, metadata.to_data(defaults = True)


@vampytest._(vampytest.call_from(_iter_options__trigger_metadata__value_serializer()).returning_last())
def test__TRIGGER_METADATA_CONVERSION__value_serializer(input_value):
    """
    Tests whether `TRIGGER_METADATA_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : `None | AutoModerationRuleTriggerMetadataBase`
        Processed value.
    
    Returns
    -------
    output : `None | dict<str, object>`
    """
    return TRIGGER_METADATA_CONVERSION.value_serializer(input_value)


def _iter_options__trigger_metadata__value_validator__passing():
    yield None, None
    
    metadata = AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = 6)
    yield metadata, metadata


def _iter_options__trigger_metadata__value_validator__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__trigger_metadata__value_validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__trigger_metadata__value_validator__type_error()).raising(TypeError))
def test__TRIGGER_METADATA_CONVERSION__value_validator(input_value):
    """
    Tests whether `TRIGGER_METADATA_CONVERSION.value_validator` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | AutoModerationRuleTriggerMetadataBase`
    
    Raises
    ------
    TypeError
    """
    return TRIGGER_METADATA_CONVERSION.value_validator(input_value)


# ---- trigger_type ----

def test__TRIGGER_TYPE_CONVERSION__generic():
    """
    Tests whether ``TRIGGER_TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TRIGGER_TYPE_CONVERSION)
    vampytest.assert_is(TRIGGER_TYPE_CONVERSION.value_validator, validate_trigger_type)


def _iter_options__trigger_type__value_deserializer():
    yield None, AutoModerationRuleTriggerType.none
    yield AutoModerationRuleTriggerType.keyword.value, AutoModerationRuleTriggerType.keyword


@vampytest._(vampytest.call_from(_iter_options__trigger_type__value_deserializer()).returning_last())
def test__TRIGGER_TYPE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `TRIGGER_TYPE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``AutoModerationRuleTriggerType``
    """
    return TRIGGER_TYPE_CONVERSION.value_deserializer(input_value)


def _iter_options__trigger_type__value_serializer():
    yield AutoModerationRuleTriggerType.none, AutoModerationRuleTriggerType.none.value
    yield AutoModerationRuleTriggerType.keyword, AutoModerationRuleTriggerType.keyword.value


@vampytest._(vampytest.call_from(_iter_options__trigger_type__value_serializer()).returning_last())
def test__TRIGGER_TYPE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `TRIGGER_TYPE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``AutoModerationRuleTriggerType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return TRIGGER_TYPE_CONVERSION.value_serializer(input_value)
