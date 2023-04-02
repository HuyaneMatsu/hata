import vampytest

from ..fields import parse_inline


def test__parse_inline():
    """
    Tests whether ``parse_inline`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'inline': False}, False),
        ({'inline': True}, True),
    ):
        output = parse_inline(input_data)
        vampytest.assert_eq(output, expected_output)
