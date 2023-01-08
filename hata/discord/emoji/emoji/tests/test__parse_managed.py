import vampytest

from ..fields import parse_managed


def test__parse_managed():
    """
    Tests whether ``parse_managed`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'managed': False}, False),
        ({'managed': True}, True),
    ):
        output = parse_managed(input_data)
        vampytest.assert_eq(output, expected_output)
