import vampytest

from ..fields import parse_default_thread_slowmode


def test__parse_default_thread_slowmode():
    """
    Tests whether ``parse_default_thread_slowmode`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'default_thread_rate_limit_per_user': None}, 0),
        ({'default_thread_rate_limit_per_user': 1}, 1),
    ):
        output = parse_default_thread_slowmode(input_data)
        vampytest.assert_eq(output, expected_output)
