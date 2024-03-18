__all__ = ('CONVERSION_ALLOWED_MENTIONS',)

from ....allowed_mentions import AllowedMentionProxy, is_allowed_mentions_valid, parse_allowed_mentions
from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....role import Role
from ....user import UserBase


class CONVERSION_ALLOWED_MENTIONS(Conversion):
    # Generic
    
    name = 'allowed_mentions'
    name_aliases = None
    expected_types_messages = (
        f'`None`,  ``{AllowedMentionProxy.__name__}``, `str`, ``{UserBase.__name__}``, ``{Role.__name__}``, '
        f'(`list`, `tuple`, `set`) of (`str`, `{UserBase.__name__}`, `{Role.__name__}`)'
    )
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    def set_merger(old_value, new_value):
        return AllowedMentionProxy._create_from_various(old_value) | new_value
    
    set_type = AllowedMentionProxy
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # use helper
        if is_allowed_mentions_valid(value):
            yield value
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'allowed_mentions'
    
    
    def serializer_optional(value):
        yield parse_allowed_mentions(value)
    
    
    def serializer_required(value):
        return parse_allowed_mentions(value)
    
    
    # Sorting
    
    sort_priority = 1500
