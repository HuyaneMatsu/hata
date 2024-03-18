import vampytest

from ..utils import create_partial_forum_tag_from_id


def test__create_partial_forum_tag_from_id():
    """
    Tests whether ``create_partial_forum_tag_from_id`` returns the same forum tag for the same id if cached.
    """
    forum_tag_id = 202209110000
    
    forum_tag_1 = create_partial_forum_tag_from_id(forum_tag_id)
    forum_tag_2 = create_partial_forum_tag_from_id(forum_tag_id)
    
    vampytest.assert_is(forum_tag_1, forum_tag_2)
