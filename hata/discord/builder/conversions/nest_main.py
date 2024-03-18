__all__ = ('CONVERSION_NEST_MAIN',)

from ..constants import CONVERSION_KIND_FIELD
from ..conversion import Conversion


class CONVERSION_NEST_MAIN(Conversion):
    # Generic
    
    name = '__nest_main__'
    name_aliases = None
    expected_types_messages = 'tuple<str, dict<str, object>>'
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None
    set_listing_identifier = None
    set_identifier = None
    
    def set_validator(value):
        # Omit validation.
        yield value
    
    # Reading
    
    get_default = None
    get_processor = None
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None

    def serializer_putter(main_data, required, value):
        key, sub_data = value
        if required or main_data:
            sub_data[key] = main_data
        return sub_data

    # Sorting
    sort_priority = 9000
