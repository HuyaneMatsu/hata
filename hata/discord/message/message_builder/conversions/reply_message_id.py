__all__ = ('CONVERSION_REPLY_MESSAGE_ID',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion

from ..message_reference_configuration import MessageReferenceConfiguration

from .message_reference_configuration import CONVERSION_MESSAGE_REFERENCE_CONFIGURATION


class CONVERSION_REPLY_MESSAGE_ID(Conversion):
    # Generic
    
    name = 'reply_message_id'
    name_aliases = None
    expected_types_messages = '`int`'
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
        
        # int
        if isinstance(value, int):
            yield MessageReferenceConfiguration(message_id = value)
            return
        
        # No other cases
        return
    
    # Reading
    
    get_default = 0
    
    def get_processor(value):
        if value is None:
            return 0
        
        return value.message_id
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    # Sorting
    
    sort_priority = 2400
