import vampytest

from ....auto_moderation import AutoModerationRule

from ..fields import put_auto_moderation_rules_into


def _iter_options():
    auto_moderation_rule_id_0 = 202406250002
    auto_moderation_rule_id_1 = 202406250003
    
    auto_moderation_rule_0 = AutoModerationRule.precreate(auto_moderation_rule_id_0)
    auto_moderation_rule_1 = AutoModerationRule.precreate(auto_moderation_rule_id_1)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'auto_moderation_rules': [],
        },
    )
    
    yield (
        {
            auto_moderation_rule_id_0: auto_moderation_rule_0,
            auto_moderation_rule_id_1: auto_moderation_rule_1,
        },
        False,
        {
            'auto_moderation_rules': [
                auto_moderation_rule_0.to_data(defaults = False, include_internals = True),
                auto_moderation_rule_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        {
            auto_moderation_rule_id_0: auto_moderation_rule_0,
            auto_moderation_rule_id_1: auto_moderation_rule_1,
        },
        True,
        {
            'auto_moderation_rules': [
                auto_moderation_rule_0.to_data(defaults = True, include_internals = True),
                auto_moderation_rule_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_auto_moderation_rules_into(input_value, defaults):
    """
    Tests whether ``put_auto_moderation_rules_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | dict<int, AutoModerationRule>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_auto_moderation_rules_into(input_value, {}, defaults)
