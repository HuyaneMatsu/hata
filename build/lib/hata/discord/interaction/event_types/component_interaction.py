__all__ = ('ComponentInteraction',)

import reprlib, warnings

from scarletio import copy_docs

from ..components import ComponentBase, ComponentType

from .interaction_field_base import InteractionFieldBase


class ComponentInteraction(InteractionFieldBase):
    """
    A component interaction of an ``InteractionEvent``.
    
    Attributes
    ----------
    custom_id : `None`, `str`
        The component's custom identifier.
    options : `None`, `tuple` of `str`
        Option values selected of the respective interaction.
    type : ``ComponentType``
        The component's type.
    """
    __slots__ = ('type', 'custom_id', 'components', 'options')
    
    @copy_docs(InteractionFieldBase.__new__)
    def __new__(cls, data, interaction_event):
        # custom_id
        custom_id = data.get('custom_id', None)
        
        # type
        type_ = ComponentType.get(data['component_type'])
        
        # options
        option_datas = data.get('values', None)
        if (option_datas is None) or (not option_datas):
            options = None
        else:
            options = tuple(option_datas)
        
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.options = options
        self.type = type_
        return self
    
    
    @copy_docs(InteractionFieldBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # type
        type_ = self.type
        repr_parts.append(' type=')
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id=')
            repr_parts.append(reprlib.repr(custom_id))
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options=[')
            index = 0
            limit = len(options)
            while True:
                option = options[index]
                repr_parts.append(repr(option))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(InteractionFieldBase.__eq__)
    def __eq__(self, other):
        other_type = type(other)
        # Compare with self type.
        if other_type is type(self):
            # type
            if self.type is not other.type:
                return False
            #custom_id
            if self.custom_id != other.custom_id:
                return False
            
            return True
        
        # Compare with components.
        if issubclass(other_type, ComponentBase):
            # Check `type` before `custom_id`
            
            # type
            if self.type is not other.type:
                return False
            
            # custom_id
            if self.custom_id != other.custom_id:
                return False
            
            return True
        
        
        return NotImplemented
    
    
    @copy_docs(InteractionFieldBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # type
        hash_value ^= self.type.value
        
        # custom_id
        hash_value ^= hash(self.custom_id)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^ len(options) << 8
            for option in options:
                hash_value ^ hash(option)
        
        return hash_value
    
    
    def component_type(cls):
        """
        ``.component_type`` is deprecated, please use ``.type`` instead. Will be removed in 2022
        February.
        """
        warnings.warn(
            (
                f'`{cls.__name__}.component_type` is deprecated, and will be removed in 2022 February. '
                f'Please use `{cls.__name__}.type` instead.'
            ),
            FutureWarning,
        )
        
        return cls.type
