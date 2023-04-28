import vampytest

from ..fields import parse_user_ids


def test__parse_user_ids():
    """
    Tests whether ``parse_user_ids`` works as intended.
    """
    user_id_0 = 202304270002
    user_id_1 = 202304270003
    
    for input_data, expected_output in (
        ({}, None),
        ({'participants': None}, None),
        ({'participants': [str(user_id_0)]}, (user_id_0,)),
        ({'participants': [str(user_id_0), str(user_id_1)]}, (user_id_0, user_id_1)),
    ):
        output = parse_user_ids(input_data)
        vampytest.assert_eq(output, expected_output)
