import vampytest

from ..helpers import guess_rule_trigger_type_from_keyword_parameters
from ..preinstanced import AutoModerationRuleTriggerType


def test__guess_rule_trigger_type_from_keyword_parameters__0():
    """
    Tests whether ``guess_rule_trigger_type_from_keyword_parameters`` works as intended.
    
    Case: Passing.
    """
    for input_trigger_type, input_keyword_parameters, expected_output in (
        (AutoModerationRuleTriggerType.none, {}, AutoModerationRuleTriggerType.none),
        (AutoModerationRuleTriggerType.keyword, {}, AutoModerationRuleTriggerType.keyword),
        (AutoModerationRuleTriggerType.none, {'keywords': None}, AutoModerationRuleTriggerType.keyword),
        (AutoModerationRuleTriggerType.keyword, {'keywords': None}, AutoModerationRuleTriggerType.keyword),
        (AutoModerationRuleTriggerType.none, {'excluded_keywords': None}, AutoModerationRuleTriggerType.none),
        (AutoModerationRuleTriggerType.keyword, {'excluded_keywords': None}, AutoModerationRuleTriggerType.keyword),
    ):
        output = guess_rule_trigger_type_from_keyword_parameters(input_trigger_type, input_keyword_parameters)
        vampytest.assert_is(output, expected_output)


def test__guess_rule_trigger_type_from_keyword_parameters__1():
    """
    Tests whether ``guess_rule_trigger_type_from_keyword_parameters`` works as intended.
    
    Case: `TypeError`.
    """
    for input_trigger_type, input_keyword_parameters in (
        (AutoModerationRuleTriggerType.mention_spam, {'keywords': None}),
        (AutoModerationRuleTriggerType.none, {'keywords': None, 'keyword_presets': None}),
        (AutoModerationRuleTriggerType.none, {'koishi': None}),
    ):
        with vampytest.assert_raises(TypeError):
            guess_rule_trigger_type_from_keyword_parameters(input_trigger_type, input_keyword_parameters)
