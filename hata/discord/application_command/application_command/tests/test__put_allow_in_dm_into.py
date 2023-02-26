import vampytest

from ..fields import put_allow_in_dm_into


def test__put_allow_in_dm_into():
    """
    Tests whether ``put_allow_in_dm_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (True, False, {}),
        (False, False, {'dm_permission': False}),
        (True, True, {'dm_permission': True}),
    ):
        data = put_allow_in_dm_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
