import vampytest

from ...user import User

from ..fields import validate_additional_owner_ids


def test__validate_additional_owner_ids__0():
    """
    Tests whether `validate_additional_owner_ids` works as intended.
    
    Case: passing.
    """
    user_id_0 = 202302100000
    user_id_1 = 202302100001
    
    for input_value, expected_output in (
        (None, None),
        (user_id_0, {user_id_0}),
        (User.precreate(user_id_1), {user_id_1}),
        ([], None),
        ([user_id_0], {user_id_0}),
        ([User.precreate(user_id_0)], {user_id_0}),
        ([user_id_0, user_id_1], {user_id_0, user_id_1}),
    ):
        output = validate_additional_owner_ids(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_additional_owner_ids__1():
    """
    Tests whether `validate_additional_owner_ids` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_additional_owner_ids(input_value)
