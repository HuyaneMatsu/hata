import vampytest

from ....permission import Permission

from ..deny import parse_deny


def test__parse_deny():
    """
    Tests whether ``parse_deny`` works as intended.
    """
    deny = Permission(1111)
    
    for input_value, expected_output in (
        ({'deny': format(deny, 'd')}, deny),
    ):
        output = parse_deny(input_value)
        vampytest.assert_instance(output, Permission)
        vampytest.assert_eq(output, expected_output)
