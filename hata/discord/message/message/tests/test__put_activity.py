import vampytest

from ...message_activity import MessageActivity

from ..fields import put_activity


def test__put_activity():
    """
    Tests whether ``put_activity`` is working as intended.
    """
    activity = MessageActivity(party_id = 'Orin')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (activity, False, {'activity': activity.to_data()}),
        (activity, True, {'activity': activity.to_data(defaults = True)}),
    ):
        data = put_activity(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
