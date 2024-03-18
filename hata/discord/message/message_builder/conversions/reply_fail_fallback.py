__all__ = ('CONVERSION_REPLY_FAIL_FALLBACK',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion

from ..reply_configuration import ReplyConfiguration

from .reply_configuration import CONVERSION_REPLY_CONFIGURATION


class CONVERSION_REPLY_FAIL_FALLBACK(Conversion):
    # Generic
    
    name = 'reply_fail_fallback'
    name_aliases = None
    expected_types_messages = '`None`, `bool`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = CONVERSION_REPLY_CONFIGURATION
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield ReplyConfiguration()
            return
        
        # bool
        if isinstance(value, bool):
            yield ReplyConfiguration(fail_fallback = value)
            return
        
        # No other cases
        return
    
    # Reading
    
    get_default = False
    
    def get_processor(value):
        if value is None:
            return False
        
        return value.fail_fallback
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    # Sorting
    
    sort_priority = 2000
