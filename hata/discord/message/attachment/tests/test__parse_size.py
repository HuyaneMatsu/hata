import vampytest

from ..fields import parse_size


def test__parse_size():
    """
    Tests whether ``parse_size`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'size': 1}, 1),
    ):
        output = parse_size(input_data)
        vampytest.assert_eq(output, expected_output)
