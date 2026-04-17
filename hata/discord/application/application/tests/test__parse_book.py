import vampytest

from ..fields import parse_hook


def test__parse_hook():
    """
    Tests whether ``parse_hook`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'hook': False}, False),
        ({'hook': True}, True),
    ):
        output = parse_hook(input_data)
        vampytest.assert_eq(output, expected_output)
