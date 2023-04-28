import vampytest

from ..fields import put_user_ids_into


def test__put_user_ids_into():
    """
    Tests whether ``put_user_ids_into`` is working as intended.
    """
    user_id_1 = 202304270004
    
    for input_value, defaults, expected_output in (
        (None, False, {'participants': []}),
        (None, True, {'participants': []}),
        ((user_id_1,), False, {'participants': [str(user_id_1)]}),
    ):
        data = put_user_ids_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
