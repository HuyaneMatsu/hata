__all__ = ('CONVERSION_INSTANCE',)

from scarletio import include

from ....builder.constants import CONVERSION_KIND_INSTANCE
from ....builder.conversion import Conversion


MessageBuilderBase = include('MessageBuilderBase')


class CONVERSION_INSTANCE(Conversion):
    # Generic
    
    name = 'instance'
    name_aliases = None
    expected_types_messages = 'MessageBuilderBase'
    kind = CONVERSION_KIND_INSTANCE
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None
    
    
    def set_identifier(value):
        # MessageBuilderBase
        if isinstance(value, MessageBuilderBase):
            yield value
            return
        
        # No other cases
        return
    
    set_listing_identifier = None
    set_validator = None
    
    # Reading
    
    get_default = None
    get_processor = None
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    # Sorting
    sort_priority = 1800
