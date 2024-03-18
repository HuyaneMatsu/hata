__all__ = ()

from scarletio import RichAttributeErrorBaseType


def _poll_type(meta_type, type_name, base_types):
    """
    Polls the type to instantiate.
    
    Parameters
    ----------
    meta_type : `type`
        Type we are sub-instantiating.
    type_name : `str`
        The instance's name to be created.
    base_types : `tuple<type>`
        Inherited types.
    
    Returns
    -------
    base_found : `type`
        The type to use.
    
    Raises
    ------
    TypeError
        - If more base types could be instantiated.
        - If disallowed base type is given.
        - If no base type to instantiate could been detected.
    """
    base_found = None
    
    for base_type in base_types:
        if (base_type is object):
            continue
        
        if isinstance(base_type, meta_type):
            if base_found is None:
                base_found = base_type
                continue
            
            raise TypeError(
                f'Base type conflict while creating {type_name!r}. '
                f'Conversions can only have 1 conversion base type, got at least 2: '
                f'{base_found.__name__!s}, {base_type.__name__!s}.'
            )
        
        raise TypeError(
            f'Base type conflict while creating {type_name!r}. '
            f'Cannot use {base_type.__name__!s} as a conversion base type.'
        )
    
    if base_found is None:
        raise TypeError(
            f'Base type conflict while creating {type_name!r}. '
            f'Cannot create conversion type without base.'
        )
    
    return base_found


def _create_default_putter(serializer_key, serializer_optional, serializer_required):
    """
    Creates a default putter function.
    
    Parameters
    ----------
    serializer_key : `str`
        Data key.
    serializer_optional : `GeneratorFunctionType`
        Serializer to use when we want to omit defaults.
    serializer_required : `FunctionType`
        Serializer to use when we want to keep defaults.
    
    Returns
    -------
    serializer_putter : `(object, bool, object) -> object`
    """
    def serializer_putter(data, defaults, value):
        nonlocal serializer_key
        nonlocal serializer_optional
        nonlocal serializer_required
        
        if defaults:
            value = serializer_required(value)
        else:
            for value in serializer_optional(value):
                break
            else:
                return data
        
        data[serializer_key] = value
        return data
    
    return serializer_putter


class ConversionMeta(type):
    """
    Meta type for conversions.
    """
    def __new__(cls, type_name, base_types, type_attributes, *, instance = True):
        """
        Creates a new conversion.
        
        Parameters
        ----------
        type_name : `str`
            The created type's name.
        base_types : `tuple<type>`
            The parent types.
        type_attributes : `dict<str, object>`
            The type attributes of the type to be created.
        instance : `bool` = `True`, Optional (Keyword only)
            Whether to create a conversion instance or a conversion type.
        
        Returns
        -------
        type : `instance<cls> | instance<instance<cls>>`
        """
        if instance:
            return _poll_type(cls, type_name, base_types)(type_attributes)
        
        return type.__new__(cls, type_name, base_types, type_attributes)


class Conversion(RichAttributeErrorBaseType, metaclass = ConversionMeta, instance = False):
    """
    Conversion type.
    
    Attributes
    ----------
    expected_types_messages : `str`
        Holds expected type message to raise `TypeError` with.
    
    get_default : `object`
        Default value to return on get operation.
    
    get_processor : `None | FunctionType`
        Function to intercept get operations enabling processing the value.
        
        Should look like:
    
        ```py
        def get_processor(value):
            # process value
            return value
        ```
    
    kind : `int`
        The kind of the field.
    
    name : `str`
        The name of the field.
    
    name_aliases : `None | bool`
        Alternative keys to match.
    
    output_conversion : `None | instance<cls>`
        Conversion to output if its not the conversion itself.
    
    serializer_key : `None | str`
        Data key.
    
    serializer_optional : `None | GeneratorFunctionType`
        Serializer to use when we want to omit defaults.
        
        Should look like:
        
        ```py
        def serializer_optional(value):
            if value_no_default:
                # process value
                yield value
        ```
    
    serializer_putter : `None | FunctionType`
        Putter to use when serializing. Has default implementations in case it is omit.
        
        Should look like:
        
        ```py
        def serializer_putter(data, required, value):
            # put value into data
            return data
        ```
    
    serializer_required : `None | FunctionType`
        Serializer to use when we want to keep defaults.
        
        Should look like:
        
        ```py
        def serializer_required(value):
            # process value
            return value
        ```
    
    set_identifier : `None | GeneratorFunctionType`
        Identifies whether the given value is indeed matched by self.
        
        Should look like:
        
        ```py
        def set_identifier(value):
            if condition:
                # Process value as required
                yield value
                return
            
            # other conditions
            return
        ```
    
    set_listing_identifier : `None | GeneratorFunctionType`
        Identifies whether the list's elements are correct type. Should yield a processed value on success.
        
        Should look like:
    
        ```py
        def set_listing_identifier(value):
            if good:
                # Process value as required
                yield value
                return
            
            # other conditions
            return
        ```
    
    set_merger : `None | FunctionType`
        Value merger to use on field duplication.
        
        Should look like:
        
        ```py
        def set_identifier(old_value, new_value):
            # merge old and new values
            return combined_value
        ```
    
    set_type : `None | type`
        The accepted type for pre-validation to avoid O(n) validation.
    
    set_type_processor : `None | FunctionType`
        Additional processor for `set_type`.
        For cases when `output_conversion` is defined and we need to convert the value before setting.
        
        Should look like:
        
        ```py
        def set_type_processor(value):
            return value
        ```
    
    set_validator : `None | GeneratorFunctionType`
        Validator to use when `name` or `name_aliases` are matched.
        
        Should look like:
        
        ```py
        def set_validator(value):
            if condition:
                # Process value as required
                yield value
                return
            
            # other conditions
            return
        ```
    
    sort_priority : `int`
        The priority of the conversion when sorting.
    """
    __slots__ = (
        'expected_types_messages', 'get_default', 'get_processor', 'kind', 'name', 'name_aliases',
        'output_conversion', 'serializer_key', 'serializer_optional', 'serializer_putter', 'serializer_required',
        'set_identifier', 'set_listing_identifier', 'set_merger', 'set_type', 'set_type_processor', 'set_validator',
        'sort_priority'
    )
    
    def __new__(cls, instance_attributes):
        """
        Creates a new conversion.
        
        Parameters
        ----------
        instance_attributes : `dict<str, object>`
            Instances to create the conversion from.
        
        Raises
        ------
        KeyError
            Missing field.
        """
        expected_types_messages = instance_attributes.pop('expected_types_messages')
        get_default = instance_attributes.pop('get_default')
        get_processor = instance_attributes.pop('get_processor')
        kind = instance_attributes.pop('kind')
        name = instance_attributes.pop('name')
        name_aliases = instance_attributes.pop('name_aliases')
        output_conversion = instance_attributes.pop('output_conversion')
        serializer_key = instance_attributes.pop('serializer_key')
        serializer_optional = instance_attributes.pop('serializer_optional')
        serializer_putter = instance_attributes.pop('serializer_putter', None)
        serializer_required = instance_attributes.pop('serializer_required')
        set_identifier = instance_attributes.pop('set_identifier')
        set_listing_identifier = instance_attributes.pop('set_listing_identifier')
        set_merger = instance_attributes.pop('set_merger')
        set_type = instance_attributes.pop('set_type')
        set_type_processor = instance_attributes.pop('set_type_processor')
        set_validator = instance_attributes.pop('set_validator')
        sort_priority = instance_attributes.pop('sort_priority')
        
        if (
            (serializer_putter is None) and
            (serializer_key is not None) and
            (serializer_optional is not None) and
            (serializer_required is not None)
        ):
            serializer_putter = _create_default_putter(serializer_key, serializer_optional, serializer_required)
        
        self = object.__new__(cls)
        self.expected_types_messages = expected_types_messages
        self.get_default = get_default
        self.get_processor = get_processor
        self.kind = kind
        self.name = name
        self.name_aliases = name_aliases
        self.output_conversion = output_conversion
        self.serializer_key = serializer_key
        self.serializer_optional = serializer_optional
        self.serializer_putter = serializer_putter
        self.serializer_required = serializer_required
        self.set_identifier = set_identifier
        self.set_listing_identifier = set_listing_identifier
        self.set_merger = set_merger
        self.set_type = set_type
        self.set_type_processor = set_type_processor
        self.set_validator = set_validator
        self.sort_priority = sort_priority
        return self
    
    
    def iter_names(self):
        """
        Iterates over the names that should be matched by the conversion.
        
        This function is an iterable generator.
        
        Yields
        ------
        name : `str`
        """
        yield self.name
        
        name_aliases = self.name_aliases
        if (name_aliases is not None):
            yield from name_aliases
    
    
    def __repr__(self):
        """Returns the conversion's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
