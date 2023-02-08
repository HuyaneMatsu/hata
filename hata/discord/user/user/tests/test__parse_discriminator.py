import vampytest

from ..fields import parse_discriminator


def test__parse_discriminator():
    """
    Tests whether ``parse_discriminator`` works as intended."""
    for input_data, expected_output in (
        ({}, 0),
        ({'discriminator': '1'}, 1),
        ({'discriminator': '0069'}, 69),
    ):
        output = parse_discriminator(input_data)
        vampytest.assert_eq(output, expected_output)
