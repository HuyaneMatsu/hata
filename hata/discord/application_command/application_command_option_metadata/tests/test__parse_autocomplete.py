import vampytest

from ..fields import parse_autocomplete


def test__parse_autocomplete():
    """
    Tests whether ``parse_autocomplete`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'autocomplete': False}, False),
        ({'autocomplete': True}, True),
    ):
        output = parse_autocomplete(input_data)
        vampytest.assert_eq(output, expected_output)
