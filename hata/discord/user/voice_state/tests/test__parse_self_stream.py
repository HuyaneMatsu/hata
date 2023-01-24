import vampytest

from ..fields import parse_self_stream


def test__parse_self_stream():
    """
    Tests whether ``parse_self_stream`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'self_stream': False}, False),
        ({'self_stream': True}, True),
    ):
        output = parse_self_stream(input_data)
        vampytest.assert_eq(output, expected_output)
