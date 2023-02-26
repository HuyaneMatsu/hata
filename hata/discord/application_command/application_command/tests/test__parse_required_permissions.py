import vampytest

from ....permission import Permission

from ..fields import parse_required_permissions


def test__parse_required_permissions():
    """
    Tests whether ``parse_required_permissions`` works as intended.
    """
    for input_data, expected_output in (
        ({}, Permission(0)),
        ({'default_member_permissions': None}, Permission()),
        ({'default_member_permissions': 1}, Permission(1)),
    ):
        output = parse_required_permissions(input_data)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)
