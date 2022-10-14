import vampytest

from ..fields import parse_moderated


def test__parse_moderated():
    """
    Tests whether ``parse_moderated`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'moderated': False}, False),
        ({'moderated': True}, True),
    ):
        output = parse_moderated(input_data)
        vampytest.assert_eq(output, expected_output)
