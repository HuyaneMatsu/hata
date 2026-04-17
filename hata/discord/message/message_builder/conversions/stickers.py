__all__ = ('CONVERSION_STICKERS',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....sticker import Sticker, create_partial_sticker_from_id

from .sticker_ids import CONVERSION_STICKER_IDS


class CONVERSION_STICKERS(Conversion):
    # Generic
    
    name = 'stickers'
    name_aliases = None
    expected_types_messages = (
        f'`None`, `(list | tuple)<{Sticker.__name__}>`, `(list | tuple)<int>`,  `{Sticker.__name__}`, `int`'
    )
    kind = CONVERSION_KIND_FIELD
    output_conversion = CONVERSION_STICKER_IDS
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None   
    set_identifier = None
    
    
    def set_listing_identifier(value):
        for element in value:
            if not isinstance(element, Sticker):
                return
        
        yield [element.id for element in value]

    
    def set_validator(value):
        # None
        if value is None:
            yield None
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
        
        
        # Sticker
        if isinstance(value, Sticker):
            yield [value.id]
        
        # int
        if isinstance(value, int):
            yield [value]
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    
    def get_processor(value):
        if value is not None:
            return [create_partial_sticker_from_id(element) for element in value]
    
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None

    
    # Sorting
    
    sort_priority = 1700
