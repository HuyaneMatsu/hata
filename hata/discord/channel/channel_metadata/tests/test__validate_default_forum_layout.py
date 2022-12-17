import vampytest

from ..fields import validate_default_forum_layout
from ..preinstanced import ForumLayout


def test__validate_default_forum_layout__0():
    """
    Validates whether ``validate_default_forum_layout`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, ForumLayout.none),
        (ForumLayout.list, ForumLayout.list),
        (ForumLayout.list.value, ForumLayout.list)
    ):
        output = validate_default_forum_layout(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_default_forum_layout__1():
    """
    Validates whether ``validate_default_forum_layout`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_default_forum_layout(input_value)
