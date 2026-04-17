import vampytest

from ..fields import parse_height


def test__parse_height():
    """
    Tests whether ``parse_height`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'height': 1}, 1),
    ):
        output = parse_height(input_data)
        vampytest.assert_eq(output, expected_output)
