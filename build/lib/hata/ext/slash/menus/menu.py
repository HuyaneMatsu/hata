__all__ = ('Menu',)

from collections import OrderedDict
from types import MemberDescriptorType

from ....backend.analyzer import CallableAnalyzer
from ....backend.utils import copy_docs
from ....backend.futures import Task, CancelledError

from ....discord.core import KOKORO
from ....discord.interaction.components import _debug_component_components, _debug_component_custom_id, \
    _debug_component_emoji, _debug_component_label, _debug_component_enabled, _debug_component_url, \
    _debug_component_description, _debug_component_default, _debug_component_options, _debug_component_placeholder, \
    _debug_component_min_values, _debug_component_max_values
from ....discord.interaction import ComponentBase, ComponentRow, ComponentButton, ComponentSelect, InteractionEvent, \
    ComponentSelectOption, ComponentType, InteractionType
from ....discord.message import Message
from ....discord.channel import ChannelTextBase
from ....discord.embed import EmbedBase
from ....discord.allowed_mentions import AllowedMentionProxy
from ....discord.client import Client
from ....discord.exceptions import DiscordException, ERROR_CODES

from ..waiters import get_client_from_message, get_client_from_interaction_event, Timeouter

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
    component : ``ComponentBase``
        The stored component by the hasher.
    """
    __slots__ = ('component', )
    def __init__(self, component):
        """
        Creates a new ``ComponentSourceIdentityHasher`` instance with the given parameters.
        
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


class ComponentAttributeDescriptor:
    """
    Descriptor for component attribute access.
    
    Attributes
    ----------
    _debugger : `callable`
        Debugger to check whether the given value is correct.
    _is_collection : `None` or ``ComponentBase``
        Sub-component type if applicable.
    _supported_types : `tuple` of `type`
        The supported types of the respective component.
    _name : `str`
        The attribute's name.
    """
    __slots__ = ('_debugger', '_is_collection', '_supported_types', '_name')
    def __new__(cls, name, supported_types, debugger, is_collection):
        """
        Creates a new ``ComponentAttributeDescriptor`` instance with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The attribute's name.
        supported_types : `tuple` of `type`
            The supported component types.
        debugger : `None`, `Function`
            Debugger function to check the passed values in debug mode.
        is_collection : `bool`
            Whether the component is collection of components.
        """
        self = object.__new__(cls)
        self._debugger = debugger
        self._supported_types = supported_types
        self._name = name
        self._is_collection = is_collection
        return self
    
    def __get__(self, instance, type_):
        """
        Returns the component's attribute's value.
        
        Parameters
        ----------
        instance : ``ComponentProxy``
            The parent component proxy.
        type_ : `type` = ``ComponentProxy``
            The component proxy type.
        
        Returns
        -------
        self / attribute_value : ``ComponentAttributeDescriptor`` / `Any`
            Self called from class, or the represented component's attribute's value.
        """
        if instance is None:
            return self
        
        is_collection = self._is_collection
        if is_collection:
            component = instance._get_component()
        else:
            component = instance._get_component_overwrite()
        
        if __debug__:
            if (not isinstance(component, self._supported_types)):
                raise AssertionError(f'{self._name} is not supported for {component.__class__.__name__}.')
        
        attribute_value = getattr(component, self._name)
        if is_collection and (attribute_value is not None):
            menu_instance = instance._instance
            
            attribute_value = tuple(components_descriptor.get_component_proxy(menu_instance) \
                for components_descriptor in attribute_value)
        
        return attribute_value
    
    
    def __set__(self, instance, value):
        """
        Sets the value to the component.
        
        Parameters
        ----------
        instance : ``ComponentProxy``
            The parent component proxy.
        value : `Any`
            The value to set as attribute.
        """
        if __debug__:
            self._debugger(value)
        
        component = instance._get_component_overwrite()
        
        if __debug__:
            if (not isinstance(component, self._supported_types)):
                raise AssertionError(f'{self._name} is not supported for {component.__class__.__name__}.')
        
        
        setattr(component, self._name, value)
    
    def __repr__(self):
        """Returns the component descriptor attribute's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' name=',
            repr(self._name),
            ', supported_types=',
            repr(self._supported_types)
        ]
        
        if self._is_collection:
            repr_parts.append(' (collection)')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class ComponentDescriptorState(ComponentBase):
    """
    Stateless component descriptor.
    
    Attributes
    ----------
    _component : ``ComponentBase``
        The wrapped component instance.
    _source_component : ``ComponentBase``
        The source component from which the descriptor is created from.
    _sub_components : `None` or `list` of ``ComponentDescriptor``
        Sub components applicable to the component.
    
    Class Attributes
    ----------------
    custom_id : `NoneType` = `None`
        Placeholder for sub-classes without `custom_id` attribute.
    """
    __slots__ = ('_component', '_source_component', '_sub_components',)
    
    def __new__(cls, source, sub_components):
        """
        Creates a new ``ComponentDescriptor`` instance from the given component.
        
        Parameters
        ----------
        source : ``ComponentBase`` instance
            The source component to create the descriptor from.
        sub_components : `None` or `list` of ``ComponentDescriptor``
            A list of sub components added
        """
        component = source.copy()
        
        self = object.__new__(cls)
        self._component = component
        self._source_component = source
        self._sub_components = sub_components
        
        return self
    
    def get_component_proxy(self, instance):
        """
        Gets component proxy of the descriptor.
        
        Parameters
        ----------
        instance : ``Menu``
            The parent menu instance.
        
        Returns
        -------
        component_proxy : ``ComponentProxy``
        """
        return ComponentProxy(self, instance)

    def __repr__(self):
        """Returns the component descriptor state's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ', component=', repr(self._component),
        ]
        
        sub_components = self._sub_components
        if (sub_components is not None):
            repr_parts.append(' sub_components=')
            repr_parts.append(repr(sub_components))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @property
    def type(self):
        return self._component.type
    
    
    def __getattr__(self, attribute_name):
        """Tries to find the attributes of the respective component."""
        component = self._component
        try:
            getter = type(component).__dict__[attribute_name]
        except KeyError:
            pass
        else:
            if isinstance(getter, MemberDescriptorType):
                return MemberDescriptorType.__get__(getter, component)
        
        raise AttributeError(attribute_name)
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        return self._component.to_data()
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        if self._source_component is other._source_component:
            return True
        
        return False
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        return hash(self._component)
    
    
    @copy_docs(ComponentBase._iter_components)
    def _iter_components(self):
        yield self
        
        sub_components = self._sub_components
        if (sub_components is not None):
            for sub_component in sub_components:
                yield from sub_component._iter_components()
    
    
    @copy_docs(ComponentBase._iter_direct_sub_components)
    def _iter_direct_sub_components(self):
        sub_components = self._sub_components
        if (sub_components is not None):
            yield from sub_components


class ComponentDescriptor(ComponentDescriptorState):
    """
    Descriptor to proxy class attribute component access for each instance.
    
    Attributes
    ----------
    _component : ``ComponentBase``
        The wrapped component instance.
    _source_component : ``ComponentBase``
        The source component from which the descriptor is created from.
    _sub_components : `None` or `list` of ``ComponentDescriptor``
        Sub components applicable to the component.
    _identifier : `int`
        The descriptor's identifier.
    
    Class Attributes
    ----------------
    _identifier_counter : `int`
        Identifier counter for caching.
    """
    _identifier_counter = 0
    
    
    __slots__ = ('_identifier',)
    def __new__(cls, source, sub_components):
        """
        Creates a new ``ComponentDescriptor`` instance from the given component.
        
        Parameters
        ----------
        source : ``ComponentBase`` instance
            The source component to create the descriptor from.
        sub_components : `list` of ``ComponentDescriptor``
            A list of sub components added
        """
        identifier = cls._identifier_counter+1
        cls._identifier_counter = identifier
        
        self = ComponentDescriptorState.__new__(cls, source, sub_components)
        self._identifier = identifier
        return self
    
    def __get__(self, instance, type_):
        """
        Gets the descriptor itself if called from class or a component proxy.
        
        Parameters
        ----------
        instance : ``Menu``
            The menu instance.
        type_ : ``MenuType``
            The menu's type.
        
        Returns
        -------
        self / component_proxy : ``ComponentDescriptor`` / ``ComponentProxy``
            Self if called from class, or the a component proxy for the represented component.
        """
        if instance is None:
            return self
        
        return self.get_component_proxy(instance)
    
    @copy_docs(ComponentDescriptorState.get_component_proxy)
    def get_component_proxy(self, instance):
        component_proxy_cache = instance._component_proxy_cache
        try:
            component_proxy = component_proxy_cache[self._identifier]
        except KeyError:
            component_proxy = component_proxy_cache[self._identifier] = ComponentProxy(self, instance)
        
        return component_proxy
    
    def __repr__(self):
        """Returns the component descriptor's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' identifier=', repr(self._identifier),
            ', component=', repr(self._component),
        ]
        
        sub_components = self._sub_components
        if (sub_components is not None):
            repr_parts.append(' sub_components=')
            repr_parts.append(repr(sub_components))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class ComponentProxy(ComponentBase):
    """
    Proxy class for components.
    
    Attributes
    ----------
    _component_overwrite : `None` or ``Component``
        Default component's overwrite.
    _descriptor : ``ComponentDescriptor``
        The creator descriptor, which describes the component's default values.
    _instance : ``Any``
        An instance's of the descriptor's owner type.
    """
    __slots__ = ('_component_overwrite', '_descriptor', '_instance')
    
    def __new__(cls, descriptor, instance):
        """
        Creates a new component proxy.
        
        Parameters
        ----------
        descriptor : ``ComponentDescriptor``
            The creator descriptor, which describes the component's default values.
        instance : ``Any``
            An instance's of the descriptor's owner type.
        """
        self = object.__new__(cls)
        self._descriptor = descriptor
        self._instance = instance
        self._component_overwrite = None
        return self
    
    
    def _iter_component_proxies(self):
        """
        Iterates over the components and sub-component proxies.
        
        This method is an iterable generator.
        
        Yields
        ------
        component_proxy : ``ComponentProxy``
        """
        yield self
        sub_components = self._descriptor._sub_components
        if (sub_components is not None):
            instance = self._instance
            for sub_component in sub_components:
                yield sub_component.get_component_proxy(instance)
    
    
    def _get_component(self):
        """
        Gets the actually used component by the proxy.
        
        Returns
        -------
        component : ``ComponentBase``
        """
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
        
        return component
    
    
    def _get_component_overwrite(self):
        """
        Gets the proxy's component overwrite.
        
        Returns
        -------
        component : ``ComponentBase``
        """
        component = self._component_overwrite
        if (component is None):
            self._component_overwrite = component = self._descriptor._component.copy()
        
        return component
    
    
    @property
    def type(self):
        """Returns the component's type."""
        return self._descriptor._component.type
    
    
    def __repr__(self):
        """Returns the component proxy's representation."""
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
        
        return f'<{self.__class__.__name__} component={component!r}>'
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
        
        return hash(component)
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        # We will brute force some things. It ain't pretty.
        component_type = type(self._descriptor._component)
        
        if issubclass(component_type, ComponentRow):
            data = {
                'type': ComponentType.row.value,
            }
            
            attribute_value = self.components
            if attribute_value is None:
                field_value = []
            else:
                field_value = [sub_component.to_data() for sub_component in attribute_value]
            data['components'] = field_value
        
        elif issubclass(component_type, ComponentButton):
            data = self._get_component().to_data()
        
        elif issubclass(component_type,  ComponentSelectOption):
            data = self._get_component().to_data()
        
        elif issubclass(component_type,  ComponentSelect):
            data = {
                'type': ComponentType.select.value,
            }
            
            attribute_value = self.options
            if attribute_value is None:
                field_value = []
            else:
                field_value = [sub_component.to_data() for sub_component in attribute_value]
            data['options'] = field_value
            
            component = self._get_component()
            
            data['custom_id'] = component.custom_id
            
            placeholder = component.placeholder
            if (placeholder is not None):
                data['placeholder'] = placeholder
            
            min_values = component.min_values
            if min_values != 1:
                data['min_values'] = min_values
            
            max_values = component.max_values
            if max_values != 1:
                data['max_values'] = max_values
            
            if (not component.enabled):
                data['disabled'] = True
                
        else:
            data = {}
        
        return data
    
    
    components = ComponentAttributeDescriptor(
        'components',
        (ComponentRow,),
        _debug_component_components,
        True,
    )
    
    custom_id = ComponentAttributeDescriptor(
        'custom_id',
        (ComponentButton, ComponentSelect,),
        _debug_component_custom_id,
        False,
    )
    
    emoji = ComponentAttributeDescriptor(
        'emoji',
        (ComponentButton, ComponentSelectOption),
        _debug_component_emoji,
        False,
    )
    
    label = ComponentAttributeDescriptor(
        'label',
        (ComponentButton, ComponentSelectOption),
        _debug_component_label,
        False,
    )

    enabled = ComponentAttributeDescriptor(
        'enabled',
        (ComponentButton, ComponentSelect),
        _debug_component_enabled,
        False,
    )

    url = ComponentAttributeDescriptor(
        'url',
        (ComponentButton,),
        _debug_component_url,
        False,
    )
    
    description = ComponentAttributeDescriptor(
        'description',
        (ComponentSelectOption,),
        _debug_component_description,
        False,
    )
    
    default = ComponentAttributeDescriptor(
        'default',
        (ComponentSelectOption,),
        _debug_component_default,
        False,
    )
    
    options = ComponentAttributeDescriptor(
        'options',
        (ComponentSelect,),
        _debug_component_options,
        True,
    )
    
    placeholder = ComponentAttributeDescriptor(
        'placeholder',
        (ComponentSelect,),
        _debug_component_placeholder,
        False,
    )
    
    min_values = ComponentAttributeDescriptor(
        'min_values',
        (ComponentSelect,),
        _debug_component_min_values,
        False,
    )
    
    max_values = ComponentAttributeDescriptor(
        'max_values',
        (ComponentSelect,),
        _debug_component_max_values,
        False,
    )


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
        raise TypeError('`check` should have NOT be be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 2:
        raise TypeError(f'`check` should accept `2` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{check!r}`.')
    
    if min_ != 2:
        if max_ < 2:
            if not analyzer.accepts_args():
                raise TypeError(f'`check` should accept `2` parameters, meanwhile the given callable expects '
                    f'up to `{max_!r}`, got `{check!r}`.')


def validate_invoke(invoke):
    """
    Validates the given invoker.
    
    Parameters
    ----------
    invoke : `None` or `async-callable`
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
        raise TypeError('`invoke` should have be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    
    if min_ > 2:
        raise TypeError(f'`invoke` should accept `2` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{invoke!r}`.')
    
    if min_ != 2:
        if max_ < 2:
            if not analyzer.accepts_args():
                raise TypeError(f'`invoke` should accept `2` parameters, meanwhile the given callable expects '
                    f'up to `{max_!r}`, got `{invoke!r}`.')


def validate_initial_invoke(initial_invoke):
    """
    Validates the given default content getter.
    
    Parameters
    ----------
    initial_invoke : `None` or `async-callable`
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
        raise TypeError('`initial_invoke` should have be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 1:
        raise TypeError(f'`initial_invoke` should accept `1` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{initial_invoke!r}`.')
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_args():
                raise TypeError(f'`initial_invoke` should accept `1` parameters, meanwhile the given callable '
                    f'expects up to `{max_!r}`, got `{initial_invoke!r}`.')


def validate_get_timeout(get_timeout):
    """
    Validates the given timeout getter.
    
    Parameters
    ----------
    get_timeout : `None` or `callable`
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
        raise TypeError('`get_timeout` should have be not be async function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 1:
        raise TypeError(f'`get_timeout` should accept `1` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{get_timeout!r}`.')
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_args():
                raise TypeError(f'`get_timeout` should accept `1` parameters, meanwhile the given callable '
                    f'expects up to `{max_!r}`, got `{get_timeout!r}`.')


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
        raise TypeError('`close` should have be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ > 2:
        raise TypeError(f'`close` should accept `2` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{close!r}`.')
    
    if min_ != 2:
        if max_ < 2:
            if not analyzer.accepts_args():
                raise TypeError(f'`close` should accept `2` parameters, meanwhile the given callable expects '
                    f'up to `{max_!r}`, got `{close!r}`.')


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
        raise TypeError('`close` should have be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
    if min_ < 3:
        raise TypeError(f'`close` should accept `3` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{init!r}`.')


class MenuStructure:
    """
    A special object to store special methods of a menu.
    
    Attributes
    ----------
    check : `None` or `function`
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
    
    get_timeout : `None` or `Function`
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
    
    close : `None` or `CoroutineFunction`
        Function to call when the menu is closed.
        
        Should accept the following parameters:
        
        +-----------+---------------------------+
        | Name      | Type                      |
        +===========+===========================+
        | self      | ``Menu``                  |
        +-----------+---------------------------+
        | exception | `None` or `BaseException` |
        +-----------+---------------------------+
    
    init : `None` or `Function`
        Initializer function.
    
        Should accept the following parameters:
        
        +-------------------+---------------------------+
        | Name              | Type                      |
        +===================+===========================+
        | self              | ``Menu``                  |
        +-------------------+---------------------------+
        | interaction_event | ``InteractionEvent``      |
        +-------------------+---------------------------+
        | *args             | Positional parameters     |
        +-------------------+---------------------------+
        | **kwargs          | Keyword parameters        |
        +-------------------+---------------------------+
    
    initial_invoke : `None` or `CoroutineFunction`
        Function to generate the default page of the menu.
        
        Should accept the following parameters:
        
        +-----------+-----------+
        | Name      | Type      |
        +===========+===========+
        | self      | ``Menu``  |
        +-----------+-----------+
        
    is_final : `bool`
        Whether the Menu has all the required fields fulfilled.
    
    invoke : `None` or `CoroutineFunction`
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
        class_attributes : `dict` of (`str`, `Any`) items
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
    
    Parameters
    ----------
    class_parents : `tuple` of `type`
        Parent classes.
    class_attributes : `dict` of (`str`, `Any`) items
        Class attributes of the source type.
    
    Yields
    ------
    attribute_name : `str`
        An attribute's name.
    attribute_value : `Any`
        An attribute's value.
    """
    for class_parent in reversed(class_parents):
        yield from class_parent.__dict__.items()
    
    yield from class_attributes.items()


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
    Meta type for ``Menu`` instances.
    """
    def __new__(cls, class_name, class_parents, class_attributes):
        """
        Creates a Discord entity type. Subclass ``DiscordEntity`` instead of using this class directly as a metaclass.
        
        Parameters
        ----------
        class_name : `str`
            The created class's name.
        class_parents : `tuple` of `type` instances
            The superclasses of the creates type.
        class_attributes : `dict` of (`str`, `Any`) items
            The class attributes of the created type.
        
        Returns
        -------
        type : ``MenuType`` instance
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
                        raise TypeError(f'Overwriting `{attribute_name}` is disallowed.')
        
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
        
        
        all_component_descriptor = {}
        
        component_descriptors = OrderedDict()
        tracked_components = OrderedDict()
        
        for attribute_name, attribute_value in _iter_attributes(class_parents, class_attributes):
            if isinstance(attribute_value, ComponentDescriptor):
                container = component_descriptors
                secondary = tracked_components
                component_hasher = ComponentSourceIdentityHasher(attribute_value._source_component)
                all_component_descriptor[component_hasher] = attribute_value
            elif isinstance(attribute_value, ComponentBase):
                container = tracked_components
                secondary = component_descriptors
            else:
                continue
            
            container[attribute_name] = attribute_value
            container.move_to_end(attribute_name)
            
            try:
                del secondary[attribute_name]
            except KeyError:
                pass
            continue
        
        component_groups = []
        component_standalone = []
        
        for attribute_name, attribute_value in tracked_components.items():
            if attribute_value.type in (ComponentType.row, ComponentType.select):
                container = component_groups
            else:
                container = component_standalone
            
            container.append((attribute_name, attribute_value))
            continue
        
        
        for component_name, component_value in component_standalone:
            component_hasher = ComponentSourceIdentityHasher(component_value)
            
            try:
                component_descriptor = all_component_descriptor[component_hasher]
            except KeyError:
                component_descriptor = ComponentDescriptor(component_value, None)
                all_component_descriptor[component_hasher] = component_descriptor
            
            component_descriptors[component_name] = component_descriptor
        
        for component_name, component_value in component_groups:
            component_hasher = ComponentSourceIdentityHasher(component_value)
            
            try:
                component_descriptor = all_component_descriptor[component_hasher]
            except KeyError:
                sub_component_relations = None
                sub_component_descriptors = None
                for sub_component in component_value._iter_direct_sub_components():
                    sub_component_hasher = ComponentSourceIdentityHasher(sub_component)
                    try:
                        sub_component_descriptor = all_component_descriptor[sub_component_hasher]
                    except KeyError:
                        sub_component_descriptor = ComponentDescriptor(sub_component, None)
                        all_component_descriptor[sub_component_hasher] = sub_component_descriptor
                    
                    if (sub_component_descriptors is None):
                        sub_component_descriptors = []
                    sub_component_descriptors.append(sub_component_descriptor)
                    
                    if (sub_component_relations is None):
                        sub_component_relations = {}
                    sub_component_relations[sub_component] = sub_component_descriptor
                
                if (sub_component_relations is not None):
                    component_value._replace_direct_sub_components(sub_component_relations)
                
                component_descriptor = ComponentDescriptor(component_value, sub_component_descriptors)
                all_component_descriptor[component_hasher] = component_descriptor
            
            component_descriptors[component_name] = component_descriptor
        
        for attribute_name, attribute_value in component_descriptors.items():
            class_attributes[attribute_name] = attribute_value
        
        if '__slots__' not in class_attributes:
            class_attributes['__slots__'] = ('__dict__', )
        
        return type.__new__(cls, class_name, class_parents, class_attributes)


class Menu(metaclass=MenuType):
    """
    Base class for custom component based menus.
    
    Attributes
    ----------
    _allowed_mentions : ``Ellipsis``, `None` or `list` of `Any`
        The used allowed mentions when editing the respective message.
    _canceller : None` or `CoroutineFunction`
        Canceller set as `._canceller_function``, meanwhile the gui is not cancelled.
    _components : `None` or `tuple` of ``ComponentBase``
        Rendered components of the menu.
    _component_proxy_cache : `dict` of (`int`, ``ComponentProxy``) items
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
    _timeouter : `None` or ``Timeouter``
        Executes the timeout feature on the menu.
    _tracked_changes : `dict` of (`str`, `Any`) items
        The tracked changes by parameter name.
    channel : ``ChannelTextBase`` instance
        The channel where the menu is executed.
    client : ``Client``
        The executor client instance.
    message : `None` or ``Message``
        The message which executes the menu.
    
    Class Attributes
    ----------------
    _menu_structure : ``MenuStructure``
        Factorized methods added by the user used by the menu itself.
    """
    __slots__ = ('_allowed_mentions', '_canceller', '_component_proxy_cache', '_gui_state', '_timeouter',
        '_tracked_changes', 'channel', 'client', 'message', '_components',)
    
    async def __new__(cls, client, target, *args, **kwargs):
        """
        Creates a new menu instance.
        
        Parameters
        ----------
        client : ``Client``
            The client instance whi will execute the action.
        target : ``InteractionEvent``, ``Message``, ``ChannelTextBase``, `int`
            The event to respond to, or the channel to send the message at, or the message to edit.
        *args : Positional parameters
            Additional positional parameters.
        **kwargs : Keyword parameters
            Additional keyword parameters.
        
        Raises
        ------
        TypeError
            If `interaction_event` was not given neither as ``InteractionEvent``, ``Message``, ``ChannelTextBase``,
             nor as instance.
        RuntimeError
            If `interaction_event` is given as ``InteractionEvent``, but it's client cannot be detected.
        """
        menu_structure = cls._menu_structure
        if not menu_structure.is_final:
            raise RuntimeError(f'{cls.__class__.__name__} has not every required fields fulfilled. Required fields: '
                f'initial_invoke, invoke')
        
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
            
            if isinstance(target, ChannelTextBase):
                target_channel_id = target.id
                target_message = None
                is_interaction = False
                break
            
            if isinstance(target, int):
                target_channel_id = target
                target_message = None
                is_interaction = False
                break
                
                
            raise TypeError(f'`target` can be given as `{InteractionEvent.__name__}`, '
                f'`{Message.__name__}`, `{ChannelTextBase.__name__}` or as `int` instance, got '
                f'{target.__class__.__name__}.')
        
        
        self = object.__new__(cls)
        self._canceller = None
        self.message = target_message
        self.client = client
        self._gui_state = GUI_STATE_NONE
        self._timeouter = None
        self._tracked_changes = {}
        self._allowed_mentions = None
        self._component_proxy_cache = {}
        self._components = None
        
        init = menu_structure.init
        if (init is not None):
            init(self, client, target, *args, **kwargs)
        
        await menu_structure.initial_invoke(self)
        
        tracked_changes = self._tracked_changes
        if not tracked_changes:
            raise RuntimeError(f'{cls.__class__.__name__}\'s `initial_invoke` method: '
                f'{menu_structure.initial_invoke!r} did not change any parameters.')
        
        kwargs = tracked_changes.copy()
        tracked_changes.clear()
        
        allowed_mentions = self._allowed_mentions
        if (allowed_mentions is not None):
            kwargs['allowed_mentions'] = allowed_mentions
        
        kwargs['components'] = self._components
        
        if is_interaction:
            interaction_event_type = interaction_event.type
            if interaction_event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
                if target_message is None:
                    if interaction_event.is_unanswered():
                        await client.interaction_application_command_acknowledge(interaction_event)
                    
                    target_message = await client.interaction_followup_message_create(interaction_event, **kwargs)
                else:
                    await client.interaction_response_message_edit(interaction_event, **kwargs)
            
            elif interaction_event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
                await client.interaction_component_message_edit(interaction_event, **kwargs)
            
            else:
                # nani desu ka?
                return
        
        else:
            if target_message is None:
                target_message = await client.message_create(target_channel_id, **kwargs)
            else:
                await client.message_edit(target_message, **kwargs)
        
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
        except BaseException as err:
            self.cancel(err)
            return
        
        if should_edit:
            tracked_changes = self._tracked_changes
            kwargs = tracked_changes.copy()
            tracked_changes.clear()
            
            allowed_mentions = self._allowed_mentions
            if (allowed_mentions is not None):
                kwargs['allowed_mentions'] = allowed_mentions
            
            try:
                await client.interaction_component_message_edit(interaction_event, **kwargs, components=self._components)
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
            except BaseException as err:
                self.cancel(err)
                return
        
        if self._gui_state == GUI_STATE_EDITING:
            self._gui_state = GUI_STATE_READY
    
    
    def cancel(self, exception=None):
        """
        Cancels the menu with the given exception.
        
        Parameters
        ----------
        exception : `None` or ``BaseException`` instance, Optional
            Exception to cancel the pagination with. Defaults to `None`
        
        Returns
        -------
        canceller_task : `None` or ``Task``
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
        
        return Task(canceller(self, exception), KOKORO)
    
    
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
        exception : `None` or `BaseException`
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
                    await client.message_edit(message, components=None)
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
        elif isinstance(content, EmbedBase):
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
        if (embed is not None) and (not isinstance(embed, EmbedBase)):
            raise TypeError(f'`embed` can be given as `None` or as `{EmbedBase.__name__}` instance, got '
                f'{embed.__class__.__name__}.')
        
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
        return tuple(self._components)
    
    
    @components.setter
    def components(self, raw_components):
        components = []
        all_component_descriptor = None
        
        if raw_components is None:
            pass
        
        elif isinstance(raw_components, ComponentProxy):
            if raw_components.type is ComponentType.row:
                components.append(raw_components)
            else:
                
                component_descriptor = ComponentDescriptorState(
                    ComponentRow(raw_components._source_component),
                    [raw_components],
                )
                component_proxy = component_descriptor.get_component_proxy(self)
                
                components.append(component_proxy)
        
        elif isinstance(raw_components, ComponentBase):
            raw_component = raw_components
            sub_component_descriptors = None
            sub_component_relations = None
            for sub_component in raw_component._iter_direct_sub_components():
                sub_component_hasher = ComponentSourceIdentityHasher(sub_component)
                
                if all_component_descriptor is None:
                    all_component_descriptor = {}
                
                try:
                    sub_component_descriptor = all_component_descriptor[sub_component_hasher]
                except KeyError:
                    sub_component_descriptor = ComponentDescriptor(sub_component, None)
                    all_component_descriptor[sub_component_hasher] = sub_component_descriptor
                
                if sub_component_descriptors is None:
                    sub_component_descriptors = []
                sub_component_descriptors.append(sub_component_descriptor)
                
                if sub_component_relations is None:
                    sub_component_relations = {}
                sub_component_relations[sub_component] = sub_component_descriptor
            
            if (sub_component_relations is not None):
                raw_component._replace_direct_sub_components(sub_component_relations)
            
            component_descriptor = ComponentDescriptorState(
                ComponentRow(raw_component),
                sub_component_descriptors,
            )
            
            component_proxy = component_descriptor.get_component_proxy(self)
            
            components.append(component_proxy)
        
        elif isinstance(raw_components, (tuple, list)):
            
            for raw_sub_component in raw_components:
                if isinstance(raw_sub_component, ComponentProxy):
                    if raw_sub_component.type is ComponentType.row:
                        components.append(raw_sub_component)
                    else:
                        
                        component_descriptor = ComponentDescriptorState(
                            ComponentRow(raw_sub_component._source_component),
                            [raw_sub_component],
                        )
                        component_proxy = component_descriptor.get_component_proxy(self)
                        
                        components.append(component_proxy)
                    
                elif isinstance(raw_sub_component, ComponentBase):
                    component_hasher = ComponentSourceIdentityHasher(raw_sub_component)
                    
                    if all_component_descriptor is None:
                        all_component_descriptor = {}
                    
                    try:
                        component_descriptor = all_component_descriptor[component_hasher]
                    except KeyError:
                        sub_component_relations = None
                        sub_component_descriptors = None
                        for sub_component in raw_sub_component._iter_direct_sub_components():
                            sub_component_hasher = ComponentSourceIdentityHasher(sub_component)
                            
                            if all_component_descriptor is None:
                                all_component_descriptor = {}
                            
                            try:
                                sub_component_descriptor = all_component_descriptor[sub_component_hasher]
                            except KeyError:
                                sub_component_descriptor = ComponentDescriptor(sub_component, None)
                                all_component_descriptor[sub_component_hasher] = sub_component_descriptor
                            
                            if sub_component_descriptors is None:
                                sub_component_descriptors = []
                                sub_component_descriptors.append(sub_component_descriptor)
                            if sub_component_relations is None:
                                sub_component_relations = {}
                            sub_component_relations[sub_component] = sub_component_descriptor
                        
                        if (sub_component_relations is not None):
                            raw_sub_component._replace_direct_sub_components(sub_component_relations)
                        
                        
                        component_descriptor = ComponentDescriptorState(
                            raw_sub_component,
                            sub_component_descriptors,
                        )
                        
                        all_component_descriptor[component_hasher] = component_descriptor
                    

                    component_proxy = component_descriptor.get_component_proxy(self)
                    components.append(component_proxy)
                
                elif isinstance(raw_sub_component, (tuple, list)):
                    sub_component_descriptors = []
                    for raw_nested_sub_component in raw_sub_component:
                        if isinstance(raw_nested_sub_component, ComponentProxy):
                            if raw_nested_sub_component.type is ComponentType.row:
                                raise TypeError(f'Cannot double-nest row components.')
                            
                            sub_component_descriptors.append(raw_nested_sub_component)
                        
                        elif isinstance(raw_nested_sub_component, ComponentBase):
                            if raw_nested_sub_component.type is ComponentType.row:
                                raise TypeError(f'Cannot double-nest row components.')
                            
                            sub_component_hasher = ComponentSourceIdentityHasher(raw_nested_sub_component)
                            
                            if all_component_descriptor is None:
                                all_component_descriptor = {}
                            
                            try:
                                sub_component_descriptor = all_component_descriptor[sub_component_hasher]
                            except KeyError:
                                sub_component_descriptor = ComponentDescriptor(raw_nested_sub_component, None)
                                all_component_descriptor[sub_component_hasher] = sub_component_descriptor
                            
                            sub_component_descriptors.append(sub_component_descriptor)
                        
                        else:
                            raise TypeError(f'Nested-sub components can be either `{ComponentProxy.__name__}` or  '
                                f'`{ComponentBase.__name__}`, got {raw_nested_sub_component.__class__.__name__}.')
                    
                    component_descriptor = ComponentDescriptorState(
                        ComponentRow(*raw_components),
                        sub_component_descriptors,
                    )
                    
                    component_proxy = component_descriptor.get_component_proxy(self)
                    
                    components.append(component_proxy)
        
        else:
            raise TypeError(f'`raw_components` can be `None`, `{ComponentProxy.__name__}`, `{ComponentBase.__name__}`, '
                f'(`list`, `tuple`) of repeat, no triple nesting, got {raw_components.__class__.__name__}.')
        
        if not components:
            components = None
        
        self._components = components
    
    @components.deleter
    def components(self):
        self._components = None
