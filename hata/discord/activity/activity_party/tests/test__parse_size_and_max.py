import vampytest

from ..fields import parse_size_and_max


def test__parse_size_and_max():
    """
    Tests whether ``parse_size_and_max`` works as intended.
    """
    for input_data, expected_output in (
        ({}, (0, 0)),
        ({'size': [10, 20]}, [10, 20]),
    ):
        output = parse_size_and_max(input_data)
        vampytest.assert_eq(output, expected_output)
