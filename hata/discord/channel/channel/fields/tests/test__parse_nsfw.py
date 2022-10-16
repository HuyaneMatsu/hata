import vampytest

from ..nsfw import parse_nsfw


def test__parse_nsfw():
    """
    Tests whether ``parse_nsfw`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'nsfw': False}, False),
        ({'nsfw': True}, True),
    ):
        output = parse_nsfw(input_data)
        vampytest.assert_eq(output, expected_output)
