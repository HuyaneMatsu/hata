import vampytest

from ...forum_tag import ForumTag
from ...forum_tag_update import ForumTagUpdate

from ..forum_tag_change import ForumTagChange


def test__ForumTagChange__repr():
    """
    Tests whether ``ForumTagChange.__repr__`` works as intended.
    """
    added = [ForumTag('hello')]
    updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    removed = [ForumTag('innit')]
    
    forum_tag_change = ForumTagChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    vampytest.assert_instance(repr(forum_tag_change), str)


def test__ForumTagChange__hash():
    """
    Tests whether ``ForumTagChange.__hash__`` works as intended.
    """
    added = [ForumTag('hello')]
    updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    removed = [ForumTag('innit')]
    
    forum_tag_change = ForumTagChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    vampytest.assert_instance(hash(forum_tag_change), int)


def test__ForumTagChange__eq():
    """
    Tests whether ``ForumTagChange.__eq__`` works as intended.
    """
    added = [ForumTag('hello')]
    updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    removed = [ForumTag('innit')]
    
    keyword_parameters = {    
        'added': added,
        'updated': updated,
        'removed': removed,
    }
    
    forum_tag_change = ForumTagChange(**keyword_parameters)
    vampytest.assert_eq(forum_tag_change, forum_tag_change)
    vampytest.assert_ne(forum_tag_change, object())
    
    for field_name, field_value in (
        ('added',  None),
        ('updated', None),
        ('removed', None),
    ):
        test_forum_tag_change = ForumTagChange(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(forum_tag_change, test_forum_tag_change)


def test__ForumTagChange__unpack():
    """
    Tests whether ``ForumTagChange`` unpacking works as intended.
    """
    added = [ForumTag('hello')]
    updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    removed = [ForumTag('innit')]
    
    forum_tag_change = ForumTagChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    unpacked = [*forum_tag_change]
    vampytest.assert_eq(len(unpacked), len(forum_tag_change))
