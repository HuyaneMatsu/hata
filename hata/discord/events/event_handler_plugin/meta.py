__all__ = ()

from itertools import chain

from ...bases.entity.slotted_meta import _get_direct_parent, _inherit_hash, _merge_type_slots

from ..core import DEFAULT_EVENT_HANDLER

from .helpers import _merge_to_type
from .event import Event
from .event_deprecation_descriptor import EventDeprecationDescriptor


def _get_reserved_attributes_from_parent(meta_type, direct_parent, type_parents):
    """
    Gets the reserved attributes from the parent type.
    
    Parameters
    ----------
    meta_type : `type`
        The meta-type.
    
    direct_parent : `type`
        The directly inherited type.
    
    type_parents : `tuple<type>`
        Cumulative parent types.
    
    Returns
    -------
    parent_event_names : `None | frozenset<str>`
    parent_default_handlers : `None | tuple<(str, async-callable, bool)>`
    parent_parameter_counts : `None | dict<str, int>`
    parent_event_deprecations : `None | frozenset<(str, EventDeprecation)>
    
    Raises
    ------
    RuntimeError
        - If a non `meta_type` parent type implements any reserved attribute.
    """
    if isinstance(direct_parent, meta_type):
        parent_event_names = direct_parent._plugin_event_names
        parent_default_handlers = direct_parent._plugin_default_handlers
        parent_parameter_counts = direct_parent._plugin_parameter_counts
        parent_event_deprecations = direct_parent._plugin_event_deprecations
    
    else:
        for type_parent in type_parents:
            for attribute_name in (
                '_plugin_event_names',
                '_plugin_default_handlers',
                '_plugin_parameter_counts',
                '_plugin_event_deprecations',
            ):
                if (getattr(type_parent, attribute_name, None) is not None):
                    raise RuntimeError(
                        f'Non {meta_type.__name__} parent type shall not implement `{attribute_name!r}`, '
                        f'but {type_parent!r} does.'
                    )
        
        parent_event_names = None
        parent_default_handlers = None
        parent_parameter_counts = None
        parent_event_deprecations = None
    
    return parent_event_names, parent_default_handlers, parent_parameter_counts, parent_event_deprecations


def _separate_events(type_attributes):
    """
    Separates out the events from the type's attributes.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        Type attributes.
    
    Returns
    -------
    events : `list<(str, Event)>`
    events_deprecated : `list<(str, Event)>`
    """
    # Collect
    events = []
    events_deprecated = []
    
    for type_attribute_name, type_attribute_value in type_attributes.items():
        if not isinstance(type_attribute_value, Event):
            continue
        
        if type_attribute_value.deprecation is None:
            container = events
        else:
            container = events_deprecated
        
        container.append((type_attribute_name, type_attribute_value))
    
    # Separate
    for event_name, event in chain(events, events_deprecated):
        del type_attributes[event_name]
    
    return events, events_deprecated


def _finalize_slots(events, slots):
    """
    Updates the slots with.
    
    Parameters
    ----------
    events : `list<(str, Event)>`
        Events to collect extra slots from.
    
    slots : `set<str>`
        Already collected slots.
    
    Returns
    -------
    finalized_sots : `tuple<str>`
    """
    slots.update(event_name for event_name, event in events)
    return tuple(sorted(slots))


def _collect_event_names(events, parent_event_names):
    """
    Collects the event names.
    
    Parameters
    ----------
    events : `list<(str, Event)>`
        Events to collect from.
    
    parent_event_names : `None | frozenset<str>`
        Event names of the parent type.
    
    Returns
    -------
    event_names : `None | frozenset<str>`
    """
    event_names = None
    for event_name, event in events:
        if event_names is None:
            event_names = []
        
        event_names.append(event_name)
    
    return _merge_to_type(parent_event_names, event_names, frozenset)


def _collect_default_handlers(events, parent_default_handlers):
    """
    Collects the default handler for each event.
    
    Parameters
    ----------
    events : `list<(str, Event)>`
        Events to collect from.
    
    parent_default_handlers : `None | tuple<(str, async-callable, bool)>`
        Default handlers of the parent type.
    
    Returns
    -------
    default_handlers : `None | tuple<(str, async-callable, bool)>`
    """
    default_handlers = None
    
    for event_name, event in events:
        default_handler = event.default_handler
        if (default_handler is None):
            default_handler = DEFAULT_EVENT_HANDLER
            instance_default_handler = False
        
        else:
            instance_default_handler = event.instance_default_handler
        
        if default_handlers is None:
            default_handlers = []
        
        default_handlers.append((event_name, default_handler, instance_default_handler))
    
    return _merge_to_type(parent_default_handlers, default_handlers, tuple)


def _collect_parameter_counts(events, parent_parameter_counts):
    """
    Collects the parameter counts for each event.
    
    Parameters
    ----------
    events : `list<(str, Event)>`
        Events to collect from.
    
    parent_parameter_counts : `None | dict<str, int>`
        Parameter counts of the parent type.
    
    Returns
    -------
    parameter_counts : `None | dict<str, int>`
    """
    parameter_counts = None
    
    for event_name, event in events:
        if (parameter_counts is None):
            parameter_counts = {}
        
        parameter_counts[event_name] = event.parameter_count
    
    if (parent_parameter_counts is not None):
        if (parameter_counts is None):
            parameter_counts = {}
        
        parameter_counts.update(parent_parameter_counts)
    
    return parameter_counts


def _collect_event_deprecations(events_deprecated, parent_event_deprecations):
    """
    Collects the deprecations from each event.
    
    Parameters
    ----------
    events_deprecated : `list<(str, Event)>`
        Deprecated events.
    
    parent_event_deprecations : `frozenset<(str, EventDeprecation)>`
        Deprecated events of the parent type.
    
    Returns
    -------
    event_deprecations : `frozenset<(str, EventDeprecation)>`
    """
    return _merge_to_type(
        (((event_name, event.deprecation) for event_name, event in events_deprecated) if events_deprecated else None),
        parent_event_deprecations,
        frozenset,
    )


class EventHandlerPluginMeta(type):
    """
    Meta type type of ``EventHandlerPlugin`` sub-types.
    
    Contains the critical logic to collect and after lookup the details about the added events.
    """
    def __new__(cls, type_name, type_parents, type_attributes):
        """
        Creates a new ``Slotted``.
        
        Parameters
        ----------
        type_name : `str`
            The created type's name.
        
        type_parents : `tuple<type>`
            The parent types of the creates type.
        
        type_attributes : `dict<str, object>`
            The type attributes of the created type.
        
        Raises
        ------
        RuntimeError
            - If there is a duplicate event entry.
        """
        direct_parent = _get_direct_parent(cls, type_name, type_parents)
        final_slots = _merge_type_slots(direct_parent, type_parents, type_attributes)
        _inherit_hash(direct_parent, type_attributes)
        
        (
            parent_event_names,
            parent_default_handlers,
            parent_parameter_counts,
            parent_event_deprecations,
        ) = _get_reserved_attributes_from_parent(cls, direct_parent, type_parents)
        events, events_deprecated = _separate_events(type_attributes)
        type_attributes['_plugin_event_names'] = _collect_event_names(events, parent_event_names)
        type_attributes['_plugin_default_handlers'] = _collect_default_handlers(events, parent_default_handlers)
        type_attributes['_plugin_parameter_counts'] = _collect_parameter_counts(events, parent_parameter_counts)
        type_attributes['_plugin_event_deprecations'] = _collect_event_deprecations(
            events_deprecated, parent_event_deprecations
        )
        type_attributes['__slots__'] = _finalize_slots(events, final_slots)
        type_attributes.update(
            (event_name, EventDeprecationDescriptor(event_name, event.deprecation))
            for event_name, event in events_deprecated
        )
        
        return type.__new__(cls, type_name, type_parents, type_attributes)
    
    
    def __call__(cls, *positional_parameters, **keyword_parameters):
        """
        Instances the type.
        
        Auto-sets event handlers.
        
        Parameters
        ----------
        *positional_parameters : Positional parameters
            Additional positional parameters.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Returns
        -------
        instance : `instance<cls>`
        """
        instance = cls.__new__(cls, *positional_parameters, **keyword_parameters)
        if type(instance) is cls:
            default_handlers = cls._plugin_default_handlers
            if (default_handlers is not None):
                for event_name, default_handler, instance_default_handler in default_handlers:
                    if instance_default_handler:
                        default_handler = default_handler()
                    
                    object.__setattr__(instance, event_name, default_handler)
            
                
            cls.__init__(instance, *positional_parameters, **keyword_parameters)
        
        return instance
