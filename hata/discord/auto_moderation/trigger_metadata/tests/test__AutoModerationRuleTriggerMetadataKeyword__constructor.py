import vampytest

from hata.discord.auto_moderation import AutoModerationRuleTriggerMetadataKeyword


def test__AutoModerationRuleTriggerMetadataKeyword__new__0():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` returns as expected.
    
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword(None)
    
    vampytest.assert_instance(metadata, AutoModerationRuleTriggerMetadataKeyword)


def test__AutoModerationRuleTriggerMetadataKeyword__new__1():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` sets `.keywords` as expected.
    
    Case: `None`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword(None)
    
    vampytest.assert_is(metadata.keywords, None)


def test__AutoModerationRuleTriggerMetadataKeyword__new__2():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` sets `.keywords` as expected.
    
    Case: `[]`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword([])
    
    vampytest.assert_is(metadata.keywords, None)


def test__AutoModerationRuleTriggerMetadataKeyword__new__3():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` sets `.keywords` as expected.
    
    Case: `'owo'`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword('owo')
    
    vampytest.assert_eq(metadata.keywords, ('owo', ))


def test__AutoModerationRuleTriggerMetadataKeyword__new__4():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` sets `.keywords` as expected.
    Case: `['owo']`.
    """
    metadata = AutoModerationRuleTriggerMetadataKeyword(['owo'])
    
    vampytest.assert_eq(metadata.keywords, ('owo', ))


def test__AutoModerationRuleTriggerMetadataKeyword__new__5():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` raises as expected on bad parameter.
    
    Case: `12.6`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRuleTriggerMetadataKeyword(12.6)


def test__AutoModerationRuleTriggerMetadataKeyword__new__6():
    """
    Tests whether ``AutoModerationRuleTriggerMetadataKeyword.__new__`` raises as expected on bad parameter.
    
    Case: `[12.6]`.
    """
    with vampytest.assert_raises(TypeError):
        AutoModerationRuleTriggerMetadataKeyword([12.6])
