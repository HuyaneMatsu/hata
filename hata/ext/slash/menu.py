__all__ = ()

# Work in progress

from collections import OrderedDict

from ...backend.analyzer import CallableAnalyzer

from ...discord.interaction.components import _debug_component_components, _debug_component_custom_id, \
    _debug_component_emoji, _debug_component_label, _debug_component_enabled, _debug_component_url, \
    _debug_component_description, _debug_component_default, _debug_component_options, _debug_component_placeholder, \
    _debug_component_min_values, _debug_component_max_values
from ...discord.interaction import ComponentBase, ComponentRow, ComponentButton, ComponentSelect, InteractionEvent, \
    ComponentSelectOption
from ...discord.message import Message
from ...discord.channel import ChannelTextBase
from ...discord.embed import EmbedBase
from ...discord.allowed_mentions import AllowedMentionProxy
from ...discord.client import Client

from .waiters import get_client_from_message


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
        """
        self = object.__new__(cls)
        self._debugger = debugger
        self._supported_types = supported_types
        self._name = name
        self._is_collection = is_collection
        return self
    
    def __get__(self, instance, type_):
        """Returns the component's attribute's value."""
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
        
        attribute_value = gettattr(component, self._name)
        if is_collection and (attribute_value is not None):
            instance_type = type(instance)
            
            attribute_value = tuple(components_descriptor.__get__(instance, instance_type) \
                for components_descriptor in components_descriptors)
        
        return attribute_value
    
    
    def __set__(self, instance, value):
        """Sets the value to the component."""
        if __debug__:
            self._debugger(value)
        
        component = instance._get_component_overwrite()
        
        if __debug__:
            if (not isinstance(component, self._supported_types)):
                raise AssertionError(f'{self._name} is not supported for {component.__class__.__name__}.')
        
        setattr(component, self._name, value)


class ComponentDescriptor:
    """
    
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
    
    __slots__ = ('_component', '_identifier', '_source_component', '_sub_components')
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
        component = source.copy()
        
        identifier = cls._identifier_counter+1
        cls._identifier_counter = identifier
        
        self = object.__new__(cls)
        self._component = component
        self._source_component = source
        self._identifier = identifier
        self._sub_components = sub_components
        return self
    
    def __get__(self, instance, type_):
        """Gets the descriptor itself if called from class or a component proxy."""
        if instance is None:
            return self
        
        component_proxy_cache = instance._component_proxy_cache
        try:
            component_proxy = component_proxy_cache[self._identifier]
        except KeyError:
            component_proxy = component_proxy_cache[self._identifier] = ComponentProxy(self, instance)
        
        return component_proxy


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
        (ComponentButton,),
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
    
    analyzer = CallableAnalyzer(check, as_method=True)
    if analyzer.is_async():
        raise TypeError('`check` should have NOT be be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_argument_range()
    if min_ > 1:
        raise TypeError(f'`check` should accept `1` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{check!r}`.')
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_args():
                raise TypeError(f'`check` should accept `1` parameters, meanwhile the given callable expects '
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
        If `invoke` is not `None` nor `async-callable` accepting 1 parameter.
    """
    if invoke is None:
        return
    
    analyzer = CallableAnalyzer(invoke, as_method=True)
    if not analyzer.is_async():
        raise TypeError('`invoke` should have be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_argument_range()
    if min_ > 1:
        raise TypeError(f'`invoke` should accept `1` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{invoke!r}`.')
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_args():
                raise TypeError(f'`invoke` should accept `1` parameters, meanwhile the given callable expects '
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
        If `initial_invoke` is not `None` nor `async-callable` accepting `0` parameters.
    """
    if initial_invoke is None:
        return
    
    analyzer = CallableAnalyzer(initial_invoke, as_method=True)
    if not analyzer.is_async():
        raise TypeError('`initial_invoke` should have be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_argument_range()
    if min_ > 0:
        raise TypeError(f'`initial_invoke` should accept `0` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{initial_invoke!r}`.')
    
    if min_ != 0:
        if max_ < 0:
            if not analyzer.accepts_args():
                raise TypeError(f'`initial_invoke` should accept `0` parameters, meanwhile the given callable '
                    f'expects up to `{max_!r}`, got `{initial_invoke!r}`.')


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
    
    analyzer = CallableAnalyzer(close, as_method=True)
    if not analyzer.is_async():
        raise TypeError('`close` should have be `async` function.')
    
    min_, max_ = analyzer.get_non_reserved_positional_argument_range()
    if min_ > 1:
        raise TypeError(f'`close` should accept `1` parameters, meanwhile the given callable expects at '
            f'least `{min_!r}`, got `{close!r}`.')
    
    if min_ != 1:
        if max_ < 1:
            if not analyzer.accepts_args():
                raise TypeError(f'`close` should accept `1` parameters, meanwhile the given callable expects '
                    f'up to `{max_!r}`, got `{close!r}`.')


class MenuStructure:
    """
    A special object to store special methods of a menu.
    
    Attributes
    ----------
    check : `None` or `function`
        The function to call when checking whether an event should be called.
        
        Should accept the following parameters:
        
        +-----------+---------------------------------------------------+
        | Name      | Type                                              |
        +===========+===================================================+
        | event     | ``ReactionAddEvent`` or ``ReactionDeleteEvent``   |
        +-----------+---------------------------------------------------+
        
        > ``ReactionDeleteEvent`` is only given, when the client has no `manage_messages` permission.
        
        Should return the following values:
        +-------------------+-----------+
        | Name              | Type      |
        +===================+===========+
        | should_process    | `bool`    |
        +-------------------+-----------+
    
    close : `None` or `async-function`
        Function to call when the pagination is closed.
        
        Should accept the following parameters:
        
        +-----------+---------------------------+
        | Name      | Type                      |
        +===========+===========================+
        | exception | `None` or `BaseException` |
        +-----------+---------------------------+
    
    initial_invoke : `None` or `async-function`
        Function to generate the default page of the menu.
        
        Should accept no parameters and return the following:
        
        +-----------+-----------------------------------+
        | Name      | Type                              |
        +===========+===================================+
        | response  | `None`, `str`, ``EmbedBase``      |
        +-----------+-----------------------------------+
    
    invoke : `None` or `async-function`
        The function call for result when invoking the menu.
        
        Should accept the following parameters:
        
        +-----------+---------------------------------------------------+
        | Name      | Type                                              |
        +===========+===================================================+
        | event     | ``ReactionAddEvent`` or ``ReactionDeleteEvent``   |
        +-----------+---------------------------------------------------+
        
        > ``ReactionDeleteEvent`` is only given, when the client has no `manage_messages` permission.
        
        Should return the following values:
        
        +-----------+-----------------------------------+
        | Name      | Type                              |
        +===========+===================================+
        | response  | `None`, `str`, ``EmbedBase``      |
        +-----------+-----------------------------------+
    
    timeout : `float`
        The time after the menu should be closed.
        
        > Define it as non-positive to never timeout. Not recommended.
    """
    __slots__ = ('check', 'close', 'initial_invoke', 'invoke', 'timeout')
    
    def __new__(cls, class_attributes):
        """
        Parameters
        ----------
        class_attributes : `dict` of (`str`, `Any`) items
            Class attributes of a type.
        
        Raises
        ------
        TypeError
            - If `check` is not `None` neither a non-async function accepting 1 parameter.
            - If `invoke` is not `None` nor an `async-callable` or accepting 1 parameter.
            - If `initial_invoke` is not `None`, nor an `async-callable` accepting no parameters.
            - If `timeout` is not convertable to float.
            - If `closed` is neither `None` nor `async-callable`.
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
        
        timeout = class_attributes.get('timeout', None)
        if timeout is None:
            timeout = -1.0
        else:
            try:
                timeout = float(timeout)
            except (TypeError, ValueError) as err:
                raise TypeError(f'`timeout` cannot be converted to `float`, got {timeout.__class__.__mame__}; '
                    f'{timeout!r}') from err
        
        close = class_attributes.get('close', None)
        validate_close(close)
        
        self = object.__new__(cls)
        self.check = check
        self.close = close
        self.initial_invoke = initial_invoke
        self.invoke = invoke
        self.timeout = timeout

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
        
        timeout = self.timeout
        if timeout > 0.0:
            if field_added:
                repr_parts.append(', ')
            
            repr_parts.append(' timeout=')
            repr_parts.append(repr(timeout))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def merge(self, other):
        """Merges the two menu structure"""
        check = self.check
        if check is None:
            check = other.check
        
        close = self.close
        if close is None:
            close = other.close
        
        initial_invoke = self.initial_invoke
        if initial_invoke is None:
            initial_invoke = other.initial_invoke
        
        invoke = self.invoke
        if invoke is None:
            invoke = other.invoke
        
        timeout = self.timeout
        if timeout <= 0.0:
            timeout = other.timeout
        
        new = object.__new__(type(self))
        new.check = check
        new.close = close
        new.initial_invoke = initial_invoke
        new.invoke = invoke
        new.timeout = timeout
        
        return self
    
    
    def validate(self):
        """
        Validates whether all required function is created.
        
        Raises
        ------
        RuntimeError
            - `invoke` and `initial-invoke` are required and they cannot be `None`.
        """
        if self.invoke is None:
            raise RuntimeError(f'`invoke` is required and cannot be `None`.')
        
        if self.initial_invoke is None:
            raise RuntimeError(f'`initial_invoke` is required and cannot be `None`.')


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


def _iter_sub_components(component):
    """
    Iterates the give component's sub-components.
    
    Parameters
    ----------
    component : ``ComponentBase``
        The component to iterate over.
    
    Yields
    ------
    sub_component : ``ComponentBase``
        The  sub components.
    """
    if isinstance(component, ComponentRow):
        sub_components = component.components
        if (sub_components is not None):
            yield from sub_components
        return
    
    if isinstance(component, ComponentSelect):
        sub_components = component.options
        if (sub_components is not None):
            yield from sub_components
        return


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
            for attribute_name in ('__call__', 'cancel', '__new__',):
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
        
        if (Menu is not None):
            new_menu_structure.validate()
        
        class_attributes['_menu_structure'] = new_menu_structure
        
        
        all_component_descriptor = []
        
        component_descriptors = OrderedDict()
        tracked_components = OrderedDict()
        
        for attribute_name, attribute_value in _iter_attributes(class_parents, class_attributes):
            if isinstance(attribute_value, ComponentDescriptor):
                container = component_descriptors
                secondary = tracked_components
                all_component_descriptor.append(attribute_value)
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
            if attribute_value.type in (ComponentRow, ComponentSelect):
                container = component_groups
            else:
                container = component_standalone
            
            container.append((attribute_name, attribute_value))
            continue
        
        
        for component_name, component_value in component_standalone:
            for component_descriptor in all_component_descriptor:
                if component_descriptor._source_component is component_value:
                    break
            else:
                component_descriptor = ComponentDescriptor(component_value, None)
                all_component_descriptor.append(component_descriptor)
            
            component_descriptors[component_name] = component_descriptor
        
        for component_name, component_value in component_groups:
            for component_descriptor in all_component_descriptor:
                if component_descriptor._source_component is component_value:
                    break
            else:
                sub_component_descriptors = []
                for sub_component in _iter_sub_components(component_value):
                    for component_descriptor in all_component_descriptor:
                        if component_descriptor._source_component is sub_component:
                            break
                    else:
                        component_descriptor = ComponentDescriptor(sub_component, None)
                        all_component_descriptor.append(component_descriptor)
                    
                    sub_component_descriptors.append(component_descriptor)
                
                component_descriptor = ComponentDescriptor(component_value, sub_component_descriptors)
                all_component_descriptor.append(component_descriptor)
            
            component_descriptors[component_name] = component_descriptor
        
        for attribute_name, attribute_value in component_descriptors.items():
            class_attributes[attribute_name] = attribute_value
        
        return type.__new__(cls, class_name, class_parents, class_attributes)


class MenuChange:
    """
    An object to store changes of a menu.
    
    Attributes
    ----------
    name : `str`
        The name of the attribute.
    value : `Any`
        The new value of the field.
    """
    __slots__ = ('name', 'value')
    def __new__(cls, name, value):
        """
        Creates a new ``MenuChange`` instance with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the attribute.
        value : `Any`
            The new value of the field.
        """
        self = object.__new__(cls)
        self.name = name
        self.value = value
        return self
    
    def __repr__(self):
        """Returns the menu change's representation"""
        return f'{self.__class__.__name__}({self.name!r}, {self.value!r})'


class Menu(metaclass=MenuType):
    """
    
    Attributes
    ----------
    _allowed_mentions : ``Ellipsis``, `None` or `list` of `Any`
        The used allowed mentions when editing the respective message.
    _component_proxy_cache : `dict` of (`int`, ``ComponentProxy``) items
        A dictionary of component proxy identifiers and component proxies.
    _timeouter : `None` or ``Timeouter``
        Executes the timeout feature on the menu.
    _tracked_changes : `list` of ``MenuChange``
        The tracked changes by attribute name.
    channel : ``ChannelTextBase`` instance
        The channel where the menu is executed.
    client : ``Client``
        The executor client instance.
    message : `None` or ``Message``
        The message which executes the menu.
    """
    __slots__ = ('_allowed_mentions', '_component_proxy_cache', '_timeouter', '_tracked_changes', 'channel', 'client',
        'message', )
    
    async def __new__(cls, interaction_event, *args, **kwargs):
        """
        Creates a new menu instance.
        
        Parameters
        ----------
        interaction_event : ``InteractionEvent``, ``Message``, `tuple` (``Client``, ``ChannelTextBase``)
            The event to respond to, or the channel to send the message at, or the message to edit.
        
        Raises
        ------
        TypeError
            If `interaction_event` was not given neither as ``InteractionEvent``, ``Message`` nor as
            ``ChannelTextBase`` instance.
        """
        # use goto
        while True:
            if isinstance(interaction_event, InteractionEvent):
                target_channel = interaction_event.channel
                target_message = interaction_event.message # Should be `None`
                target_client = interaction_event.client
                is_interaction = True
                break
                
            if isinstance(interaction_event, Message):
                target_channel = interaction_event.channel
                target_message = interaction_event
                target_client = get_client_from_message(interaction_event)
                is_interaction = False
                break
            
            if isinstance(interaction_event, tuple) and (len(interaction_event) == 2):
                target_client, target_channel = interaction_event
                if isinstance(target_client, Client) and isinstance(target_channel, ChannelTextBase):
                    target_message = None
                    is_interaction = False
                    break
            
            raise TypeError(f'`interaction_event` can be given as `{InteractionEvent.__name__}`, '
                f'`{Message.__name__}` or as `{ChannelTextBase.__name__}` instance, got '
                f'{interaction_event.__class__.__name__}.')
        
        
        self = object.__new__(cls)
        self.channel = target_channel
        self.message = target_message
        self.client = target_client
        self._timeouter = None
        self._tracked_changes = []
        self._allowed_mentions = None
        self._component_proxy_cache = {}
        # TODO
    
    
    @property
    def content(self):
        """
        A get-set-del property to modify the menu's content.
        """
        message = self.message
        if message is None:
            content = ''
        else:
            content = message.content
        
        return content
    
    @content.setter
    def content(self, content):
        if content is None:
            change_name = 'content'
            change_value = None
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
        
        self._tracked_changes.append(MenuChange(change_name, change_value))
    
    @content.deleter
    def content(self):
        self._tracked_changes.append(MenuChange('content', None))
    
    
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
        
        self._tracked_changes.append(MenuChange('embed', embed))
    
    @embed.deleter
    def embed(self):
        self._tracked_changes.append(MenuChange('embed', None))
    
    
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
        if isinstance(allowed_mentions_input, AllowedMentionProxy):
            allowed_mentions = allowed_mentions_input.copy()
        else:
            allowed_mentions = AllowedMentionProxy(allowed_mentions_input)
        
        self._allowed_mentions = allowed_mentions
    
    @allowed_mentions.deleter
    def allowed_mentions(self):
        self._allowed_mentions = None


