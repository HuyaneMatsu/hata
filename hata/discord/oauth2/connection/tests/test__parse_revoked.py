import vampytest

from ..fields import parse_revoked


def test__parse_revoked():
    """
    Tests whether ``parse_revoked`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'revoked': False}, False),
        ({'revoked': True}, True),
    ):
        output = parse_revoked(input_data)
        vampytest.assert_eq(output, expected_output)
