import vampytest

from ..fields import parse_name_and_sub_command_name_stack


def test__parse_name_and_sub_command_name_stack():
    """
    Tests whether ``parse_name_and_sub_command_name_stack`` works as intended.
    """
    for input_data, expected_output in (
        ({'name': None}, ('', None)),
        ({'name': ''}, ('', None)),
        ({'name': 'a'}, ('a', None)),
        ({'name': 'a hello there'}, ('a', ('hello', 'there'))),
        ({'name': 'a there hello'}, ('a', ('there', 'hello'))),
    ):
        output = parse_name_and_sub_command_name_stack(input_data)
        vampytest.assert_eq(output, expected_output)
