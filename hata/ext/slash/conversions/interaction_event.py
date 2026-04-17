__all__ = ('CONVERSION_INTERACTION_EVENT',)

from ....discord.builder.conversion import Conversion
from ....discord.builder.constants import CONVERSION_KIND_FIELD
from ....discord.interaction import InteractionEvent


class CONVERSION_INTERACTION_EVENT(Conversion):
    # Generic
    
    name = 'interaction_event'
    name_aliases = ('event', )
    expected_types_messages = f'`None`, `{InteractionEvent.__name__}`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = InteractionEvent
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # InteractionEvent
        if isinstance(value, InteractionEvent):
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
