__all__ = ('Event', 'EventHandlerPlugin', )


from scarletio import CallableAnalyzer

from ..bases.entity import _get_direct_parents_and_merge_slots

from .core import DEFAULT_EVENT_HANDLER


def _merge_to_type(iterable_1, iterable_2, type_):
    """
    Merges the two iterable to one of the given type.
    
    Parameters
    ----------
    iterable_1 : `None`, `iterable`
        the first iterable to merge.
    iterable_2 : `None`, `iterable`
        the second iterable to merge.
    type_ : `type`
        The expected output type.
    
    Returns
    -------
    merged : `None`, `type_`
        Returns `None` if both `iterable_1` and `iterable_2` are `None`.
    """
    if iterable_1 is None:
        if iterable_2 is None:
            merged = None
        else:
            if type(iterable_2) is type_:
                merged = iterable_2
            else:
                merged = type_(iterable_2)
    
    else:
        if iterable_2 is None:
            if type(iterable_1) is type_:
                merged = iterable_1
            else:
                merged = type_(iterable_1)
        
        else:
            merged = (*iterable_1, *iterable_2)
            
            if type_ is not tuple:
                merged = type_(merged)
    
    return merged


class Event:
    """
    Custom event slot for event handler plugins.
    
    Attributes
    ----------
    callback : `None`, `callable`
        Optional function to run when an event handler is added or removed.
    default_handler : `None`, `async-callable`
        Default handler to add by default.
    instance_default_handler : `bool`
        Whether `default_handler` should be instanced.
    parameter_count : `int`
        How much parameters does the event handler should accept.
    """
    __slots__ = ('callback', 'default_handler', 'instance_default_handler', 'parameter_count')
    
    def __new__(cls, parameter_count, default_handler = None, callback = None):
        """
        Creates a new event handler instance form the given parameters.
        
        Parameters
        ---------
        parameter_count : `int`
            How much parameters does the event handler should accept.
        default_handler : `None`, `async-callable` = `None`, Optional
            Default handler to add by default.
        callback : `None`, `callable` = `None`, Optional
            Optional function to run when an event handler is added or removed.
        
        Raises
        ------
        TypeError
            - If `parameter_count` is not `int`.
            - If `default_handler` is neither `None`, `async-callable` and cannot be instanced to async callable either.
            - If `default_handler` accepts different amount of parameters as `parameter_count` defined.
        ValueError
            - If `parameter_count` is negative.
        """
        
        # Check `parameter_count`
        if type(parameter_count) is int:
            pass
        elif isinstance(parameter_count, int):
            parameter_count = int(parameter_count)
        else:
            raise TypeError(
                f'`parameter_count` can be `int`, got {parameter_count.__class__.__name__}; {parameter_count!r}.'
            )
        
        if (parameter_count < 0):
            raise ValueError(
                f'`parameter_count` cannot be negative, got {parameter_count!r}.'
            )
        
        # Check `default_handler`
        if (default_handler is None):
            instance_default_handler = False
        else:
            while True:
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
                    
                    sub_analyzer = CallableAnalyzer(default_handler.__call__, as_method=True)
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
        
        # Check `callback`
        # TODO
        
        self = object.__new__(cls)
        self.parameter_count = parameter_count
        self.default_handler = default_handler
        self.instance_default_handler = instance_default_handler
        self.callback = callback
        return self
    
    def __repr__(self):
        """Returns the custom event's representation."""
        repr_parts = [self.__class__.__name__, ' parameter_count = ', repr(self.parameter_count)]
        
        default_handler = self.default_handler
        if (default_handler is not None):
            repr_parts.append(', default_handler = ')
            repr_parts.append(repr(default_handler))
            
            if self.instance_default_handler:
                repr_parts.append(' (instance)')
        
        callback = self.callback
        if (callback is None):
            repr_parts.append(', callback = ')
            repr_parts.append(repr(callback))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class EventHandlerPluginType(type):
    """
    Metaclass of ``EventHandlerPlugin`` subclasses.
    
    Contains the critical logic to collect and after lookup the details about the added events.
    """
    def __new__(cls, class_name, class_parents, class_attributes):
        """
        Creates a new ``Slotted``.
        
        Parameters
        ----------
        class_name : `str`
            The created class's name.
        class_parents : `tuple` of `type`
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        
        Raises
        ------
        RuntimeError
            - If there is a duplicate event entry.
        """
        direct_parent, final_slots = _get_direct_parents_and_merge_slots(class_name, class_parents, class_attributes)
        
        if isinstance(direct_parent, cls):
            old_event_names = direct_parent._plugin_event_names
            old_default_handlers = direct_parent._plugin_default_handlers
            old_non_default_handlers = direct_parent._plugin_non_default_handlers
            old_callbacks = direct_parent._plugin_callbacks
            old_parameter_counts = direct_parent._plugin_parameter_counts
        else:
            for class_parent in class_parents:
                for attribute_name in (
                    '_plugin_event_names',
                    '_plugin_default_handlers',
                    '_plugin_non_default_handlers',
                    '_plugin_callbacks',
                    '_plugin_parameter_counts',
                ):
                    if (getattr(class_parent, attribute_name, None) is not None):
                        raise RuntimeError(
                            f'superclasses shall not implement `{attribute_name!r}`, but {class_parent!r} does.'
                        )
            
            old_event_names = None
            old_default_handlers = None
            old_non_default_handlers = None
            old_callbacks = None
            old_parameter_counts = None
        
        # Do small cycles
        
        # Collect events.
        events = []
        
        for class_attribute_name, class_attribute_value in class_attributes.items():
            if isinstance(class_attribute_value, Event):
                events.append((class_attribute_name, class_attribute_value))
        
        # Remove class attributes
        for event_name, event in events:
            del class_attributes[event_name]
        
        # Collect event names
        event_names = []
        for event_name, event in events:
            event_names.append(event_name)
        
        event_names = _merge_to_type(old_event_names, event_names, frozenset)
        
        # Extend slots
        final_slots.update(event_names)
        
        # Collect default and non-default handlers.
        default_handlers = None
        non_default_handlers = None
        
        for event_name, event in events:
            default_handler = event.default_handler
            if (default_handler is None):
                if non_default_handlers is None:
                    non_default_handlers = []
                
                non_default_handlers.append(event_name)
                
            else:
                if default_handlers is None:
                    default_handlers = []
                
                default_handlers.append((event_name, default_handler, event.instance_default_handler))
        
        default_handlers = _merge_to_type(old_default_handlers, default_handlers, tuple)
        non_default_handlers = _merge_to_type(old_non_default_handlers, non_default_handlers, tuple)
        
        # Collect callbacks
        callbacks = None
        for event_name, event in events:
            callback = event.callback
            if (callback is not None):
                if callbacks is None:
                    callbacks = {}
                
                callbacks[event_name] = callback
        
        if (old_callbacks is not None):
            if callbacks is None:
                callbacks = old_callbacks.copy()
            else:
                callbacks = {**old_callbacks, **callbacks}
        
        # collect parameter counts.
        parameter_counts = {}
        for event_name, event in events:
            parameter_counts[event_name] = event.parameter_count
        
        if (old_parameter_counts is not None):
            parameter_counts.update(old_parameter_counts)
        
        class_attributes['_plugin_event_names'] = event_names
        class_attributes['_plugin_default_handlers'] = default_handlers
        class_attributes['_plugin_non_default_handlers'] = non_default_handlers
        class_attributes['_plugin_callbacks'] = callbacks
        class_attributes['_plugin_parameter_counts'] = parameter_counts
        
        class_attributes['__slots__'] = tuple(sorted(final_slots))
        
        return type.__new__(cls, class_name, class_parents, class_attributes)
    
    
    def __call__(cls, *args, **kwargs):
        """
        Instances the type.
        
        Auto-sets event handlers.
        
        Parameters
        ----------
        *args : Additional positional parameters
        **kwargs : Additional keyword parameters
        
        Returns
        -------
        object_ : `Any`
        """
        object_ = cls.__new__(cls, *args, **kwargs)
        if type(object_) is cls:
            default_handlers = cls._plugin_default_handlers
            if (default_handlers is not None):
                for event_name, default_handler, instance_default_handler in default_handlers:
                    if instance_default_handler:
                        default_handler = default_handler()
                    
                    object.__setattr__(object_, event_name, default_handler)
            
            non_default_handlers = cls._plugin_non_default_handlers
            if (non_default_handlers is not None):
                for event_name in non_default_handlers:
                    object.__setattr__(object_, event_name, DEFAULT_EVENT_HANDLER)
                
                
            cls.__init__(object_, *args, **kwargs)
        
        return object_


class EventHandlerPlugin(metaclass=EventHandlerPluginType):
    """
    Inherit event handler manager plugins from this class, like:
    
    ```py
    class MyPlugin(EventHandlerPlugin):
        my_event = Event(...)
    ```
    
    Each ``Event`` will be picked up and added as a plugin event.
    
    To register the plugin:
    
    ```
    my_plugin = MyPlugin()
    client.events.register_plugin(my_plugin)
    ```
    
    After it, you are able to add new event handlers to your client.
    
    ```py
    @client.events
    async def my_event(...):
        pass
    ```
    
    To ensure an event, do:
    
    ```py
    Task(KOKORO, my_plugin.my_event(...))
    ```
    """
    __slots__ = ()
