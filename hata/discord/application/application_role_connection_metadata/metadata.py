__all__ = ('ApplicationRoleConnectionMetadata',)

from scarletio import RichAttributeErrorBaseType

from ...localization.utils import hash_locale_dictionary

from .fields import (
    parse_description, parse_description_localizations, parse_key, parse_name, parse_name_localizations, parse_type,
    put_description_into, put_description_localizations_into, put_key_into, put_name_into, put_name_localizations_into,
    put_type_into, validate_description, validate_description_localizations, validate_key, validate_name,
    validate_name_localizations, validate_type
)
from .helpers import escape_name_to_key
from .preinstanced import ApplicationRoleConnectionMetadataType


class ApplicationRoleConnectionMetadata(RichAttributeErrorBaseType):
    """
    Role connection metadata of an application.
    
    If a bot's application has `.role_connection_verification_url` configured, then the application will show up as a
    verification method in the guild's settings.
    
    These metadatas will appear in the role verification configuration when the application has been linked to a role.
    
    When a user connects their account using the bot's `.role_connection_verification_url`, the bot will update the
    user's role connection with metadata using the oauth2 `role_connections.write` scope.
    
    Attributes
    ----------
    description : `None`, `str`
        The metadata's description.
    description_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized descriptions of the metadata.
    key : `str`
        The dictionary key for the metadata.
    name : `str`
        The name of the metadata.
    name_localizations : `None`, `dict` of (``Locale``, `str`) items
        Localized names of the metadata.
    type : ``ApplicationRoleConnectionMetadataType``
        The dictionary value's type and their respective operation.
    """
    __slots__ = ('description', 'description_localizations', 'key', 'name', 'name_localizations', 'type')
    
    def __new__(
        cls,
        name,
        metadata_type, 
        *,
        description = ...,
        description_localizations = ...,
        key = ...,
        name_localizations = ...,
    ):
        """
        Creates a new role connection metadata.
        
        Parameters
        ----------
        name : `str`
            The name of the metadata.
        
        metadata_type : `int`, ``ApplicationRoleConnectionMetadataType``
            The dictionary value's type and their respective operation.
        
        description : `None`, `str`, Optional (Keyword only)
            The metadata's description.
        
        description_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items, Optional (Keyword only)
            Localized descriptions of the metadata.
        
        key : `str`, Optional (Keyword only)
            The dictionary key for the metadata.
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items, Optional (Keyword only)
            Localized names of the metadata.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # Required: name & metadata_type
        name = validate_name(name)
        metadata_type = validate_type(metadata_type)
        
        # description
        if description is ...:
            description = name
        else:
            description = validate_description(description)
        
        # description_localizations
        if description_localizations is ...:
            description_localizations = None
        else:
            description_localizations = validate_description_localizations(description_localizations)
        
        # key
        if key is ...:
            key = escape_name_to_key(name)
        else:
            key = validate_key(key)

        # name_localizations
        if name_localizations is ...:
            name_localizations = None
        else:
            name_localizations = validate_name_localizations(name_localizations)
        
        self = object.__new__(cls)
        self.description = description
        self.description_localizations = description_localizations
        self.key = key
        self.name = name
        self.name_localizations = name_localizations
        self.type = metadata_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a role connection metadata from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Role connection data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.description = parse_description(data)
        self.description_localizations = parse_description_localizations(data)
        self.key = parse_key(data)
        self.name = parse_name(data)
        self.name_localizations = parse_name_localizations(data)
        self.type = parse_type(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the role connection metadata to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_description_into(self.description, data, defaults)
        put_description_localizations_into(self.description_localizations, data, defaults)
        put_key_into(self.key, data, defaults)
        put_name_into(self.name, data, defaults)
        put_name_localizations_into(self.name_localizations, data, defaults)
        put_type_into(self.type, data, defaults)
        return data
    
    
    def __hash__(self):
        """Returns the role connection metadata's hash value."""
        hash_value = 0
        
        # description
        description = self.description
        if (description is not None) and (description != self.name):
            hash_value ^= hash(description)
        
        # description_localizations
        description_localizations = self.description_localizations
        if (description_localizations is not None):
            hash_value ^= hash_locale_dictionary(description_localizations)
        
        # key
        key = self.key
        if (key != self.key):
            hash_value ^= hash(key)
        
        # name
        hash_value ^= hash(self.name)
        
        # name_localizations
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            hash_value ^= hash_locale_dictionary(name_localizations)
        
        # type
        hash_value ^= self.type.value
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the role connection metadata's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        metadata_type = self.type
        repr_parts.append(', type = ')
        repr_parts.append(str(metadata_type.name))
        repr_parts.append('~')
        repr_parts.append(repr(metadata_type.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # description
        if self.description != other.description:
            return False
        
        # description_localizations
        if self.description_localizations != other.description_localizations:
            return False
        
        # key
        if self.key != other.key:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # name_localizations
        if self.name_localizations != other.name_localizations:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the role connection metadata.
        
        Returns
        -------
        new : `instance<type<cls>>`
        """
        new = object.__new__(type(self))
        new.description = self.description
        description_localizations = self.description_localizations
        if (description_localizations is not None):
            description_localizations = description_localizations.copy()
        new.description_localizations = description_localizations
        new.key = self.key
        new.name = self.name
        name_localizations = self.name_localizations
        if (name_localizations is not None):
            name_localizations = name_localizations.copy()
        new.name_localizations = name_localizations
        new.type = self.type
        return new
    
    
    def copy_with(
        self,
        *,
        description = ...,
        description_localizations = ...,
        key = ...,
        metadata_type = ...,
        name = ...,
        name_localizations = ...,
    ):
        """
        Copies the role connection metadata with the given fields.
        
        Parameters
        ----------
        description : `None`, `str`, Optional (Keyword only)
            The metadata's description.
        
        description_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items, Optional (Keyword only)
            Localized descriptions of the metadata.
        
        key : `str`, Optional (Keyword only)
            The dictionary key for the metadata.
        
        metadata_type : `int`, ``ApplicationRoleConnectionMetadataType``, Optional (Keyword only)
            The dictionary value's type and their respective operation.
        
        name : `str`, Optional (Keyword only)
            The name of the metadata.
        
        name_localizations : `None`, `dict` of ((`str`, ``Locale``), `str`) items, Optional (Keyword only)
            Localized names of the metadata.
        
        Returns
        -------
        new : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # description_localizations
        if description_localizations is ...:
            description_localizations = self.description_localizations
            if (description_localizations is not None):
                 description_localizations = description_localizations.copy()
        else:
            description_localizations = validate_description_localizations(description_localizations)
        
        # key
        if key is ...:
            key = self.key
        else:
            key = validate_key(key)
        
        # metadata_type
        if metadata_type is ...:
            metadata_type = self.type
        else:
            metadata_type = validate_type(metadata_type)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # name_localizations
        if name_localizations is ...:
            name_localizations = self.name_localizations
            if (name_localizations is not None):
                 name_localizations = name_localizations.copy()
        else:
            name_localizations = validate_name_localizations(name_localizations)
        
        
        new = object.__new__(type(self))
        new.description = description
        new.description_localizations = description_localizations
        new.key = key
        new.name = name
        new.name_localizations = name_localizations
        new.type = metadata_type
        return new
