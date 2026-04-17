import vampytest

from ....core import BUILTIN_EMOJIS

from ..forum_tag import ForumTag


def test__ForumTag__hash():
    """
    Tests whether ``ForumTag.__hash__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    name = 'EMOTiON'
    moderated = True
    
    forum_tag = ForumTag(name, emoji = emoji, moderated = moderated)
    
    vampytest.assert_instance(hash(forum_tag), int)


def test__ForumTag__repr():
    """
    Tests whether ``ForumTag.__repr__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    name = 'EMOTiON'
    moderated = True
    
    forum_tag = ForumTag(name, emoji = emoji, moderated = moderated)
    
    vampytest.assert_instance(repr(forum_tag), str)


def test__ForumTag__eq():
    """
    Tests whether ``ForumTag.__eq__`` works as intended.
    """
    fields = {
        'emoji': BUILTIN_EMOJIS['heart'],
        'name': 'EMOTiON',
        'moderated': True,
    }
    
    forum_tag = ForumTag(**fields)
    
    vampytest.assert_eq(forum_tag, forum_tag)
    vampytest.assert_ne(forum_tag, object())
    
    for field_name, field_value in (
        ('emoji', None),
        ('name', 'ALiCE\'S'),
        ('moderated', False),
    ):
        test_forum_tag = ForumTag(**{**fields, field_name: field_value})
        vampytest.assert_ne(forum_tag, test_forum_tag)
