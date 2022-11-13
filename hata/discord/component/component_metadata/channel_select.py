__all__ = ('ComponentMetadataChannelSelect', )

from scarletio import copy_docs

from .fields import parse_channel_types, put_channel_types_into, validate_channel_types
from .select_base import ComponentMetadataSelectBase


class ComponentMetadataChannelSelect(ComponentMetadataSelectBase):
    """
    Channel select component metadata.
    
    Attributes
    ----------
    custom_id : `None`, `str`
        Custom identifier to detect which component was used by the user.
    
    enabled : `bool`
        Whether the component is enabled.
    
    max_values : `int
        The maximal amount of options to select.
    
    min_values : `int`
        The minimal amount of options to select.
    
    placeholder : `None`, `str`
        Placeholder text of the select.
    
    channel_types : `None`, `tuple` of ``ChannelType``
        The allowed channel types by the select.
    """
    __slots__ = ('channel_types',)

    @copy_docs(ComponentMetadataSelectBase.__new__)
    def __new__(cls, keyword_parameters):
        # channel_types
        try:
            channel_types = keyword_parameters.pop('channel_types')
        except KeyError:
            channel_types = None
        else:
            channel_types = validate_channel_types(channel_types)
        
        # Construct
        self = ComponentMetadataSelectBase.__new__(cls, keyword_parameters)
        self.channel_types = channel_types
        
        return self
    
    
    @copy_docs(ComponentMetadataSelectBase._add_type_specific_repr_fields_into)
    def _add_type_specific_repr_fields_into(self, repr_parts):
        # channel_types
        repr_parts.append(', channel_types = ')
        channel_types = self.channel_types
        if (channel_types is None):
            repr_parts.append('[]')
        else:
            repr_parts.append('[')
            
            index = 0
            limit = len(channel_types)
            
            while True:
                option = channel_types[index]
                index += 1
                
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
    
    
    @copy_docs(ComponentMetadataSelectBase.__hash__)
    def __hash__(self):
        hash_value = ComponentMetadataSelectBase.__hash__(self)
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            hash_value ^= len(channel_types) << 12
            for index, channel_type in enumerate(channel_types):
                hash_value ^= channel_type.value << (index << 1)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataSelectBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ComponentMetadataSelectBase._is_equal_same_type(self, other):
            return False
        
        # channel_types
        if self.channel_types != other.channel_types:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataSelectBase.from_data)
    def from_data(cls, data):
        self = super(ComponentMetadataChannelSelect, cls).from_data(data)
        self.channel_types = parse_channel_types(data)
        return self
    
    
    @copy_docs(ComponentMetadataSelectBase.to_data)
    def to_data(self, *, defaults = False):
        data =  ComponentMetadataSelectBase.to_data(self)
        
        put_channel_types_into(self.channel_types, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataSelectBase.copy)
    def copy(self):
        new = ComponentMetadataSelectBase.copy(self)
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            channel_types = tuple(channel_types)
        new.channel_types = channel_types
        
        return new
    
    
    @copy_docs(ComponentMetadataSelectBase.copy_with)
    def copy_with(self, keyword_parameters):
        # channel_types
        try:
            channel_types = keyword_parameters.pop('channel_types')
        except KeyError:
            channel_types = self.channel_types
            if (channel_types is not None):
                channel_types = tuple(channel_types)
        else:
            channel_types = validate_channel_types(channel_types)
        
        # Construct
        
        new = ComponentMetadataSelectBase.copy_with(self, keyword_parameters)
        new.channel_types = channel_types
        return new
