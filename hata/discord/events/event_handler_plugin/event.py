__all__ = ('Event',)

from scarletio import CallableAnalyzer, RichAttributeErrorBaseType

from .event_deprecation import EventDeprecation


def _validate_parameter_count(parameter_count):
    """
    Validates the `parameter_count` parameter of ``Event.__new__``.
    
    Parameters
    ----------
    parameter_count : `object`
        The parameter to validate.
    
    Returns
    -------
    parameter_count : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    # parameter_count
    if type(parameter_count) is int:
        pass
    elif isinstance(parameter_count, int):
        parameter_count = int(parameter_count)
    else:
        raise TypeError(
            f'`parameter_count` can be `int`, got {type(parameter_count).__name__}; {parameter_count!r}.'
        )
    
    if (parameter_count < 0):
        raise ValueError(
            f'`parameter_count` must be positive, got {parameter_count!r}.'
        )
    
    return parameter_count


def _validate_default_handler(default_handler, parameter_count):
    """
    Validates the given `default_handler`.
    
    Parameters
    ----------
    default_handler : `object`
        Default handler to add by default.
    
    parameter_count : `int`
        How much parameters does the event handler should accept.
    
    Returns
    -------
    default_handler : `None | async-callable`
        Default handler to add by default.
    
    instance_default_handler : `bool`
        Whether `default_handler` should be instanced.
    """
    while True:
        if (default_handler is None):
            instance_default_handler = False
            break
        
        analyzer = CallableAnalyzer(default_handler)
        
        if analyzer.is_async():
            min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
            if min_ <= parameter_count:
                if min_ == parameter_count:
                    instance_default_handler = False
                    break
                
                # min < expected
                if max_ >= parameter_count:
                    instance_default_handler = False
                    break
                
                if analyzer.accepts_args():
                    instance_default_handler = False
                    break
            
            raise TypeError(
                f'`default_handler` should accept `{parameter_count!r}` parameters as defined, '
                f'but it accepts [{min_!r}:{max_!r}], got {default_handler!r}.'
            )
        
        
        if analyzer.can_instance_to_async_callable():
            sub_analyzer = CallableAnalyzer(default_handler.__call__, as_method = True)
            if sub_analyzer.is_async():
                min_, max_ = sub_analyzer.get_non_reserved_positional_parameter_range()
                
                if min_ <= parameter_count:
                    if min_ == parameter_count:
                        instance_default_handler = True
                        break
                    
                    # min < expected
                    if max_ >= parameter_count:
                        instance_default_handler = True
                        break
                    
                    if sub_analyzer.accepts_args():
                        instance_default_handler = True
                        break
                    
                raise TypeError(
                    f'`default_handler` should accept `{parameter_count!r}` parameters as '
                    f'defined, but after instancing it accepts [{min_!r}:{max_!r}], got '
                    f'{default_handler!r}.'
                )
        
        raise TypeError(
            f'`default_handler` can be `None`, `async-callable`, instantiable to '
            f'`async-callable`, got {default_handler!r}.'
        )

    return default_handler, instance_default_handler


def _validate_deprecation(deprecation):
    """
    Validates the given `deprecation`
    
    Parameters
    ----------
    deprecation : `object`
        Deprecations to validate.
    
    Returns
    -------
    deprecation `None | tuple<Deprecations>`
    """
    if deprecation is None:
        return None
    
    if isinstance(deprecation, EventDeprecation):
        if deprecation.allowed:        
            return deprecation
        
        return None
    
    raise TypeError(
        f'`deprecation` can be `None`, `{EventDeprecation.__name__}`, '
        f'got {type(deprecation).__name__}; {deprecation!r}.'
    )


class Event(RichAttributeErrorBaseType):
    """
    Custom event slot for event handler plugins.
    
    Attributes
    ----------
    default_handler : `None | async-callable`
        Default handler to add by default.
    
    deprecation : `None | EventDeprecation`
        Deprecation for this event.
    
    instance_default_handler : `bool`
        Whether `default_handler` should be instanced.
    
    parameter_count : `int`
        How much parameters does the event handler should accept.
    """
    __slots__ = ('default_handler', 'deprecation', 'instance_default_handler', 'parameter_count')
    
    def __new__(cls, parameter_count, default_handler = None, *, deprecation = None):
        """
        Creates a new event handler instance form the given parameters.
        
        Parameters
        ---------
        parameter_count : `int`
            How much parameters does the event handler should accept.
        
        default_handler : `None | async-callable` = `None`, Optional
            Default handler to add by default.
    
        deprecation : `None | EventDeprecation` = `None`, Optional (Keyword only)
            Deprecation for this event.
        
        Raises
        ------
        TypeError
            - If `parameter_count` is not `int`.
            - If `default_handler` is neither `None`, `async-callable` and cannot be instanced to async callable either.
            - If `default_handler` accepts different amount of parameters as `parameter_count` defined.
        ValueError
            - If `parameter_count` is negative.
        """
        parameter_count = _validate_parameter_count(parameter_count)
        default_handler, instance_default_handler = _validate_default_handler(default_handler, parameter_count)
        deprecation = _validate_deprecation(deprecation)
        
        # Construct
        self = object.__new__(cls)
        self.default_handler = default_handler
        self.deprecation = deprecation
        self.instance_default_handler = instance_default_handler
        self.parameter_count = parameter_count
        return self
    
    
    def __repr__(self):
        """Returns the custom event's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # parameter_count
        repr_parts.append(' parameter_count = ')
        repr_parts.append(repr(self.parameter_count))
        
        # default_handler
        default_handler = self.default_handler
        if (default_handler is not None):
            repr_parts.append(', default_handler = ')
            repr_parts.append(repr(default_handler))
            
            if self.instance_default_handler:
                repr_parts.append(' (instance)')
        
        # deprecation
        deprecation = self.deprecation
        if (deprecation is not None):
            repr_parts.append(', deprecation = ')
            repr_parts.append(repr(deprecation))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two events are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # default_handler
        if self.default_handler != other.default_handler:
            return False
        
        # deprecation
        if self.deprecation != other.deprecation:
            return False
        
        # instance_default_handler
        if self.instance_default_handler != other.instance_default_handler:
            return False
        
        # parameter_count
        if self.parameter_count != other.parameter_count:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the event's hash value."""
        hash_value = 0
        
        # default_handler
        default_handler = self.default_handler
        if (default_handler is not None):
            try:
                default_handler_hash = hash(default_handler)
            except TypeError:
                default_handler_hash = object.__hash__(default_handler)
            hash_value ^= default_handler_hash
        
        # deprecation
        deprecation = self.deprecation
        if (deprecation is not None):
            hash_value ^= hash(deprecation)
        
        # instance_default_handler
        hash_value ^= self.instance_default_handler << 8
        
        # parameter_count
        hash_value ^= self.parameter_count
        
        return hash_value
