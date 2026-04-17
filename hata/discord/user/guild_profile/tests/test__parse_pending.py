import vampytest

from ..fields import parse_pending


def test__parse_pending():
    """
    Tests whether ``parse_pending`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'pending': False}, False),
        ({'pending': True}, True),
    ):
        output = parse_pending(input_data)
        vampytest.assert_eq(output, expected_output)
