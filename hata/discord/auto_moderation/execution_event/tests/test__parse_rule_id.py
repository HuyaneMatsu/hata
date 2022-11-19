import vampytest

from ..fields import parse_rule_id


def test__parse_rule_id():
    """
    Tests whether ``parse_rule_id`` works as intended.
    """
    rule_id = 202211160003
    
    for input_data, expected_output in (
        ({}, 0),
        ({'rule_id': None}, 0),
        ({'rule_id': str(rule_id)}, rule_id),
    ):
        output = parse_rule_id(input_data)
        vampytest.assert_eq(output, expected_output)
