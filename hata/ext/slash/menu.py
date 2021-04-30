__all__ = ()

# Work in progress

from ...backend.utils import copy_docs

from ...discord.preinstanced import ButtonStyle, ComponentType
from ...discord.preconverters import preconvert_preinstanced_type
from ...discord.emoji import create_partial_emoji_data, create_partial_emoji, Emoji
from ...discord.interaction import Component, ComponentBase, COMPONENT_TYPE_ATTRIBUTE_COMPONENTS, \
    COMPONENT_TYPE_ATTRIBUTE_CUSTOM_ID, COMPONENT_TYPE_ATTRIBUTE_ENABLED, COMPONENT_TYPE_ATTRIBUTE_EMOJI, \
    COMPONENT_TYPE_ATTRIBUTE_LABEL, COMPONENT_TYPE_ATTRIBUTE_STYLE, COMPONENT_TYPE_ATTRIBUTE_URL
from ...discord.interaction import ComponentBase, Component, _debug_component_components, _debug_component_custom_id, \
    _debug_component_emoji, _debug_component_label, _debug_component_enabled, _debug_component_url, \
    COMPONENT_TYPE_TO_STYLE

from .components import Button, Row

class ComponentDescriptor:
    """
    
    Attributes
    ----------
    _component : ``Component``
        The wrapped component instance.
    _source_component : ``ComponentBase``
        The source component from which the descriptor is created from.
    _source_name : `str`
        The descriptor's name.
    """
    __slots__ = ('_component', '_source_component', '_source_name')
    def __new__(cls, source, name):
        """
        Creates a new ``ComponentDescriptor`` instance from the given component.
        
        Parameters
        ----------
        source : ``ComponentBase`` instance
            The source component to create the descriptor from.
        name : `str` or `None`
            The source component's name.
        """
        component = Component.from_data(source.to_data())
        
        self = object.__new__(cls)
        self._component = component
        self._source_component = source
        self._source_name = name
        return self
    
    def __get__(self, instance, type_):
        """Gets the descriptor itself if called from class or a component proxy."""
        if instance is None:
            return self
        
        component_proxy_cache = instance._component_proxy_cache
        try:
            component_proxy = component_proxy_cache[self._source_name]
        except KeyError:
            component_proxy = component_proxy_cache[self._source_name] = ComponentProxy(self, instance)
        
        return component_proxy


class ComponentProxy:
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
    
    
    @property
    def type(self):
        """Returns the component's type."""
        return self._descriptor._component.type
    
    
    @property
    @copy_docs(Button.style)
    def style(self):
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
        
        return component.style
    
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
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
        
        return component.custom_id
    
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
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
        
        return component.emoji
    
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
        component = self._component_overwrite
        if (component is None):
            component = self._descriptor._component
        
        return component.url
    
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




