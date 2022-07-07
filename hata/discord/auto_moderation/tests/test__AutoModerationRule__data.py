import vampytest

from ...channel import Channel
from ...role import Role

from .. import (
    AutoModerationRule, AutoModerationRuleTriggerType, AutoModerationAction, AutoModerationActionType,
    AutoModerationEventType, KeywordPresetTriggerMetadata, AutoModerationKeywordPresetType, KeywordTriggerMetadata
)

def get_rule_data():
    return {
        'id': '1',
        'creator_id': '1',
        'guild_id': '1',
        'actions': [],
        'enabled': False,
        'exempt_channels': [],
        'exempt_roles': [],
        'name': 'name',
        'trigger_type': AutoModerationRuleTriggerType.spam.value,
        'trigger_metadata': {},
        'event_type': AutoModerationEventType.message_send.value,
    }


def test__AutoModerationRule__from_data_0():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method returns as expected.
    """
    data = get_rule_data()
    
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_instance(rule, AutoModerationRule)


def test__AutoModerationRule__from_data_1():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method caches.
    """
    data = get_rule_data()
    
    rule_1 = AutoModerationRule.from_data(data)
    rule_2 = AutoModerationRule.from_data(data)
    
    vampytest.assert_is(rule_1, rule_2)


def test__AutoModerationRule__from_data_2():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.id` as expected.
    """
    data = get_rule_data()
    data['id'] = 23
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.id, 23)


def test__AutoModerationRule__from_data_3():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.guild_id` as expected.
    Case: `69`.
    """
    data = get_rule_data()
    data['guild_id'] = '69'
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.guild_id, 69)


def test__AutoModerationRule__from_data_4():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.guild_id` as expected.
    Case: `None`.
    """
    data = get_rule_data()
    data['guild_id'] = None
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.guild_id, 0)


def test__AutoModerationRule__from_data_5():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.guild_id` as expected.
    Case: *missing*.
    """
    data = get_rule_data()
    data.pop('guild_id', None)
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.guild_id, 0)


def test__AutoModerationRule__from_data_6():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.creator_id` as expected.
    Case: `69`.
    """
    data = get_rule_data()
    data['creator_id'] = '69'
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.creator_id, 69)


def test__AutoModerationRule__from_data_7():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.creator_id` as expected.
    Case: `None`.
    """
    data = get_rule_data()
    data['creator_id'] = None
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.creator_id, 0)


def test__AutoModerationRule__from_data_8():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.creator_id` as expected.
    Case: *missing*.
    """
    data = get_rule_data()
    data.pop('creator_id', None)
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.creator_id, 0)


def test__AutoModerationRule__to_data_0():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` works as intended.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    return rule.to_data()


def test__AutoModerationRule__to_data_1():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` skips `id` field.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    vampytest.assert_not_in('id', output_data)


def test__AutoModerationRule__to_data_2():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `actions` field as expected.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['actions'], [])


def test__AutoModerationRule__to_data_3():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `actions` field as expected.
    """
    rule = AutoModerationRule('name', [AutoModerationAction(duration=6)], AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(
        output_data['actions'],
        [
            {
                'type': AutoModerationActionType.timeout.value,
                'metadata': {
                    'duration_seconds': 6
                },
            },
        ],
    )


def test__AutoModerationRule__to_data_4():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` skips `creator_id` field.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    vampytest.assert_not_in('creator_id', output_data)


def test__AutoModerationRule__to_data_5():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `enabled` field.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_in('enabled', output_data,)
    vampytest.assert_instance(output_data['enabled'], bool)


def test__AutoModerationRule__to_data_6():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `enabled` field as expected.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, enabled=True)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['enabled'], True)


def test__AutoModerationRule__to_data_7():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `event_type` field.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_in('event_type', output_data)
    vampytest.assert_instance(output_data['event_type'], int)
    
    
def test__AutoModerationRule__to_data_8():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `excluded_channel_ids` field as expected.
    Case: *None*
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['exempt_channels'], [])


def test__AutoModerationRule__to_data_9():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `excluded_channel_ids` field as expected.
    Case: `[1]`
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=[1])
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['exempt_channels'], [1])


def test__AutoModerationRule__to_data_10():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `excluded_role_ids` field as expected.
    Case: *none*.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['exempt_roles'], [])


def test__AutoModerationRule__to_data_11():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `excluded_role_ids` field as expected.
    Case: `[1]`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=[1])
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['exempt_roles'], [1])


def test__AutoModerationRule__to_data_12():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `name` field as expected.
    Case: `'name'`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['name'], 'name')



def test__AutoModerationRule__to_data_13():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `trigger_metadata` field as expected.
    Case: *none*.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['trigger_metadata'], {})


def test__AutoModerationRule__to_data_14():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `trigger_metadata` field as expected.
    Case: `keywords='owo'`.
    """
    rule = AutoModerationRule('name', None, keywords='owo')
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['trigger_metadata'], {'keyword_filter': ['owo']})


def test__AutoModerationRule__to_data_15():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `trigger_type` field as expected.
    Case: `keywords='owo'`.
    """
    rule = AutoModerationRule('name', None, keywords='owo')
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['trigger_type'], AutoModerationRuleTriggerType.keyword.value)
