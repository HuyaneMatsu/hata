import vampytest

from ....channel import Channel
from ....guild import Guild
from ....role import Role
from ....user import ClientUserBase

from ...action import AutoModerationAction
from ...trigger_metadata import AutoModerationRuleTriggerMetadataKeyword

from ..preinstanced import AutoModerationEventType, AutoModerationRuleTriggerType
from ..rule import AutoModerationRule

from .test__AutoModerationRule__constructor import _assert_fields_set


def test__AutoModerationRule__copy():
    """
    Tests whether ``AutoModerationRule.copy`` works as intended.
    """
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211180071, 202211180072]
    excluded_role_ids = [202211180073, 202211180074]
    name = 'Border'
    mention_limit = 14
    
    rule = AutoModerationRule(
        actions = actions,
        enabled = enabled,
        event_type = event_type,
        excluded_channel_ids = excluded_channel_ids,
        excluded_role_ids = excluded_role_ids,
        name = name,
        mention_limit = mention_limit,
    )
    
    copy = rule.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, rule)
    vampytest.assert_eq(copy, rule)


def test__AutoModerationRule__copy_with__0():
    """
    Tests whether ``AutoModerationRule.copy_with`` works as intended.
    
    Case: No parameters.
    """
    actions = [AutoModerationAction(duration = 69)]
    enabled = False
    event_type = AutoModerationEventType.message_send
    excluded_channel_ids = [202211180075, 202211180076]
    excluded_role_ids = [202211180077, 202211180078]
    name = 'Border'
    mention_limit = 14
    
    rule = AutoModerationRule(
        actions = actions,
        enabled = enabled,
        event_type = event_type,
        excluded_channel_ids = excluded_channel_ids,
        excluded_role_ids = excluded_role_ids,
        name = name,
        mention_limit = mention_limit,
    )
    
    copy = rule.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, rule)
    vampytest.assert_eq(copy, rule)


def test__AutoModerationRule__copy_with__1():
    """
    Tests whether ``AutoModerationRule.copy_with`` works as intended.
    
    Case: No parameters.
    """
    old_actions = [AutoModerationAction(duration = 69)]
    new_actions = [AutoModerationAction(channel_id = 202211180079)]
    old_enabled = False
    new_enabled = True
    old_event_type = AutoModerationEventType.message_send
    new_event_type = AutoModerationEventType.none
    old_excluded_channel_ids = [202211180080, 202211180081]
    new_excluded_channel_ids = [202211180082]
    old_excluded_role_ids = [202211180083, 2022111800884]
    new_excluded_role_ids = [202211180085]
    old_name = 'Border'
    new_name = 'of life'
    old_mention_limit = 20
    new_keywords = ['Kisaki']
    
    rule = AutoModerationRule(
        actions = old_actions,
        enabled = old_enabled,
        event_type = old_event_type,
        excluded_channel_ids = old_excluded_channel_ids,
        excluded_role_ids = old_excluded_role_ids,
        name = old_name,
        mention_limit = old_mention_limit,
    )
    
    copy = rule.copy_with(
        actions = new_actions,
        enabled = new_enabled,
        event_type = new_event_type,
        excluded_channel_ids = new_excluded_channel_ids,
        excluded_role_ids = new_excluded_role_ids,
        name = new_name,
        keywords = new_keywords,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, rule)

    vampytest.assert_eq(copy.actions, tuple(new_actions))
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_is(copy.event_type, new_event_type)
    vampytest.assert_eq(copy.excluded_channel_ids, tuple(new_excluded_channel_ids))
    vampytest.assert_eq(copy.excluded_role_ids, tuple(new_excluded_role_ids))
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(
        copy.trigger_metadata, AutoModerationRuleTriggerMetadataKeyword(keywords = new_keywords)
    )
    vampytest.assert_is(copy.trigger_type, AutoModerationRuleTriggerType.keyword)


def test__AutoModerationRule__partial():
    """
    Tests whether ``AutoModerationRule.partial`` works as intended,
    """
    rule = AutoModerationRule.precreate(202211180087)
    vampytest.assert_false(rule.partial)

    rule = AutoModerationRule()
    vampytest.assert_true(rule.partial)


def test__AutoModerationRule__iter_actions():
    """
    Tests whether ``AutoModerationRule.iter_actions`` works as intended,
    """
    action_1 = AutoModerationAction(duration = 69)
    action_2 = AutoModerationAction(channel_id = 202211180088)
    
    for input_actions, expected_output in (
        (None, []),
        ([action_1], [action_1]),
        ([action_1, action_2], [action_1, action_2]),
    ):
        rule = AutoModerationRule(actions = input_actions)
        vampytest.assert_eq([*rule.iter_actions()], expected_output)


def test__AutoModerationRule__creator():
    """
    Tests whether ``AutoModerationRule.creator`` works as intended,
    """
    rule_id = 202211180089
    creator_id = 202211180090
    
    rule = AutoModerationRule.precreate(rule_id, creator_id = creator_id)
    creator = rule.creator
    
    vampytest.assert_instance(creator, ClientUserBase)
    vampytest.assert_eq(creator.id, creator_id)


def test__AutoModerationRule__guild():
    """
    Tests whether ``AutoModerationRule.guild`` works as intended,
    """
    rule_id = 202211180093
    guild_id = 202211180091
    guild = Guild.precreate(guild_id)
    
    for input_guild_id, expected_output in (
        (0, None),
        (guild_id, guild),
        (202211180092, None),
    ):
        rule = AutoModerationRule.precreate(rule_id, guild_id = input_guild_id)
        vampytest.assert_is(rule.guild, expected_output)


def test__AutoModerationRule__iter_excluded_channel_ids():
    """
    Tests whether ``AutoModerationRule.iter_excluded_channel_ids`` works as intended,
    """
    for input_value, expected_output in (
        (None, []),
        ([202211180094], [202211180094]),
        ([202211180095, 202211180096], [202211180095, 202211180096]),
    ):
        rule = AutoModerationRule(excluded_channel_ids = input_value)
        vampytest.assert_eq([*rule.iter_excluded_channel_ids()], expected_output)


def test__AutoModerationRule__excluded_channels():
    """
    Tests whether ``AutoModerationRule.excluded_channels`` works as intended,
    """
    for input_value, expected_output in (
        (None, None),
        ([202211180097], (Channel.precreate(202211180097),)),
        ([202211180098, 202211180099], (Channel.precreate(202211180098), Channel.precreate(202211180099))),
    ):
        rule = AutoModerationRule(excluded_channel_ids = input_value)
        vampytest.assert_eq(rule.excluded_channels, expected_output)



def test__AutoModerationRule__iter_excluded_channels():
    """
    Tests whether ``AutoModerationRule.iter_excluded_channels`` works as intended,
    """
    for input_value, expected_output in (
        (None, []),
        ([202211180100], [Channel.precreate(202211180100)]),
        ([202211180101, 202211180102], [Channel.precreate(202211180101), Channel.precreate(202211180102)]),
    ):
        rule = AutoModerationRule(excluded_channel_ids = input_value)
        vampytest.assert_eq([*rule.iter_excluded_channels()], expected_output)


def test__AutoModerationRule__iter_excluded_role_ids():
    """
    Tests whether ``AutoModerationRule.iter_excluded_role_ids`` works as intended,
    """
    for input_value, expected_output in (
        (None, []),
        ([202211180103], [202211180103]),
        ([202211180104, 202211180105], [202211180104, 202211180105]),
    ):
        rule = AutoModerationRule(excluded_role_ids = input_value)
        vampytest.assert_eq([*rule.iter_excluded_role_ids()], expected_output)


def test__AutoModerationRule__excluded_roles():
    """
    Tests whether ``AutoModerationRule.excluded_roles`` works as intended,
    """
    for input_value, expected_output in (
        (None, None),
        ([202211180106], (Role.precreate(202211180106),)),
        ([202211180107, 202211180108], (Role.precreate(202211180107), Role.precreate(202211180108))),
    ):
        rule = AutoModerationRule(excluded_role_ids = input_value)
        vampytest.assert_eq(rule.excluded_roles, expected_output)



def test__AutoModerationRule__iter_excluded_roles():
    """
    Tests whether ``AutoModerationRule.iter_excluded_roles`` works as intended,
    """
    for input_value, expected_output in (
        (None, []),
        ([202211180109], [Role.precreate(202211180109)]),
        ([202211180110, 202211180111], [Role.precreate(202211180110), Role.precreate(202211180111)]),
    ):
        rule = AutoModerationRule(excluded_role_ids = input_value)
        vampytest.assert_eq([*rule.iter_excluded_roles()], expected_output)
