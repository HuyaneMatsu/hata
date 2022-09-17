import vampytest

from ....user import User

from ..users import parse_users


def test__parse_users():
    """
    Tests whether ``parse_users`` works as intended.
    """
    user_id_1 = 202209150000
    user_id_2 = 202209150001
    
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    for input_data, expected_output in (
        ({}, []),
        ({'recipients': []}, []),
        ({'recipients': [user_1.to_data(), user_2.to_data()]}, [user_1, user_2]),
        ({'recipients': [user_2.to_data(), user_1.to_data()]}, [user_1, user_2]),
    ):
        output = parse_users(input_data)
        vampytest.assert_eq(output, expected_output)
