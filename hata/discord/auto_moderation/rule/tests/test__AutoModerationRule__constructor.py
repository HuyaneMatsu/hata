import vampytest

from ...action import AutoModerationAction
from ...trigger_metadata import AutoModerationRuleTriggerMetadataBase, AutoModerationRuleTriggerMetadataMentionSpam

from ..preinstanced import AutoModerationEventType, AutoModerationRuleTriggerType
from ..rule import AutoModerationRule


def _assert_fields_set(rule):
    """
    Asserts whether every attribute of the given rule is set.
    
    Parameters
    ----------
    rule : ``AutoModerationRule ``
        The rule to check.
    """
    vampytest.assert_instance(rule, AutoModerationRule)
    vampytest.assert_instance(rule.id, int)
    vampytest.assert_instance(rule.actions, tuple, nullable = True)
    vampytest.assert_instance(rule.creator_id, int)
    vampytest.assert_instance(rule.enabled, bool)
    vampytest.assert_instance(rule.event_type, AutoModerationEventType)
    vampytest.assert_instance(rule.excluded_channel_ids, tuple, nullable = True)
    vampytest.assert_instance(rule.excluded_role_ids, tuple, nullable = True)
    vampytest.assert_instance(rule.guild_id, int)
    vampytest.assert_instance(rule.name, str)
    vampytest.assert_instance(rule.trigger_metadata, AutoModerationRuleTriggerMetadataBase)
    vampytest.assert_instance(rule.trigger_type, AutoModerationRuleTriggerType)


def test__AutoModerationRule__new__0():
    """
    Asserts whether ``AutoModerationRule.__new__`` works as intended.
    
    Case: No parameters given.
    """
    rule = AutoModerationRule()
    _assert_fields_set(rule)


def test__AutoModerationRule__new__1():
    """
    Asserts whether ``AutoModerationRule.__new__`` works as intended.
    
    Case: All parameters given.
    """
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211170042, 202211170043]
    excluded_role_ids = [202211170044, 202211170045]
    name = 'Border'
    mention_limit = 20
    
    rule = AutoModerationRule(
        actions = actions,
        enabled = enabled,
        event_type = event_type,
        excluded_channel_ids = excluded_channel_ids,
        excluded_role_ids = excluded_role_ids,
        name = name,
        mention_limit = mention_limit,
    )
    _assert_fields_set(rule)
    
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


def test__AutoModerationRule__create_empty():
    """
    Asserts whether ``AutoModerationRule._create_empty`` works as intended.
    """
    rule_id = 202211170086
    
    rule = AutoModerationRule._create_empty(rule_id)
    
    _assert_fields_set(rule)
    vampytest.assert_eq(rule.id, rule_id)


def test__AutoModerationRule__precreate__0():
    """
    Asserts whether ``AutoModerationRule.precreate`` works as intended.
    
    Case: No parameters.
    """
    rule_id = 202211180000
    
    rule = AutoModerationRule.precreate(rule_id)
    _assert_fields_set(rule)
    vampytest.assert_eq(rule.id, rule_id)


def test__AutoModerationRule__precreate__1():
    """
    Asserts whether ``AutoModerationRule.precreate`` works as intended.
    
    Case: All parameters.
    """
    rule_id = 202211180001
    creator_id = 202211180002
    guild_id = 202211180003
    
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211178004, 202211180005]
    excluded_role_ids = [20221118006, 202211180007]
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


def test__AutoModerationRule__precreate__2():
    """
    Asserts whether ``AutoModerationRule.precreate`` works as intended.
    
    Case: Check caching.
    """
    rule_id = 202211170008
    
    rule = AutoModerationRule.precreate(rule_id)
    test_rule = AutoModerationRule.precreate(rule_id)
    vampytest.assert_is(rule, test_rule)
