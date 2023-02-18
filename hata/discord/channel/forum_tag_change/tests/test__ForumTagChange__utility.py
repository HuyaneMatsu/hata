import vampytest

from ...forum_tag import ForumTag
from ...forum_tag_update import ForumTagUpdate

from ..forum_tag_change import ForumTagChange


from .test__ForumTagChange__constructor import _assert_fields_set


def test__ForumTagChange__copy():
    """
    Tests whether ``ForumTagChange.copy`` works as intended.
    """
    added = [ForumTag('hello')]
    updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    removed = [ForumTag('innit')]
    
    forum_tag_change = ForumTagChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    copy = forum_tag_change.copy()
    _assert_fields_set(forum_tag_change)
    vampytest.assert_is_not(forum_tag_change, copy)
    vampytest.assert_eq(forum_tag_change, copy)


def test__ForumTagChange__copy_with__0():
    """
    Tests whether ``ForumTagChange.copy_with`` works as intended.
    
    Case: No fields given.
    """
    added = [ForumTag('hello')]
    updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    removed = [ForumTag('innit')]
    
    forum_tag_change = ForumTagChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    copy = forum_tag_change.copy_with()
    _assert_fields_set(forum_tag_change)
    vampytest.assert_is_not(forum_tag_change, copy)
    vampytest.assert_eq(forum_tag_change, copy)



def test__ForumTagChange__copy_with__1():
    """
    Tests whether ``ForumTagChange.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_added = [ForumTag('hello')]
    old_updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    old_removed = [ForumTag('innit')]
    new_added = [ForumTag('hell')]
    new_updated = [ForumTagUpdate(old_attributes = {'b': 'c'})]
    new_removed = [ForumTag('yall')]
    
    forum_tag_change = ForumTagChange(
        added = old_added,
        updated = old_updated,
        removed = old_removed,
    )
    
    copy = forum_tag_change.copy_with(
        added = new_added,
        updated = new_updated,
        removed = new_removed,
    )
    
    _assert_fields_set(forum_tag_change)
    vampytest.assert_is_not(forum_tag_change, copy)

    vampytest.assert_eq(copy.added, new_added)
    vampytest.assert_eq(copy.updated, new_updated)
    vampytest.assert_eq(copy.removed, new_removed)


def test__ForumTagChange__iter_added():
    """
    Tests whether ``ForumTagChange.iter_added`` works as intended.
    """
    forum_tag_0 = ForumTag('hello')
    forum_tag_1 = ForumTag('hell')
    
    for input_value, expected_output in (
        (None, []),
        ([forum_tag_0], [forum_tag_0]),
        ([forum_tag_0, forum_tag_1], [forum_tag_0, forum_tag_1]),
    ):
        forum_tag_change = ForumTagChange(
            added = input_value,
        )
        
        vampytest.assert_eq([*forum_tag_change.iter_added()], expected_output)


def test__ForumTagChange__iter_removed():
    """
    Tests whether ``ForumTagChange.iter_removed`` works as intended.
    """
    forum_tag_0 = ForumTag('hello')
    forum_tag_1 = ForumTag('hell')
    
    for input_value, expected_output in (
        (None, []),
        ([forum_tag_0], [forum_tag_0]),
        ([forum_tag_0, forum_tag_1], [forum_tag_0, forum_tag_1]),
    ):
        forum_tag_change = ForumTagChange(
            removed = input_value,
        )
        
        vampytest.assert_eq([*forum_tag_change.iter_removed()], expected_output)


def test__ForumTagChange__iter_updated():
    """
    Tests whether ``ForumTagChange.iter_updated`` works as intended.
    """
    forum_tag_update_0 = ForumTagUpdate(forum_tag = ForumTag('hello'))
    forum_tag_update_1 = ForumTagUpdate(forum_tag = ForumTag('hell'))
    
    for input_value, expected_output in (
        (None, []),
        ([forum_tag_update_0], [forum_tag_update_0]),
        ([forum_tag_update_0, forum_tag_update_1], [forum_tag_update_0, forum_tag_update_1]),
    ):
        forum_tag_change = ForumTagChange(
            updated = input_value,
        )
        
        vampytest.assert_eq([*forum_tag_change.iter_updated()], expected_output)
