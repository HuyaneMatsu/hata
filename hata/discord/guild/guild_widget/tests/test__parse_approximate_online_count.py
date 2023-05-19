import vampytest

from ..fields import parse_approximate_online_count


def test__parse_approximate_online_count():
    """
    Tests whether ``parse_approximate_online_count`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'presence_count': 1}, 1),
    ):
        output = parse_approximate_online_count(input_data)
        vampytest.assert_eq(output, expected_output)
