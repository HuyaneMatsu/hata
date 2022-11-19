import vampytest

from ..fields import put_user_id_into


def test__put_user_id_into():
    """
    Tests whether ``put_user_id_into`` is working as intended.
    """
    user_id = 202211160009
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'user_id': None}),
        (user_id, False, {'user_id': str(user_id)}),
    ):
        data = put_user_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
