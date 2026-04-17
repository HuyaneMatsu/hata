import vampytest

from ....message import Message

from ...message_reference_configuration import MessageReferenceConfiguration
from ...preinstanced import MessageReferenceType

from ..forward_message import CONVERSION_FORWARD_MESSAGE


def _iter_options__set_validator():
    channel_id = 202405220001
    message_id = 202405220000
    
    yield (
        object(),
        [],
    )
    
    yield (
        None,
        [MessageReferenceConfiguration()],
    )
    
    yield (
        (channel_id, message_id),
        [
            MessageReferenceConfiguration(
                channel_id = channel_id,
                message_id = message_id,
                message_reference_type = MessageReferenceType.forward,
            ),
        ],
    )
    
    yield (
        Message.precreate(message_id, channel_id = channel_id),
        [
            MessageReferenceConfiguration(
                channel_id = channel_id,
                message_id = message_id,
                message_reference_type = MessageReferenceType.forward,
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_FORWARD_MESSAGE__set_validator(input_value):
    """
    Tests whether ``CONVERSION_FORWARD_MESSAGE.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<MessageReferenceConfiguration>`
    """
    return [*CONVERSION_FORWARD_MESSAGE.set_validator(input_value)]


def _iter_options__get_processor():
    channel_id = 202405220010
    message_id = 202405220011
    
    yield None, None
    yield (
        MessageReferenceConfiguration(
            channel_id = channel_id,
            message_id = message_id,
            message_reference_type = MessageReferenceType.forward,
        ),
        (channel_id, message_id),
    )


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_FORWARD_MESSAGE__get_processor(input_value):
    """
    Tests whether ``CONVERSION_FORWARD_MESSAGE.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `None | MessageReferenceConfiguration`
        Value to test.
    
    Returns
    -------
    output : `None | (int, int)`
    """
    output = CONVERSION_FORWARD_MESSAGE.get_processor(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
