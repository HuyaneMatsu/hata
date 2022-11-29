import vampytest

from ..fields import put_owner_id_into


def test__put_owner_id_into():
    """
    Tests whether ``put_owner_id_into`` is working as intended.
    """
    owner_id = 202211270006
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'owner_id': None}),
        (owner_id, False, {'owner_id': str(owner_id)}),
    ):
        data = put_owner_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
