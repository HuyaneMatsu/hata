__all__ = ('CONVERSION_THREAD_NAME',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion


class CONVERSION_THREAD_NAME(Conversion):
    # Generic
    
    name = 'thread_name'
    name_aliases = None
    expected_types_messages = '`str`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield ''
            return
        
        # str
        if isinstance(value, str):
            yield value
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'thread_name'
    
    
    def serializer_optional(value):
        yield value
    
    
    def serializer_required(value):
        return value
    
    
    # Sorting
    
    sort_priority = -1
