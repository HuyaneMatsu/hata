import vampytest

from ....core import BUILTIN_EMOJIS, FORUM_TAGS
from ....emoji import Emoji

from .. import ForumTag


def test__ForumTag__new__0():
    """
    Tests whether ``ForumTag.__new__`` works as intended.
    
    Case: No fields given.
    """
    forum_tag = ForumTag('')
    
    vampytest.assert_instance(forum_tag, ForumTag)
    
    vampytest.assert_instance(forum_tag.id, int)
    vampytest.assert_instance(forum_tag.name, str)
    vampytest.assert_instance(forum_tag.emoji, Emoji, nullable = True)
    vampytest.assert_instance(forum_tag.moderated, bool)


def test__ForumTag__new__1():
    """
    Tests whether ``ForumTag.__new__`` works as intended.
    
    Case: All fields given.
    """
    emoji = BUILTIN_EMOJIS['heart']
    name = 'EMOTiON'
    moderated = True
    
    forum_tag = ForumTag(name, emoji = emoji, moderated = moderated)
    
    vampytest.assert_instance(forum_tag, ForumTag)
    
    vampytest.assert_instance(forum_tag.id, int)
    vampytest.assert_eq(forum_tag.name, name)
    vampytest.assert_is(forum_tag.emoji, emoji)
    vampytest.assert_eq(forum_tag.moderated, moderated)


def test__ForumTag__create_empty():
    """
    Tests whether ``ForumTag._create_empty`` works as intended.
    """
    forum_tag_id = 202209090001
    
    forum_tag = ForumTag._create_empty(forum_tag_id)
    
    vampytest.assert_instance(forum_tag, ForumTag)
    vampytest.assert_eq(forum_tag.id, forum_tag_id)
    
    vampytest.assert_instance(forum_tag.name, str)
    vampytest.assert_instance(forum_tag.emoji, Emoji, nullable = True)
    vampytest.assert_instance(forum_tag.moderated, bool)


def test__ForumTag__precreate__0():
    """
    Tests whether ``ForumTag.precreate`` works as intended.
    
    Case: checking cache and fields.
    """
    forum_tag_id = 202209090003
    emoji = BUILTIN_EMOJIS['heart']
    name = 'EMOTiON'
    moderated = True
    
    forum_tag = ForumTag.precreate(forum_tag_id, name = name, emoji = emoji, moderated = moderated)
    
    vampytest.assert_instance(forum_tag, ForumTag)
    vampytest.assert_eq(forum_tag.id, forum_tag_id)
    
    vampytest.assert_in(forum_tag_id, FORUM_TAGS)
    vampytest.assert_is(FORUM_TAGS[forum_tag_id], forum_tag)
    
    vampytest.assert_eq(forum_tag.name, name)
    vampytest.assert_is(forum_tag.emoji, emoji)
    vampytest.assert_eq(forum_tag.moderated, moderated)


def test__ForumTag__precreate__1():
    """
    Tests whether ``ForumTag.precreate`` works as intended.
    
    Case: duplicate call.
    """
    forum_tag_id = 202209090004
    
    forum_tag = ForumTag.precreate(forum_tag_id)
    new_forum_tag = ForumTag.precreate(forum_tag_id)
    
    vampytest.assert_is(forum_tag, new_forum_tag)
