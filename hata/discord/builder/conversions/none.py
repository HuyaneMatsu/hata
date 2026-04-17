__all__ = ('CONVERSION_NONE',)

from ..constants import CONVERSION_KIND_NONE
from ..conversion import Conversion


class CONVERSION_NONE(Conversion):
    # Generic
    
    name = 'none'
    name_aliases = None
    expected_types_messages = 'None'
    kind = CONVERSION_KIND_NONE
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = type(None)
    set_type_processor = None
    set_listing_identifier = None
    
    
    def set_identifier(value):
        # None
        if value is None:
            yield value
            return
        
        # No other cases
        return
    
    
    set_validator = None
    
    # Reading
    
    get_default = None
    get_processor = None
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    # Sorting
    sort_priority = 0
