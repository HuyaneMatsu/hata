import vampytest

from ...forum_tag import ForumTag

from ..forum_tag_update import ForumTagUpdate


def test__ForumTagUpdate__repr():
    """
    Tests whether ``ForumTagUpdate.__repr__`` works as intended.
    """
    forum_tag = ForumTag('hello')
    old_attributes = {'a': 'b'}
    
    forum_tag_update = ForumTagUpdate(
        forum_tag = forum_tag,
        old_attributes = old_attributes,
    )
    vampytest.assert_instance(repr(forum_tag_update), str)


def test__ForumTagUpdate__hash():
    """
    Tests whether ``ForumTagUpdate.__hash__`` works as intended.
    """
    forum_tag = ForumTag('hello')
    old_attributes = {'a': 'b'}
    
    forum_tag_update = ForumTagUpdate(
        forum_tag = forum_tag,
        old_attributes = old_attributes,
    )
    vampytest.assert_instance(hash(forum_tag_update), int)


def test__ForumTagUpdate__eq():
    """
    Tests whether ``ForumTagUpdate.__eq__`` works as intended.
    """
    forum_tag = ForumTag('hello')
    old_attributes = {'a': 'b'}
    
    keyword_parameters = {    
        'forum_tag': forum_tag,
        'old_attributes': old_attributes,
    }
    
    forum_tag_update = ForumTagUpdate(**keyword_parameters)
    vampytest.assert_eq(forum_tag_update, forum_tag_update)
    vampytest.assert_ne(forum_tag_update, object())
    
    for field_name, field_value in (
        ('forum_tag',  ForumTag('hell')),
        ('old_attributes', {'everyone': 'lies'}),
    ):
        test_forum_tag_update = ForumTagUpdate(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(forum_tag_update, test_forum_tag_update)


def test__ForumTagUpdate__unpack():
    """
    Tests whether ``ForumTagUpdate`` unpacking works as intended.
    """
    forum_tag = ForumTag('hello')
    old_attributes = {'a': 'b'}
    
    forum_tag_update = ForumTagUpdate(
        forum_tag = forum_tag,
        old_attributes = old_attributes,
    )
    
    unpacked = [*forum_tag_update]
    vampytest.assert_eq(len(unpacked), len(forum_tag_update))
