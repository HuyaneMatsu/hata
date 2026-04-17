__all__ = ('CONVERSION_SHOW_FOR_INVOKING_USER_ONLY',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion

from ...message import MessageFlag

from .flags import CONVERSION_FLAGS

MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY = MessageFlag().update_by_keys(invoking_user_only = True)


class CONVERSION_SHOW_FOR_INVOKING_USER_ONLY(Conversion):
    # Generic
    
    name = 'show_for_invoking_user_only'
    name_aliases = None
    expected_types_messages = '`None`, `bool`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = CONVERSION_FLAGS
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield 0
            return
        
        # bool
        if isinstance(value, bool):
            if value:
                value = MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY
            
            yield value
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = False
    
    def get_processor(value):
        return True if value & MESSAGE_FLAG_VALUE_SHOW_FOR_INVOKING_USER_ONLY else False
    
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    
    # Sorting
    
    sort_priority = -1
