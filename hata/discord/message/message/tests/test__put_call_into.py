import vampytest

from ...message_call import MessageCall

from ..fields import put_call_into


def test__put_call_into():
    """
    Tests whether ``put_call_into`` is working as intended.
    """
    user_id_0 = 202304300001
    call = MessageCall(user_ids = [user_id_0])
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (call, False, {'call': call.to_data()}),
        (call, True, {'call': call.to_data(defaults = True)}),
    ):
        data = put_call_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
