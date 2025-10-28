__all__ = ('CONVERSION_SHARED_CLIENT_THEME',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion

from ...shared_client_theme import SharedClientTheme


class CONVERSION_SHARED_CLIENT_THEME(Conversion):
    # Generic
    
    name = 'shared_client_theme'
    name_aliases = None
    expected_types_messages = f'`None`, `{SharedClientTheme.__name__}`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = SharedClientTheme
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # SharedClientTheme
        if isinstance(value, SharedClientTheme):
            yield value
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'shared_client_theme'
    
    
    def serializer_optional(value):
        if (value is not None):
            yield value.to_data()
    
    
    def serializer_required(value):
        return None if value is None else value.to_data()
    
    
    # Sorting
    
    sort_priority = 1900
