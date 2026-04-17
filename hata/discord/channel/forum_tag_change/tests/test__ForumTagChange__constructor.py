import vampytest

from ...forum_tag import ForumTag
from ...forum_tag_update import ForumTagUpdate

from ..forum_tag_change import ForumTagChange


def _assert_fields_set(forum_tag_change):
    """
    Tests whether all fields are set of the given forum_tag change.
    
    Parameters
    ----------
    forum_tag_change : ``ForumTagChange``
        The forum_tag change to check.
    """
    vampytest.assert_instance(forum_tag_change, ForumTagChange)
    vampytest.assert_instance(forum_tag_change.added, list, nullable = True)
    vampytest.assert_instance(forum_tag_change.updated, list, nullable = True)
    vampytest.assert_instance(forum_tag_change.removed, list, nullable = True)


def test__ForumTagChange__new__0():
    """
    Tests whether ``ForumTagChange.__new__`` works as intended.
    
    Case: No fields given.
    """
    forum_tag_change = ForumTagChange()
    _assert_fields_set(forum_tag_change)


def test__ForumTagChange__new__1():
    """
    Tests whether ``ForumTagChange.__new__`` works as intended.
    
    Case: All fields given.
    """
    added = [ForumTag('hello')]
    updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    removed = [ForumTag('innit')]
    
    forum_tag_change = ForumTagChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    _assert_fields_set(forum_tag_change)

    vampytest.assert_eq(forum_tag_change.added, added)
    vampytest.assert_eq(forum_tag_change.updated, updated)
    vampytest.assert_eq(forum_tag_change.removed, removed)


def test__ForumTagChange__from_fields():
    """
    Tests whether ``ForumTagChange.__new__`` works as intended.
    
    Case: All fields given.
    """
    added = [ForumTag('hello')]
    updated = [ForumTagUpdate(old_attributes = {'a': 'b'})]
    removed = [ForumTag('innit')]
    
    forum_tag_change = ForumTagChange.from_fields(added, updated, removed)
    _assert_fields_set(forum_tag_change)

    vampytest.assert_eq(forum_tag_change.added, added)
    vampytest.assert_eq(forum_tag_change.updated, updated)
    vampytest.assert_eq(forum_tag_change.removed, removed)
