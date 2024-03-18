__all__ = ('CONVERSION_EMBEDS',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....embed import Embed


class CONVERSION_EMBEDS(Conversion):
    # Generic
    
    name = 'embeds'
    name_aliases = None
    expected_types_messages = f'`None`, `{Embed.__name__}`, `tuple<{Embed.__name__}>`, `list<{Embed.__name__}>`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None
    set_identifier = None
    
    
    def set_listing_identifier(value):
        for element in value:
            if not isinstance(element, Embed):
                return
        
        yield value
        return
    
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # list<length = 0> | tuple<length = 0> | list<Embed> | tuple<Embed>
        if isinstance(value, list) or isinstance(value, tuple):
            if not value:
                yield None
                return
            
            for element in value:
                if not isinstance(element, Embed):
                    return
            
            yield value
            return
        
        # Embed
        if isinstance(value, Embed):
            yield [value]
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'embeds'
    
    def serializer_optional(value):
        if value is not None:
            yield [element.to_data() for element in value]
    
    
    def serializer_required(value):
        if value is not None:
            return [element.to_data() for element in value]
    
    
    # Sorting
    
    sort_priority = 1300
