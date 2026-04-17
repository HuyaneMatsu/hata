import vampytest

from ..fields import validate_sub_command_name_stack


def test__validate_sub_command_name_stack__0():
    """
    Tests whether `validate_sub_command_name_stack` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('a', ('a', )),
        (['a', 'b'], ('a', 'b')),
        (['b', 'a'], ('b', 'a')),
    ):
        output = validate_sub_command_name_stack(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_sub_command_name_stack__1():
    """
    Tests whether `validate_sub_command_name_stack` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_sub_command_name_stack(input_value)
