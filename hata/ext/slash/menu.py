__all__ = ()

# Work in progress

from collections import OrderedDict

from ...backend.utils import copy_docs
from ...backend.analyzer import CallableAnalyzer

from ...discord.preinstanced import ButtonStyle, ComponentType
from ...discord.preconverters import preconvert_preinstanced_type
from ...discord.emoji import create_partial_emoji_data, create_partial_emoji, Emoji
from ...discord.interaction import Component, ComponentBase, COMPONENT_TYPE_ATTRIBUTE_COMPONENTS, \
    COMPONENT_TYPE_ATTRIBUTE_CUSTOM_ID, COMPONENT_TYPE_ATTRIBUTE_ENABLED, COMPONENT_TYPE_ATTRIBUTE_EMOJI, \
    COMPONENT_TYPE_ATTRIBUTE_LABEL, COMPONENT_TYPE_ATTRIBUTE_STYLE, COMPONENT_TYPE_ATTRIBUTE_URL
from ...discord.interaction import ComponentBase, Component, _debug_component_components, _debug_component_custom_id, \
    _debug_component_emoji, _debug_component_label, _debug_component_enabled, _debug_component_url, \
    COMPONENT_TYPE_TO_STYLE
from ...discord.parsers import InteractionEvent
from ...discord.message import Message
from ...discord.channel import ChannelTextBase
from ...discord.embed import EmbedBase

from .components import Button, Row


class ComponentDescriptor:
    """
    
    Attributes
    ----------
    _component : ``Component``
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
        component = Component.from_data(source.to_data())
        
        identifier = cls._identifier_counter+1
        cls._identifier_counter = identifier
        
        self = object.__new__(cls)
        self._component = component
        self._source_component = source
        self._identifier = name
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
        component : ``Component``
        """
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
        
        return component
    
    
    @property
    def type(self):
        """Returns the component's type."""
        return self._descriptor._component.type
    
    
    @property
    @copy_docs(Button.style)
    def style(self):
        return self._get_component().style
    
    @style.setter
    def style(self, style):
        component_style_type = COMPONENT_TYPE_TO_STYLE.get(self.type, None)
        if component_style_type is None:
            style = None
        else:
            style = preconvert_preinstanced_type(style, 'style', component_style_type)
        
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
            
            if (style is not component.style):
                component = component.copy()
                component.style = style
                self._component_overwrite = component
        else:
            if (style is not component.style):
                component.style = style
    
    
    @property
    @copy_docs(Button.custom_id)
    def custom_id(self):
        return self._get_component().custom_id
    
    @custom_id.setter
    def custom_id(self, custom_id):
        if __debug__:
            _debug_component_custom_id(custom_id)
        
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
            
            if (custom_id != component.custom_id):
                component = component.copy()
                component.custom_id = custom_id
                self._component_overwrite = component
        else:
            if (custom_id != component.custom_id):
                component.custom_id = custom_id
    
    
    @property
    @copy_docs(Button.emoji)
    def emoji(self):
        return self._get_component().emoji
    
    @emoji.setter
    def emoji(self, emoji):
        if __debug__:
            _debug_component_emoji(emoji)
        
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
            
            if (emoji is not component.emoji):
                component = component.copy()
                component.emoji = emoji
                self._component_overwrite = component
        else:
            if (emoji is not component.emoji):
                component.emoji = emoji
    
    
    @property
    @copy_docs(Button.url)
    def url(self):
        return self._get_component().url
    
    @url.setter
    def url(self, url):
        if __debug__:
            _debug_component_url(url)
        
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
            
            if (url != component.url):
                component = component.copy()
                component.url = url
                self._component_overwrite = component
        else:
            if (url != component.url):
                component.url = url
    
    
    @property
    @copy_docs(Button.label)
    def label(self):
        return self._get_component().label
    
    @label.setter
    def label(self, label):
        if __debug__:
            _debug_component_label(label)
        
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
            
            if (label != component.label):
                component = component.copy()
                component.label = label
                self._component_overwrite = component
        else:
            if (label != component.label):
                component.label = label
    
    
    @property
    @copy_docs(Button.enabled)
    def enabled(self):
        return self._get_component().enabled
    
    @enabled.setter
    def enabled(self, enabled):
        if __debug__:
            _debug_component_enabled(enabled)
        
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
            
            if (enabled != component.enabled):
                component = component.copy()
                component.enabled = enabled
                self._component_overwrite = component
        else:
            if (enabled != component.enabled):
                component.enabled = enabled
    
    
    @property
    @copy_docs(Row.url)
    def components(self):
        components_descriptors = self._descriptor.sub_components
        if components_descriptors is None:
            return None
        
        instance = self.insatnce
        instance_type = type(instance)
        
        return tuple(components_descriptor.__get__(instance, instance_type) \
            for components_descriptor in components_descriptors)


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
    """
    for class_parent in reversed(class_parents):
        yield from class_parent.__dict__.items()
    
    yield from class_attributes.items()


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
            if attribute_value.type in COMPONENT_TYPE_ATTRIBUTE_COMPONENTS:
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
                sub_components = component_value.components
                if (sub_components is not None):
                    for sub_component in sub_components:
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
        The name of teh attribute.
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
            The name of teh attribute.
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
    
    async def __new__(cls, event_or_channel_or_message, *args, **kwargs):
        """
        Creates a new menu instance.
        
        Parameters
        ----------
        event_or_channel_or_message : ``InteractionEvent``, ``Message``, ``ChannelTextBase``
            The event to respond to, or the channel to send the message at, or the message to edit.
        
        Raises
        ------
        TypeError
            If `event_or_channel_or_message` was not given neither as ``InteractionEvent``, ``Message`` nor as
            ``ChannelTextBase`` instance.
        """
        if isinstance(event_or_channel_or_message, InteractionEvent):
            target_channel = event_or_channel_or_message.channel
            target_message = event_or_channel_or_message.message # Should be `None`
            
            is_interaction = True
        
        else:
            if isinstance(event_or_channel_or_message, Message):
                target_channel = event_or_channel_or_message.channel
                target_message = event_or_channel_or_message
            
            elif isinstance(event_or_channel_or_message, ChannelTextBase):
                target_channel = event_or_channel_or_message
                target_message = None
            
            else:
                raise TypeError(f'`event_or_channel_or_message` can be given as `{InteractionEvent.__name__}`, '
                    f'`{Message.__name__}` or as `{ChannelTextBase.__name__}` instance, got '
                    f'{event_or_channel_or_message.__class__.__name__}.')
            
            is_interaction = False
        
        self = object.__new__(cls)
        self.channel = target_channel
        self.message = target_message
        self._timeouter = None
        self._tracked_changes = []
        self._allowed_mentions = ...
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
        
