__all__ = ('CONVERSION_APPLIED_TAG_IDS',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....channel import ForumTag


class CONVERSION_APPLIED_TAG_IDS(Conversion):
    # Generic
    
    name = 'applied_tag_ids'
    name_aliases = None
    expected_types_messages = (
        f'`None`, `(list | tuple)<int>`, `(list | tuple)<{ForumTag.__name__}>`, `int`, `{ForumTag.__name__}`'
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
        
        # (list | tuple)<int | ForumTag>
        if isinstance(value, list) or isinstance(value, tuple):
            applied_tag_ids = None
            
            for element in value:
                if isinstance(element, int):
                    pass
                
                elif isinstance(element, ForumTag):
                    element = element.id
                
                else:
                    return
            
                if applied_tag_ids is None:
                    applied_tag_ids = []
                    
                applied_tag_ids.append(element)
                continue
            
            yield applied_tag_ids
            return
        
        # int
        if isinstance(value, int):
            yield [value]
            return
        
        # ForumTag
        if isinstance(value, ForumTag):
            yield [value.id]
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'applied_tags'
    
    def serializer_optional(value):
        if value is not None:
            yield [str(applied_tag_id) for applied_tag_id in value]
    
    
    def serializer_required(value):
        if value is not None:
            return [str(applied_tag_id) for applied_tag_id in value]
    
    
    # Sorting
    
    sort_priority = 2100
