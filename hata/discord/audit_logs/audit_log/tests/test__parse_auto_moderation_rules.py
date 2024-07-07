import vampytest

from ....auto_moderation import AutoModerationRule

from ..fields import parse_auto_moderation_rules


def _iter_options():
    auto_moderation_rule_id_0 = 202406240004
    auto_moderation_rule_id_1 = 202406240005
    
    auto_moderation_rule_0 = AutoModerationRule.precreate(auto_moderation_rule_id_0)
    auto_moderation_rule_1 = AutoModerationRule.precreate(auto_moderation_rule_id_1)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'auto_moderation_rules': [],
        },
        None,
    )
    
    yield (
        {
            'auto_moderation_rules': [
                auto_moderation_rule_0.to_data(defaults = True, include_internals = True),
                auto_moderation_rule_1.to_data(defaults = True, include_internals = True),
            ],
        },
        {
            auto_moderation_rule_id_0: auto_moderation_rule_0,
            auto_moderation_rule_id_1: auto_moderation_rule_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_auto_moderation_rules(input_data):
    """
    Tests whether ``parse_auto_moderation_rules`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `dict<int, AutoModerationRule>`
    """
    return parse_auto_moderation_rules(input_data)
