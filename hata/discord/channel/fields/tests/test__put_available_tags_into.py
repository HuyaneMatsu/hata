import vampytest

from ...forum_tag import ForumTag

from ..available_tags import put_available_tags_into


def test__put_available_tags_into():
    """
    Tests whether ``put_available_tags_into`` works as intended.
    
    Case: include internals.
    """
    forum_tag = ForumTag.precreate(202209110002, name = 'ExistRuth')
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'available_tags': []}),
        ([forum_tag], False, {'available_tags': [forum_tag.to_data(include_internals = True)]}),
    ):
        data = put_available_tags_into(input_, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
