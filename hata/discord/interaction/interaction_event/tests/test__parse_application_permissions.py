import vampytest

from ....permission import Permission

from ..fields import parse_application_permissions


def test__parse_application_permissions():
    """
    Tests whether ``parse_application_permissions`` works as intended."""
    for input_data, expected_output in (
        ({}, Permission(0)),
        ({'app_permissions': 1}, Permission(1)),
    ):
        output = parse_application_permissions(input_data)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)
