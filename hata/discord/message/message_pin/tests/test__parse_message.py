import vampytest

from ....message import Message

from ..fields import parse_message


def _iter_options():
    message_id = 202511070000
    channel_id = 202511070001
    
    message = Message.precreate(message_id, channel_id = channel_id)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'message': None,
        },
        None,
    )
    
    yield (
        {
            'message': message.to_data(include_internals = True),
        },
        message,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_message(input_data):
    """
    Tests whether ``parse_message`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | Message``
    """
    output = parse_message(input_data)
    vampytest.assert_instance(output, Message, nullable = True)
    return output
