import vampytest

from .. import (
    AutoModerationRule, AutoModerationRuleTriggerType, AutoModerationAction, AutoModerationEventType,
    AutoModerationKeywordPresetType,
)


def test__AutoModerationRule__eq__0():
    """
    Tests whether the auto moderation action's `__eq__` method works.
    """
    vampytest.assert_eq(
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam),
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam),
    )
    
    vampytest.assert_eq(
        AutoModerationRule(
            'name',
            [AutoModerationAction(duration=6)],
            enabled = False,
            event_type = AutoModerationEventType.none,
            excluded_channels = [12],
            excluded_roles = [12],
            keywords = 'owo',
        ),
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
    
    vampytest.assert_not_eq(
        AutoModerationRule(
            'name',
            [AutoModerationAction(duration=6)],
            enabled = False,
            event_type = AutoModerationEventType.none,
            excluded_channels = [12],
            excluded_roles = [12],
            keywords = 'owo',
        ),
        AutoModerationRule(
            'weather boy',
            [AutoModerationAction(channel=6)],
            enabled = True,
            event_type = AutoModerationEventType.message_send,
            excluded_channels = [68],
            excluded_roles = None,
            keyword_presets = [AutoModerationKeywordPresetType.slur],
        )
    )

def test__AutoModerationRule__eq__1():
    """
    Tests whether the auto moderation action's `__eq__` method refuses incorrect types.
    """
    vampytest.assert_not_eq(
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam),
        1337,
    )


def test__AutoModerationRule__hash():
    """
    Tests whether the auto moderation action's `__hash__` method works.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam),
    
    vampytest.assert_instance(hash(rule), int)


def test__AutoModerationRule__repr():
    """
    Tests whether the auto moderation action's `__repr__` method works.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam),
    
    vampytest.assert_instance(repr(rule), str)
