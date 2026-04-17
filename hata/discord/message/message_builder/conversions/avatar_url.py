__all__ = ('CONVERSION_AVATAR_URL',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion


class CONVERSION_AVATAR_URL(Conversion):
    # Generic
    
    name = 'avatar_url'
    name_aliases = None
    expected_types_messages = '`None`, `str`'
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
    
    serializer_key = 'avatar_url'
    
    
    def serializer_optional(value):
        if (value is not None):
            yield value
    
    
    def serializer_required(value):
        return value
    
    
    # Sorting
    
    sort_priority = -1
