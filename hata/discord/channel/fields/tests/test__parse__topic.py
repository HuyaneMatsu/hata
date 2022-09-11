import vampytest

from ..topic import parse_topic

def test__parse_topic():
    """
    Tests whether ``parse_topic`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'topic': None}, None),
        ({'topic': ''}, None),
        ({'topic': 'a'}, 'a'),
    ):
        output = parse_topic(input_data)
        vampytest.assert_eq(output, expected_output)
