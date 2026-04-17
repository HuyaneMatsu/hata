import vampytest

from ...forum_tag import ForumTag

from ..fields import validate_forum_tag


def test__validate_forum_tag__0():
    """
    Tests whether ``validate_forum_tag`` works as intended.
    
    Case: passing.
    """
    forum_tag = ForumTag('tsuki')
    
    for input_value, expected_output in (
        (forum_tag, forum_tag),
    ):
        output = validate_forum_tag(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_forum_tag__1():
    """
    Tests whether ``validate_forum_tag`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
        None,
    ):
        with vampytest.assert_raises(TypeError):
            validate_forum_tag(input_value)
