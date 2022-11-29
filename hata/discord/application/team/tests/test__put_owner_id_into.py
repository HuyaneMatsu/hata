import vampytest

from ..fields import put_owner_id_into


def test__put_owner_id_into():
    """
    Tests whether ``put_owner_id_into`` works as intended.
    """
    owner_id = 202211230018
    
    for input_, defaults, expected_output in (
        (owner_id, False, {'owner_user_id': str(owner_id)}),
    ):
        data = put_owner_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
