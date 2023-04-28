import vampytest

from ....user import User

from ..fields import validate_user_ids


def test__validate_user_ids__0():
    """
    Tests whether `validate_user_ids` works as intended.
    
    Case: passing.
    """
    user_id_0 = 202304270005
    user_id_1 = 202304270006
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([user_id_0], (user_id_0,)),
        ([User.precreate(user_id_0)], (user_id_0,)),
        ([user_id_0, user_id_1], (user_id_0, user_id_1)),
    ):
        output = validate_user_ids(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_user_ids__1():
    """
    Tests whether `validate_user_ids` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_user_ids(input_value)
