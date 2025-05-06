import vampytest

from ...forum_tag import ForumTag

from ..fields import put_available_tags


def test__put_available_tags():
    """
    Tests whether ``put_available_tags`` works as intended.
    
    Case: include internals.
    """
    forum_tag = ForumTag.precreate(202209110002, name = 'ExistRuth')
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'available_tags': []}),
        ([forum_tag], False, {'available_tags': [forum_tag.to_data(include_internals = True)]}),
    ):
        data = put_available_tags(input_, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
