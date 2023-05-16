import vampytest

from ..fields import parse_display_name


def test__parse_display_name():
    """
    Tests whether ``parse_display_name`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'global_name': None}, None),
        ({'global_name': ''}, None),
        ({'global_name': 'meow'}, 'meow'),
    ):
        output = parse_display_name(input_data)
        vampytest.assert_eq(output, expected_output)
