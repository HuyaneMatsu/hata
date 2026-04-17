import vampytest

from ...action import AutoModerationAction
from ...trigger_metadata import AutoModerationRuleTriggerMetadataKeyword, AutoModerationRuleTriggerMetadataMentionSpam

from ..preinstanced import AutoModerationEventType, AutoModerationRuleTriggerType
from ..rule import AutoModerationRule

from .test__AutoModerationRule__constructor import _assert_fields_set


def test__AutoModerationRule__from_data__0():
    """
    tests whether ``AutoModerationRule.from_data`` works as intended.
    
    Case: default.
    """
    rule_id = 202211180009
    creator_id = 202211180010
    guild_id = 202211180011
    
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211180012, 202211180013]
    excluded_role_ids = [202211180014, 202211180015]
    name = 'Border'
    mention_limit = 20
    
    data = {
        'id': str(rule_id),
        'creator_id': str(creator_id),
        'guild_id': str(guild_id),
        'actions': [action.to_data(defaults = True) for action in actions],
        'enabled': enabled,
        'event_type': event_type.value,
        'exempt_channels': [str(channel_id) for channel_id in excluded_channel_ids],
        'exempt_roles': [str(role_id) for role_id in excluded_role_ids],
        'name': name,
        'trigger_type': AutoModerationRuleTriggerType.mention_spam.value,
        'trigger_metadata': AutoModerationRuleTriggerMetadataMentionSpam(
            mention_limit = mention_limit
        ).to_data(defaults = True)
    }
    
    rule = AutoModerationRule.from_data(data)
    _assert_fields_set(rule)
    vampytest.assert_eq(rule.id, rule_id)
    vampytest.assert_eq(rule.creator_id, creator_id)
    vampytest.assert_eq(rule.guild_id, guild_id)
    
    vampytest.assert_eq(rule.actions, tuple(actions))
    vampytest.assert_eq(rule.enabled, enabled)
    vampytest.assert_is(rule.event_type, event_type)
    vampytest.assert_eq(rule.excluded_channel_ids, tuple(excluded_channel_ids))
    vampytest.assert_eq(rule.excluded_role_ids, tuple(excluded_role_ids))
    vampytest.assert_eq(rule.name, name)
    vampytest.assert_eq(
        rule.trigger_metadata, AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = mention_limit)
    )
    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.mention_spam)


def test__AutoModerationRule__from_data__1():
    """
    tests whether ``AutoModerationRule.from_data`` works as intended.
    
    Case: check caching.
    """
    rule_id = 202211180016
    
    data = {
        'id': str(rule_id),
    }
    
    rule = AutoModerationRule.from_data(data)
    test_rule = AutoModerationRule.from_data(data)
    vampytest.assert_is(rule, test_rule)



def test__AutoModerationRule__to_data():
    """
    tests whether ``AutoModerationRule.to_data`` works as intended.
    
    Case: include internals and defaults.
    """
    rule_id = 202211180017
    creator_id = 202211180018
    guild_id = 202211180019
    
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211180020, 202211180021]
    excluded_role_ids = [202211180022, 202211180023]
    name = 'Border'
    mention_limit = 20
    
    rule = AutoModerationRule.precreate(
        rule_id,
        creator_id = creator_id,
        guild_id = guild_id,
        actions = actions,
        enabled = enabled,
        event_type = event_type,
        excluded_channel_ids = excluded_channel_ids,
        excluded_role_ids = excluded_role_ids,
        name = name,
        mention_limit = mention_limit,
    )
    
    expected_data = {
        'id': str(rule_id),
        'creator_id': str(creator_id),
        'guild_id': str(guild_id),
        'actions': [action.to_data(defaults = True) for action in actions],
        'enabled': enabled,
        'event_type': event_type.value,
        'exempt_channels': [str(channel_id) for channel_id in excluded_channel_ids],
        'exempt_roles': [str(role_id) for role_id in excluded_role_ids],
        'name': name,
        'trigger_type': AutoModerationRuleTriggerType.mention_spam.value,
        'trigger_metadata': AutoModerationRuleTriggerMetadataMentionSpam(
            mention_limit = mention_limit
        ).to_data(defaults = True)
    }
    
    vampytest.assert_eq(
        rule.to_data(
            defaults = True,
            include_internals = True,
        ),
        expected_data,
    )


def test__AutoModerationRule__set_attributes():
    """
    tests whether ``AutoModerationRule._set_attributes`` works as intended.
    """
    creator_id = 202211180024
    guild_id = 202211180025
    
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211180036, 202211180037]
    excluded_role_ids = [202211180038, 202211180039]
    name = 'Border'
    mention_limit = 20
    
    data = {
        'creator_id': str(creator_id),
        'guild_id': str(guild_id),
        'actions': [action.to_data(defaults = True) for action in actions],
        'enabled': enabled,
        'event_type': event_type.value,
        'exempt_channels': [str(channel_id) for channel_id in excluded_channel_ids],
        'exempt_roles': [str(role_id) for role_id in excluded_role_ids],
        'name': name,
        'trigger_type': AutoModerationRuleTriggerType.mention_spam.value,
        'trigger_metadata': AutoModerationRuleTriggerMetadataMentionSpam(
            mention_limit = mention_limit
        ).to_data(defaults = True)
    }
    
    rule = AutoModerationRule()
    rule._set_attributes(data)
    
    vampytest.assert_eq(rule.creator_id, creator_id)
    vampytest.assert_eq(rule.guild_id, guild_id)
    
    vampytest.assert_eq(rule.actions, tuple(actions))
    vampytest.assert_eq(rule.enabled, enabled)
    vampytest.assert_is(rule.event_type, event_type)
    vampytest.assert_eq(rule.excluded_channel_ids, tuple(excluded_channel_ids))
    vampytest.assert_eq(rule.excluded_role_ids, tuple(excluded_role_ids))
    vampytest.assert_eq(rule.name, name)
    vampytest.assert_eq(
        rule.trigger_metadata, AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = mention_limit)
    )
    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.mention_spam)


def test__AutoModerationRule__update_attributes():
    """
    tests whether ``AutoModerationRule._update_attributes`` works as intended.
    """
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211180040, 202211180041]
    excluded_role_ids = [202211180042, 202211180043]
    name = 'Border'
    mention_limit = 20
    
    data = {
        'actions': [action.to_data(defaults = True) for action in actions],
        'enabled': enabled,
        'event_type': event_type.value,
        'exempt_channels': [str(channel_id) for channel_id in excluded_channel_ids],
        'exempt_roles': [str(role_id) for role_id in excluded_role_ids],
        'name': name,
        'trigger_type': AutoModerationRuleTriggerType.mention_spam,
        'trigger_metadata': AutoModerationRuleTriggerMetadataMentionSpam(
            mention_limit = mention_limit
        ).to_data(defaults = True)
    }
    
    rule = AutoModerationRule()
    rule._update_attributes(data)
    
    vampytest.assert_eq(rule.actions, tuple(actions))
    vampytest.assert_eq(rule.enabled, enabled)
    vampytest.assert_is(rule.event_type, event_type)
    vampytest.assert_eq(rule.excluded_channel_ids, tuple(excluded_channel_ids))
    vampytest.assert_eq(rule.excluded_role_ids, tuple(excluded_role_ids))
    vampytest.assert_eq(rule.name, name)
    vampytest.assert_eq(
        rule.trigger_metadata, AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = mention_limit)
    )
    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.mention_spam)


def test__AutoModerationRule__difference_update_attributes():
    """
    tests whether ``AutoModerationRule._update_attributes`` works as intended.
    """
    old_actions = [AutoModerationAction(duration = 69)]
    new_actions = [AutoModerationAction(channel_id = 202211180044)]
    old_enabled = False
    new_enabled = True
    old_event_type = AutoModerationEventType.message_send
    new_event_type = AutoModerationEventType.none
    old_excluded_channel_ids = [202211180045, 202211180046]
    new_excluded_channel_ids = [202211180047]
    old_excluded_role_ids = [202211180048, 202211180049]
    new_excluded_role_ids = [202211180050]
    old_name = 'Border'
    new_name = 'of life'
    old_mention_limit = 20
    new_keywords = ['Kisaki']
    
    data = {
        'actions': [action.to_data(defaults = True) for action in new_actions],
        'enabled': new_enabled,
        'event_type': new_event_type.value,
        'exempt_channels': [str(channel_id) for channel_id in new_excluded_channel_ids],
        'exempt_roles': [str(role_id) for role_id in new_excluded_role_ids],
        'name': new_name,
        'trigger_type': AutoModerationRuleTriggerType.keyword.value,
        'trigger_metadata': AutoModerationRuleTriggerMetadataKeyword(
            keywords = new_keywords
        ).to_data(defaults = True)
    }
    
    rule = AutoModerationRule(
        actions = old_actions,
        enabled = old_enabled,
        event_type = old_event_type,
        excluded_channel_ids = old_excluded_channel_ids,
        excluded_role_ids = old_excluded_role_ids,
        name = old_name,
        mention_limit = old_mention_limit,
    )
    
    old_attributes = rule._difference_update_attributes(data)
    
    vampytest.assert_eq(rule.actions, tuple(new_actions))
    vampytest.assert_eq(rule.enabled, new_enabled)
    vampytest.assert_is(rule.event_type, new_event_type)
    vampytest.assert_eq(rule.excluded_channel_ids, tuple(new_excluded_channel_ids))
    vampytest.assert_eq(rule.excluded_role_ids, tuple(new_excluded_role_ids))
    vampytest.assert_eq(rule.name, new_name)
    vampytest.assert_eq(
        rule.trigger_metadata, AutoModerationRuleTriggerMetadataKeyword(keywords = new_keywords)
    )
    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.keyword)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'actions': tuple(old_actions),
            'enabled': old_enabled,
            'event_type': old_event_type,
            'excluded_channel_ids': tuple(old_excluded_channel_ids),
            'excluded_role_ids': tuple(old_excluded_role_ids),
            'name': old_name,
            'trigger_type': AutoModerationRuleTriggerType.mention_spam,
            'trigger_metadata': AutoModerationRuleTriggerMetadataMentionSpam(mention_limit = old_mention_limit),
        },
    )
