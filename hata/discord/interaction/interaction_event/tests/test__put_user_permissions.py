import vampytest

from ....permission import Permission

from ..fields import put_user_permissions


def test__put_user_permissions():
    """
    Tests whether ``put_user_permissions`` works as intended.
    """
    for input_value, input_data, expected_output in (
        (Permission(12), {}, {}),
        (Permission(12), {'member': {}}, {'member': {'permissions': '12'}}),
    ):
        output = put_user_permissions(input_value, input_data, True)
        vampytest.assert_eq(output, expected_output)
