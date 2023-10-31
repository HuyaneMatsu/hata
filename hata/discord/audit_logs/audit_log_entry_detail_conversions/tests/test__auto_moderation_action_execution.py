import vampytest

from ....auto_moderation import AutoModerationRuleTriggerType
from ....auto_moderation.execution_event.fields import validate_channel_id
from ....auto_moderation.rule.fields import validate_name, validate_trigger_type

from ...conversion_helpers.converters import get_converter_id, get_converter_name, put_converter_id, put_converter_name

from ..auto_moderation_action_execution import (
    AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS, CHANNEL_ID_CONVERSION, RULE_NAME_CONVERSION, TRIGGER_TYPE_CONVERSION
)


def test__AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS():
    """
    Tests whether `AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS.get_converters.keys()},
        {'channel_id', 'auto_moderation_rule_name', 'auto_moderation_rule_trigger_type'}
    )


# ---- channel_id ----

def test__CHANNEL_ID_CONVERSION__generic():
    """
    Tests whether ``CHANNEL_ID_CONVERSION`` works as intended.
    """
    vampytest.assert_is(CHANNEL_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(CHANNEL_ID_CONVERSION.validator, validate_channel_id)


# ---- rule_name ----

def test__RULE_NAME_CONVERSION__generic():
    """
    Tests whether ``RULE_NAME_CONVERSION`` works as intended.
    """
    vampytest.assert_is(RULE_NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(RULE_NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(RULE_NAME_CONVERSION.validator, validate_name)


# ---- trigger_type ----

def test__TRIGGER_TYPE_CONVERSION__generic():
    """
    Tests whether ``TRIGGER_TYPE_CONVERSION`` works as intended.
    """
    # vampytest.assert_is(TRIGGER_TYPE_CONVERSION.get_converter, )
    # vampytest.assert_is(TRIGGER_TYPE_CONVERSION.put_converter, )
    vampytest.assert_is(TRIGGER_TYPE_CONVERSION.validator, validate_trigger_type)



def _iter_options__trigger_type__get_converter():
    yield None, AutoModerationRuleTriggerType.none
    yield AutoModerationRuleTriggerType.keyword.value, AutoModerationRuleTriggerType.keyword


@vampytest._(vampytest.call_from(_iter_options__trigger_type__get_converter()).returning_last())
def test__TRIGGER_TYPE_CONVERSION__get_converter(input_value):
    """
    Tests whether `TRIGGER_TYPE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``AutoModerationRuleTriggerType``
    """
    return TRIGGER_TYPE_CONVERSION.get_converter(input_value)


def _iter_options__trigger_type__put_converter():
    yield AutoModerationRuleTriggerType.none, AutoModerationRuleTriggerType.none.value
    yield AutoModerationRuleTriggerType.keyword, AutoModerationRuleTriggerType.keyword.value


@vampytest._(vampytest.call_from(_iter_options__trigger_type__put_converter()).returning_last())
def test__TRIGGER_TYPE_CONVERSION__put_converter(input_value):
    """
    Tests whether `TRIGGER_TYPE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``AutoModerationRuleTriggerType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return TRIGGER_TYPE_CONVERSION.put_converter(input_value)
