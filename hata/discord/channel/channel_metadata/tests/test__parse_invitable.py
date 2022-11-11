import vampytest

from ..fields import parse_invitable


def test__parse_invitable():
    """
    Tests whether ``parse_invitable`` works as intended.
    """
    for input_data, expected_output in (
        ({}, True),
        ({'thread_metadata': {}}, True),
        ({'thread_metadata': {'invitable': False}}, False),
        ({'thread_metadata': {'invitable': True}}, True),
    ):
        output = parse_invitable(input_data)
        vampytest.assert_eq(output, expected_output)
