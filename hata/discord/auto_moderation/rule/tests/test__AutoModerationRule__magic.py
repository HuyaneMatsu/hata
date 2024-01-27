import vampytest

from ..rule import AutoModerationRule
from ..preinstanced import AutoModerationEventType

from ...action import AutoModerationAction


def test__AutoModerationRule__eq():
    """
    Tests whether ``AutoModerationRule.__eq__`` works as intended.
    """
    rule_id_0 = 202211180051
    rule_id_1 = 202211180052

    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211180053, 202211180054]
    excluded_role_ids = [202211180055, 202211180056]
    name = 'Border'
    keywords = ['find', 'way',  'your']

    keyword_parameters = {
        'actions': actions,
        'enabled': enabled,
        'event_type': event_type,
        'excluded_channel_ids': excluded_channel_ids,
        'excluded_role_ids': excluded_role_ids,
        'name': name,
        'keywords': keywords,
    }
    
    rule = AutoModerationRule.precreate(rule_id_0, **keyword_parameters)
    vampytest.assert_eq(rule, rule)
    vampytest.assert_ne(rule, object())
    
    test_rule = AutoModerationRule.precreate(rule_id_1, **keyword_parameters)
    vampytest.assert_ne(rule, test_rule)
    
    test_rule = AutoModerationRule(**keyword_parameters)
    vampytest.assert_eq(rule, test_rule)
    
    for field_name, field_value in (
        ('actions', None),
        ('enabled', True),
        ('event_type', AutoModerationEventType.none),
        ('excluded_channel_ids', None),
        ('excluded_role_ids', None),
        ('name', 'Gape'),
        ('keywords', None),
        ('regex_patterns', ['fumo']),
    ):
        test_rule = AutoModerationRule(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(rule, test_rule)


def test__AutoModerationRule__hash():
    """
    Tests whether ``AutoModerationRule.__hash__`` works as intended.
    """
    rule_id = 202211180057
    creator_id = 202211180058
    guild_id = 202211180059
    
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211180060, 202211180061]
    excluded_role_ids = [202211180062, 202211180063]
    name = 'Border'
    keywords = ['find', 'way',  'your']
    
    keyword_parameters = {
        'actions': actions,
        'enabled': enabled,
        'event_type': event_type,
        'excluded_channel_ids': excluded_channel_ids,
        'excluded_role_ids': excluded_role_ids,
        'name': name,
        'keywords': keywords,
    }
    
    rule = AutoModerationRule.precreate(
        rule_id,
        creator_id = creator_id,
        guild_id = guild_id,
        **keyword_parameters,
    )
    vampytest.assert_instance(hash(rule), int)

    rule = AutoModerationRule(**keyword_parameters,)
    vampytest.assert_instance(hash(rule), int)


def test__AutoModerationRule__repr():
    """
    Tests whether ``AutoModerationRule.__repr__`` works as intended.
    """
    rule_id = 202211180064
    creator_id = 202211180065
    guild_id = 202211180066
    
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.user_update
    excluded_channel_ids = [202211180067, 202211180068]
    excluded_role_ids = [202211180069, 202211180070]
    name = 'Border'
    keywords = ['find', 'way',  'your']
    
    keyword_parameters = {
        'actions': actions,
        'enabled': enabled,
        'event_type': event_type,
        'excluded_channel_ids': excluded_channel_ids,
        'excluded_role_ids': excluded_role_ids,
        'name': name,
        'keywords': keywords,
    }
    
    rule = AutoModerationRule.precreate(
        rule_id,
        creator_id = creator_id,
        guild_id = guild_id,
        **keyword_parameters,
    )
    vampytest.assert_instance(repr(rule), str)

    rule = AutoModerationRule(**keyword_parameters,)
    vampytest.assert_instance(repr(rule), str)
