import vampytest

from ...channel import Channel
from ...role import Role
from ...user import User, ZEROUSER

from .. import (
    AutoModerationRule, AutoModerationRuleTriggerType, AutoModerationAction, AutoModerationEventType,
    AutoModerationKeywordPresetType,
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


def test__AutoModerationRule__copy():
    """
    Tests whether the auto moderation rule's `copy` method works.
    """
    rule = AutoModerationRule(
        'name',
        [AutoModerationAction(duration=6)],
        enabled = False,
        event_type = AutoModerationEventType.none,
        excluded_channels = [12],
        excluded_roles = [12],
        keywords = 'owo',
    )
    
    copy = rule.copy()
    
    vampytest.assert_eq(rule, copy)
    vampytest.assert_not_is(rule, copy)


def test__AutoModerationRule__copy_with_0():
    """
    Tests whether the auto moderation rule's `copy_with` method works.
    """
    rule = AutoModerationRule(
        'name',
        [AutoModerationAction(duration=6)],
        enabled = False,
        event_type = AutoModerationEventType.none,
        excluded_channels = [12],
        excluded_roles = [12],
        keywords = 'owo',
    )
    
    copy = rule.copy_with()
    
    vampytest.assert_eq(rule, copy)
    vampytest.assert_not_is(rule, copy)


def test__AutoModerationRule__copy_with_1():
    """
    Tests whether the auto moderation rule's `copy_with` method works.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    copy = rule.copy_with(
        name = 'name',
        actions = [AutoModerationAction(duration=6)],
        enabled = False,
        event_type = AutoModerationEventType.none,
        excluded_channels = [12],
        excluded_roles = [12],
        keywords = 'owo',
    )
    
    vampytest.assert_eq(
        copy,
        AutoModerationRule(
            'name',
            [AutoModerationAction(duration=6)],
            enabled = False,
            event_type = AutoModerationEventType.none,
            excluded_channels = [12],
            excluded_roles = [12],
            keywords = 'owo',
        )
    )

def test__AutoModerationRule__copy_with_2():
    """
    Tests whether the auto moderation rule's `copy_with` method drops mismatch error on passing multiple trigger
    metadata parameters.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    with vampytest.assert_raises(TypeError):
        return rule.copy_with(
            mention_limit = None,
            keywords = None,
        )


def test__AutoModerationRule__partial():
    """
    Tests whether the auto moderation rule's `partial` property works.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    vampytest.assert_true(rule.partial)
    
    
    rule = AutoModerationRule.from_data(get_rule_data())
    vampytest.assert_false(rule.partial)



def test__AutoModerationRule__iter_actions():
    """
    Tests whether the auto moderation rule's `iter_actions` method works.
    """
    actions = []
    rule = AutoModerationRule('name', actions, AutoModerationRuleTriggerType.spam)
    vampytest.assert_eq([*rule.iter_actions()], actions)
    
    actions = [AutoModerationAction(duration=6)]
    rule = AutoModerationRule('name', actions, AutoModerationRuleTriggerType.spam)
    vampytest.assert_eq([*rule.iter_actions()], actions)


def test__AutoModerationRule__creator():
    """
    Tests whether the auto moderation rule's `creator` property works.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    vampytest.assert_is(rule.creator, ZEROUSER)
    
    data = get_rule_data()
    data['creator_id'] = '69'
    user = User.precreate(69)
    rule = AutoModerationRule.from_data(data)
    
    vampytest.assert_is(rule.creator, user)


def test__AutoModerationRule__iter_excluded_channel_ids():
    """
    Tests whether the auto moderation rule's `iter_excluded_channel_ids` method works.
    """
    excluded_channel_ids = []
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=excluded_channel_ids)
    vampytest.assert_eq([*rule.iter_excluded_channel_ids()], excluded_channel_ids)
    
    excluded_channel_ids = [69]
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=excluded_channel_ids)
    vampytest.assert_eq([*rule.iter_excluded_channel_ids()], excluded_channel_ids)


def test__AutoModerationRule__iter_excluded_channels():
    """
    Tests whether the auto moderation rule's `iter_excluded_channels` method works.
    """
    excluded_channel_ids = []
    excluded_channels = [Channel.precreate(channel_id) for channel_id in excluded_channel_ids]
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=excluded_channel_ids)
    vampytest.assert_eq([*rule.iter_excluded_channels()], excluded_channels)
    
    excluded_channel_ids = [69]
    excluded_channels = [Channel.precreate(channel_id) for channel_id in excluded_channel_ids]
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=excluded_channel_ids)
    vampytest.assert_eq([*rule.iter_excluded_channels()], excluded_channels)


def test__AutoModerationRule__excluded_channels():
    """
    Tests whether the auto moderation rule's `excluded_channels` property works.
    """
    excluded_channel_ids = []
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=excluded_channel_ids)
    vampytest.assert_eq(rule.excluded_channels, None)
    
    excluded_channel_ids = [69]
    excluded_channels = [Channel.precreate(channel_id) for channel_id in excluded_channel_ids]
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=excluded_channel_ids)
    vampytest.assert_eq(rule.excluded_channels, tuple(excluded_channels))


def test__AutoModerationRule__iter_excluded_role_ids():
    """
    Tests whether the auto moderation rule's `iter_excluded_role_ids` method works.
    """
    excluded_role_ids = []
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=excluded_role_ids)
    vampytest.assert_eq([*rule.iter_excluded_role_ids()], excluded_role_ids)
    
    excluded_role_ids = [69]
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=excluded_role_ids)
    vampytest.assert_eq([*rule.iter_excluded_role_ids()], excluded_role_ids)


def test__AutoModerationRule__iter_excluded_roles():
    """
    Tests whether the auto moderation rule's `iter_excluded_roles` method works.
    """
    excluded_role_ids = []
    excluded_roles = [Role.precreate(role_id) for role_id in excluded_role_ids]
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=excluded_role_ids)
    vampytest.assert_eq([*rule.iter_excluded_roles()], excluded_roles)
    
    excluded_role_ids = [69]
    excluded_roles = [Role.precreate(role_id) for role_id in excluded_role_ids]
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=excluded_role_ids)
    vampytest.assert_eq([*rule.iter_excluded_roles()], excluded_roles)


def test__AutoModerationRule__excluded_roles():
    """
    Tests whether the auto moderation rule's `excluded_roles` property works.
    """
    excluded_role_ids = []
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=excluded_role_ids)
    vampytest.assert_eq(rule.excluded_roles, None)
    
    excluded_role_ids = [69]
    excluded_roles = [Role.precreate(role_id) for role_id in excluded_role_ids]
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=excluded_role_ids)
    vampytest.assert_eq(rule.excluded_roles, tuple(excluded_roles))
