import vampytest

from ..slowmode import parse_slowmode


def test__parse_slowmode():
    """
    Tests whether ``parse_slowmode`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'rate_limit_per_user': None}, 0),
        ({'rate_limit_per_user': 1}, 1),
    ):
        output = parse_slowmode(input_data)
        vampytest.assert_eq(output, expected_output)
