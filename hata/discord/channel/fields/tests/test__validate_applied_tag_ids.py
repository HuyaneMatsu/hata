import vampytest

from ...forum_tag import ForumTag

from ..applied_tag_ids import validate_applied_tag_ids


def test__validate_applied_tag_ids__0():
    """
    Tests whether `validate_applied_tag_ids` works as intended.
    
    Case: passing.
    """
    forum_tag_id_1 = 202209140024
    forum_tag_id_2 = 202209140025
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([forum_tag_id_2, forum_tag_id_1], (forum_tag_id_1, forum_tag_id_2)),
        ([ForumTag.precreate(forum_tag_id_1)], (forum_tag_id_1, )),
    ):
        output = validate_applied_tag_ids(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_applied_tag_ids__1():
    """
    Tests whether `validate_applied_tag_ids` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_applied_tag_ids(input_value)
