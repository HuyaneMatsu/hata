__all__ = ('Button', 'ButtonStyle', 'Row')

import reprlib

from ...backend.utils import copy_docs

from ...discord.preinstanced import ButtonStyle, ComponentType
from ...discord.interaction import ComponentBase, Component
from ...discord.preconverters import preconvert_preinstanced_type
from ...discord.emoji import create_partial_emoji_data, create_partial_emoji, Emoji
from ...discord.limits import COMPONENT_SUB_COMPONENT_LIMIT, COMPONENT_LABEL_LENGTH_MAX, COMPONENT_CUSTOM_ID_LENGTH_MAX


COMPONENT_TYPE_ACTION_ROW = ComponentType.action_row
COMPONENT_TYPE_BUTTON = ComponentType.button


class Button(ComponentBase):
    """
    Button message component.
    
    Attributes
    ----------
    _data : `dict` of (`str`, `Any`) items
        Serialized component data.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.button`
        The component's type.
    default_style : ``ButtonStyle`` = `ButtonStyle.secondary`
        The default button style to use if style is not given.
    """
    type = COMPONENT_TYPE_BUTTON
    default_style = ButtonStyle.secondary
    
    __slots__ = ('_data', )
    
    def __new__(cls, label=None, emoji=None, *, custom_id=None, url=None, style=None, enabled=True):
        """
        Creates a new component instance with the given parameters.
        
        Parameters
        ----------
        label : `None` or `str`
            Label of the component.
        emoji : `None` or ``Emoji``
            Emoji of the button if applicable.
        custom_id : `None` or `str`, Optional (Keyword only)
            Custom identifier to detect which button was clicked by the user.
            
            > Mutually exclusive with the `url` field.

        url : `None` or `str`, Optional (Keyword only)
            Url to redirect to when clicking on the button.
            
            > Mutually exclusive with the `custom_id` field.
        
        style : ``ButtonStyle``, `int`, Optional (Keyword only)
            The components's style. Applicable for buttons.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        
        Raises
        ------
        TypeError
            - If `style`'s type is unexpected.
        AssertionError
            - If `custom_id` was not given neither as `None` or `str` instance.
            - `url` is mutually exclusive with `custom_id`.
            - If `emoji` was not given as ``Emoji`` instance.
            - If `url` was not given neither as `None` or `str` instance.
            - If `style` was not given as any of the `type`'s expected styles.
            - If `label` was not given neither as `None` nor as `int` instance.
            - If `enabled` was not given as `bool` instance.
            - If `label`'s length is over `80`.
            - If `custom_id`'s length is over `100`.
        """
        if style is None:
            style = cls.default_style
        else:
            style = preconvert_preinstanced_type(style, 'style', ButtonStyle)
        
        data = {
            'type': cls.type.value,
            'style': style.value,
        }
        
        if __debug__:
            if (custom_id is not None) and (url is not None):
                raise AssertionError(f'`custom_id` and `url` fields are mutually exclusive, got '
                    f'custom_id={custom_id!r}, url={url!r}.')
        
        if (custom_id is not None):
            if __debug__:
                if (not isinstance(custom_id, str)):
                    raise TypeError(f'`custom_id` can be given either as `None` or as `str` instance, got '
                        f'{custom_id.__class__.__name__}.')
            
            data['custom_id'] = custom_id
        
        if (emoji is not None):
            if __debug__:
                if (not isinstance(emoji, Emoji)):
                    raise AssertionError(f'`emoji` can be given as `{Emoji.__name__}` instance, got '
                        f'{emoji.__class__.__name__}')
            
            data['emoji'] = create_partial_emoji_data(emoji)
        
        if (url is not None):
            if __debug__:
                if (not isinstance(url, str)):
                    raise AssertionError(f'`url` can be given either as `None` or as `str` instance, got '
                        f'{url.__class__.__name__}.')
            
            data['url'] = url
            
        if (label is not None):
            if __debug__:
                if (not isinstance(label, str)):
                    raise AssertionError(f'`label` can be given either as `None` or as `str` instance, got '
                        f'{label.__class__.__name__}.')
                
                if len(label) > COMPONENT_LABEL_LENGTH_MAX:
                    raise AssertionError(f'`label`\'s max length can be {COMPONENT_LABEL_LENGTH_MAX!r}, got '
                        f'{len(label)!r}; {label!r}.')
            
            if label:
                data['label'] = label
        
        if __debug__:
            if not isinstance(enabled, bool):
                raise AssertionError(f'`enabled` can be given as `bool` instance, got {enabled.__class__.__name__}.')
        
        if not enabled:
            data['disabled'] = True
        
        self = object.__new__(cls)
        self._data = data
        return self
    
    
    @property
    def style(self):
        """
        A get-set property for accessing the button's `style`.
        
        Accepts and returns ``ButtonStyle`` and `int` instances.
        """
        return ButtonStyle.get(self._data['style'])
    
    @style.setter
    def style(self, style):
        style = preconvert_preinstanced_type(style, 'style', ButtonStyle)
        self._data['style'] = style
    
    
    @property
    def custom_id(self):
        """
        A get-set property for accessing the button's `custom_id`.
        
        Accepts and returns ``None`` and `str` instances.
        """
        return self._data.get('custom_id', None)
    
    @custom_id.setter
    def custom_id(self, custom_id):
        if (custom_id is None):
            try:
                del self._data['custom_id']
            except KeyError:
                pass
        else:
            if __debug__:
                if (not isinstance(custom_id, str)):
                    raise TypeError(f'`custom_id` can be given either as `None` or as `str` instance, got '
                        f'{custom_id.__class__.__name__}.')
                
                if len(custom_id) > COMPONENT_CUSTOM_ID_LENGTH_MAX:
                    raise AssertionError(f'`custom_id`\'s max length can be {COMPONENT_CUSTOM_ID_LENGTH_MAX!r}, got '
                        f'{len(custom_id)!r}; {custom_id!r}.')
            
            self._data['custom_id'] = custom_id
    
    
    @property
    def emoji(self):
        """
        A get-set property for accessing the button's `emoji`.
        
        Accepts and returns ``None`` and ``Emoji`` instances.
        """
        try:
            emoji_data = self._data['emoji']
        except KeyError:
            emoji = None
        else:
            emoji = create_partial_emoji(emoji_data)
        
        return emoji
    
    @emoji.setter
    def emoji(self, emoji):
        if (emoji is None):
            try:
                del self._data['emoji']
            except KeyError:
                pass
        else:
            if __debug__:
                if (not isinstance(emoji, Emoji)):
                    raise TypeError(f'`emoji` can be given either as `None` or as `{Emoji.__name__}` instance, got '
                        f'{Emoji.__class__.__name__}.')
            
            self._data['Emoji'] = create_partial_emoji_data(emoji)
    
    
    @property
    def url(self):
        """
        A get-set property for accessing the button's `url`.
        
        Accepts and returns ``None`` and `str` instances.
        """
        return self._data.get('url', None)
    
    @url.setter
    def url(self, url):
        if (url is None):
            try:
                del self._data['url']
            except KeyError:
                pass
        else:
            if __debug__:
                if (not isinstance(url, str)):
                    raise TypeError(f'`url` can be given either as `None` or as `str` instance, got '
                        f'{url.__class__.__name__}.')
            
            self._data['url'] = url
    
    
    @property
    def label(self):
        """
        A get-set property for accessing the button's `label`.
        
        Accepts and returns ``None`` and `str` instances.
        """
        return self._data.get('url', None)
    
    @label.setter
    def label(self, label):
        if (label is not None):
            if __debug__:
                if (not isinstance(url, str)):
                    raise TypeError(f'`label` can be given either as `None` or as `str` instance, got '
                        f'{label.__class__.__name__}.')
                
                if len(label) > COMPONENT_LABEL_LENGTH_MAX:
                    raise AssertionError(f'`label`\'s max length can be {COMPONENT_LABEL_LENGTH_MAX!r}, got '
                        f'{len(label)!r}; {label!r}.')
            
            if label:
                self._data['label'] = label
                return
        
        try:
            del self._data['label']
        except KeyError:
            pass
    
    
    @property
    def enabled(self):
        """
        A get-set property for accessing the button's `enabled` field.
        
        Accepts and returns `None` and `str` instance.
        """
        return (not self._data.get('disabled', False))
    
    @enabled.setter
    def enabled(self, value):
        if __debug__:
            if not isinstance(enabled, bool):
                raise AssertionError(f'`enabled` can be given as `bool` instance, got {enabled.__class__.__name__}.')
        
        if value:
            try:
                del self._data['disabled']
            except KeyError:
                pass
        else:
            self._data['disabled'] = True
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        if __debug__:
            if data['type'] != cls.type.value:
                raise AssertionError(f'The received data is not a {cls.type.name} component, got: {data!r}.')
        
        self = object.__new__(cls)
        self._data = data
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        return self._data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = [self.__class__.__name__, '(']
        
        data = self._data
        try:
            label = data['label']
        except KeyError:
            added_field = False
        else:
            repr_parts.append(reprlib.repr(label))
            added_field = True
        
        try:
            emoji = data['emoji']
        except KeyError:
            pass
        else:
            if added_field:
                repr_parts.append(', ')
            else:
                added_field = True
                repr_parts.append('emoji=')
            
            repr_parts.append(repr(emoji))
        
        for field_name in ('custom_id', 'url'):
            try:
                field_value = data[field_name]
            except KeyError:
                pass
            else:
                if added_field:
                    repr_parts.append(', ')
                else:
                    added_field = True
                
                repr_parts.append(field_name)
                repr_parts.append('=')
                repr_parts.append(reprlib.repr(field_value))
        
        style = data['style']
        if style != self.default_style:
            if added_field:
                repr_parts.append(', ')
            else:
                added_field = True
            repr_parts.append('style=')
            repr_parts.append(repr(style))
        
        
        enabled = not data.get('disabled', False)
        if (not enabled):
            if added_field:
                repr_parts.append(', ')
            
            repr_parts.append('enabled=')
            repr_parts.append(repr(enabled))
        
        repr_parts.append(')')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new._data = self._data.copy()
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is type(self):
            if self._data == other._data:
                return True
            else:
                return False
        
        if isinstance(other, ComponentBase):
            if self.type is not other.type:
                return False
            
            if self.emoji is not other.emoji:
                return False
            
            if self.style is not other.style:
                return False
            
            if self.custom_id != other.custom_id:
                return False
            
            if self.label != other.label:
                return False
            
            if self.enabled != other.enabled:
                return False
            
            return True
        
        
        return NotImplemented
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        data = self._data
        hash_value = self.type.value
        
        try:
            emoji = data['emoji']
        except KeyError:
            pass
        else:
            hash_value ^= emoji.id
        
        hash_value ^= data['style'].value
        
        for field_name in ('custom_id', 'url', 'label'):
            try:
                field_value = data[field_name]
            except KeyError:
                pass
            else:
                hash_value ^= hash(field_value)
        
        enabled = not data.get('disabled', False)
        if enabled:
            hash_value ^= 1<<8
        
        return hash_value


class Row(ComponentBase):
    """
    Action row message component.
    
    Attributes
    ----------
    _data : `dict` of (`str`, `Any`) items
        Serialized component data.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.action_row`
        The component's type.
    """
    type = COMPONENT_TYPE_ACTION_ROW
    
    __slots__ = ('_data', )
    
    def __new__(cls, *components):
        component_datas = None
        for component in components:
            if __debug__:
                if not isinstance(component, ComponentBase):
                    raise AssertionError(f'`component` can be given as `{ComponentBase.__name__}` instance, got '
                        f'{component.__class__.__name__}.')
                
                if component.type is COMPONENT_TYPE_ACTION_ROW:
                    raise AssertionError(f'Cannot add `{COMPONENT_TYPE_ACTION_ROW}` type as sub components, got '
                        f'{component!r}.')
            
            if component_datas is None:
                component_datas = []
            
            component_datas.append(component.to_data())
        
        if __debug__:
            if (component_datas is not None) and (len(component_datas) > COMPONENT_SUB_COMPONENT_LIMIT):
                raise AssertionError(f'A `{cls.__name__}` can have maximum 5 sub-components, got '
                    f'{len(component_datas)}; {component_datas!r}.')
        
        data = {
            'type': cls.type.value
        }
        
        if (components is not None):
            data['components'] = component_datas
        
        self = object.__new__(cls)
        self._data = data
        return self
    
    
    @property
    def components(self):
        """
        A get property for accessing the row's components.
        
        Accepts `None` or a `list` of ``ComponentBase`` instances.
        """
        try:
            component_datas = self._data['components']
        except KeyError:
            components = None
        else:
            components = [
                COMPONENT_TYPE_MAP.get(component_data['type'], Component).from_data(component_data)
                    for component_data in component_datas
            ]
        
        return components


    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        if __debug__:
            if data['type'] != cls.type.value:
                raise AssertionError(f'The received data is not a {cls.type.name} component, got: {data!r}.')
        
        self = object.__new__(cls)
        self._data = data
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        return self._data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = [self.__class__.__name__, '(']
        
        try:
            component_datas = self._data['components']
        except KeyError:
            pass
        else:
            field_added = False
            for component_data in component_datas:
                if field_added:
                    repr_parts.append(', ')
                else:
                    field_added = True
                
                component = COMPONENT_TYPE_MAP.get(component_data['type'], Component).from_data(component_data)
                repr_parts.append(component)
                
        repr_parts.append(')')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        old_data = self._data
        new_data = {'type': old_data['style']}
        try:
            component_datas = old_data['components']
        except KeyError:
            pass
        else:
            new_data['components'] = [component_data.copy() for component_data in component_datas]
        
        new = object.__new__(type(self))
        new._data = new_data
        return new


    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is  type(self):
            if self._data == other._data:
                return True
            else:
                return False
        
        if isinstance(other, ComponentBase):
            if self.type is not other.type:
                return False
            
            if self.components != other.components:
                return False
            
            return True
        
        return NotImplemented
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        hash_value = self.type.value
        
        components = self.components
        if (components is not None):
            hash_value ^= len(components)<<12
            for component in components:
                hash_value ^= hash(component)
        
        return hash_value


        
COMPONENT_TYPE_MAP = {
    COMPONENT_TYPE_ACTION_ROW.value: Row,
    COMPONENT_TYPE_BUTTON.value: Button,
}


