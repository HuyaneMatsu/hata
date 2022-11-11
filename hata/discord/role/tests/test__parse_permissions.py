import vampytest

from ...permission import Permission

from ..fields import parse_permissions


def test__parse_permissions():
    """
    Tests whether ``parse_permissions`` works as intended."""
    for input_data, expected_output in (
        ({}, Permission(0)),
        ({'permissions': 1}, Permission(1)),
    ):
        output = parse_permissions(input_data)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)
