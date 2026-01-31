import vampytest

from ...message import Message

from ..fields import validate_messages


def _iter_options__passing():
    channel_id = 202601070006
    
    message_id_0 = 202601070007
    message_content_0 = 'Far'
    
    message_id_1 = 202601070008
    message_content_1 = 'East'
    
    message_0 = Message.precreate(
        message_id_0,
        channel_id = channel_id,
        content = message_content_0,
    )
    
    message_1 = Message.precreate(
        message_id_1,
        channel_id = channel_id,
        content = message_content_1,
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            message_0,
            message_1,
        ],
        (
            message_0,
            message_1,
        )
    )
    
    yield (
        [
            message_1,
            message_0,
        ],
        (
            message_1,
            message_0,
        )
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_messages(input_data):
    """
    Tests whether ``validate_messages`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | tuple<Message>``
    """
    output = validate_messages(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Message)
    
    return output
