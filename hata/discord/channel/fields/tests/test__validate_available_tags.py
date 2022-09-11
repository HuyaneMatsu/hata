import vampytest

from ...forum_tag import ForumTag

from ..available_tags import validate_available_tags


def test__validate_available_tags():
    """
    Tests whether ``validate_available_tags`` works as intended.
    """
    forum_tag = ForumTag(name = 'ExistRuth')
    
    for input_parameter, expected_output in (
        (None, None),
        ([], None),
        ([forum_tag], (forum_tag, ))
    ):
        output = validate_available_tags(input_parameter)
        vampytest.assert_eq(output, expected_output)
