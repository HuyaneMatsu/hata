import vampytest

from ...forum_tag import ForumTag

from ..fields import validate_removed


def test__validate_removed__0():
    """
    Tests whether ``validate_removed`` works as intended.
    
    Case: passing.
    """
    forum_tag = ForumTag('tsuki')
    
    for input_value, expected_output in (
        ([], None),
        ([forum_tag], [forum_tag]),
        (None, None),
    ):
        output = validate_removed(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_removed__1():
    """
    Tests whether ``validate_removed`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.5,
        [12.6,]
    ):
        with vampytest.assert_raises(TypeError):
            validate_removed(input_value)
