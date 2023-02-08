import vampytest

from ..fields import parse_email_verified


def test__parse_email_verified():
    """
    Tests whether ``parse_email_verified`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'verified': False}, False),
        ({'verified': True}, True),
    ):
        output = parse_email_verified(input_data)
        vampytest.assert_eq(output, expected_output)
