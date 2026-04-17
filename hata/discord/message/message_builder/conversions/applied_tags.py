__all__ = ('CONVERSION_APPLIED_TAGS',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....channel import ForumTag, create_partial_forum_tag_from_id

from .applied_tag_ids import CONVERSION_APPLIED_TAG_IDS


class CONVERSION_APPLIED_TAGS(Conversion):
    # Generic
    
    name = 'applied_tags'
    name_aliases = None
    expected_types_messages = (
        f'`None`, `(list | tuple)<{ForumTag.__name__}>`, `(list | tuple)<int>`,  `{ForumTag.__name__}`, `int`'
    )
    kind = CONVERSION_KIND_FIELD
    output_conversion = CONVERSION_APPLIED_TAG_IDS
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None   
    set_identifier = None
    
    
    def set_listing_identifier(value):
        for element in value:
            if not isinstance(element, ForumTag):
                return
        
        yield [element.id for element in value]

    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # (list | tuple)<int | ForumTag>
        if isinstance(value, list) or isinstance(value, tuple):
            applied_tag_ids = None
            
            for element in value:
                if isinstance(element, ForumTag):
                    element = element.id
                
                elif isinstance(element, int):
                    pass
                
                else:
                    return
            
                if applied_tag_ids is None:
                    applied_tag_ids = []
                    
                applied_tag_ids.append(element)
                continue
            
            yield applied_tag_ids
            return
        
        
        # ForumTag
        if isinstance(value, ForumTag):
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
            return [create_partial_forum_tag_from_id(element) for element in value]
    
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None

    
    # Sorting
    
    sort_priority = 2200
