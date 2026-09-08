__all__ = ('ApplicationCommandOptionMetadataAttachment',)

from scarletio import copy_docs

from .fields import parse_file_type_filter, put_file_type_filter, validate_file_type_filter
from .parameter import ApplicationCommandOptionMetadataParameter


class ApplicationCommandOptionMetadataAttachment(ApplicationCommandOptionMetadataParameter):
    """
    Attachment parameter application command option metadata.
    
    Parameters
    ----------
    file_type_filter : ``None | FileTypeFilter``
        Filter to apply on accepted file types.
    
    required : `bool`
        Whether the parameter is required. Defaults to `False`.
    """
    __slots__ = ('file_type_filter',)
    
    def __new__(cls, *, file_type_filter = ..., required = ...):
        """
        Creates a new attachment application command option metadata with the given parameters.
        
        Parameters
        ----------
        file_type_filter : ``None | FileTypeFilter``, Optional (Keyword only)
            Filter to apply on accepted file types.
        
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        # file_type_filter
        if file_type_filter is ...:
            file_type_filter = None
        else:
            file_type_filter = validate_file_type_filter(file_type_filter)
        
        # Construct
        new = ApplicationCommandOptionMetadataParameter.__new__(
            cls,
            required = required,
        )
        new.file_type_filter = file_type_filter
        return new
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataParameter.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            file_type_filter = keyword_parameters.pop('file_type_filter', ...),
            required = keyword_parameters.pop('required', ...),
        )
    
    
    @classmethod
    @copy_docs(ApplicationCommandOptionMetadataParameter.from_data)
    def from_data(cls, data):
        self = super(ApplicationCommandOptionMetadataAttachment, cls).from_data(data)
        self.file_type_filter = parse_file_type_filter(data)
        return self
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter.to_data)
    def to_data(self, *, defaults = False):
        data = ApplicationCommandOptionMetadataParameter.to_data(self, defaults = defaults)
        put_file_type_filter(self.file_type_filter, data, defaults)
        return data
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter._add_type_specific_repr_fields)
    def _add_type_specific_repr_fields(self, repr_parts):
        ApplicationCommandOptionMetadataParameter._add_type_specific_repr_fields(self, repr_parts)
        
        repr_parts.append(', file_type_filter = ')
        repr_parts.append(repr(self.file_type_filter))
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ApplicationCommandOptionMetadataParameter._is_equal_same_type(self, other):
            return False
        
        if self.file_type_filter != other.file_type_filter:
            return False
        
        return True
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter.__hash__)
    def __hash__(self):
        hash_value = ApplicationCommandOptionMetadataParameter.__hash__(self)
        
        # file_type_filter
        file_type_filter = self.file_type_filter
        if (file_type_filter is not None):
            hash_value ^= len(file_type_filter) << 12
            
            for attachment_type in file_type_filter:
                hash_value ^= hash(attachment_type)
        
        return hash_value
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter.copy)
    def copy(self):
        new = ApplicationCommandOptionMetadataParameter.copy(self)
        
        # file_type_filter
        new.file_type_filter = self.file_type_filter
        
        return new
    
    
    def copy_with(self,  *, file_type_filter = ..., required = ...):
        """
        Copies the attachment application command option metadata with the given fields.
        
        Parameters
        ----------
        file_type_filter : ``None | FileTypeFilter``, Optional (Keyword only)
            Filter to apply on accepted file types.
        
        required : `bool`, Optional (Keyword only)
            Whether the parameter is required.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        ValueError
            - If a parameter of incorrect value given.
        """
        # file_type_filter
        if file_type_filter is ...:
            file_type_filter = self.file_type_filter
        else:
            file_type_filter = validate_file_type_filter(file_type_filter)
        
        # Construct
        new = ApplicationCommandOptionMetadataParameter.copy_with(
            self,
            required = required,
        )
        new.file_type_filter = file_type_filter
        return new
    
    
    @copy_docs(ApplicationCommandOptionMetadataParameter.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            file_type_filter = keyword_parameters.pop('file_type_filter', ...),
            required = keyword_parameters.pop('required', ...),
        )
