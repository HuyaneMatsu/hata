import vampytest

from ..fields import parse_user_id


def test__parse_user_id():
    """
    Tests whether ``parse_user_id`` works as intended.
    """
    user_id = 202211160004
    
    for input_data, expected_output in (
        ({}, 0),
        ({'user_id': None}, 0),
        ({'user_id': str(user_id)}, user_id),
    ):
        output = parse_user_id(input_data)
        vampytest.assert_eq(output, expected_output)
