__all__ = ('ComponentMetadataChannelSelect', )

from scarletio import copy_docs

from .fields import parse_channel_types, put_channel_types_into, validate_channel_types
from .select_base import ComponentMetadataSelectBase


class ComponentMetadataChannelSelect(ComponentMetadataSelectBase):
    """
    Channel select component metadata.
    
    Attributes
    ----------
    channel_types : `None`, `tuple` of ``ChannelType``
        The allowed channel types by the select.
    
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
    """
    __slots__ = ('channel_types',)
    
    
    def __new__(
        cls,
        *,
        channel_types = ...,
        custom_id = ...,
        enabled = ...,
        max_values = ...,
        min_values = ...,
        placeholder = ...,
    ):
        """
        Creates a new channel select component metadata with the given parameters.
        
        Parameters
        ----------
        channel_types : `None`, `iterable` of (``ChannelType``, `int`), Optional (Keyword only)
            The allowed channel types by the select.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        max_values : `int, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        placeholder : `None`, `str`, Optional (Keyword only)
            Placeholder text of the select.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_types
        if channel_types is ...:
            channel_types = None
        else:
            channel_types = validate_channel_types(channel_types)
        
        # Construct
        self = ComponentMetadataSelectBase.__new__(
            cls,
            custom_id = custom_id,
            enabled = enabled,
            max_values = max_values,
            min_values = min_values,
            placeholder = placeholder,
        )
        self.channel_types = channel_types
        
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataSelectBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            channel_types = keyword_parameters.pop('channel_types', ...),
            custom_id = keyword_parameters.pop('custom_id', ...),
            enabled = keyword_parameters.pop('enabled', ...),
            max_values = keyword_parameters.pop('max_values', ...),
            min_values = keyword_parameters.pop('min_values', ...),
            placeholder = keyword_parameters.pop('placeholder', ...),
        )
    
    
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
    
    
    def copy_with(
        self,
        *,
        channel_types = ...,
        custom_id = ...,
        enabled = ...,
        max_values = ...,
        min_values = ...,
        placeholder = ...,
    ):
        """
        Copies the channel select component metadata with the given fields.
        
        Parameters
        ----------
        channel_types : `None`, `iterable` of (``ChannelType``, `int`), Optional (Keyword only)
            The allowed channel types by the select.
        
        custom_id : `None`, `str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        max_values : `int, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        placeholder : `None`, `str`, Optional (Keyword only)
            Placeholder text of the select.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_types
        if channel_types is ...:
            channel_types = self.channel_types
            if (channel_types is not None):
                channel_types = tuple(channel_types)
        else:
            channel_types = validate_channel_types(channel_types)
        
        # Construct
        
        new = ComponentMetadataSelectBase.copy_with(
            self,
            custom_id = custom_id,
            enabled = enabled,
            max_values = max_values,
            min_values = min_values,
            placeholder = placeholder,
        )
        new.channel_types = channel_types
        return new
    
    
    @copy_docs(ComponentMetadataSelectBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            channel_types = keyword_parameters.pop('channel_types', ...),
            custom_id = keyword_parameters.pop('custom_id', ...),
            enabled = keyword_parameters.pop('enabled', ...),
            max_values = keyword_parameters.pop('max_values', ...),
            min_values = keyword_parameters.pop('min_values', ...),
            placeholder = keyword_parameters.pop('placeholder', ...),
        )
