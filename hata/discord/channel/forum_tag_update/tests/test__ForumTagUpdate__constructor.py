import vampytest

from ...forum_tag import ForumTag

from ..forum_tag_update import ForumTagUpdate


def _assert_fields_set(forum_tag_update):
    """
    Tests whether all fields are set of the given forum_tag update.
    
    Parameters
    ----------
    forum_tag_update : ``ForumTagUpdate``
        The forum_tag update to check.
    """
    vampytest.assert_instance(forum_tag_update, ForumTagUpdate)
    vampytest.assert_instance(forum_tag_update.forum_tag, ForumTag)
    vampytest.assert_instance(forum_tag_update.old_attributes, dict)


def test__ForumTagUpdate__new__0():
    """
    Tests whether ``ForumTagUpdate.__new__`` works as intended.
    
    Case: No fields given.
    """
    forum_tag_update = ForumTagUpdate()
    _assert_fields_set(forum_tag_update)


def test__ForumTagUpdate__new__1():
    """
    Tests whether ``ForumTagUpdate.__new__`` works as intended.
    
    Case: All fields given.
    """
    forum_tag = ForumTag('hello')
    old_attributes = {'a': 'b'}
    
    forum_tag_update = ForumTagUpdate(
        forum_tag = forum_tag,
        old_attributes = old_attributes,
    )
    _assert_fields_set(forum_tag_update)

    vampytest.assert_eq(forum_tag_update.forum_tag, forum_tag)
    vampytest.assert_eq(forum_tag_update.old_attributes, old_attributes)


def test__ForumTagUpdate__from_fields():
    """
    Tests whether ``ForumTagUpdate.__new__`` works as intended.
    
    Case: All fields given.
    """
    forum_tag = ForumTag('hello')
    old_attributes = {'a': 'b'}
    
    forum_tag_update = ForumTagUpdate.from_fields(forum_tag, old_attributes)
    _assert_fields_set(forum_tag_update)

    vampytest.assert_eq(forum_tag_update.forum_tag, forum_tag)
    vampytest.assert_eq(forum_tag_update.old_attributes, old_attributes)
