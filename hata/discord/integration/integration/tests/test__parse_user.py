import vampytest

from ....user import User

from ..fields import parse_user


def test__parse_user():
    """
    Tests whether ``parse_user`` works as intended.
    """
    user = User.precreate(202210140024, name = 'Ken')
    
    for input_data, expected_output in (
        ({'user': user.to_data(defaults = True, include_internals = True)}, user),
    ):
        output = parse_user(input_data)
        vampytest.assert_is(output, expected_output)
