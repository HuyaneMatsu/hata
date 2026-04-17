import vampytest

from ....auto_moderation import AutoModerationRule

from ..fields import validate_auto_moderation_rules


def _iter_options__passing():
    auto_moderation_rule_id_0 = 202406270006
    auto_moderation_rule_id_1 = 202406270007
    
    auto_moderation_rule_0 = AutoModerationRule.precreate(auto_moderation_rule_id_0)
    auto_moderation_rule_1 = AutoModerationRule.precreate(auto_moderation_rule_id_1)

    yield None, None
    yield [], None
    yield [auto_moderation_rule_0], {auto_moderation_rule_id_0: auto_moderation_rule_0}
    yield (
        [auto_moderation_rule_0, auto_moderation_rule_0],
        {auto_moderation_rule_id_0: auto_moderation_rule_0},
    )
    yield (
        [auto_moderation_rule_1, auto_moderation_rule_0],
        {auto_moderation_rule_id_0: auto_moderation_rule_0, auto_moderation_rule_id_1: auto_moderation_rule_1},
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_auto_moderation_rules(input_value):
    """
    Validates whether ``validate_auto_moderation_rules`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | dict<int, AutoModerationRule>`
    
    Raises
    ------
    TypeError
    """
    output = validate_auto_moderation_rules(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
