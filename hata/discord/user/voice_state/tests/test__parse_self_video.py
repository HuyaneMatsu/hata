import vampytest

from ..fields import parse_self_video


def test__parse_self_video():
    """
    Tests whether ``parse_self_video`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'self_video': False}, False),
        ({'self_video': True}, True),
    ):
        output = parse_self_video(input_data)
        vampytest.assert_eq(output, expected_output)
