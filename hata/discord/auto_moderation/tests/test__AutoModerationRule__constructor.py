import vampytest

from ...channel import Channel
from ...role import Role

from .. import (
    AutoModerationRule, AutoModerationRuleTriggerType, AutoModerationAction, AutoModerationActionType,
    AutoModerationEventType, KeywordPresetTriggerMetadata, AutoModerationKeywordPresetType, KeywordTriggerMetadata,
    MentionSpamTriggerMetadata
)


def test__AutoModerationRule__constructor__0():
    """
    Tests whether ``AutoModerationRule``'s constructor_ returns as expected.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    vampytest.assert_instance(rule, AutoModerationRule)


def test__AutoModerationRule__constructor__defaults():
    """
    Tests whether ``AutoModerationRule`` sets all the default parameters as expected.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    vampytest.assert_eq(rule.id, 0)
    vampytest.assert_eq(rule.creator_id, 0)
    vampytest.assert_eq(rule.guild_id, 0)


def test__AutoModerationRule__constructor__actions_0():
    """
    Tests whether ``AutoModerationRule`` sets `.actions` attribute as expected.
    Case : `None`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    vampytest.assert_is(rule.actions, None)


def test__AutoModerationRule__constructor__actions_1():
    """
    Tests whether ``AutoModerationRule`` sets `.actions` attribute as expected.
    Case : `[]`.
    """
    rule = AutoModerationRule('name', [], AutoModerationRuleTriggerType.spam)
    
    vampytest.assert_is(rule.actions, None)


def test__AutoModerationRule__constructor__actions_2():
    """
    Tests whether ``AutoModerationRule`` sets `.actions` attribute as expected.
    Case : `[action]`.
    """
    action = AutoModerationAction(AutoModerationActionType.block_message)
    
    rule = AutoModerationRule('name', [action], AutoModerationRuleTriggerType.spam)
    
    vampytest.assert_eq(rule.actions, (action, ))


def test__AutoModerationRule__constructor__actions_3():
    """
    Tests whether ``AutoModerationRule`` checks `actions` parameter as expected.
    Case : `69`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', 69, AutoModerationRuleTriggerType.spam)


def test__AutoModerationRule__constructor__actions_4():
    """
    Tests whether ``AutoModerationRule`` checks `actions` parameter as expected.
    Case : `[69]`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', [69], AutoModerationRuleTriggerType.spam)
     


def test__AutoModerationRule__constructor__enabled_0():
    """
    Tests whether ``AutoModerationRule`` sets `.enabled` attribute as expected.
    Case : `False`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, enabled=False)
    
    vampytest.assert_eq(rule.enabled, False)


def test__AutoModerationRule__constructor__enabled_1():
    """
    Tests whether ``AutoModerationRule`` sets `.enabled` attribute as expected.
    Case : `True`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, enabled=True)
    
    vampytest.assert_eq(rule.enabled, True)


def test__AutoModerationRule__constructor__enabled_2():
    """
    Tests whether ``AutoModerationRule`` checks `enabled` parameter as expected.
    Case : `'owo'`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, enabled='owo')


def test__AutoModerationRule__constructor__enabled_3():
    """
    Tests whether ``AutoModerationRule`` sets `.enabled` attribute as expected.
    Case : *default*
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    vampytest.assert_instance(rule.enabled, bool)


def test__AutoModerationRule__constructor__event_type_0():
    """
    Tests whether ``AutoModerationRule`` sets `.event_type` attribute as expected.
    Case : `AutoModerationEventType.none`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, event_type=AutoModerationEventType.none)
    
    vampytest.assert_is(rule.event_type, AutoModerationEventType.none)


def test__AutoModerationRule__constructor__event_type_1():
    """
    Tests whether ``AutoModerationRule`` sets `.event_type` attribute as expected.
    Case : `AutoModerationEventType.none.value`.
    """
    rule = AutoModerationRule(
        'name', None, AutoModerationRuleTriggerType.spam, event_type=AutoModerationEventType.none.value,
    )
    
    vampytest.assert_is(rule.event_type, AutoModerationEventType.none)


def test__AutoModerationRule__constructor__event_type_2():
    """
    Tests whether ``AutoModerationRule`` checks `event_type` parameter as expected.
    Case : `'owo'`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, event_type='owo')


def test__AutoModerationRule__constructor__event_type_3():
    """
    Tests whether ``AutoModerationRule`` sets `.event_type` attribute as expected.
    Case : *default*
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    vampytest.assert_instance(rule.event_type, AutoModerationEventType)


def test__AutoModerationRule__constructor__excluded_channels_0():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_channel_ids` attribute as expected.
    Case : `None`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=None)
    
    vampytest.assert_is(rule.excluded_channel_ids, None)


def test__AutoModerationRule__constructor__excluded_channels_1():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_channel_ids` attribute as expected.
    Case : `[]`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=[])
    
    vampytest.assert_is(rule.excluded_channel_ids, None)


def test__AutoModerationRule__constructor__excluded_channels_2():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_channel_ids` attribute as expected.
    Case : `69`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=69)
    
    vampytest.assert_eq(rule.excluded_channel_ids, (69, ))


def test__AutoModerationRule__constructor__excluded_channels_3():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_channel_ids` attribute as expected.
    Case : `Channel.precreate(69)`.
    """
    rule = AutoModerationRule(
        'name', None, AutoModerationRuleTriggerType.spam, excluded_channels=Channel.precreate(69)
    )
    
    vampytest.assert_eq(rule.excluded_channel_ids, (69, ))



def test__AutoModerationRule__constructor__excluded_channels_4():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_channel_ids` attribute as expected.
    Case : `[69]`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=[69])
    
    vampytest.assert_eq(rule.excluded_channel_ids, (69, ))


def test__AutoModerationRule__constructor__excluded_channels_5():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_channel_ids` attribute as expected.
    Case : `[Channel.precreate(69)]`.
    """
    rule = AutoModerationRule(
        'name', None, AutoModerationRuleTriggerType.spam, excluded_channels=[Channel.precreate(69)]
    )
    
    vampytest.assert_eq(rule.excluded_channel_ids, (69, ))


def test__AutoModerationRule__constructor__excluded_channels_6():
    """
    Tests whether ``AutoModerationRule`` checks `excluded_channels` parameter as expected.
    Case : `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=12.6)


def test__AutoModerationRule__constructor__excluded_channels_7():
    """
    Tests whether ``AutoModerationRule`` checks `excluded_channels` parameter as expected.
    Case : `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_channels=[12.6])


def test__AutoModerationRule__constructor__excluded_channels_8():
    """
    Tests whether ``AutoModerationRule`` checks `excluded_channels` parameter as expected.
    Case : *default*.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)

    vampytest.assert_is(rule.excluded_channel_ids, None)


def test__AutoModerationRule__constructor__excluded_roles_0():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_role_ids` attribute as expected.
    Case : `None`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=None)
    
    vampytest.assert_is(rule.excluded_role_ids, None)


def test__AutoModerationRule__constructor__excluded_roles_1():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_role_ids` attribute as expected.
    Case : `[]`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=[])
    
    vampytest.assert_is(rule.excluded_role_ids, None)


def test__AutoModerationRule__constructor__excluded_roles_2():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_role_ids` attribute as expected.
    Case : `69`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=69)
    
    vampytest.assert_eq(rule.excluded_role_ids, (69, ))


def test__AutoModerationRule__constructor__excluded_roles_3():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_role_ids` attribute as expected.
    Case : `Role.precreate(69)`.
    """
    rule = AutoModerationRule(
        'name', None, AutoModerationRuleTriggerType.spam, excluded_roles=Role.precreate(69)
    )
    
    vampytest.assert_eq(rule.excluded_role_ids, (69, ))



def test__AutoModerationRule__constructor__excluded_roles_4():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_role_ids` attribute as expected.
    Case : `[69]`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=[69])
    
    vampytest.assert_eq(rule.excluded_role_ids, (69, ))


def test__AutoModerationRule__constructor__excluded_roles_5():
    """
    Tests whether ``AutoModerationRule`` sets `.excluded_role_ids` attribute as expected.
    Case : `[Role.precreate(69)]`.
    """
    rule = AutoModerationRule(
        'name', None, AutoModerationRuleTriggerType.spam, excluded_roles=[Role.precreate(69)]
    )
    
    vampytest.assert_eq(rule.excluded_role_ids, (69, ))


def test__AutoModerationRule__constructor__excluded_roles_6():
    """
    Tests whether ``AutoModerationRule` checks `excluded_roles` parameter as expected.
    Case : `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=12.6)


def test__AutoModerationRule__constructor__excluded_roles_7():
    """
    Tests whether ``AutoModerationRule``'s `excluded_roles` parameter as expected.
    Case : `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam, excluded_roles=[12.6])


def test__AutoModerationRule__constructor__excluded_roles_8():
    """
    Tests whether ``AutoModerationRule``'s `excluded_roles` parameter as expected.
    Case : *default*.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)

    vampytest.assert_is(rule.excluded_role_ids, None)


def test__AutoModerationRule__constructor__keyword_presets_0():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_type` is set as expected when passing the `keyword_presets`
    parameter.
    """
    rule = AutoModerationRule('name', None, keyword_presets=None)

    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.keyword_preset)


def test__AutoModerationRule__constructor__keyword_presets_1():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata` is set as expected when passing the
    `keyword_presets` parameter.
    """
    rule = AutoModerationRule('name', None, keyword_presets=None)

    vampytest.assert_instance(rule.trigger_metadata, KeywordPresetTriggerMetadata)


def test__AutoModerationRule__constructor__keyword_presets_2():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keyword_presets` is set as expected when passing
    the `keyword_presets` parameter.
    Case: `None`.
    """
    rule = AutoModerationRule('name', None, keyword_presets=None)

    vampytest.assert_is(rule.trigger_metadata.keyword_presets, None)


def test__AutoModerationRule__constructor__keyword_presets_3():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keyword_presets` is set as expected when passing
    the `keyword_presets` parameter.
    Case: `[]`.
    """
    rule = AutoModerationRule('name', None, keyword_presets=[])

    vampytest.assert_is(rule.trigger_metadata.keyword_presets, None)


def test__AutoModerationRule__constructor__keyword_presets_4():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keyword_presets` is set as expected when passing
    the `keyword_presets` parameter.
    Case: `AutoModerationKeywordPresetType.cursing`.
    """
    rule = AutoModerationRule('name', None, keyword_presets=AutoModerationKeywordPresetType.cursing)

    vampytest.assert_eq(rule.trigger_metadata.keyword_presets, (AutoModerationKeywordPresetType.cursing, ))


def test__AutoModerationRule__constructor__keyword_presets_5():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keyword_presets` is set as expected when passing
    the `keyword_presets` parameter.
    Case: `AutoModerationKeywordPresetType.cursing.value`.
    """
    rule = AutoModerationRule('name', None, keyword_presets=AutoModerationKeywordPresetType.cursing.value)

    vampytest.assert_eq(rule.trigger_metadata.keyword_presets, (AutoModerationKeywordPresetType.cursing, ))


def test__AutoModerationRule__constructor__keyword_presets_6():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keyword_presets` is set as expected when passing
    the `keyword_presets` parameter.
    Case: `[AutoModerationKeywordPresetType.cursing]`.
    """
    rule = AutoModerationRule('name', None, keyword_presets=[AutoModerationKeywordPresetType.cursing])

    vampytest.assert_eq(rule.trigger_metadata.keyword_presets, (AutoModerationKeywordPresetType.cursing, ))


def test__AutoModerationRule__constructor__keyword_presets_7():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keyword_presets` is set as expected when passing
    the `keyword_presets` parameter.
    Case: `[AutoModerationKeywordPresetType.cursing.value]`.
    """
    rule = AutoModerationRule('name', None, keyword_presets=[AutoModerationKeywordPresetType.cursing.value])

    vampytest.assert_eq(rule.trigger_metadata.keyword_presets, (AutoModerationKeywordPresetType.cursing, ))


def test__AutoModerationRule__constructor__keyword_presets_8():
    """
    Tests whether ``AutoModerationRule`` checks `.keyword_presets` parameter as expected.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, keyword_presets=[12.6])


def test__AutoModerationRule__constructor__keyword_presets_9():
    """
    Tests whether ``AutoModerationRule`` checks `.trigger_metadata.keyword_presets` is set as expected when passing
    the `keyword_presets` parameter.
    Case: `[12.6]`
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, keyword_presets=[12.6])


def test__AutoModerationRule__constructor__keywords_0():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_type` is set as expected when passing the `keywords`
    parameter.
    """
    rule = AutoModerationRule('name', None, keywords=None)

    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.keyword)


def test__AutoModerationRule__constructor__keywords_1():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata` is set as expected when passing the
    `keywords` parameter.
    """
    rule = AutoModerationRule('name', None, keywords=None)

    vampytest.assert_instance(rule.trigger_metadata, KeywordTriggerMetadata)


def test__AutoModerationRule__constructor__keywords_2():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keywords` is set as expected when passing
    the `keywords` parameter.
    Case: `None`.
    """
    rule = AutoModerationRule('name', None, keywords=None)

    vampytest.assert_is(rule.trigger_metadata.keywords, None)


def test__AutoModerationRule__constructor__keywords_3():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keywords` is set as expected when passing
    the `keywords` parameter.
    Case: `[]`.
    """
    rule = AutoModerationRule('name', None, keywords=[])

    vampytest.assert_is(rule.trigger_metadata.keywords, None)


def test__AutoModerationRule__constructor__keywords_4():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keywords` is set as expected when passing
    the `keywords` parameter.
    Case: `'cursing'`.
    """
    rule = AutoModerationRule('name', None, keywords='cursing')

    vampytest.assert_eq(rule.trigger_metadata.keywords, ('cursing', ))


def test__AutoModerationRule__constructor__keywords_5():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata.keywords` is set as expected when passing
    the `keywords` parameter.
    Case: `['cursing']`.
    """
    rule = AutoModerationRule('name', None, keywords=['cursing'])

    vampytest.assert_eq(rule.trigger_metadata.keywords, ('cursing', ))



def test__AutoModerationRule__constructor__keywords_6():
    """
    Tests whether ``AutoModerationRule`` checks `.keywords` parameter as expected.
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, keywords=[12.6])


def test__AutoModerationRule__constructor__keywords_7():
    """
    Tests whether ``AutoModerationRule`` checks `.trigger_metadata.keywords` is set as expected when passing
    the `keywords` parameter.
    Case: `[12.6]`
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, keywords=[12.6])


def test__AutoModerationRule__constructor__trigger_type_match_None():
    """
    Tests whether the auto moderation rule's trigger type type & trigger ype specific keyword parameters are
    accepted at the same time. Case: `send_alert_message`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.keyword, keywords=None)
    
    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.keyword)


def test__AutoModerationRule__constructor__trigger_type_match_1():
    """
    Tests whether the auto moderation rule's trigger type type & trigger type specific keyword parameters are
    accepted at the same time. Case: `timeout`.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.keyword_preset, keyword_presets=None)
    
    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.keyword_preset)


def test__AutoModerationRule__constructor__trigger_type_contradiction_2():
    """
    Tests whether the auto moderation rule's trigger type & different trigger type specific keyword parameters are
    not accepted at the same time.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, AutoModerationRuleTriggerType.keyword_preset, keywords=None)


def test__AutoModerationRule__constructor__trigger_type_missing():
    """
    Tests whether the auto moderation rule requires trigger type to be specified.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None)


def test__AutoModerationRule__constructor__trigger_type_contradiction_1():
    """
    Tests whether the auto moderation rule's two trigger type specific parameters are not accepted at the same.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, keywords=None, keyword_presets=None)


def test__AutoModerationRule__constructor__name_0():
    """
    Tests whether ``AutoModerationRule``'s `.name` attribute is set as expected.
    """
    rule = AutoModerationRule('name', None, AutoModerationRuleTriggerType.spam)
    
    vampytest.assert_eq(rule.name, 'name')


def test__AutoModerationRule__constructor__name_1():
    """
    Tests whether ``AutoModerationRule``'s raises when `name` parameter is given with an invalid type.
    Case : `None`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule(None, None, AutoModerationRuleTriggerType.spam)


def test__AutoModerationRule__constructor__excluded_keywords_0():
    """
    Tests whether ``AutoModerationRule`` wont accept `excluded_keywords` alone.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, excluded_keywords=None)


def test__AutoModerationRule__constructor__excluded_keywords_1():
    """
    Tests whether ``AutoModerationRule`` wont accept `excluded_keywords` with `keywords`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRule('name', None, excluded_keywords=None, keywords=None)


def test__AutoModerationRule__constructor__excluded_keywords_2():
    """
    Tests whether ``AutoModerationRule`` wont accept `excluded_keywords` with `keyword_presets` correctly.
    """
    rule = AutoModerationRule(
        'name', None, excluded_keywords='owo', keyword_presets=AutoModerationKeywordPresetType.cursing
    )
    
    trigger_metadata = KeywordPresetTriggerMetadata(AutoModerationKeywordPresetType.cursing, 'owo')
    
    vampytest.assert_eq(rule.trigger_metadata, trigger_metadata)


def test__AutoModerationRule__constructor__mention_limit_0():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_type` is set as expected when passing the `mention_limit`
    parameter.
    """
    rule = AutoModerationRule('name', None, mention_limit=None)

    vampytest.assert_is(rule.trigger_type, AutoModerationRuleTriggerType.mention_spam)


def test__AutoModerationRule__constructor__mention_limit_1():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata` is set as expected when passing the
    `mention_limit` parameter.
    """
    rule = AutoModerationRule('name', None, mention_limit=None)

    vampytest.assert_instance(rule.trigger_metadata, MentionSpamTriggerMetadata)


def test__AutoModerationRule__constructor__mention_limit_2():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata`'s `.mention_limit` is set as expected.
    """
    rule = AutoModerationRule('name', None, mention_limit=20)

    vampytest.assert_eq(rule.trigger_metadata.mention_limit, 20)


def test__AutoModerationRule__constructor__mention_limit_3():
    """
    Tests whether ``AutoModerationRule`` wont accept `mention_limit` with other trigger metadata parameters.
    """
    with vampytest.assert_raises(TypeError):
        return AutoModerationRule('name', None, mention_limit=None, keywords=None)


def test__AutoModerationRule__constructor__mention_limit_4():
    """
    Tests whether ``AutoModerationRule``'s `.trigger_metadata`'s `.mention_limit` is type checked as expected
    """
    with vampytest.assert_raises(TypeError):
        return AutoModerationRule('name', None, mention_limit=12.6)
