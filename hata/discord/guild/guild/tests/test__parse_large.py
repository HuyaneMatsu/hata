import vampytest

from ..fields import parse_large


def test__parse_large():
    """
    Tests whether ``parse_large`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'large': False}, False),
        ({'large': True}, True),
    ):
        output = parse_large(input_data)
        vampytest.assert_eq(output, expected_output)
