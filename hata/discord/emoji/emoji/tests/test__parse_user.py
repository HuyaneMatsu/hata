import vampytest

from ....user import User, ZEROUSER

from ..fields import parse_user


def test__parse_user():
    """
    Tests whether ``parse_user`` works as intended.
    """
    user = User.precreate(202212310010, name = 'Ken')
    
    for input_data, expected_output in (
        ({}, ZEROUSER),
        ({'user': None}, ZEROUSER),
        ({'user': user.to_data()}, user),
    ):
        output = parse_user(input_data)
        vampytest.assert_is(output, expected_output)
