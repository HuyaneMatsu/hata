import vampytest

from ..fields import parse_discoverable


def test__parse_discoverable():
    """
    Tests whether ``parse_discoverable`` works as intended.
    """
    for input_data, expected_output in (
        ({}, True),
        ({'discoverable_disabled': False}, True),
        ({'discoverable_disabled': True}, False),
    ):
        output = parse_discoverable(input_data)
        vampytest.assert_eq(output, expected_output)
