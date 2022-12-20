import vampytest

from .....permission import Permission

from ..deny import put_deny_into


def test__put_deny_into():
    """
    Tests whether ``put_deny_into`` works as intended.
    """
    deny = Permission(1111)
    
    for input_value, expected_output in (
        (deny, {'deny': format(deny, 'd')}),
    ):
        output_data = put_deny_into(input_value, {}, True)
        vampytest.assert_eq(output_data, expected_output)
