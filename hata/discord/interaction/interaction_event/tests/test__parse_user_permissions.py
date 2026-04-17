import vampytest

from ....permission import Permission
from ....permission.permission import PERMISSION_PRIVATE

from ..fields import parse_user_permissions


def test__parse_user_permissions():
    """
    Tests whether ``parse_user_permissions`` works as intended.
    """
    for input_value, expected_output in (
        ({}, PERMISSION_PRIVATE),
        ({'member': {}}, PERMISSION_PRIVATE),
        ({'member': {'permissions': '69'}}, Permission(69)),
    ):
        output = parse_user_permissions(input_value)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)
