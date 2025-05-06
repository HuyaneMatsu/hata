import vampytest

from ..fields import put_owner_id


def test__put_owner_id():
    """
    Tests whether ``put_owner_id`` works as intended.
    """
    owner_id = 202211230018
    
    for input_, defaults, expected_output in (
        (owner_id, False, {'owner_user_id': str(owner_id)}),
    ):
        data = put_owner_id(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
