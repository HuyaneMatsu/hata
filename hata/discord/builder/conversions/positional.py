__all__ = ('CONVERSION_POSITIONAL',)

from ..constants import CONVERSION_KIND_POSITIONAL
from ..conversion import Conversion


class CONVERSION_POSITIONAL(Conversion):
    # Generic
    
    name = 'positional'
    name_aliases = None
    expected_types_messages = 'tuple<object>'
    kind = CONVERSION_KIND_POSITIONAL
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = tuple
    set_type_processor = None
    set_listing_identifier = None
    
    
    def set_identifier(value):
        # tuple<object>
        if isinstance(value, tuple):
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
    sort_priority = 100
