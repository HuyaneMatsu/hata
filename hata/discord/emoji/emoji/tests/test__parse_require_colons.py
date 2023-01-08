import vampytest

from ..fields import parse_require_colons


def test__parse_require_colons():
    """
    Tests whether ``parse_require_colons`` works as intended.
    """
    for input_data, expected_output in (
        ({}, True),
        ({'require_colons': False}, False),
        ({'require_colons': True}, True),
    ):
        output = parse_require_colons(input_data)
        vampytest.assert_eq(output, expected_output)
