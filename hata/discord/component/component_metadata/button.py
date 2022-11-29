__all__ = ('ComponentMetadataButton', )

import reprlib, warnings

from scarletio import copy_docs

from ...utils import url_cutter

from ..shared_fields import (
    parse_custom_id, parse_emoji, put_custom_id_into, put_emoji_into, validate_custom_id, validate_emoji
)
from ..shared_helpers import create_auto_custom_id

from .base import ComponentMetadataBase
from .constants import BUTTON_STYLE_DEFAULT
from .fields import (
    parse_button_style, parse_enabled, parse_label, parse_url, put_button_style_into, put_enabled_into, put_label_into,
    put_url_into, validate_button_style, validate_enabled, validate_label, validate_url
)
from .preinstanced import ButtonStyle


class ComponentMetadataButton(ComponentMetadataBase):
    """
    Button component metadata.
    
    Attributes
    ----------
    button_style : ``ButtonStyle``
        The button's style.
    
    custom_id : `None`, `str`
        Custom identifier to detect which button was clicked by the user.
        
        > Mutually exclusive with the `url` field.
    
    emoji : `None`, ``Emoji``
        Emoji of the button if applicable.
    
    enabled : `bool`
        Whether the component is enabled.
    
    label : `None`, `str`
        Label of the component.
    
    url : `None`, `str`
        Url to redirect to when clicking on the button.
        
        > Mutually exclusive with the `custom_id` field.
    """
    __slots__ = ('button_style', 'custom_id', 'emoji', 'enabled', 'label', 'url',)
    
    @copy_docs(ComponentMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        # button_style
        try:
            button_style = keyword_parameters.pop('button_style')
        except KeyError:
            button_style = BUTTON_STYLE_DEFAULT
        else:
            button_style = validate_button_style(button_style)
        
        # custom_id
        try:
            custom_id = keyword_parameters.pop('custom_id')
        except KeyError:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # emoji
        try:
            emoji = keyword_parameters.pop('emoji')
        except KeyError:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # enabled
        try:
            enabled = keyword_parameters.pop('enabled')
        except KeyError:
            enabled = True
        else:
            enabled = validate_enabled(enabled)
        
        # label
        try:
            label = keyword_parameters.pop('label')
        except KeyError:
            label = None
        else:
            label = validate_label(label)
        
        # url
        try:
            url = keyword_parameters.pop('url')
        except KeyError:
            url = None
        else:
            url = validate_url(url)
        
        
        self = object.__new__(cls)
        self.button_style = button_style
        self.custom_id = custom_id
        self.emoji = emoji
        self.enabled = enabled
        self.label = label
        self.url = url
        
        self._validate()
        
        return self
    
    
    def _validate(self):
        """
        Runs additional validation after the component is created.
        
        Raises
        ------
        ValueError
            - `url` is mutually exclusive with `custom_id`.
        """
        if self.url is None:
            if self.custom_id is None:
                self.custom_id = create_auto_custom_id()
            
            if (self.button_style is ButtonStyle.link) or (self.button_style is ButtonStyle.none):
                self.button_style = BUTTON_STYLE_DEFAULT
            
        else:
            if self.custom_id is None:
                self.button_style = ButtonStyle.link
            
            else:
                raise ValueError(
                    f'`custom_id` and `url` fields are mutually exclusive, got '
                    f'custom_id = {self.custom_id!r}, url = {self.url!r}.'
                )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields : button_style
        
        # button_style
        button_style = self.button_style
        repr_parts.append(' button_style = ')
        repr_parts.append(button_style.name)
        repr_parts.append(' (')
        repr_parts.append(repr(button_style.value))
        repr_parts.append(')')
        
        # System fields : custom_id
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id = ')
            repr_parts.append(reprlib.repr(custom_id))
        
        # Text fields : emoji & label
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji = ')
            repr_parts.append(repr(emoji))
        
        # label
        label = self.label
        if (label is not None):
            repr_parts.append(', label = ')
            repr_parts.append(reprlib.repr(label))
        
        
        # Optional descriptive fields: url & enabled
        
        # url
        url = self.url
        if (url is not None):
            repr_parts.append(', url = ')
            repr_parts.append(url_cutter(url))
        
        # enabled
        enabled = self.enabled
        if (not enabled):
            repr_parts.append(', enabled = ')
            repr_parts.append(repr(enabled))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # button_style
        hash_value ^= self.button_style.value
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= emoji.id
        
        # enabled
        if self.enabled:
            hash_value ^= 1 << 8
        
        # label
        label = self.label
        if (label is not None):
            hash_value ^= hash(label)
        
        # url
        url = self.url
        if (url is not None):
            hash_value ^= hash(url)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # button_style
        if self.button_style is not other.button_style:
            return False
        
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # emoji
        if self.emoji is not other.emoji:
            return False
        
        # enabled
        if self.enabled != other.enabled:
            return False
        
        # label
        if self.label != other.label:
            return False
            
        # url
        if self.url != other.url:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        self.button_style = parse_button_style(data)
        self.custom_id = parse_custom_id(data)
        self.emoji = parse_emoji(data)
        self.enabled = parse_enabled(data)
        self.label = parse_label(data)
        self.url = parse_url(data)
        
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data =  {}
        
        put_button_style_into(self.button_style, data, defaults)
        put_custom_id_into(self.custom_id, data, defaults)
        put_emoji_into(self.emoji, data, defaults)
        put_enabled_into(self.enabled, data, defaults)
        put_label_into(self.label, data, defaults)
        put_url_into(self.url, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.button_style = self.button_style
        new.custom_id = self.custom_id
        new.emoji = self.emoji
        new.enabled = self.enabled
        new.label = self.label
        new.url = self.url
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with)
    def copy_with(self, keyword_parameters):
        # button_style
        try:
            button_style = keyword_parameters.pop('button_style')
        except KeyError:
            button_style = self.button_style
        else:
            button_style = validate_button_style(button_style)
        
        # custom_id
        try:
            custom_id = keyword_parameters.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # emoji
        try:
            emoji = keyword_parameters.pop('emoji')
        except KeyError:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # enabled
        try:
            enabled = keyword_parameters.pop('enabled')
        except KeyError:
            enabled = self.enabled
        else:
            enabled = validate_enabled(enabled)
        
        # label
        try:
            label = keyword_parameters.pop('label')
        except KeyError:
            label = self.label
        else:
            label = validate_label(label)
        
        # url
        try:
            url = keyword_parameters.pop('url')
        except KeyError:
            url = self.url
        else:
            url = validate_url(url)
        
        # Deprecated: style
        
        try:
            style = keyword_parameters.pop('style')
        except KeyError:
            pass
        else:
            warnings.warn(
                (
                    '`style` parameter of components is deprecated and will be removed in 2023 February. '
                    'Please use `button_style` for button components.'
                ),
                FutureWarning,
                stacklevel = 3,
            )
            
            button_style = validate_button_style(style)
        
        # Construct
        
        new = object.__new__(type(self))
        new.button_style = button_style
        new.custom_id = custom_id
        new.emoji = emoji
        new.enabled = enabled
        new.label = label
        new.url = url
        
        new._validate()
        
        return new
