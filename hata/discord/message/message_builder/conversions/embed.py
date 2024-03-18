__all__ = ('CONVERSION_EMBED',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....embed import Embed

from .embeds import CONVERSION_EMBEDS


class CONVERSION_EMBED(Conversion):
    # Generic
    
    name = 'embed'
    name_aliases = None
    expected_types_messages = f'`None`, `{Embed.__name__}`, `tuple<{Embed.__name__}>`, `list<{Embed.__name__}>`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = CONVERSION_EMBEDS
    
    # Setting
    
    set_merger = None
    set_type = Embed
    
    def set_type_processor(value):
        return [value]
    
    set_identifier = None
    set_listing_identifier = None
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # Embed
        if isinstance(value, Embed):
            yield [value]
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
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    
    
    def get_processor(value):
        if value is not None:
            return value[0]
    
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    
    # Sorting
    
    sort_priority = 1200
