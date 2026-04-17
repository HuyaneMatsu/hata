__all__ = ('CONVERSION_KEYWORD',)

from ..constants import CONVERSION_KIND_KEYWORD
from ..conversion import Conversion


class CONVERSION_KEYWORD(Conversion):
    # Generic
    
    name = 'keyword'
    name_aliases = None
    expected_types_messages = 'dict<str, object>'
    kind = CONVERSION_KIND_KEYWORD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = dict
    set_type_processor = None
    set_listing_identifier = None
    
    
    def set_identifier(value):
        # dict<str, object>
        if isinstance(value, dict):
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
    sort_priority = 200
