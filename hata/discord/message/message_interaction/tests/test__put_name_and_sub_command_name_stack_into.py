import vampytest

from ..fields import put_name_and_sub_command_name_stack_into


def test__put_name_and_sub_command_name_stack_into():
    """
    Tests whether ``put_name_and_sub_command_name_stack_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (('', None), False, {'name': ''}),
        (('a', None), False, {'name': 'a'}),
        (('a', ('hello', 'there')), False, {'name': 'a hello there'}),
        (('a', ('there', 'hello')), False, {'name': 'a there hello'}),
    ):
        data = put_name_and_sub_command_name_stack_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
