import vampytest

from ..open_ import parse_open


def test__parse_open():
    """
    Tests whether ``parse_open`` works as intended.
    """
    for input_data, expected_output in (
        ({}, True),
        ({'thread_metadata': {}}, True),
        ({'thread_metadata': {'locked': False}}, True),
        ({'thread_metadata': {'locked': True}}, False),
    ):
        output = parse_open(input_data)
        vampytest.assert_eq(output, expected_output)
