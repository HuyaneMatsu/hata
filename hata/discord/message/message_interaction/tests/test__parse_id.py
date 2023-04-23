import vampytest

from ..fields import parse_id


def test__parse_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    message_interaction_id = 202304230007
    
    for input_data, expected_output in (
        ({}, 0),
        ({'id': None}, 0),
        ({'id': str(message_interaction_id)}, message_interaction_id),
    ):
        output = parse_id(input_data)
        vampytest.assert_eq(output, expected_output)
