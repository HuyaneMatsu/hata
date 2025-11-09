__all__ = ('ComponentMetadataAttachmentInput', )

from scarletio import copy_docs

from ..shared_helpers import create_auto_custom_id

from .base import ComponentMetadataBase
from .constants import MAX_VALUES_DEFAULT, MIN_VALUES_DEFAULT
from .fields import (
    parse_custom_id, parse_max_values, parse_min_values, parse_required, put_custom_id, put_max_values, put_min_values,
    put_required, validate_custom_id, validate_max_values__attachment_input, validate_min_values__attachment_input,
    validate_required
)


class ComponentMetadataAttachmentInput(ComponentMetadataBase):
    """
    Attachment input component metadata.
    
    Attributes
    ----------
    custom_id : `None | str`
        Custom identifier to detect which component was used by the user.
    
    max_values : `int
        The maximal amount of attachments to input.
    
    min_values : `int`
        The minimal amount of attachments to input.
    
    required : `bool`
        Whether the field is required to be fulfilled.
    """
    __slots__ = ('custom_id', 'max_values', 'min_values', 'required')
    
    
    def __new__(
        cls,
        *,
        custom_id = ...,
        max_values = ...,
        min_values = ...,
        required = ...,
    ):
        """
        Creates a new attachment input component metadata with the given parameters.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        max_values : `int, Optional (Keyword only)
            The maximal amount of attachments to input.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of attachments to input.
        
        required : `None | bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # custom_id
        if custom_id is ...:
            custom_id = None
        else:
            custom_id = validate_custom_id(custom_id)
        
        # max_values
        if max_values is ...:
            max_values = MAX_VALUES_DEFAULT
        else:
            max_values = validate_max_values__attachment_input(max_values)
        
        # min_values
        if min_values is ...:
            min_values = MIN_VALUES_DEFAULT
        else:
            min_values = validate_min_values__attachment_input(min_values)
        
        # required
        if required is ...:
            required = None
        else:
            if (required is not None):
                required = validate_required(required)
        
        # Auto detect required if not-given / None
        
        if (required is None):
            if min_values > 0:
                required = True
            else:
                required = False
        
        # Extra checks
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.max_values = max_values
        self.min_values = min_values
        self.required = required
        return self
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            custom_id = keyword_parameters.pop('custom_id', ...),
            max_values = keyword_parameters.pop('max_values', ...),
            min_values = keyword_parameters.pop('min_values', ...),
            required = keyword_parameters.pop('required', ...),
        )
    
    
    @copy_docs(ComponentMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # System fields : custom_id
        
        # custom_id
        repr_parts.append(' custom_id = ')
        repr_parts.append(repr(self.custom_id))
        
        # Optional descriptive fields: min_values & max_values & required
        
        # min_values
        min_values = self.min_values
        if min_values != MIN_VALUES_DEFAULT:
            repr_parts.append(', min_values = ')
            repr_parts.append(repr(min_values))
        
        # max_values
        max_values = self.max_values
        if max_values != MAX_VALUES_DEFAULT:
            repr_parts.append(', max_values = ')
            repr_parts.append(repr(max_values))
        
        # required (relation with `min_values`)
        required = self.required
        if (min_values > 0) ^ required:
            repr_parts.append(', required = ')
            repr_parts.append(repr(required))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # custom_id
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        # max_values
        max_values = self.max_values
        if (max_values != 1):
            hash_value ^= (max_values << 18)
        
        # min_values
        min_values = self.min_values
        if (min_values != 1):
            min_values ^= (min_values << 22)
        
        # required
        if self.required:
            hash_value ^= (1 << 28)
        
        return hash_value
    
    
    @copy_docs(ComponentMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # custom_id
        if self.custom_id != other.custom_id:
            return False
        
        # max_values
        if self.max_values != other.max_values:
            return False
        
        # min_values
        if self.min_values != other.min_values:
            return False
        
        # required
        if self.required != other.required:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ComponentMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.custom_id = parse_custom_id(data)
        self.max_values = parse_max_values(data)
        self.min_values = parse_min_values(data)
        self.required = parse_required(data)
        return self
    
    
    @copy_docs(ComponentMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = {}
        
        put_custom_id(self.custom_id, data, defaults)
        put_max_values(self.max_values, data, defaults)
        put_min_values(self.min_values, data, defaults)
        put_required(self.required, data, defaults)
        
        return data
    
    
    @copy_docs(ComponentMetadataBase.clean_copy)
    def clean_copy(self, guild = None):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        # max_values
        new.max_values = self.max_values
        
        # min_values
        new.min_values = self.min_values
        
        # required
        new.required = self.required
        
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # custom_id
        new.custom_id = self.custom_id
        
        # max_values
        new.max_values = self.max_values
        
        # min_values
        new.min_values = self.min_values
        
        # required
        new.required = self.required
        
        return new
    
    
    def copy_with(
        self,
        *,
        custom_id = ...,
        max_values = ...,
        min_values = ...,
        required = ...,
    ):
        """
        Copies the attachment input component metadata with the given fields.
        
        Parameters
        ----------
        custom_id : `None | str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        
        max_values : `int, Optional (Keyword only)
            The maximal amount of attachments to input.
        
        min_values : `int`, Optional (Keyword only)
            The minimal amount of attachments to input.
        
        required : `None | bool`, Optional (Keyword only)
            Whether the field is required to be fulfilled.
        
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
        # custom_id
        if custom_id is ...:
            custom_id = self.custom_id
        else:
            custom_id = validate_custom_id(custom_id)
        
        # max_values
        if max_values is ...:
            max_values = self.max_values
        else:
            max_values = validate_max_values__attachment_input(max_values)
        
        # min_values
        if min_values is ...:
            min_values = self.min_values
        else:
            min_values = validate_min_values__attachment_input(min_values)
        
        # required
        if required is ...:
            required = self.required
        else:
            required = validate_required(required)
        
        # Extra checks
        
        if custom_id is None:
            custom_id = create_auto_custom_id()
        
        # Construct
        new = object.__new__(type(self))
        new.custom_id = custom_id
        new.max_values = max_values
        new.min_values = min_values
        new.required = required
        return new
    
    
    @copy_docs(ComponentMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            custom_id = keyword_parameters.pop('custom_id', ...),
            max_values = keyword_parameters.pop('max_values', ...),
            min_values = keyword_parameters.pop('min_values', ...),
            required = keyword_parameters.pop('required', ...),
        )
