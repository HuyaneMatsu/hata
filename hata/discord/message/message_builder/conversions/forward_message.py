__all__ = ('CONVERSION_FORWARD_MESSAGE',)

from ....bases import maybe_snowflake_pair
from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion

from ...message import Message

from ..message_reference_configuration import MessageReferenceConfiguration
from ..preinstanced import MessageReferenceType

from .message_reference_configuration import CONVERSION_MESSAGE_REFERENCE_CONFIGURATION


class CONVERSION_FORWARD_MESSAGE(Conversion):
    # Generic
    
    name = 'forward_message'
    name_aliases = None
    expected_types_messages = f'`None`, `{Message.__name__}`, `(int, int)`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = CONVERSION_MESSAGE_REFERENCE_CONFIGURATION
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield MessageReferenceConfiguration()
            return
        
        # Message
        if isinstance(value, Message):
            yield MessageReferenceConfiguration(
                channel_id = value.channel_id,
                message_id = value.id,
                message_reference_type = MessageReferenceType.forward,
            )
            return
        
        # (int, int)
        snowflake_pair = maybe_snowflake_pair(value)
        if (snowflake_pair is not None):
            yield MessageReferenceConfiguration(
                channel_id = snowflake_pair[0],
                message_id = snowflake_pair[1],
                message_reference_type = MessageReferenceType.forward,
            )
            return
        
        # No other cases
        return
    
    # Reading
    
    get_default = None
    
    def get_processor(value):
        if value is None:
            return None
        
        return (value.channel_id, value.message_id)
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    # Sorting
    
    sort_priority = 2300
