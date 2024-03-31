__all__ = ('ApplicationIntegrationTypeConfiguration',)

from scarletio import RichAttributeErrorBaseType

from .fields import parse_install_parameters, put_install_parameters_into, validate_install_parameters


class ApplicationIntegrationTypeConfiguration(RichAttributeErrorBaseType):
    """
    Integration type specific configuration for installing the application.
    
    Attributes
    ----------
    install_parameters : `None`, ``ApplicationInstallParameters``
        Parameters to install the integration with.        
    """
    __slots__ = ('install_parameters', )
    
    def __new__(cls, *, install_parameters = ...):
        """
        Creates a new application integration type configuration.
        
        Parameters
        ----------
        install_parameters : `None`, ``ApplicationInstallParameters``, Optional (Keyword only)
            Parameters to install the integration with.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        if install_parameters is ...:
            install_parameters = None
        else:
            install_parameters = validate_install_parameters(install_parameters)
        
        self = object.__new__(cls)
        self.install_parameters = install_parameters
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a application integration type configuration instance from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Application installation parameters data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.install_parameters = parse_install_parameters(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the application integration type configuration to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_install_parameters_into(self.install_parameters, data, defaults)
        return data
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an integration type configuration with its default values set.
        
        Returns
        -------
        self : `instance<cls>
        """
        self = object.__new__(cls)
        self.install_parameters = None
        return self
    
    
    def __repr__(self):
        """Returns the application install parameters' representation."""
        repr_parts = ['<', type(self).__name__]
        
        install_parameters = self.install_parameters
        if (install_parameters is not None):
            repr_parts.append(', install_parameters = ')
            repr_parts.append(repr(install_parameters))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the application install parameters' hash value."""
        hash_value = 0
        
        # install_parameters
        install_parameters = self.install_parameters
        if (install_parameters is not None):
            hash_value ^= hash(install_parameters)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two application install parameters are equal."""
        if type(other) is not ApplicationIntegrationTypeConfiguration:
            return NotImplemented
        
        if self.install_parameters != other.install_parameters:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the application install parameters.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        install_parameters = self.install_parameters
        if (install_parameters is not None):
            install_parameters = install_parameters.copy()
        new.install_parameters = install_parameters
        
        return new

    
    def copy_with(self, install_parameters = ...):
        """
        Copies the application install parameters with the given fields.
        
        Parameters
        ----------
        install_parameters : `None`, ``ApplicationInstallParameters``, Optional (Keyword only)
            Parameters to install the integration with.
        
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
        if install_parameters is ...:
            install_parameters = self.install_parameters
        else:
            install_parameters = validate_install_parameters(install_parameters)
        
        new = object.__new__(type(self))
        new.install_parameters = install_parameters
        return new
