import vampytest

from ...message_activity import MessageActivity

from ..fields import parse_activity


def test__parse_activity():
    """
    Tests whether ``parse_activity`` works as intended.
    """
    activity = MessageActivity(party_id = 'orin')
    
    for input_data, expected_output in (
        ({}, None),
        ({'activity': None}, None),
        ({'activity': activity.to_data()}, activity),
    ):
        output = parse_activity(input_data)
        vampytest.assert_eq(output, expected_output)
