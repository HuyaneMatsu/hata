import vampytest

from ....core import BUILTIN_EMOJIS

from .. import ForumTag


def test__ForumTag__copy():
    """
    Tests whether ``ForumTag.copy`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    name = 'EMOTiON'
    moderated = True
    
    forum_tag = ForumTag(name, emoji = emoji, moderated = moderated)
    
    copy = forum_tag.copy()
    
    vampytest.assert_instance(copy, ForumTag)
    
    vampytest.assert_instance(copy.id, int)
    vampytest.assert_eq(copy.name, name)
    vampytest.assert_is(copy.emoji, emoji)
    vampytest.assert_eq(copy.moderated, moderated)


def test__ForumTag__copy_with():
    """
    Tests whether ``ForumTag.copy_with`` works as intended.
    """
    old_emoji = BUILTIN_EMOJIS['heart']
    new_emoji = BUILTIN_EMOJIS['x']
    old_name = 'EMOTiON'
    new_name = 'EMPEROR'
    old_moderated = True
    new_moderated = False
    
    forum_tag = ForumTag(old_name, emoji = old_emoji, moderated = old_moderated)
    
    copy = forum_tag.copy_with(name = new_name, emoji = new_emoji, moderated = new_moderated)
    
    vampytest.assert_instance(copy, ForumTag)
    
    vampytest.assert_instance(copy.id, int)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.moderated, new_moderated)


def test__ForumTag__partial__0():
    """
    Tests whether ``ForumTag.partial`` works as intended.
    
    Case: partial.
    """
    forum_tag = ForumTag('')
    vampytest.assert_true(forum_tag.partial)


def test__ForumTag__partial__1():
    """
    Tests whether ``ForumTag.partial`` works as intended.
    
    Case: not partial.
    """
    forum_tag_id = 202209090007
    
    forum_tag = ForumTag._create_empty(forum_tag_id)
    
    vampytest.assert_false(forum_tag.partial)
