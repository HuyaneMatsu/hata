import vampytest

from .. import (
    AutoModerationRule, AutoModerationRuleTriggerType, AutoModerationAction, AutoModerationActionType,
    AutoModerationEventType, KeywordTriggerMetadata
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


EDITIONS = (
    (
        [
            ('actions', [{'type': AutoModerationActionType.timeout.value, 'metadata': {'duration_seconds': 6},},],)
        ], [
            ('actions', (AutoModerationAction(duration=6),),)
        ], [
            ('actions', None,),
        ]
    ), (
        [
            ('actions', [],)
        ], [
            ('actions', None,),
        ], [
            ('actions', (AutoModerationAction(duration=6),),)
        ]
    ), (
        [
            ('enabled', True),
        ], [
            ('enabled', True),
        ], [
            ('enabled', False)
        ],
    ), (
        [
            ('event_type', AutoModerationEventType.none.value,),
        ], [
            ('event_type', AutoModerationEventType.none,),
        ], [
            ('event_type', AutoModerationEventType.message_send,),
        ],
    ), (
        [
            ('exempt_channels', ['12'],),
        ], [
            ('excluded_channel_ids', (12,),),
        ], [
            ('excluded_channel_ids', None,),
        ]
    ), (
        [
            ('exempt_channels', [],),
        ], [
            ('excluded_channel_ids', None,),
        ], [
            ('excluded_channel_ids', (12,),),
        ]
    ), (
        [
            ('exempt_roles', ['12'],),
        ], [
            ('excluded_role_ids', (12,),),
        ], [
            ('excluded_role_ids', None,),
        ]
    ), (
        [
            ('exempt_roles', [],),
        ], [
            ('excluded_role_ids', None,),
        ], [
            ('excluded_role_ids', (12,),),
        ]
    ), (
        [
            ('name', 'hell',),
        ], [
            ('name', 'hell',),
        ], [
            ('name', 'name',),
        ]
    ), (
        [
            ('trigger_type', AutoModerationRuleTriggerType.harmful_link.value,),
            ('trigger_metadata', {},),
        ], [
            ('trigger_type', AutoModerationRuleTriggerType.harmful_link,),
            ('trigger_metadata', None,),
        ], [
            ('trigger_type', AutoModerationRuleTriggerType.spam,),
        ],
    ), (
        [
            ('trigger_type', AutoModerationRuleTriggerType.keyword.value,),
            ('trigger_metadata', {'keyword_filter': ['owo']},),
        ], [
            ('trigger_type', AutoModerationRuleTriggerType.keyword,),
            ('trigger_metadata', KeywordTriggerMetadata(keywords='owo'),),
        ], [
            ('trigger_type', AutoModerationRuleTriggerType.harmful_link,),
            ('trigger_metadata', None,),
        ],
    ), (
        [
            ('trigger_type', AutoModerationRuleTriggerType.keyword.value,),
            ('trigger_metadata', {'keyword_filter': ['typhoon']},),
        ], [
            ('trigger_type', AutoModerationRuleTriggerType.keyword,),
            ('trigger_metadata', KeywordTriggerMetadata(keywords='typhoon'),),
        ], [
            ('trigger_metadata', KeywordTriggerMetadata(keywords='owo'),),
        ],
    )
)


def test__AutoModerationRule__from_data__0():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method returns as expected.
    """
    data = get_rule_data()
    
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_instance(rule, AutoModerationRule)


def test__AutoModerationRule__from_data__1():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method caches.
    """
    data = get_rule_data()
    
    rule_1 = AutoModerationRule.from_data(data)
    rule_2 = AutoModerationRule.from_data(data)
    
    vampytest.assert_is(rule_1, rule_2)


def test__AutoModerationRule__from_data__2():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.id` as expected.
    """
    data = get_rule_data()
    data['id'] = 23
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.id, 23)


def test__AutoModerationRule__from_data__3():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.guild_id` as expected.
    Case: `69`.
    """
    data = get_rule_data()
    data['guild_id'] = '69'
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.guild_id, 69)


def test__AutoModerationRule__from_data__4():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.guild_id` as expected.
    Case: `None`.
    """
    data = get_rule_data()
    data['guild_id'] = None
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.guild_id, 0)


def test__AutoModerationRule__from_data__5():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.guild_id` as expected.
    Case: *missing*.
    """
    data = get_rule_data()
    data.pop('guild_id', None)
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.guild_id, 0)


def test__AutoModerationRule__from_data__6():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.creator_id` as expected.
    Case: `69`.
    """
    data = get_rule_data()
    data['creator_id'] = '69'
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.creator_id, 69)


def test__AutoModerationRule__from_data__7():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.creator_id` as expected.
    Case: `None`.
    """
    data = get_rule_data()
    data['creator_id'] = None
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.creator_id, 0)


def test__AutoModerationRule__from_data__8():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets `.creator_id` as expected.
    Case: *missing*.
    """
    data = get_rule_data()
    data.pop('creator_id', None)
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_eq(rule.creator_id, 0)


def test__AutoModerationRule__from_data__9():
    """
    Tests whether ``AutoModerationRule``'s `.from_data` method sets everything else as `_update_attributes`.
    """
    test__AutoModerationRule__update_attributes()


def test__AutoModerationRule__to_data__0():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` works as intended.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    return rule.to_data()


def test__AutoModerationRule__to_data__1():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` skips `id` field.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    vampytest.assert_not_in('id', output_data)


def test__AutoModerationRule__to_data__2():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `actions` field as expected.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['actions'], [])


def test__AutoModerationRule__to_data__3():
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


def test__AutoModerationRule__to_data__4():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` skips `creator_id` field.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    vampytest.assert_not_in('creator_id', output_data)


def test__AutoModerationRule__to_data__5():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `enabled` field.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_in('enabled', output_data,)
    vampytest.assert_instance(output_data['enabled'], bool)


def test__AutoModerationRule__to_data__6():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `enabled` field as expected.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, enabled=True)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['enabled'], True)


def test__AutoModerationRule__to_data__7():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `event_type` field.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_in('event_type', output_data)
    vampytest.assert_instance(output_data['event_type'], int)
    
    
def test__AutoModerationRule__to_data__8():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `excluded_channel_ids` field as expected.
    Case: *None*
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['exempt_channels'], [])


def test__AutoModerationRule__to_data__9():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `excluded_channel_ids` field as expected.
    Case: `[1]`
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=[1])
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['exempt_channels'], [1])


def test__AutoModerationRule__to_data__10():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `excluded_role_ids` field as expected.
    Case: *none*.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['exempt_roles'], [])


def test__AutoModerationRule__to_data__11():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `excluded_role_ids` field as expected.
    Case: `[1]`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=[1])
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['exempt_roles'], [1])


def test__AutoModerationRule__to_data__12():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `name` field as expected.
    Case: `'name'`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['name'], 'name')



def test__AutoModerationRule__to_data__13():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `trigger_metadata` field as expected.
    Case: *none*.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['trigger_metadata'], {})


def test__AutoModerationRule__to_data__14():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `trigger_metadata` field as expected.
    Case: `keywords='owo'`.
    """
    rule = AutoModerationRule('name', None, keywords='owo')
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['trigger_metadata'], {'keyword_filter': ['owo']})


def test__AutoModerationRule__to_data__15():
    """
    Tests whether ``AutoModerationRule``'s `.to_data` adds `trigger_type` field as expected.
    Case: `keywords='owo'`.
    """
    rule = AutoModerationRule('name', None, keywords='owo')
    
    output_data = rule.to_data()
    
    vampytest.assert_eq(output_data['trigger_type'], AutoModerationRuleTriggerType.keyword.value)


def test__AutoModerationRule__update_attributes():
    """
    Tests whether ``AutoModerationRule``'s ``._update_attributes`` updates every attributes as expected.
    """
    data = get_rule_data()
    rule = AutoModerationRule.from_data(data)
    
    for data_fields, object_fields, difference in EDITIONS:
        data.update(data_fields)
        
        rule._update_attributes(data)
        
        for attribute_name, attribute_value in object_fields:
            vampytest.assert_eq(getattr(rule, attribute_name), attribute_value)


def test__AutoModerationRule__difference_update_attributes():
    """
    Tests whether ``AutoModerationRule``'s ``._difference_update_attributes`` updates every attributes as expected.
    """
    data = get_rule_data()
    rule = AutoModerationRule.from_data(data)
    
    for data_fields, object_fields, difference in EDITIONS:
        data.update(data_fields)
        
        old_attributes = rule._difference_update_attributes(data)
        
        for attribute_name, attribute_value in object_fields:
            vampytest.assert_eq(getattr(rule, attribute_name), attribute_value)
        
        vampytest.assert_eq(old_attributes, dict(difference))
