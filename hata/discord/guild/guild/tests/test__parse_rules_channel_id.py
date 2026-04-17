import vampytest

from ..fields import parse_rules_channel_id


def test__parse_rules_channel_id():
    """
    Tests whether ``parse_rules_channel_id`` works as intended.
    """
    rules_channel_id = 202306100009
    
    for input_data, expected_output in (
        ({}, 0),
        ({'rules_channel_id': None}, 0),
        ({'rules_channel_id': str(rules_channel_id)}, rules_channel_id),
    ):
        output = parse_rules_channel_id(input_data)
        vampytest.assert_eq(output, expected_output)
