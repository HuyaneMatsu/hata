import vampytest

from .....permission import Permission

from ..allow import parse_allow


def test__parse_allow():
    """
    Tests whether ``parse_allow`` works as intended.
    """
    allow = Permission(1111)
    
    for input_value, expected_output in (
        ({'allow': format(allow, 'd')}, allow),
    ):
        output = parse_allow(input_value)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)
