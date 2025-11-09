import vampytest

from ....message import Message

from ..fields import put_message


def _iter_options():
    message_id = 202511070002
    channel_id = 202511070003
    
    message = Message.precreate(message_id, channel_id = channel_id)
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'message': None,
        },
    )
    
    yield (
        message,
        False,
        {
            'message': message.to_data(defaults = False, include_internals = True),
        },
    )
    
    yield (
        message,
        True,
        {
            'message': message.to_data(defaults = True, include_internals = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_message(input_value, defaults):
    """
    Tests whether ``put_message`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | Message``
        The value to serialize.
    
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    input_data : `dict<str, object>`
    """
    return put_message(input_value, {}, defaults)
