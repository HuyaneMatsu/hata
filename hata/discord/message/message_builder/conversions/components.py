__all__ = ('CONVERSION_COMPONENTS',)

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....component import Component, ComponentType, create_row


def _is_component_listing(value):
    """
    Yields the outcome if the input `value` is a component listing. `value` must be a non-empty list.
    
    This function is a generator.    
    
    Parameters
    ----------
    value : `(list | tuple)<object>`
        Value to identify.
    
    Yields
    ------
    components : `list<Component>`
    """
    built = None
    
    for element in value:
        if isinstance(element, Component):
            if not element.type.layout_flags.top_level:
                element = create_row(element)
        
        elif isinstance(element, list) or isinstance(element, tuple):
            if not all(isinstance(nested_element, Component) for nested_element in element):
                return
            
            element = create_row(*element)
        
        else:
            return
        
        if built is None:
            built = []
        built.append(element)
        continue
    
    yield built
    return



class CONVERSION_COMPONENTS(Conversion):
    # Generic
    
    name = 'components'
    name_aliases = None
    expected_types_messages = (
        f'``None`, ``{Component.__name__}``, (`list`, `tuple`) of (``{Component.__name__}``, '
        f'(`list`, `tuple`) of ``{Component.__name__}``)'
    )
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    
    set_type = Component
    
    
    def set_type_processor(value):
        if not value.type.layout_flags.top_level:
            value = create_row(value)
        
        return [value]
    
    
    set_listing_identifier = _is_component_listing
    set_identifier = None
    
    
    def set_validator(value):
        # None
        if value is None:
            yield None
            return
        
        # Component
        if isinstance(value, Component):
            if not value.type.layout_flags.top_level:
                value = create_row(value)
            
            yield [value]
            return
        
        # (list | tuple)<length = 0> | (list | tuple)<Component | (list | tuple)<Component>>
        if isinstance(value, list) or isinstance(value, tuple):
            if not value:
                yield None
                return
            
            yield from _is_component_listing(value)
            return
        
        # No other cases
        return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = 'components'
    
    def serializer_optional(value):
        if value is not None:
            yield [element.to_data() for element in value]
    
    
    def serializer_required(value):
        if value is None:
            return []
        
        return [element.to_data() for element in value]
    
    
    # Sorting
    
    sort_priority = 1400
