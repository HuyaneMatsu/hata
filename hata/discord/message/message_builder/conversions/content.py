__all__ = ('CONVERSION_CONTENT',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion


class CONVERSION_CONTENT(Conversion):
    # Generic
    
    name = 'content'
    name_aliases = None
    expected_types_messages = '`None`, `str`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = str
    
    def set_type_processor(value):
        if not value:
            value = None
        
        return value
    
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # str
        if isinstance(value, str):
            if not value:
                value = None
            
            yield value
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'content'
    
    
    def serializer_optional(value):
        if (value is not None):
            yield value
    
    
    def serializer_required(value):
        return '' if value is None else value
    
    
    # Sorting
    
    sort_priority = 1100
