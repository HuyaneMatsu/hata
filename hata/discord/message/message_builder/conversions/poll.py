__all__ = ('CONVERSION_POLL',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....poll import Poll


class CONVERSION_POLL(Conversion):
    # Generic
    
    name = 'poll'
    name_aliases = None
    expected_types_messages = f'`None`, `{Poll.__name__}`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = Poll
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # Poll
        if isinstance(value, Poll):
            yield value
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'poll'
    
    
    def serializer_optional(value):
        if (value is not None):
            yield value.to_data()
    
    
    def serializer_required(value):
        return None if value is None else value.to_data()
    
    
    # Sorting
    
    sort_priority = 1900
