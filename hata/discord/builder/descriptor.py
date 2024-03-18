__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .constants import (
    CONVERSION_KIND_FIELD, CONVERSION_KIND_INSTANCE, CONVERSION_KIND_KEYWORD, CONVERSION_KIND_NONE,
    CONVERSION_KIND_POSITIONAL
)


def _select_setter(kind, attribute_requester):
    """
    Selects the setter for the given conversion.
    
    Parameters
    ----------
    kind : `int`
        Conversion kind to select setter for.
    attribute_requester : `callable`
        Function allowing to request type attribute before the type is created.
    
    Returns
    -------
    setter : `FunctionType`
    
    Raises
    ------
    RuntimeError
        - Unexpected kind.
        - Missing attribute.
    """
    if kind == CONVERSION_KIND_NONE:
        setter_name = '_setter_none'
    elif kind == CONVERSION_KIND_FIELD:
        setter_name = '_setter_field'
    elif kind == CONVERSION_KIND_POSITIONAL:
        setter_name = '_setter_positional'
    elif kind == CONVERSION_KIND_KEYWORD:
        setter_name = '_setter_keyword'
    elif kind == CONVERSION_KIND_INSTANCE:
        setter_name = '_setter_instance'
    else:
        raise RuntimeError(f'Unexpected kind value. Got: {kind!r}.')
    
    return attribute_requester(setter_name)


def _select_getter(kind, attribute_requester):
    """
    Selects the getter for the given conversion.
    
    Parameters
    ----------
    kind : `int`
        Conversion kind to select setter for.
    attribute_requester : `callable`
        Function allowing to request type attribute before the type is created.
    
    Returns
    -------
    getter : `FunctionType`
    
    Raises
    ------
    RuntimeError
        - Unexpected kind.
        - Missing attribute.
    """
    if kind == CONVERSION_KIND_NONE:
        getter_name = '_getter_none'
    elif kind == CONVERSION_KIND_FIELD:
        getter_name = '_getter_field'
    elif kind == CONVERSION_KIND_POSITIONAL:
        getter_name = '_getter_none'
    elif kind == CONVERSION_KIND_KEYWORD:
        getter_name = '_getter_none'
    elif kind == CONVERSION_KIND_INSTANCE:
        getter_name = '_getter_none'
    else:
        raise RuntimeError(f'Unexpected kind value. Got: {kind!r}.')
    
    return attribute_requester(getter_name)


def _conversion_descriptor_sort_key(conversion_descriptor):
    """
    Sort key for conversions.
    
    Parameters
    ----------
    conversion_descriptor : ``ConversionDescriptor``
        Conversion to get its sort key of.
    
    Returns
    -------
    sort_key : `int`
    """
    return conversion_descriptor.conversion.sort_priority


class ConversionDescriptor(RichAttributeErrorBaseType):
    """
    Wraps a conversion into a descriptor linking it into the respective type.
    
    Attributes
    ----------
    attribute_name : `None | str`
        The attribute's name the descriptor represents.
    conversion : ``Conversion``
        The descripted conversion.
    getter : `FunctionType`
        Field getter to use on get operations.
    output_conversion : ``Conversion``
        Conversion that ``.conversion`` outputs. Can be the same.
    setter : `FunctionType`
        Field setter to use on set operations.
    """
    __slots__ = ('attribute_name', 'conversion', 'getter', 'output_conversion', 'setter')
    
    def __new__(cls, attribute_name, conversion, attribute_requester):
        """
        Creates a new conversion descriptor.
        
        Parameters
        ----------
        attribute_name : `None | str`
            The attribute's name the descriptor represents.
        conversion : ``Conversion``
            Conversion we are descripting. Is that even a word?
        attribute_requester : `callable`
            Function allowing to request type attribute before the type is created.
        """
        output_conversion = conversion.output_conversion
        if output_conversion is None:
            output_conversion = conversion
        
        getter = _select_getter(output_conversion.kind, attribute_requester)
        setter = _select_setter(output_conversion.kind, attribute_requester)
        
        self = object.__new__(cls)
        self.attribute_name = attribute_name
        self.conversion = conversion
        self.getter = getter
        self.output_conversion = output_conversion
        self.setter = setter
        return self
    
    
    def __set__(self, instance, value):
        """
        Sets the field with the defined conversion.
        
        Parameters
        ----------
        instance : ``BuilderBase``
            Instance to set the fields to.
        value : `object`
            Object to set.
        
        Raises
        ------
        RuntimeError
            - Field is not settable.
        TypeError
            - `value` of invalid type given.
        """
        conversion = self.conversion
        set_validator = conversion.set_validator
        if (set_validator is None):
            raise RuntimeError(
                f'Field {conversion.name!r} is not settable.'
            )
        
        for value in set_validator(value):
            self.setter(instance, self.output_conversion, value)
            return
        
        return self.raise_type_error(None, value)
    
    
    def __get__(self, instance, instance_type):
        """
        Gets the field with the conversion.
        If accessed as a type attribute returns itself.
        
        Parameters
        ----------
        instance : `None | BuilderBase`
            Instance to set the fields to.
        instance_type : ``BuilderMeta``
            The instance's type.
        
        Returns
        -------
        value : `object`
        
        Raises
        ------
        RuntimeError
            - Field is not gettable.
        """
        if instance is None:
            return self
        
        output_conversion = self.output_conversion
        value = self.getter(instance, output_conversion)
        
        conversion = self.conversion
        if conversion is not output_conversion:
            get_processor = conversion.get_processor
            if (get_processor is not None):
                value = get_processor(value)
        
        return value
    
    
    def raise_type_error(self, key, value):
        """
        Raises context fit `TypeError` with they given `key` and `value`.
        This function always raises. Use `return ...` to help you IDE identify that it is a function exit.
        
        Parameters
        ----------
        key : `None | str`
            Conversion name to use. Can be passed as `None` to default.
        value : `object`
            The value that should be raised exception with.
        
        Raises
        ------
        TypeError
        """
        conversion = self.conversion
        if key is None:
            key = self.attribute_name
            if key is None:
                key = conversion.name
        
        raise TypeError(
            f'{key!s} can be {conversion.expected_types_messages!s}. Got {type(value).__name__}; {value!r}.'
        )
    
    
    def __repr__(self):
        """Returns the descriptor's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' conversion = ')
        repr_parts.append(repr(self.conversion))
        
        attribute_name = self.attribute_name
        if (attribute_name is not None):
            repr_parts.append(' attribute_name = ')
            repr_parts.append(repr(attribute_name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
