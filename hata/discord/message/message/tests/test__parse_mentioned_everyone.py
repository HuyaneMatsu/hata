import vampytest

from ..fields import parse_mentioned_everyone


def test__parse_mentioned_everyone():
    """
    Tests whether ``parse_mentioned_everyone`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'mention_everyone': False}, False),
        ({'mention_everyone': True}, True),
    ):
        output = parse_mentioned_everyone(input_data)
        vampytest.assert_eq(output, expected_output)
