import vampytest

from ....role import Role

from ..fields import validate_mentioned_role_ids


def test__validate_mentioned_role_ids__0():
    """
    Tests whether `validate_mentioned_role_ids` works as intended.
    
    Case: passing.
    """
    role_id_1 = 202305010017
    role_id_2 = 202305010018
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([role_id_2, role_id_1], (role_id_1, role_id_2)),
        ([Role.precreate(role_id_1)], (role_id_1, )),
    ):
        output = validate_mentioned_role_ids(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_mentioned_role_ids__1():
    """
    Tests whether `validate_mentioned_role_ids` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_mentioned_role_ids(input_value)
