__all__ = ('CONVERSION_MESSAGE',)

from ....discord.builder.conversion import Conversion
from ....discord.builder.constants import CONVERSION_KIND_FIELD
from ....discord.message import Message


class CONVERSION_MESSAGE(Conversion):
    # Generic
    
    name = 'message'
    name_aliases = None
    expected_types_messages = f'`None`, `{Message.__name__}`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = Message
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # Message
        if isinstance(value, Message):
            yield value
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    # Sorting
    
    sort_priority = -1
