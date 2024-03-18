__all__ = ('CONVERSION_TTS',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion


class CONVERSION_TTS(Conversion):
    # Generic
    
    name = 'tts'
    name_aliases = None
    expected_types_messages = '`None`, `bool`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_identifier = None
    set_type = None
    set_type_processor = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield False
            return
        
        # bool
        if isinstance(value, bool):
            yield value
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = False
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'tts'
    
    
    def serializer_optional(value):
        if value:
            yield value
    
    
    def serializer_required(value):
        return value
    
    
    # Sorting
    
    sort_priority = -1
