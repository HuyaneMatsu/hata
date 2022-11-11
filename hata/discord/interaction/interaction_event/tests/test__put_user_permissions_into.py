import vampytest

from ....permission import Permission

from ..fields import put_user_permissions_into


def test__put_user_permissions_into():
    """
    Tests whether ``put_user_permissions_into`` works as intended.
    """
    for input_value, input_data, expected_output in (
        (Permission(12), {}, {}),
        (Permission(12), {'member': {}}, {'member': {'permissions': '12'}}),
    ):
        output = put_user_permissions_into(input_value, input_data, True)
        vampytest.assert_eq(output, expected_output)
