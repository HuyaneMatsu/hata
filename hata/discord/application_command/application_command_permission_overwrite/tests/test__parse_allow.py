import vampytest

from ..fields import parse_allow


def test__parse_allow():
    """
    Tests whether ``parse_allow`` works as intended.
    """
    for input_data, expected_output in (
        ({}, True),
        ({'permission': False}, False),
        ({'permission': True}, True),
    ):
        output = parse_allow(input_data)
        vampytest.assert_eq(output, expected_output)
