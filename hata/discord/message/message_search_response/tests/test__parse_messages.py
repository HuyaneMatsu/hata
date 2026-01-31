import vampytest

from ...message import Message

from ..fields import parse_messages


def _iter_options():
    channel_id = 202601070002
    
    message_id_0 = 202601070000
    message_content_0 = 'Far'
    
    message_id_1 = 202601070001
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
        {},
        None,
    )
    
    yield (
        {
            'messages': None,
        },
        None,
    )
    
    yield (
        {
            'messages': [],
        },
        None,
    )
    
    yield (
        {
            'messages': [
                [
                    message_0.to_data(include_internals = True),
                ], [
                    message_1.to_data(include_internals = True),
                ],
            ],
        },
        (
            message_0,
            message_1,
        ),
    )
    
    yield (
        {
            'messages': [
                [
                    message_1.to_data(include_internals = True),
                ], [
                    message_0.to_data(include_internals = True),
                ],
            ],
        },
        (
            message_1,
            message_0,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_messages(input_data):
    """
    Tests whether ``parse_messages`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<Message>``
    """
    output = parse_messages(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Message)
    
    return output
