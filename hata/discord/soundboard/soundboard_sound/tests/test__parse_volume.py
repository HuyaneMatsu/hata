import vampytest

from ..fields import parse_volume


def test__parse_volume():
    """
    Tests whether ``parse_volume`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 1.0),
        ({'volume': 0.0}, 0.0),
        ({'volume': 0.5}, 0.5),
        ({'volume': 1.0}, 1.0),
    ):
        output = parse_volume(input_data)
        vampytest.assert_eq(output, expected_output)
