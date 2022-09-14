import vampytest

from ..archived import parse_archived


def test__parse_archived():
    """
    Tests whether ``parse_archived`` works as intended.
    """
    for input_data, expected_output in (
        ({}, False),
        ({'thread_metadata': {}}, False),
        ({'thread_metadata': {'archived': False}}, False),
        ({'thread_metadata': {'archived': True}}, True),
    ):
        output = parse_archived(input_data)
        vampytest.assert_eq(output, expected_output)
