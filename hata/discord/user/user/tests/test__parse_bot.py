import vampytest

from ..fields import parse_bot


def test__parse_bot():
    """
    Tests whether ``parse_bot`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'bot': False}, False),
        ({'bot': True}, True),
    ):
        output = parse_bot(input_data)
        vampytest.assert_eq(output, expected_output)
