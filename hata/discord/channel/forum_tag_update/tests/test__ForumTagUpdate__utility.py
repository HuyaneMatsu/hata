import vampytest

from ...forum_tag import ForumTag

from ..forum_tag_update import ForumTagUpdate

from .test__ForumTagUpdate__constructor import _assert_fields_set


def test__ForumTagUpdate__copy():
    """
    Tests whether ``ForumTagUpdate.copy`` works as intended.
    """
    forum_tag = ForumTag('hello')
    old_attributes = {'a': 'b'}
    
    forum_tag_update = ForumTagUpdate(
        forum_tag = forum_tag,
        old_attributes = old_attributes,
    )
    
    copy = forum_tag_update.copy()
    _assert_fields_set(forum_tag_update)
    vampytest.assert_is_not(forum_tag_update, copy)
    vampytest.assert_eq(forum_tag_update, copy)


def test__ForumTagUpdate__copy_with__0():
    """
    Tests whether ``ForumTagUpdate.copy_with`` works as intended.
    
    Case: No fields given.
    """
    forum_tag = ForumTag('hello')
    old_attributes = {'a': 'b'}
    
    forum_tag_update = ForumTagUpdate(
        forum_tag = forum_tag,
        old_attributes = old_attributes,
    )
    
    copy = forum_tag_update.copy_with()
    _assert_fields_set(forum_tag_update)
    vampytest.assert_is_not(forum_tag_update, copy)
    vampytest.assert_eq(forum_tag_update, copy)



def test__ForumTagUpdate__copy_with__1():
    """
    Tests whether ``ForumTagUpdate.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_forum_tag = ForumTag('hello')
    old_old_attributes = {'a': 'b'}
    new_forum_tag = ForumTag('hell')
    new_old_attributes = {'b': 'c'}
    
    forum_tag_update = ForumTagUpdate(
        forum_tag = old_forum_tag,
        old_attributes = old_old_attributes,
    )
    
    copy = forum_tag_update.copy_with(
        forum_tag = new_forum_tag,
        old_attributes = new_old_attributes,
    )
    
    _assert_fields_set(forum_tag_update)
    vampytest.assert_is_not(forum_tag_update, copy)

    vampytest.assert_eq(copy.forum_tag, new_forum_tag)
    vampytest.assert_eq(copy.old_attributes, new_old_attributes)
