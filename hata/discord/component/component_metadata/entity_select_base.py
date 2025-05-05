__all__ = ('ComponentMetadataEntitySelectBase', )

from scarletio import copy_docs

from .fields import parse_default_values, put_default_values, validate_default_values
from .select_base import ComponentMetadataSelectBase


class ComponentMetadataEntitySelectBase(ComponentMetadataSelectBase):
    """
    Channel select component metadata.
    
    Attributes
    ----------
    custom_id : `None | str`
        Custom identifier to detect which component was used by the user.
    
    default_values : ``None | tuple<EntitySelectDefaultValue>``
        Entities presented in the select by default.
    
    enabled : `bool`
        Whether the component is enabled.
    
    max_values : `int
        The maximal amount of options to select.
    
    min_values : `int`
        The minimal amount of options to select.
    
    placeholder : `None | str`
        Placeholder text of the select.
    """
    __slots__ = ('default_values',)
    
    
    def __new__(
        cls,
        *,
        custom_id = ...,
        default_values = ...,
        enabled = ...,
        max_values = ...,
        min_values = ...,
        placeholder = ...,
    ):
        """
        Creates a new channel select component metadata with the given parameters.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        default_values : ``None | iterable<Channel> | iterable<Role> | iterable<ClientUserBase> | iterable<EntitySelectDefaultValue> | iterable<(str | EntitySelectDefaultValueTyp, int | str)>>`` \
                , Optional (Keyword only)
            Entities presented in the select by default.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        max_values : `int, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        placeholder : `None | str`, Optional (Keyword only)
            Placeholder text of the select.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # default_values
        if default_values is ...:
            default_values = None
        else:
            default_values = validate_default_values(default_values)
        
        # Construct
        self = ComponentMetadataSelectBase.__new__(
            cls,
            custom_id = custom_id,
            enabled = enabled,
            max_values = max_values,
            min_values = min_values,
            placeholder = placeholder,
        )
        self.default_values = default_values
        
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataSelectBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            custom_id = keyword_parameters.pop('custom_id', ...),
            default_values = keyword_parameters.pop('default_values', ...),
            enabled = keyword_parameters.pop('enabled', ...),
            max_values = keyword_parameters.pop('max_values', ...),
            min_values = keyword_parameters.pop('min_values', ...),
            placeholder = keyword_parameters.pop('placeholder', ...),
        )
    
    
    @copy_docs(ComponentMetadataSelectBase._add_type_specific_repr_fields_into)
    def _add_type_specific_repr_fields_into(self, repr_parts):
        # default_values
        repr_parts.append(', default_values = ')
        default_values = self.default_values
        if (default_values is None):
            repr_parts.append('[]')
        else:
            repr_parts.append('[')
            
            index = 0
            limit = len(default_values)
            
            while True:
                option = default_values[index]
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
        
        # default_values
        default_values = self.default_values
        if (default_values is not None):
            hash_value ^= hash(default_values)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataSelectBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ComponentMetadataSelectBase._is_equal_same_type(self, other):
            return False
        
        # default_values
        if self.default_values != other.default_values:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataSelectBase.from_data)
    def from_data(cls, data):
        self = super(ComponentMetadataEntitySelectBase, cls).from_data(data)
        self.default_values = parse_default_values(data)
        return self
    
    
    @copy_docs(ComponentMetadataSelectBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ComponentMetadataSelectBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        put_default_values(self.default_values, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataSelectBase.clean_copy)
    def clean_copy(self, guild = None):
        new = ComponentMetadataSelectBase.clean_copy(self, guild)
        
        # default_values
        default_values = self.default_values
        if (default_values is not None):
            default_values = (*default_values,)
        new.default_values = default_values
        
        return new
    
    
    @copy_docs(ComponentMetadataSelectBase.copy)
    def copy(self):
        new = ComponentMetadataSelectBase.copy(self)
        
        # default_values
        default_values = self.default_values
        if (default_values is not None):
            default_values = (*default_values,)
        new.default_values = default_values
        
        return new
    
    
    def copy_with(
        self,
        *,
        custom_id = ...,
        default_values = ...,
        enabled = ...,
        max_values = ...,
        min_values = ...,
        placeholder = ...,
    ):
        """
        Copies the channel select component metadata with the given fields.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        default_values : ``None | iterable<Channel> | iterable<Role> | iterable<ClientUserBase> | iterable<EntitySelectDefaultValue> | iterable<(str | EntitySelectDefaultValueTyp, int | str)>>`` \
                , Optional (Keyword only)
            Entities presented in the select by default.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the component is enabled.
        
        max_values : `int, Optional (Keyword only)
            The maximal amount of options to select.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select.
        
        placeholder : `None | str`, Optional (Keyword only)
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
        # default_values
        if default_values is ...:
            default_values = self.default_values
            if (default_values is not None):
                default_values = (*default_values,)
        else:
            default_values = validate_default_values(default_values)
        
        # Construct
        
        new = ComponentMetadataSelectBase.copy_with(
            self,
            custom_id = custom_id,
            enabled = enabled,
            max_values = max_values,
            min_values = min_values,
            placeholder = placeholder,
        )
        new.default_values = default_values
        return new
    
    
    @copy_docs(ComponentMetadataSelectBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            custom_id = keyword_parameters.pop('custom_id', ...),
            default_values = keyword_parameters.pop('default_values', ...),
            enabled = keyword_parameters.pop('enabled', ...),
            max_values = keyword_parameters.pop('max_values', ...),
            min_values = keyword_parameters.pop('min_values', ...),
            placeholder = keyword_parameters.pop('placeholder', ...),
        )
