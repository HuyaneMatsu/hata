__all__ = ('InteractionMetadataApplicationCommandAutocomplete',)

from scarletio import copy_docs

from .base import InteractionMetadataBase
from .fields import (
    parse_id, parse_name, parse_options, put_id_into, put_name_into, put_options_into, validate_id, validate_name,
    validate_options
)


class InteractionMetadataApplicationCommandAutocomplete(InteractionMetadataBase):
    """
    Interaction metadata used when the interaction was triggered by an application command's auto completion.
    
    Parameters
    ----------
    id : `int`
        The represented application command's identifier number.
    
    name : `str`
        The represented application command's name.
    
    options : `None`, `tuple` of ``InteractionOption``
        Application command option representations. Like sub-command or parameter.
    """
    __slots__ = ('id', 'name', 'options')
    
    @classmethod
    @copy_docs(InteractionMetadataBase._create_empty)
    def _create_empty(cls):
        self = object.__new__(cls)
        self.id = 0
        self.name = ''
        self.options = None
        return self
    
    
    @copy_docs(InteractionMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.id = self.id
        new.name = self.name
        
        options = self.options
        if (options is not None):
            options = tuple(option.copy() for option in options)
        new.options = options
        
        return new
    
    
    @copy_docs(InteractionMetadataBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        # id
        try:
            application_command_id = keyword_parameters.pop('id')
        except KeyError:
            pass
        else:
            self.id = validate_id(application_command_id)
        
        # name
        try:
            application_command_name = keyword_parameters.pop('name')
        except KeyError:
            pass
        else:
            self.name = validate_name(application_command_name)
        
        # options
        try:
            options = keyword_parameters.pop('options')
        except KeyError:
            pass
        else:
            self.options = validate_options(options)
        
        
        InteractionMetadataBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
    
    
    @classmethod
    @copy_docs(InteractionMetadataBase.from_data)
    def from_data(cls, data, interaction_event):
        self = object.__new__(cls)
        self.id = parse_id(data)
        self.name = parse_name(data)
        self.options = parse_options(data)
        return self
    
    
    @copy_docs(InteractionMetadataBase.to_data)
    def to_data(self, *, defaults = False, interaction_event = None):
        data = {}
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        put_options_into(self.options, data, defaults)
        return data
    
    
    @copy_docs(InteractionMetadataBase._put_attribute_representations_into)
    def _put_attribute_representations_into(self, repr_parts):
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # options
        options = self.options
        if (options is not None):
            repr_parts.append(', options = ')
            repr_parts.append(repr(options))
        
        return True
    
    
    @copy_docs(InteractionMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        # options
        options = self.options
        if (options is not None):
            hash_value ^= len(options)
            
            for option in options:
                hash_value ^= hash(option)
        
        return hash_value
    
    
    @copy_docs(InteractionMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # options
        if self.options != other.options:
            return False
        
        return True
