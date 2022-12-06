__all__ = ('ApplicationRoleConnection',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_metadata_values, parse_platform_name, parse_platform_user_name, put_metadata_values_into,
    put_platform_name_into, put_platform_user_name_into, validate_metadata_values, validate_platform_name,
    validate_platform_user_name
)


class ApplicationRoleConnection(RichAttributeErrorBaseType):
    """
    Application role connection attached to a user.
    
    Attributes
    ----------
    platform_name : `None`, `str`
        The vanity name of the platform the application represents.
    platform_user_name : `None`, `str`
        The name of the user on the application's platform.
    metadata_values : `None`, `dict` of (`str`, `str`) items
        Metadata key to attached value relation.
    """
    __slots__ = ('platform_name', 'platform_user_name', 'metadata_values')
    
    def __new__(cls, *, platform_name = ..., platform_user_name = ..., metadata_values = ...):
        """
        Creates a new application role connection.
        
        Parameters
        ----------
        platform_name : `None`, `str`, Optional (Keyword only)
            The vanity name of the platform the application represents.
        platform_user_name : `None`, `str`, Optional (Keyword only)
            The name of the user on the application's platform.
        metadata_values : `None`, `dict` of (`str`, `str`) items, Optional (Keyword only)
            Metadata key to attached value relation.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # platform_name
        if platform_name is ...:
            platform_name = None
        else:
            platform_name = validate_platform_name(platform_name)
        
        # platform_user_name
        if platform_user_name is ...:
            platform_user_name = None
        else:
            platform_user_name = validate_platform_user_name(platform_user_name)
        
        # metadata_values
        if metadata_values is ...:
            metadata_values = None
        else:
            metadata_values = validate_metadata_values(metadata_values)
        
        self = object.__new__(cls)
        self.platform_name = platform_name
        self.platform_user_name = platform_user_name
        self.metadata_values = metadata_values
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an application role connection from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Role connection data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.platform_name = parse_platform_name(data)
        self.platform_user_name = parse_platform_user_name(data)
        self.metadata_values = parse_metadata_values(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the application role connection to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_platform_name_into(self.platform_name, data, defaults)
        put_platform_user_name_into(self.platform_user_name, data, defaults)
        put_metadata_values_into(self.metadata_values, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the role connection's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        platform_name = self.platform_name
        if (platform_name is not None):
            if field_added:
                repr_parts.append(', ')
            else:
                field_added = True
            repr_parts.append(' platform_name = ')
            repr_parts.append(repr(platform_name))
        
        platform_user_name = self.platform_user_name
        if (platform_user_name is not None):
            if field_added:
                repr_parts.append(', ')
            else:
                field_added = True
            repr_parts.append(' platform_user_name = ')
            repr_parts.append(repr(platform_user_name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the hash value of the role connection."""
        hash_value = 0
        
        # platform_name
        platform_name = self.platform_name
        if (platform_name is not None):
            hash_value ^= hash(platform_name)
        
        # platform_user_name
        platform_user_name = self.platform_user_name
        if (platform_user_name is not None):
            hash_value ^= hash(platform_user_name)
        
        # metadata_values
        metadata_values = self.metadata_values
        if (metadata_values is not None):
            hash_value ^= len(metadata_values)
            
            for field_name, field_value in metadata_values.items():
                hash_value ^= hash(field_name) ^ hash(field_value)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two role connections are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # platform_name
        if self.platform_name != other.platform_name:
            return False
        
        # platform_user_name
        if self.platform_user_name != other.platform_user_name:
            return False
        
        # metadata_values
        if self.metadata_values != other.metadata_values:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the application role connection.
        
        Returns
        -------
        new : `instance<type<cls>>`
        """
        new = object.__new__(type(self))
        new.platform_name = self.platform_name
        new.platform_user_name = self.platform_user_name
        metadata_values = self.metadata_values
        if (metadata_values is not None):
            metadata_values = metadata_values.copy()
        new.metadata_values = metadata_values
        return new
    
    
    def copy_with(self, *, platform_name = ..., platform_user_name = ..., metadata_values = ...):
        
        """
        Copies the application role connection with the given fields.
        
        Parameters
        ----------
        platform_name : `None`, `str`, Optional (Keyword only)
            The vanity name of the platform the application represents.
        platform_user_name : `None`, `str`, Optional (Keyword only)
            The name of the user on the application's platform.
        metadata_values : `None`, `dict` of (`str`, `str`) items, Optional (Keyword only)
            Metadata key to attached value relation.
        
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
        # platform_name
        if platform_name is ...:
            platform_name = self.platform_name
        else:
            platform_name = validate_platform_name(platform_name)
        
        # platform_user_name
        if platform_user_name is ...:
            platform_user_name = self.platform_user_name
        else:
            platform_user_name = validate_platform_user_name(platform_user_name)
        
        # metadata_values
        if metadata_values is ...:
            metadata_values = self.metadata_values
            if (metadata_values is not None):
                metadata_values = metadata_values.copy()
        else:
            metadata_values = validate_metadata_values(metadata_values)
        
        new = object.__new__(type(self))
        new.platform_name = platform_name
        new.platform_user_name = platform_user_name
        new.metadata_values = metadata_values
        return new
    
    
    def translate_value(self, metadata):
        """
        Translates the given metadata's respective value ``.metadata_values`` to their type-correct representation.
        Returns `None` on failure.
        
        Parameters
        ----------
        metadata : ``ApplicationRoleConnectionMetadata``
            Application role connection metadata to translate with.
        
        Returns
        -------
        translated_value : `None`, `object`
        """
        metadata_values = self.metadata_values
        if (metadata_values is None):
            return
        
        try:
            raw_value = metadata_values[metadata.key]
        except KeyError:
            return
        
        return metadata.type.value_type.deserializer(raw_value)
    
    
    def translate_values(self, metadatas):
        """
        Translates the ``.metadata_values`` of the role connection to their type-correct representation.
        
        Parameters
        ----------
        metadatas : `iterable` of ``ApplicationRoleConnectionMetadata``
            Application role connection metadatas to translate with.
        
        Returns
        -------
        translated_values : `dict` of (``ApplicationRoleConnectionMetadata``, `object`) items
        """
        translated_values = {}
        
        metadata_values = self.metadata_values
        if (metadata_values is not None):
            for metadata in metadatas:
                try:
                    raw_value = metadata_values[metadata.key]
                except KeyError:
                    continue
                
                converted_value = metadata.type.value_type.deserializer(raw_value)
                if (converted_value is not None):
                    translated_values[metadata] = converted_value
        
        return translated_values
