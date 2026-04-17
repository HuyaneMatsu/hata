import vampytest

from ...message_call import MessageCall

from ..fields import parse_call


def test__parse_call():
    """
    Tests whether ``parse_call`` works as intended.
    """
    user_id_0 = 202304300000
    call = MessageCall(user_ids = [user_id_0])
    
    for input_data, expected_output in (
        ({}, None),
        ({'call': None}, None),
        ({'call': call.to_data()}, call),
    ):
        output = parse_call(input_data)
        vampytest.assert_eq(output, expected_output)
