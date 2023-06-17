__all__ = ('Menu',)

from collections import OrderedDict
from types import MemberDescriptorType

from scarletio import CallableAnalyzer, CancelledError, RichAttributeErrorBaseType, Task, copy_docs

from ....discord.allowed_mentions import AllowedMentionProxy
from ....discord.channel import Channel
from ....discord.client import Client
from ....discord.core import KOKORO
from ....discord.embed import Embed
from ....discord.exceptions import DiscordException, ERROR_CODES
from ....discord.component import Component, ComponentType, create_row
from ....discord.interaction import  InteractionEvent, InteractionType
from ....discord.message import Message

from ..waiters import Timeouter


GUI_STATE_NONE = 0
GUI_STATE_READY = 1
GUI_STATE_EDITING = 2
GUI_STATE_CANCELLING = 3
GUI_STATE_CANCELLED = 4
GUI_STATE_SWITCHING_CONTEXT = 5

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_MESSAGE_COMPONENT = InteractionType.message_component

class ComponentSourceIdentityHasher:
    """
    Hasher for components based on their identity.
    
    Attributes
    ----------
    component : ``Component``
        The stored component by the hasher.
    """
    __slots__ = ('component', )
    
    def __init__(self, component):
        """
        Creates a new ``ComponentSourceIdentityHasher`` with the given parameters.
        
        Parameters
        ----------
        component : ``Component``
            The source component.
        """
        self.component = component
    
    def __hash__(self):
        """Returns the component source identity hasher's hash value."""
        return object.__hash__(self.component)
    
    def __eq__(self, other):
        """Returns whether the two component identity hashers are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.component is other.component



class ComponentDescriptor:
    """
    Descriptor to proxy class attribute component access for each instance.
    
    Attributes
    ----------
    _source_component : ``Component``
        The source component from which the descriptor is created from.
    _sub_component_descriptors : `None`, `list` of ``ComponentDescriptor``
        Sub components applicable to the component.
    _identifier : `int`
        The descriptor's identifier.
    
    Class Attributes
    ----------------
    _identifier_counter : `int`
        Identifier counter for caching.
    """
    __slots__ = ('_source_component', '_sub_component_descriptors', '_identifier',)
    
    _identifier_counter = 0
    
    
    def __new__(cls, source_component, sub_components):
        """
        Creates a new ``ComponentDescriptor`` from the given component.
        
        Parameters
        ----------
        source_component : ``Component``
            The source component to create the descriptor from.
        sub_component_descriptors : `None`, `list` of ``ComponentDescriptor``
            A list of sub components added
        """
        identifier = cls._identifier_counter + 1
        cls._identifier_counter = identifier
        
        self = object.__new__(cls)
        self._source_component = source_component
        self._sub_component_descriptors = sub_components
        self._identifier = identifier
        return self
    
    
    def __get__(self, instance, type_):
        """
        Gets the descriptor itself if called from class or a component proxy.
        
        Parameters
        ----------
        instance : `None`, ``Menu``
            The menu instance.
        type_ : ``MenuType``
            The menu's type.
        
        Returns
        -------
        self / component : ``ComponentDescriptor`` / ``Component``
            Self if called from class, or the a component proxy for the represented component.
        """
        if instance is None:
            return self
        
        component_cache = instance._component_cache
        try:
            component = component_cache[self._identifier]
        except KeyError:
            component = self._create_component(instance)
            component_cache[self._identifier] = component
        
        return component
    
    
    def __set__(self, instance, value):
        """
        Sets a new component overwriting the already existing value.
        
        Parameters
        ----------
        instance : `None`, ``Menu``
            The menu instance.
        value : ``Component``
            The component to set.
        
        Raises
        ------
        TypeError
            - If `value` is not a ``Component`` instance.
        """
        if not isinstance(value, Component):
            raise TypeError(
                f'Attribute can be set only as `{Component.__name__}`, got {value.__class__.__name__}; {value!r}.'
            )
            
        instance._component_cache[self._identifier] = value
    
    
    def _create_component(self, instance):
        """
        Crates the component of the descriptor.
        
        Parameters
        ----------
        instance : ``Menu``
            The menu instance.
        
        Returns
        -------
        component : ``Component``
        """
        sub_component_descriptors = self._sub_component_descriptors
        source_component = self._source_component
        if (sub_component_descriptors is None):
            return source_component.copy()
        
        return source_component.copy_with(
            components = [
                sub_component_descriptor.__get__(instance, type(instance))
                for sub_component_descriptor in sub_component_descriptors
            ],
        )
    
    def __repr__(self):
        """Returns the component descriptor's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' identifier=', repr(self._identifier),
            ', source_component=', repr(self._source_component),
        ]
        
        sub_component_descriptors = self._sub_component_descriptors
        if (sub_component_descriptors is not None):
            repr_parts.append(' sub_component_descriptors=')
            repr_parts.append(repr(sub_component_descriptors))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


def validate_check(check):
    """
    Validates the given check.
    
    Parameters
    ----------
    check : `None` of `callable`
        The check to validate.
    
    Raises
    ------
    TypeError
        If `check` is not `None` neither a non-async function accepting 1 parameter.
    """
    if check is None:
        return
    
    analyzer = CallableAnalyzer(check)
    if analyzer.is_async():
        raise TypeError(
            f'`check` should have NOT be an `async` function, got {check!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 2:
        raise TypeError(
            f'`check` should accept `2` parameters, meanwhile the given one expects at '
            f'least `{min_!r}`, got {check!r}.'
        )
    
    if min_ != 2:
        if max_ < 2:
            if not analyzer.accepts_positional_parameters():
                raise TypeError(
                    f'`check` should accept `2` parameters, meanwhile the given one expects '
                    f'up to `{max_!r}`, got {check!r}.'
                )


def validate_invoke(invoke):
    """
    Validates the given invoker.
    
    Parameters
    ----------
    invoke : `None`, `async-callable`
        The invoker to validate.
    
    Raises
    ------
    TypeError
        If `invoke` is not `None` nor `async-callable` accepting `2` parameter.
    """
    if invoke is None:
        return
    
    analyzer = CallableAnalyzer(invoke)
    if not analyzer.is_async():
        raise TypeError(
            f'`invoke` should be an `async` function, got {invoke!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    
    if min_ > 2:
        raise TypeError(
            f'`invoke` should accept `2` parameters, meanwhile the given one expects at '
            f'least `{min_!r}`, got {invoke!r}.'
        )
    
    if min_ != 2:
        if max_ < 2:
            if not analyzer.accepts_positional_parameters():
                raise TypeError(
                    f'`invoke` should accept `2` parameters, meanwhile the given one expects '
                    f'up to `{max_!r}`, got {invoke!r}.'
                )


def validate_initial_invoke(initial_invoke):
    """
    Validates the given default content getter.
    
    Parameters
    ----------
    initial_invoke : `None`, `async-callable`
        The default content getter to validate.
    
    Raises
    ------
    TypeError
        If `initial_invoke` is not `None` nor `async-callable` accepting `1` parameters.
    """
    if initial_invoke is None:
        return
    
    analyzer = CallableAnalyzer(initial_invoke)
    if not analyzer.is_async():
        raise TypeError(
            f'`initial_invoke` should be an `async` function, got {initial_invoke!r}'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 1:
        raise TypeError(
            f'`initial_invoke` should accept `1` parameters, meanwhile the given one expects at '
            f'least `{min_!r}`, got {initial_invoke!r}.'
        )
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_positional_parameters():
                raise TypeError(
                    f'`initial_invoke` should accept `1` parameters, meanwhile the given callable '
                    f'expects up to `{max_!r}`, got {initial_invoke!r}.'
                )


def validate_get_timeout(get_timeout):
    """
    Validates the given timeout getter.
    
    Parameters
    ----------
    get_timeout : `None`, `callable`
        Timeout getter.
    
    Raises
    ------
    TypeError
        If `get_timeout` is not `None` nor `callable` accepting `1` parameters.
    """
    if get_timeout is None:
        return
    
    analyzer = CallableAnalyzer(get_timeout)
    if analyzer.is_async():
        raise TypeError(
            f'`get_timeout` should not be an `async` function, got {get_timeout!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 1:
        raise TypeError(
            f'`get_timeout` should accept `1` parameter, meanwhile the given one expects at '
            f'least `{min_!r}`, got {get_timeout!r}.'
        )
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_positional_parameters():
                raise TypeError(
                    f'`get_timeout` should accept `1` parameters, meanwhile the given callable '
                    f'expects up to `{max_!r}`, got {get_timeout!r}.'
                )


def validate_close(close):
    """
    Validates the given closer.
    
    Parameters
    ----------
    close : `callable`
        The closer to validate.
    
    Raises
    ------
    TypeError
        If `close` is not `None` nor an `async-callable` accepting 1 parameter.
    """
    if close is None:
        return
    
    analyzer = CallableAnalyzer(close)
    if not analyzer.is_async():
        raise TypeError(
            f'`close` should be an `async` function, got {close!r}.'
        )
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 2:
        raise TypeError(
            f'`close` should accept `2` parameters, meanwhile the given one expects at '
            f'least `{min_!r}`, got {close!r}.'
        )
    
    if min_ != 2:
        if max_ < 2:
            if not analyzer.accepts_positional_parameters():
                raise TypeError(
                    f'`close` should accept `2` parameters, meanwhile the given one expects '
                    f'up to `{max_!r}`, got {close!r}.'
                )


def validate_init(init):
    """
    Validates the given initializer.
    
    Parameters
    ----------
    init : `callable`
        The initializer to validate.
    
    Raises
    ------
    TypeError
        If `init` is not `None` or is `async-callable` or accepts less than `3` parameters.
    """
    if (init is None) or (init is object.__init__):
        return
    
    analyzer = CallableAnalyzer(init)
    if analyzer.is_async():
        raise TypeError(
            f'`init` should not be an `async` function, got {init!r}.')
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ < 3:
        raise TypeError(
            f'`init` should accept at least `3` parameters, meanwhile the given one expects at '
            f'least `{min_!r}`, got {init!r}.'
        )


class MenuStructure:
    """
    A special object to store special methods of a menu.
    
    Attributes
    ----------
    check : `None`, `function`
        The function to call when checking whether an event should be called.
        
        Should accept the following parameters:
        
        +-----------+-----------------------+
        | Name      | Type                  |
        +===========+=======================+
        | self      | ``Menu``              |
        +-----------+-----------------------+
        | event     | ``InteractionEvent``  |
        +-----------+-----------------------+
        
        > ``ReactionDeleteEvent`` is only given, when the client has no `manage_messages` permission.
        
        Should return the following values:
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | should_process    | `bool`    |
        +-------------------+-----------+
    
    get_timeout : `None`, `Function`
        Return the time after the menu should be closed.
        
        > Define it as non-positive to never timeout. Not recommended.
        
        Should accept the following parameters:
        
        +-----------+-----------+
        | Name      | Type      |
        +===========+===========+
        | self      | ``Menu``  |
        +-----------+-----------+
        
        
        Should return the following parameter:
        
        +---------------+-----------+
        | Name          | Type      |
        +===============+===========+
        | timeout       | `int`     |
        +---------------+-----------+
    
    close : `None`, `CoroutineFunction`
        Function to call when the menu is closed.
        
        Should accept the following parameters:
        
        +-----------+---------------------------+
        | Name      | Type                      |
        +===========+===========================+
        | self      | ``Menu``                  |
        +-----------+---------------------------+
        | exception | `None`, `BaseException` |
        +-----------+---------------------------+
    
    init : `None`, `Function`
        Initializer function.
    
        Should accept the following parameters:
        
        +-------------------+---------------------------+
        | Name              | Type                      |
        +===================+===========================+
        | self              | ``Menu``                  |
        +-------------------+---------------------------+
        | interaction_event | ``InteractionEvent``      |
        +-------------------+---------------------------+
        | *positional_parameters             | Positional parameters     |
        +-------------------+---------------------------+
        | **keyword_parameters          | Keyword parameters        |
        +-------------------+---------------------------+
    
    initial_invoke : `None`, `CoroutineFunction`
        Function to generate the default page of the menu.
        
        Should accept the following parameters:
        
        +-----------+-----------+
        | Name      | Type      |
        +===========+===========+
        | self      | ``Menu``  |
        +-----------+-----------+
        
    is_final : `bool`
        Whether the Menu has all the required fields fulfilled.
    
    invoke : `None`, `CoroutineFunction`
        The function call for result when invoking the menu.
        
        Should accept the following parameters:
        
        +-----------+-----------------------+
        | Name      | Type                  |
        +===========+=======================+
        | self      | ``Menu``              |
        +-----------+-----------------------+
        | event     | ``InteractionEvent``  |
        +-----------+-----------------------+
        
        Should return the following parameter:
        
        +---------------+-----------+
        | Name          | Type      |
        +===============+===========+
        | should_edit   | `bool`    |
        +---------------+-----------+
    """
    __slots__ = ('check', 'close', 'get_timeout', 'init', 'is_final', 'initial_invoke', 'invoke')
    
    def __new__(cls, class_attributes):
        """
        Creates a new menu structure instance from the given class attributes dictionary.
        
        Parameters
        ----------
        class_attributes : `dict` of (`str`, `object`) items
            Class attributes of a type.
        
        Raises
        ------
        TypeError
            - If `check` is not `None` neither a non-async function.
            - If `check` accepts less or more than `2` parameters.
            - If `invoke` is not `None` nor an `async-callable`.
            - If `invoke` accepts less or more than `2` parameters.
            - If `initial_invoke` is not `None`, nor an `async-callable`.
            - If `initial_invoke` accepts less or more than `1` parameter.
            - If `get_timeout` is not a non-async callable.
            - If `get_timeout` accepts less or more than `1` parameter.
            - If `close` is neither `None` nor `async-callable`.
            - If `close` accepts more or less than `2` parameters.
            - If `init` is not `None` or is `async-callable`.
            - If `init` accepts less than `3` parameters.
        """
        self = class_attributes.get('_menu_structure', None)
        if (self is not None) and (type(self) is cls):
            return self
        
        check = class_attributes.get('check', None)
        validate_check(check)
        
        invoke = class_attributes.get('invoke', None)
        validate_invoke(invoke)
        
        initial_invoke = class_attributes.get('initial_invoke', None)
        validate_initial_invoke(initial_invoke)
        
        get_timeout = class_attributes.get('get_timeout', None)
        validate_get_timeout(get_timeout)
        
        close = class_attributes.get('close', None)
        validate_close(close)
        
        init = class_attributes.get('__init__', None)
        validate_init(init)
        
        if (invoke is None) or (initial_invoke is None):
            is_final = False
        else:
            is_final = True
        
        self = object.__new__(cls)
        self.is_final = is_final
        self.check = check
        self.close = close
        self.init = init
        self.initial_invoke = initial_invoke
        self.invoke = invoke
        self.get_timeout = get_timeout
        
        return self
    
    
    def __repr__(self):
        """Returns the user menu structure's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        check = self.check
        if (check is None):
            field_added = False
        else:
            field_added = True
            
            repr_parts.append(' check=')
            repr_parts.append(repr(check))
        
        close = self.close
        if (close is not None):
            if field_added:
                repr_parts.append(', ')
            else:
                field_added = True
            
            repr_parts.append(' close=')
            repr_parts.append(repr(close))
        
        init = self.init
        if (init is not None):
            if field_added:
                repr_parts.append(', ')
            else:
                field_added = True
            
            repr_parts.append(' init=')
            repr_parts.append(repr(init))
        
        initial_invoke = self.initial_invoke
        if (initial_invoke is not None):
            if field_added:
                repr_parts.append(', ')
            else:
                field_added = True
            
            repr_parts.append(' initial_invoke=')
            repr_parts.append(repr(initial_invoke))
        
        invoke = self.invoke
        if (invoke is not None):
            if field_added:
                repr_parts.append(', ')
            else:
                field_added = True
            
            repr_parts.append(' invoke=')
            repr_parts.append(repr(invoke))
        
        get_timeout = self.get_timeout
        if (get_timeout is not None):
            if field_added:
                repr_parts.append(', ')
            
            repr_parts.append(' get_timeout=')
            repr_parts.append(repr(get_timeout))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def merge(self, other):
        """
        Merges the two menu structure.
        
        Parameters
        ----------
        other : ``MenuStructure``
            The other menu structure to merge into self creating a new one.
        
        Returns
        -------
        new : ``MenuStructure``
        """
        check = self.check
        if check is None:
            check = other.check
        
        close = self.close
        if close is None:
            close = other.close
        
        init = self.init
        if init is None:
            init = other.init
        
        initial_invoke = self.initial_invoke
        if initial_invoke is None:
            initial_invoke = other.initial_invoke
        
        invoke = self.invoke
        if invoke is None:
            invoke = other.invoke
        
        get_timeout = self.get_timeout
        if get_timeout is None:
            get_timeout = other.get_timeout
        
        if (invoke is None) or (initial_invoke is None):
            is_final = False
        else:
            is_final = True
        
        new = object.__new__(type(self))
        new.check = check
        new.close = close
        new.init = init
        new.initial_invoke = initial_invoke
        new.invoke = invoke
        new.get_timeout = get_timeout
        new.is_final = is_final
        
        return new


def _iter_attributes(class_parents, class_attributes):
    """
    Iterates over the given class's attributes and the given attributes.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    class_parents : `tuple` of `type`
        Parent classes.
    class_attributes : `dict` of (`str`, `object`) items
        Class attributes of the source type.
    
    Yields
    ------
    attribute_name : `str`
        An attribute's name.
    attribute_value : `object`
        An attribute's value.
    """
    for class_parent in reversed(class_parents):
        yield from class_parent.__dict__.items()
    
    yield from class_attributes.items()


def _get_component_descriptor(component, component_descriptors, sub_component_descriptors):
    """
    Gets the component descriptor for the given component.
    
    Parameters
    ----------
    component : ``Component``
        The component to get the descriptor for.
    component_descriptors : `dict` of (``ComponentSourceIdentityHasher``, ``ComponentDescriptor``) items
        Already matched component descriptors.
    sub_component_descriptors : `None`, `list` of ``ComponentDescriptor``
        Sub descriptors used by the main one.
    
    Returns
    -------
    component_descriptor : ``ComponentDescriptor``
    """
    component_hasher = ComponentSourceIdentityHasher(component)
    try:
        component_descriptor = component_descriptors[component_hasher]
    except KeyError:
        component_descriptor = ComponentDescriptor(component, sub_component_descriptors)
        component_descriptors[component_hasher] = component_descriptor
    
    return component_descriptor


DISALLOWED_MENU_ATTRIBUTE_NAMES = (
    '__new__',
    '__call__',
    'cancel',
    '_canceller_function',
    '_handle_close_exception',
    'content',
    'embed',
    'allowed_mentions',
    'components',
)

Menu = None

class MenuType(type):
    """
    Meta type for ``Menu``-s.
    """
    def __new__(cls, class_name, class_parents, class_attributes):
        """
        Creates a Discord entity type. Subclass ``DiscordEntity`` instead of using this class directly as a metaclass.
        
        Parameters
        ----------
        class_name : `str`
            The created class's name.
        class_parents : `tuple` of `type`
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `object`) items
            The class attributes of the created type.
        
        Returns
        -------
        type : ``MenuType``
        """
        if (Menu is not None):
            for attribute_name in DISALLOWED_MENU_ATTRIBUTE_NAMES:
                menu_attribute = getattr(Menu, attribute_name)
                try:
                    actual_attribute = class_attributes[attribute_name]
                except KeyError:
                    class_attributes[attribute_name] = menu_attribute
                else:
                    if (actual_attribute is not menu_attribute):
                        raise TypeError(
                            f'Overwriting `{attribute_name}` is disallowed.'
                        )
        
        old_menu_structure = None
        for class_parent in reversed(class_parents):
            new_menu_structure = MenuStructure(class_parent.__dict__)
            if old_menu_structure is None:
                old_menu_structure = new_menu_structure
            else:
                old_menu_structure = new_menu_structure.merge(old_menu_structure)
        
        new_menu_structure = MenuStructure(class_attributes)
        if (old_menu_structure is not None):
            new_menu_structure = new_menu_structure.merge(old_menu_structure)
        
        class_attributes['_menu_structure'] = new_menu_structure
        
        
        component_descriptors = {}
        components_to_track = []
        new_attributes = {}
        
        for attribute_name, attribute_value in _iter_attributes(class_parents, class_attributes):
            if isinstance(attribute_value, ComponentDescriptor):
                component_hasher = ComponentSourceIdentityHasher(attribute_value._source_component)
                component_descriptors[component_hasher] = attribute_value
                new_attributes[attribute_name] = attribute_value
                continue
            
            if isinstance(attribute_value, Component):
                components_to_track.append((attribute_name, attribute_value))
                continue
        
        
        for attribute_name, attribute_value in components_to_track:
            if attribute_value.components is None:
                sub_component_descriptors = None
            
            else:
                sub_component_descriptors = [
                    _get_component_descriptor(sub_component, component_descriptors, None)
                    for sub_component in attribute_value.iter_components()
                ]
                
            component_descriptor = _get_component_descriptor(
                attribute_value, component_descriptors, sub_component_descriptors
            )
        
            new_attributes[attribute_name] = component_descriptor
            continue    
        
        
        for attribute_name, attribute_value in new_attributes.items():
            class_attributes[attribute_name] = attribute_value
        
        if '__slots__' not in class_attributes:
            class_attributes['__slots__'] = ('__dict__', )
        
        return type.__new__(cls, class_name, class_parents, class_attributes)


class Menu(metaclass = MenuType):
    """
    Base class for custom component based menus.
    
    Attributes
    ----------
    _allowed_mentions : ``Ellipsis``, `None`, `list` of `object`
        The used allowed mentions when editing the respective message.
    _canceller : None`, `CoroutineFunction`
        Canceller set as `._canceller_function``, meanwhile the gui is not cancelled.
    _components : `None`, `tuple` of ``Component``
        Rendered components of the menu.
    _component_cache : `dict` of (`int`, ``ComponentProxy``) items
        A dictionary of component proxy identifiers and component proxies.
    _gui_state : `int`
        The gui's state.
        
        Can be any of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +===============================+=======+
        | GUI_STATE_NONE                | 0     |
        +===============================+=======+
        | GUI_STATE_READY               | 1     |
        +-------------------------------+-------+
        | GUI_STATE_EDITING             | 2     |
        +-------------------------------+-------+
        | GUI_STATE_CANCELLING          | 3     |
        +-------------------------------+-------+
        | GUI_STATE_CANCELLED           | 4     |
        +-------------------------------+-------+
        | GUI_STATE_SWITCHING_CONTEXT   | 5     |
        +-------------------------------+-------+
    _timeouter : `None`, ``Timeouter``
        Executes the timeout feature on the menu.
    _tracked_changes : `dict` of (`str`, `object`) items
        The tracked changes by parameter name.
    channel : ``Channel``
        The channel where the menu is executed.
    client : ``Client``
        The executor client instance.
    message : `None`, ``Message``
        The message which executes the menu.
    
    Class Attributes
    ----------------
    _menu_structure : ``MenuStructure``
        Factorized methods added by the user used by the menu itself.
    """
    __slots__ = (
        '_allowed_mentions', '_canceller', '_component_cache', '_gui_state', '_timeouter', '_tracked_changes',
        'channel', 'client', 'message', '_components',
    )
    
    async def __new__(cls, client, target, *positional_parameters, **keyword_parameters):
        """
        Creates a new menu instance.
        
        Parameters
        ----------
        client : ``Client``
            The client instance whi will execute the action.
        target : ``InteractionEvent``, ``Message``, ``Channel``, `int`
            The event to respond to, or the channel to send the message at, or the message to edit.
        *positional_parameters : Positional parameters
            Additional positional parameters.
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Raises
        ------
        TypeError
            If `interaction_event` was not given neither as ``InteractionEvent``, ``Message``, ``Channel``,
             nor as instance.
        RuntimeError
            If `interaction_event` is given as ``InteractionEvent``, but it's client cannot be detected.
        """
        menu_structure = cls._menu_structure
        if not menu_structure.is_final:
            raise RuntimeError(
                f'{cls.__class__.__name__} has not every required fields fulfilled. Required fields: '
                f'`initial_invoke`, `invoke`.'
            )
        
        # use goto
        while True:
            if isinstance(target, InteractionEvent):
                target_message = target.message # Should be `None`
                interaction_event = target
                is_interaction = True
                break
                
            if isinstance(target, Message):
                target_channel_id = target.channel_id
                target_message = target
                is_interaction = False
                break
            
            if isinstance(target, Channel):
                target_channel_id = target.id
                target_message = None
                is_interaction = False
                break
            
            if isinstance(target, int):
                target_channel_id = target
                target_message = None
                is_interaction = False
                break
                
                
            raise TypeError(
                f'`target` can be `{InteractionEvent.__name__}`, '
                f'`{Message.__name__}`, `{Channel.__name__}`, `int`, got '
                f'{target.__class__.__name__}; {target!r}.'
            )
        
        self = object.__new__(cls)
        self._canceller = None
        self.message = target_message
        self.client = client
        self._gui_state = GUI_STATE_NONE
        self._timeouter = None
        self._tracked_changes = {}
        self._allowed_mentions = None
        self._component_cache = {}
        self._components = None
        
        init = menu_structure.init
        if (init is not None):
            init(self, client, target, *positional_parameters, **keyword_parameters)
        
        await menu_structure.initial_invoke(self)
        
        tracked_changes = self._tracked_changes
        if not tracked_changes:
            raise RuntimeError(
                f'{cls.__class__.__name__}\'s `initial_invoke` method: '
                f'{menu_structure.initial_invoke!r} did not change any parameters.'
            )
        
        keyword_parameters = tracked_changes.copy()
        tracked_changes.clear()
        
        allowed_mentions = self._allowed_mentions
        if (allowed_mentions is not None):
            keyword_parameters['allowed_mentions'] = allowed_mentions
        
        keyword_parameters['components'] = self._components
        
        if is_interaction:
            interaction_event_type = interaction_event.type
            if interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
                if target_message is None:
                    if interaction_event.is_unanswered():
                        await client.interaction_application_command_acknowledge(interaction_event)
                    
                    target_message = await client.interaction_followup_message_create(
                        interaction_event, **keyword_parameters
                    )
                else:
                    await client.interaction_response_message_edit(interaction_event, **keyword_parameters)
            
            elif interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
                await client.interaction_component_message_edit(interaction_event, **keyword_parameters)
            
            else:
                # nani desu ka?
                return
        
        else:
            if target_message is None:
                target_message = await client.message_create(target_channel_id, **keyword_parameters)
            else:
                await client.message_edit(target_message, **keyword_parameters)
        
        self.message = target_message
        
        get_timeout = menu_structure.get_timeout
        if (get_timeout is None):
            timeout = -1.0
        else:
            timeout = get_timeout(self)
        
        if (timeout > 0.0):
            self._timeouter = Timeouter(self, timeout)
        
        self._gui_state = GUI_STATE_READY
        self._canceller = cls._canceller_function
        
        client.slasher.add_component_interaction_waiter(target_message, self)
        
        return self
    
    
    async def __call__(self, interaction_event):
        """
        Processes a received component interaction event.
        
        This method is a coroutine.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``
            Component interaction event.
        """
        client = self.client
        gui_state = self._gui_state
        if (gui_state == GUI_STATE_EDITING) or (GUI_STATE_EDITING == GUI_STATE_CANCELLING):
            await client.interaction_component_acknowledge(interaction_event)
        
        if (gui_state != GUI_STATE_READY):
            return
        
        check = self._menu_structure.check
        if (check is not None):
            try:
                should_process = check(self, interaction_event)
            except GeneratorExit as err:
                self.cancel(err)
                raise
            
            except BaseException as err:
                self.cancel(err)
                return
            
            if not should_process:
                await client.interaction_component_acknowledge(interaction_event)
                return
        
        self._gui_state = GUI_STATE_EDITING
        
        invoke = self._menu_structure.invoke
        try:
            should_edit = await invoke(self, interaction_event)
        except GeneratorExit as err:
            self.cancel(err)
            raise
        
        except BaseException as err:
            self.cancel(err)
            return
        
        if should_edit:
            tracked_changes = self._tracked_changes
            keyword_parameters = tracked_changes.copy()
            tracked_changes.clear()
            
            allowed_mentions = self._allowed_mentions
            if (allowed_mentions is not None):
                keyword_parameters['allowed_mentions'] = allowed_mentions
            
            try:
                await client.interaction_component_message_edit(
                    interaction_event,
                    **keyword_parameters,
                    components = self._components,
                )
            except GeneratorExit as err:
                self.cancel(err)
                raise
            
            except BaseException as err:
                self.cancel(err)
                return
            
            
            get_timeout = self._menu_structure.get_timeout
            if (get_timeout is None):
                timeout = -1.0
            else:
                timeout = get_timeout(self)
            
            timeouter = self._timeouter
            if (timeout > 0.0):
                if timeouter is None:
                    self._timeouter = Timeouter(self, timeout)
                else:
                    timeouter.set_timeout(timeout)
            else:
                if (timeouter is not None):
                    self._timeouter = None
                    timeouter.cancel()
        
        else:
            try:
                await client.interaction_component_acknowledge(interaction_event)
            except GeneratorExit as err:
                self.cancel(err)
                raise
            
            except BaseException as err:
                self.cancel(err)
                return
        
        if self._gui_state == GUI_STATE_EDITING:
            self._gui_state = GUI_STATE_READY
    
    
    def cancel(self, exception = None):
        """
        Cancels the menu with the given exception.
        
        Parameters
        ----------
        exception : `None`, ``BaseException`` = `None`, Optional
            Exception to cancel the pagination with. Defaults to `None`
        
        Returns
        -------
        canceller_task : `None`, ``Task``
        """
        if self._gui_state in (GUI_STATE_READY, GUI_STATE_EDITING, GUI_STATE_CANCELLING):
            self._gui_state = GUI_STATE_CANCELLED
        
        canceller = self._canceller
        if canceller is None:
            return
        
        self._canceller = None
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(KOKORO, canceller(self, exception))
    
    
    async def _canceller_function(self, exception):
        """
        Cancels the gui state, saving the current game if needed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None`, ``BaseException``
        """
        client = self.client
        message = self.message
        
        client.slasher.remove_component_interaction_waiter(message, self)
        
        
        if self._gui_state == GUI_STATE_SWITCHING_CONTEXT:
            # the message is not our, we should not do anything with it.
            return
        
        self._gui_state = GUI_STATE_CANCELLED
        
        close = self._menu_structure.close
        
        try:
            if (close is None):
                handled = await self._handle_close_exception(exception)
            else:
                await close(self, exception)
                handled = True
        except GeneratorExit:
            raise
        
        except BaseException as err:
            await client.events.error(client, f'{self!r}._canceller_function', err)
        
        else:
            if not handled:
                await client.events.error(client, f'{self!r}.cancel', exception)
    
    
    async def _handle_close_exception(self, exception):
        """
        Handles close exception if any.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None`, `BaseException`
            The close exception to handle.
        
        Returns
        -------
        handled : `bool`
            Whether the exception was handled.
        """
        if exception is None:
            return True
        
        client = self.client
        message = self.message
        
        if isinstance(exception, CancelledError):
            try:
                await client.message_delete(message)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    # no internet
                    return True
                
                if isinstance(err, DiscordException):
                    if err.code in (
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_access, # client removed
                    ):
                        return True
                
                await client.events.error(client, f'{self!r}._handle_close_exception', err)
            
            return True
        
        if isinstance(exception, TimeoutError):
            if (message.components is not None):
                try:
                    await client.message_edit(message, components = None)
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    if isinstance(err, ConnectionError):
                        # no internet
                        return True
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ):
                            return True
                    
                    await client.events.error(client, f'{self!r}._handle_close_exception', err)
            
            return True
        
        if isinstance(exception, PermissionError):
            return True
        
        return False
    
    
    @property
    def content(self):
        """
        A get-set-del property to modify the menu's content.
        """
        message = self.message
        if message is None:
            content = None
        else:
            content = message.content
        
        return content
    
    
    @content.setter
    def content(self, content):
        if content is None:
            change_name = 'content'
            change_value = ''
        elif isinstance(content, str):
            change_name = 'content'
            change_value = content
        elif isinstance(content, Embed):
            change_name = 'embed'
            change_value = content
        else:
            change_name = 'content'
            change_value = str(content)
            if len(change_value) > 2000:
                change_value = change_value[:2000]
        
        self._tracked_changes[change_name] = change_value
    
    @content.deleter
    def content(self):
        self._tracked_changes['content'] = None
    
    
    @property
    def embed(self):
        """
        A get-set-del property to modify the menu's embed.
        """
        message = self.message
        if message is None:
            embed = None
        else:
            embeds = message.embeds
            if embeds is None:
                embed = None
            else:
                embed = embeds[0]
        
        return embed
    
    @embed.setter
    def embed(self, embed):
        if (embed is not None) and (not isinstance(embed, Embed)):
            raise TypeError(
                f'`embed` can be `None`, `{Embed.__name__}`, got '
                f'{embed.__class__.__name__}; {embed!r}.'
            )
        
        self._tracked_changes['embed'] =  embed
    
    @embed.deleter
    def embed(self):
        self._tracked_changes['embed'] = None
    
    
    @property
    def allowed_mentions(self):
        """
        A get-set-del property to modify the menu's message's allowed mentions.
        """
        allowed_mentions = self._allowed_mentions
        if allowed_mentions is None:
            allowed_mentions_output = AllowedMentionProxy()
        else:
            allowed_mentions_output = allowed_mentions.copy()
        
        return allowed_mentions_output
    
    @allowed_mentions.setter
    def allowed_mentions(self, allowed_mentions_input):
        if allowed_mentions_input is None:
            allowed_mentions = AllowedMentionProxy()
        elif isinstance(allowed_mentions_input, AllowedMentionProxy):
            allowed_mentions = allowed_mentions_input.copy()
        else:
            allowed_mentions = AllowedMentionProxy(allowed_mentions_input)
        
        self._allowed_mentions = allowed_mentions
    
    @allowed_mentions.deleter
    def allowed_mentions(self):
        self._allowed_mentions = None
    
    
    @property
    def components(self):
        """
        A get-set-del property to modify the menu's components.
        """
        return self._components
    
    
    @components.setter
    def components(self, raw_components):
        components = None
        
        if raw_components is None:
            pass
        
        elif isinstance(raw_components, Component):
            if raw_components.type is ComponentType.row:
                component = raw_components
            else:
                component = create_row(raw_components)
            
            if components is None:
                components = []
            
            components.append(component)
        
        elif isinstance(raw_components, (tuple, list)):
            
            for raw_sub_component in raw_components:
                if isinstance(raw_sub_component, Component):
                    if raw_sub_component.type is ComponentType.row:
                        component = raw_sub_component
                    else:
                        component = create_row(raw_sub_component)
                
                elif isinstance(raw_sub_component, (tuple, list)):
                    component_line = []
                    for raw_sub_sub_component in raw_sub_component:
                        if not isinstance(raw_sub_sub_component, Component):
                            raise TypeError(
                                f'Double nested component can only be `{Component.__name__}`, got '
                                f'{raw_sub_sub_component.__class__.__name__}; {raw_sub_sub_component!r}.'
                            )
                        
                        if raw_sub_sub_component.type is ComponentType.row:
                            raise TypeError(
                                f'Triple nesting components not allowed, got {raw_sub_sub_component!r}.'
                            )
                        
                        component_line.append(raw_sub_sub_component)
                    
                    component = create_row(*component_line)
                
                else:
                    raise TypeError(
                        f'`components` contains an element of unexpected type, got '
                        f'{raw_sub_component.__class__.__name__}; {raw_sub_component!r}; components = {raw_components!r}.'
                    )
                
                if components is None:
                    components = []
                
                components.append(component)
        
        else:
            raise TypeError(
                f'`components` can be `None`, `{Component.__name__}`, (`list`, `tuple`) of repeat, '
                f'no triple nesting, got {raw_components.__class__.__name__}; {raw_components!r}.'
            )
        
        if (components is not None):
            components = tuple(components)
        
        self._components = components
    
    
    @components.deleter
    def components(self):
        self._components = None
