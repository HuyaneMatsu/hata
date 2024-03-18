__all__ = ('CONVERSION_STICKER',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....sticker import Sticker, create_partial_sticker_from_id

from .sticker_ids import CONVERSION_STICKER_IDS


class CONVERSION_STICKER(Conversion):
    # Generic
    
    name = 'sticker'
    name_aliases = None
    expected_types_messages = (
        f'`None`, `{Sticker.__name__}`, `int`, `(list | tuple)<{Sticker.__name__}>`, `(list | tuple)<int>`'
    )
    kind = CONVERSION_KIND_FIELD
    output_conversion = CONVERSION_STICKER_IDS
    
    # Setting
    
    set_merger = None
    set_type = Sticker
    
    def set_type_processor(value):
        return [value.id]
    
    
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # Sticker
        if isinstance(value, Sticker):
            yield [value.id]
        
        # int
        if isinstance(value, int):
            yield [value]
            return
        
        # (list | tuple)<int | Sticker>
        if isinstance(value, list) or isinstance(value, tuple):
            sticker_ids = None
            
            for element in value:
                if isinstance(element, Sticker):
                    element = element.id
                
                elif isinstance(element, int):
                    pass
                
                else:
                    return
            
                if sticker_ids is None:
                    sticker_ids = []
                    
                sticker_ids.append(element)
                continue
            
            yield sticker_ids
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    
    def get_processor(value):
        if value is not None:
            return create_partial_sticker_from_id(value[0])
    
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    
    # Sorting
    
    sort_priority = 1600
