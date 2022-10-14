import vampytest

from ...forum_tag import ForumTag

from ..available_tags import validate_available_tags


def test__validate_available_tags__0():
    """
    Tests whether ``validate_available_tags`` works as intended.
    
    Case: passing.
    """
    forum_tag = ForumTag(name = 'ExistRuth')
    
    for input_parameter, expected_output in (
        (None, None),
        ([], None),
        ([forum_tag], (forum_tag, ))
    ):
        output = validate_available_tags(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_available_tags__1():
    """
    Tests whether ``validate_available_tags`` works as intended.
    
    Case: `TypeError`.
    """
    for input_parameter in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_available_tags(input_parameter)
