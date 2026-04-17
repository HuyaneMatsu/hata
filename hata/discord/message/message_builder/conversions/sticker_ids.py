__all__ = ('CONVERSION_STICKER_IDS',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....sticker import Sticker


class CONVERSION_STICKER_IDS(Conversion):
    # Generic
    
    name = 'sticker_ids'
    name_aliases = None
    expected_types_messages = (
        f'`None`, `(list | tuple)<int>`, `(list | tuple)<{Sticker.__name__}>`, `int`, `{Sticker.__name__}`'
    )
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
            yield None
            return
        
        # (list | tuple)<int | Sticker>
        if isinstance(value, list) or isinstance(value, tuple):
            sticker_ids = None
            
            for element in value:
                if isinstance(element, int):
                    pass
                
                elif isinstance(element, Sticker):
                    element = element.id
                
                else:
                    return
            
                if sticker_ids is None:
                    sticker_ids = []
                    
                sticker_ids.append(element)
                continue
            
            yield sticker_ids
            return
        
        # int
        if isinstance(value, int):
            yield [value]
            return
        
        # Sticker
        if isinstance(value, Sticker):
            yield [value.id]
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'sticker_ids'
    
    def serializer_optional(value):
        if value is not None:
            yield [str(sticker_id) for sticker_id in value]
    
    
    def serializer_required(value):
        if value is not None:
            return [str(sticker_id) for sticker_id in value]
    
    
    # Sorting
    
    sort_priority = 1500
