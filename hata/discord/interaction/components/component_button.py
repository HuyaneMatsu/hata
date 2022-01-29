__all__ = ('ComponentButton', )

import reprlib

from scarletio import copy_docs, include

from ...emoji import create_partial_emoji_data, create_partial_emoji_from_data
from ...preconverters import preconvert_preinstanced_type
from ...utils import url_cutter

from .component_base import ComponentBase
from .debug import (
    _debug_component_custom_id, _debug_component_emoji, _debug_component_enabled, _debug_component_label,
    _debug_component_url
)
from .preinstanced import ButtonStyle, ComponentType


create_auto_custom_id = include('create_auto_custom_id')


class ComponentButton(ComponentBase):
    """
    Button component.
    
    Attributes
    ----------
    custom_id : `None`, `str`
        Custom identifier to detect which button was clicked by the user.
        
        > Mutually exclusive with the `url` field.
    
    enabled : `bool`
        Whether the component is enabled.
    
    emoji : `None`, ``Emoji``
        Emoji of the button if applicable.
    
    label : `None`, `str`
        Label of the component.
    
    style : `None`, ``ButtonStyle``
        The button's style.
    
    url : `None`, `str`
        Url to redirect to when clicking on the button.
        
        > Mutually exclusive with the `custom_id` field.
    
    Class Attributes
    ----------------
    default_style : ``ButtonStyle`` = `ButtonStyle.violet`
        The default button style to use if style is not given.
    type : ``ComponentType`` = `ComponentType.button`
        The component's type.
    """
    default_style = ButtonStyle.violet
    type = ComponentType.button
    
    __slots__ = ('custom_id', 'enabled', 'emoji', 'label', 'style', 'url',)
    
    def __new__(cls, label=None, emoji=None, *, custom_id=None, enabled=True, style=None, url=None):
        """
        Creates a new component instance with the given parameters.
        
        Parameters
        ----------
        label : `None`, `str` = `None`, Optional
            Label of the component.
        
        emoji : `None`, ``Emoji`` = `None`, Optional
            Emoji of the button if applicable.
        
        custom_id : `None`, `str` = `None`, Optional (Keyword only)
            Custom identifier to detect which button was clicked by the user.
            
            > Mutually exclusive with the `url` field.
        
        enabled : `bool` = `True`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        
        style : `None`, ``ButtonStyle``, `int` = `None`, Optional (Keyword only)
            The button's style.
        
        url : `None`, `str` = `None`, Optional (Keyword only)
            Url to redirect to when clicking on the button.
            
            > Mutually exclusive with the `custom_id` field.
        
        Raises
        ------
        TypeError
            If `style`'s type is unexpected.
        AssertionError
            - If `custom_id` was not given neither as `None`, `str`.
            - `url` is mutually exclusive with `custom_id`.
            - If `emoji` was not given as ``Emoji``.
            - If `url` was not given neither as `None`, `str`.
            - If `style` was not given as any of the `type`'s expected styles.
            - If `label` was not given neither as `None` nor as `int`.
            - If `enabled` was not given as `bool`.
            - If `label`'s length is over `80`.
            - If `custom_id`'s length is over `100`.
        """
        if __debug__:
            _debug_component_custom_id(custom_id)
            _debug_component_enabled(enabled)
            _debug_component_emoji(emoji)
            _debug_component_label(label)
            _debug_component_url(url)
        
        # custom_id
        if (custom_id is not None) and (not custom_id):
            custom_id = None
        
        # enabled
        # No additional checks
        
        # emoji
        # No additional checks
        
        # label
        if (label is not None) and (not label):
            label = None
        
        # url
        if (url is not None) and (not url):
            url = None
        
        # custom_id & custom_id mixed
        if __debug__:
            if (custom_id is not None) and (url is not None):
                raise AssertionError(
                    f'`custom_id` and `url` fields are mutually exclusive, got '
                    f'custom_id={custom_id!r}, url={url!r}.'
                )
        
        # style
        if (url is None):
            # style
            if style is None:
                style = cls.default_style
            else:
                style = preconvert_preinstanced_type(style, 'style', ButtonStyle)
            
            # If `custom_id` is required, but not given, generate one.
            if (custom_id is None):
                custom_id = create_auto_custom_id()
        
        else:
            style = ButtonStyle.link
        
        
        self = object.__new__(cls)
        
        self.custom_id = custom_id
        self.enabled = enabled
        self.emoji = emoji
        self.label = label
        self.style = style
        self.url = url
        
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        # custom_id
        self.custom_id = data.get('custom_id', None)
        
        # enabled
        self.enabled = not data.get('disabled', False)
        
        # emoji
        emoji_data = data.get('emoji', None)
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji_from_data(emoji_data)
        self.emoji = emoji
        
        # label
        self.label = data.get('label', None)
        
        # style
        self.style = ButtonStyle.get(data.get('style', 0))
        
        # url
        self.url = data.get('url', None)
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        # type
        data = {
            'type' : self.type.value
        }
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            data['custom_id'] = custom_id
        
        # enabled
        if (not self.enabled):
            data['disabled'] = True
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            data['emoji'] = create_partial_emoji_data(emoji)
        
        # label
        label = self.label
        if (label is not None):
            data['label'] = label
        
        # style
        style = self.style
        if (style is not None):
            data['style'] = style.value
        
        # url
        url = self.url
        if (url is not None):
            data['url'] = url
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__, ]
        
        # Descriptive fields : type & style
        
        # type
        type_ = self.type
        repr_parts.append(' type=')
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        # style
        style = self.style
        repr_parts.append(', style=')
        repr_parts.append(style.name)
        repr_parts.append(' (')
        repr_parts.append(repr(style.value))
        repr_parts.append(')')
        
        # System fields : custom_id
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id=')
            repr_parts.append(reprlib.repr(custom_id))
        
        # Text fields : emoji & label
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji=')
            repr_parts.append(repr(emoji))
        
        # label
        label = self.label
        if (label is not None):
            repr_parts.append(', label=')
            repr_parts.append(reprlib.repr(label))
        
        
        # Optional descriptive fields: url & enabled
        
        # url
        url = self.url
        if (url is not None):
            repr_parts.append(', url=')
            repr_parts.append(url_cutter(url))
        
        # enabled
        enabled = self.enabled
        if (not enabled):
            repr_parts.append(', enabled=')
            repr_parts.append(repr(enabled))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.custom_id = self.custom_id
        new.enabled = self.enabled
        new.emoji = self.emoji
        new.label = self.label
        new.style = self.style
        new.url = self.url
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Other Parameters
        ----------------
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which button was clicked by the user.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            Emoji of the button if applicable.
        
        label : `None`, `str`, Optional (Keyword only)
            Label of the component.
        
        style : `None`, ``ButtonStyle``, `int`, Optional (Keyword only)
            The button's style.
        
        url : `None`, `str`, Optional (Keyword only)
            Url to redirect to when clicking on the button.
        
        Returns
        -------
        new : ``ComponentButton``
        """
        # custom_id
        try:
            custom_id = kwargs.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            if __debug__:
                _debug_component_custom_id(custom_id)
            
            if (custom_id is not None) and (not custom_id):
                custom_id = None
        
        # enabled
        try:
            enabled = kwargs.pop('enabled')
        except KeyError:
            enabled = self.enabled
        else:
            if __debug__:
                _debug_component_enabled(enabled)
        
        # emoji
        try:
            emoji = kwargs.pop('emoji')
        except KeyError:
            emoji = self.emoji
        else:
            if __debug__:
                _debug_component_emoji(emoji)
        
        # label
        try:
            label = kwargs.pop('label')
        except KeyError:
            label = self.label
        else:
            if __debug__:
                _debug_component_label(label)
        
        # style
        try:
            style = kwargs.pop('style')
        except KeyError:
            style = self.style
        
        # url
        try:
            url = kwargs.pop('url')
        except KeyError:
            url = self.url
        else:
            if __debug__:
                _debug_component_url(url)
            
            if (url is not None) and (not url):
                url = None

        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        
        # custom_id & url
        if __debug__:
            if (custom_id is not None) and (url is not None):
                raise AssertionError(
                    f'`custom_id` and `url` fields are mutually exclusive, got '
                    f'custom_id={custom_id!r}, url={url!r}.'
                )
        
        # url # style & custom
        if (url is None):
            if style is None:
                style = self.default_style
            else:
                style = preconvert_preinstanced_type(style, 'style', ButtonStyle)
            
            if (custom_id is None):
                custom_id = create_auto_custom_id()
        
        else:
            style = ButtonStyle.link
        
        new = object.__new__(type(self))
        
        new.custom_id = custom_id
        new.enabled = enabled
        new.emoji = emoji
        new.label = label
        new.url = url
        new.style = style
        
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # enabled
        if self.enabled != other.enabled:
            return False
        
        # emoji
        if self.emoji is not other.emoji:
            return False
        
        # label
        if self.label != other.label:
            return False
        
        # style
        if self.style is not other.style:
            return False
            
        # url
        if self.url != other.url:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        hash_value = self.type.value
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # enabled
        if self.enabled:
            hash_value ^= 1 << 8
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= emoji.id
        
        # label
        label = self.label
        if (label is not None):
            hash_value ^= hash(label)
        
        # style
        style = self.style
        if (style is not None):
            hash_value ^= style.value
        
        # url
        url = self.url
        if (url is not None):
            hash_value ^= hash(url)
        
        return hash_value
