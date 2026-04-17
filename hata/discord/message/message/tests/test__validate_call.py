import vampytest

from ...message_call import MessageCall

from ..fields import validate_call


def test__validate_call__0():
    """
    Tests whether `validate_call` works as intended.
    
    Case: passing.
    """
    user_id_0 = 202304300002
    call = MessageCall(user_ids = [user_id_0])
    
    for input_value, expected_output in (
        (None, None),
        (call, call),
    ):
        output = validate_call(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_call__1():
    """
    Tests whether `validate_call` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_call(input_value)
