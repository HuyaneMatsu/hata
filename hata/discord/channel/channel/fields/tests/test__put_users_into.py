import vampytest

from .....user import User

from ..users import put_users_into


def test__put_users_into():
    """
    Tests whether ``put_users_into`` is working as intended.
    """
    user_id_1 = 202209150004
    
    user_1 = User.precreate(user_id_1)
    
    for input_, defaults, expected_output in (
        ([], False, {'recipients': []}),
        ([user_1], False, {'recipients': [user_1.to_data()]}),
    ):
        data = put_users_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
