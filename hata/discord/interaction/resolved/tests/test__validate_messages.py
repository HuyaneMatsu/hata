import vampytest

from ....message import Message

from ..fields import validate_messages


def test__validate_messages__0():
    """
    Tests whether ``validate_messages`` works as intended.
    
    Case: passing.
    """
    message_id = 202211050021
    message_content = 'Faker'
    
    message = Message.precreate(
        message_id,
        content = message_content,
    )
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ({}, None),
        ([message], {message_id: message}),
        ({message_id: message}, {message_id: message}),
    ):
        output = validate_messages(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_messages__1():
    """
    Tests whether ``validate_messages`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_messages(input_value)
