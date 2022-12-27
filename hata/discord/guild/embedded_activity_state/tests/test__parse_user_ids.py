import vampytest

from ..fields import parse_user_ids


def test__parse_user_ids():
    """
    Tests whether ``parse_user_ids`` works as intended.
    """
    user_id_0 = 202212250007
    user_id_1 = 202212250008
    
    for input_data, expected_output in (
        ({}, set()),
        ({'users': None}, set()),
        ({'users': [str(user_id_0)]}, {user_id_0}),
        ({'users': [str(user_id_0), str(user_id_1)]}, {user_id_0, user_id_1}),
    ):
        output = parse_user_ids(input_data)
        vampytest.assert_eq(output, expected_output)
