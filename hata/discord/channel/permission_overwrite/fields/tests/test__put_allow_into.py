import vampytest

from .....permission import Permission

from ..allow import put_allow_into


def test__put_allow_into():
    """
    Tests whether ``put_allow_into`` works as intended.
    """
    allow = Permission(1111)
    
    for input_value, expected_output in (
        (allow, {'allow': format(allow, 'd')}),
    ):
        output_data = put_allow_into(input_value, {}, True)
        vampytest.assert_eq(output_data, expected_output)
