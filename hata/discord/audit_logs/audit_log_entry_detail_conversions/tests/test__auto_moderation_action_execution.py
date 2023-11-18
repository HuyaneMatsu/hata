import vampytest

from ....auto_moderation import AutoModerationRuleTriggerType
from ....auto_moderation.execution_event.fields import validate_channel_id
from ....auto_moderation.rule.fields import validate_name, validate_trigger_type

from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_detail_conversion.tests.test__AuditLogEntryDetailConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import (
    value_deserializer_id, value_deserializer_name, value_serializer_id, value_serializer_name
)

from ..auto_moderation_action_execution import (
    AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS, CHANNEL_ID_CONVERSION, RULE_NAME_CONVERSION, TRIGGER_TYPE_CONVERSION
)


def test__AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS():
    """
    Tests whether `AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS)
    vampytest.assert_eq(
        {conversion.field_key for conversion in AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS.conversions},
        {'channel_id', 'auto_moderation_rule_name', 'auto_moderation_rule_trigger_type'}
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(CHANNEL_ID_CONVERSION)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.value_validator, validate_channel_id)


# ---- rule_name ----

def test__RULE_NAME_CONVERSION__generic():
    """
    Tests whether ``RULE_NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(RULE_NAME_CONVERSION)
    vampytest.assert_is(RULE_NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(RULE_NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(RULE_NAME_CONVERSION.value_validator, validate_name)


# ---- trigger_type ----

def test__TRIGGER_TYPE_CONVERSION__generic():
    """
    Tests whether ``TRIGGER_TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TRIGGER_TYPE_CONVERSION)
    # vampytest.assert_is(TRIGGER_TYPE_CONVERSION.value_deserializer, )
    # vampytest.assert_is(TRIGGER_TYPE_CONVERSION.value_serializer, )
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
