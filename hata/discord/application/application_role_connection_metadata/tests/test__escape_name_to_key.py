import vampytest

from ..helpers import escape_name_to_key


def test__escape_name_to_key():
    """
    Tests whether ``escape_name_to_key`` works as intended.
    """
    for input_value, expected_output in (
        ('east_new', 'east_new'),
        ('East New', 'east_new'),
        ('Höffman', 'hffman'),
    ):
        output = escape_name_to_key(input_value)
        vampytest.assert_eq(output, expected_output)
