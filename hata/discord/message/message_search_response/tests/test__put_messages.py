import vampytest

from ...message import Message

from ..fields import put_messages


def _iter_options():
    channel_id = 202601070003
    
    message_id_0 = 202601070004
    message_content_0 = 'Far'
    
    message_id_1 = 202601070005
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
        False,
        {
            'messages': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'messages': [],
        },
    )
    
    yield (
        (
            message_0,
            message_1,
        ),
        False,
        {
            'messages': [
                [
                    message_0.to_data(defaults = False, include_internals = True),
                ], [
                    message_1.to_data(defaults = False, include_internals = True),
                ],
            ],
        },
    )
    
    yield (
        (
            message_0,
            message_1,
        ),
        True,
        {
            'messages': [
                [
                    message_0.to_data(defaults = True, include_internals = True),
                ], [
                    message_1.to_data(defaults = True, include_internals = True),
                ],
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_messages(input_value, defaults):
    """
    Tests whether ``put_messages`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<Message>``
        The value to serialise.
    
    defaults : `bool`
        Whether fields as their default should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_messages(input_value, {}, defaults)
