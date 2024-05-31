__all__ = ('CONVERSION_MESSAGE_REFERENCE_CONFIGURATION',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion

from ..message_reference_configuration import MessageReferenceConfiguration


class CONVERSION_MESSAGE_REFERENCE_CONFIGURATION(Conversion):
    # Generic
    
    name = 'message_reference_configuration'
    name_aliases = None
    expected_types_messages = f'`{MessageReferenceConfiguration.__name__}`'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    def set_merger(old_value, new_value):
        return old_value | new_value
    
    set_identifier = None
    set_type = None
    set_type_processor = None
    set_listing_identifier = None
    set_validator = None
    
    # Reading
    
    get_default = False
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'message_reference'
    
    
    def serializer_optional(value):
        if value:
            yield value.to_data()
    
    
    def serializer_required(value):
        return value.to_data()
    
    
    # Sorting
    
    sort_priority = -1
