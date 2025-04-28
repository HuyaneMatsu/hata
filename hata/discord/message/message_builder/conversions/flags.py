__all__ = ('CONVERSION_FLAGS',)

from ...message import MessageFlag

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion


class CONVERSION_FLAGS(Conversion):
    # Generic
    
    name = 'flags'
    name_aliases = None
    expected_types_messages = f'`None | int | {MessageFlag.__name__}`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    def set_merger(old_value, new_value):
        return old_value | new_value
    
    
    set_type = MessageFlag
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield 0
            return
        
        # int | MessageFlag
        if isinstance(value, int):
            yield value
            return
        
        # No other cases
        return
    
    # Reading
    
    get_default = MessageFlag()
    
    
    def get_processor(value):
        return MessageFlag(value)
    
    
    # Serialization
    
    serializer_key = 'flags'
    
    
    def serializer_optional(value):
        if value:
            yield int(value)
    
    
    def serializer_required(value):
        return int(value)
    
    
    # Sorting
    
    sort_priority = 1800
