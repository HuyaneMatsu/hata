__all__ = ('ComponentDynamic', )

import reprlib

from scarletio import RichAttributeErrorBaseType, copy_docs

from ...bases import PreinstancedBase
from ...emoji import create_partial_emoji_data, create_partial_emoji_from_data
from ...preconverters import preconvert_preinstanced_type

from .component_base import ComponentBase
from .preinstanced import ComponentType


def dynamic_component_style_serializer(style):
    if isinstance(style, PreinstancedBase):
        style = style.value
    
    return style


COMPONENT_DYNAMIC_SERIALIZERS = {
    'emoji': create_partial_emoji_data,
    'style': dynamic_component_style_serializer,
}

del dynamic_component_style_serializer

COMPONENT_DYNAMIC_DESERIALIZERS = {
    'emoji': create_partial_emoji_from_data,
}


COMPONENT_ATTRIBUTE_NAMES = frozenset((
    'components',
    'custom_id',
    'disabled',
    'emoji',
    'label',
    'max_length',
    'max_values',
    'min_length',
    'min_values',
    'options',
    'placeholder',
    'required',
    'style',
    'url',
    'value',
))


class ComponentDynamic(ComponentBase):
    """
    Dynamic component type for not implemented component models.
    
    Attributes
    ----------
    _data : `dict` of (`str`, `Any`)
        The dynamically stored attributes of the component.
    type : ``ComponentType``
        The component's type.
    """
    __slots__ = ('_data', 'type')
    
    def __new__(cls, type_, **kwargs):
        """
        Creates a new component instance.
        
        Parameters
        ----------
        type_ : ``ComponentType``, `int`
            The component's type.
        **kwargs : Keyword parameters
            Additional attributes of the component.
        """
        type_ = preconvert_preinstanced_type(type_, 'type_', ComponentType)
        
        self = object.__new__(cls)
        self.type = type_
        self._data = kwargs
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.type = ComponentType.get(data['type'])
        
        validated_data = {}
        for key, value in data.items():
            if key == 'type':
                continue
            
            try:
                deserializer = COMPONENT_DYNAMIC_DESERIALIZERS[key]
            except KeyError:
                pass
            else:
                value = deserializer(value)
            
            validated_data[key] = value
        
        self._data = validated_data
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        data = {
            'type' : self.type.value
        }
        
        for key, value in self._data:
            try:
                serializer = COMPONENT_DYNAMIC_DESERIALIZERS[key]
            except KeyError:
                pass
            else:
                value = serializer(value)
            
            data[key] = value
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__, ' type=']
        
        type_ = self.type
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        for key, value in self._data:
            if value is None:
                continue
            
            if isinstance(value, str):
                value = reprlib.repr(value)
            else:
                value = repr(value)
            
            repr_parts.append(', ')
            repr_parts.append(key)
            repr_parts.append('=')
            repr_parts.append(value)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.type = self.type
        new._data = self._data.copy()
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        > Dynamic component do not accepts any additional attributes, and returns just a copy of itself.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Returns
        -------
        new : ``ComponentDynamic``
        """
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        return self.copy()
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self._data != other._data:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        return object.__hash__(self)
    
    
    def __getattr__(self, attribute_name):
        """Returns the component's fields if applicable"""
        try:
            attribute_value = self._data[attribute_name]
        except KeyError:
            if attribute_name in COMPONENT_ATTRIBUTE_NAMES:
                attribute_value = None
            else:
                # Linter wont cry if we do a return or such.
                return RichAttributeErrorBaseType.__getattr__(self, attribute_name)
        
        return attribute_value
    
    
    def __dir__(self):
        """Returns the attributes of the component."""
        directory = set(object.__dir__(self))
        directory.update(self._data.keys())
        directory.update(COMPONENT_ATTRIBUTE_NAMES)
        return sorted(directory)
