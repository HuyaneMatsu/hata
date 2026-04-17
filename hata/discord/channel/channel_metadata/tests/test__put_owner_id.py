import vampytest

from ..fields import put_owner_id


def test__put_owner_id():
    """
    Tests whether ``put_owner_id`` is working as intended.
    """
    owner_id = 202211270006
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'owner_id': None}),
        (owner_id, False, {'owner_id': str(owner_id)}),
    ):
        data = put_owner_id(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
