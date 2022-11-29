import vampytest

from ....user import User

from ..fields import put_user_into


def test__put_user_into():
    """
    Tests whether ``put_user_into`` is working as intended.
    """
    user = User.precreate(202211230001, name = 'Ken')
    
    for input_, defaults, expected_output in (
        (user, True, {'user': user.to_data(defaults = True, include_internals = True)}),
    ):
        data = put_user_into(input_, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
