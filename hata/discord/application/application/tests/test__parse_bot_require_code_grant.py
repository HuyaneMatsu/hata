import vampytest

from ..fields import parse_bot_require_code_grant


def test__parse_bot_require_code_grant():
    """
    Tests whether ``parse_bot_require_code_grant`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'bot_require_code_grant': False}, False),
        ({'bot_require_code_grant': True}, True),
    ):
        output = parse_bot_require_code_grant(input_data)
        vampytest.assert_eq(output, expected_output)
