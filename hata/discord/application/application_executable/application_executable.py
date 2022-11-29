__all__ = ('ApplicationExecutable',)

import warnings

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_launcher, parse_name, parse_os, parse_parameters, put_launcher_into, put_name_into, put_os_into,
    put_parameters_into, validate_launcher, validate_name, validate_os, validate_parameters
)
from .preinstanced import OperationSystem


class ApplicationExecutable(RichAttributeErrorBaseType):
    """
    Represents a game's executable.
    
    Attributes
    ----------
    launcher : `bool`
        Whether the application is a launcher. Defaults to `False`.
    name : `str`
        The executable's name.
    os : ``OperationSystem``
        The operation system, the executable is for.
    parameters : `None`, `str`
        The parameters to start the application with. Defaults to `None`.
    """
    __slots__ = ('launcher', 'name', 'os', 'parameters')
    
    def __new__(cls, *, launcher = ..., name = ..., os = ..., parameters = ...):
        """
        Creates an application executable.
        
        Parameters
        ----------
        launcher : `bool`, Optional (Keyword only)
            Whether the application is a launcher.
        
        name : `str`, Optional (Keyword only)
            The executable's name.
        
        os : ``OperationSystem``, `str`, Optional (Keyword only)
            The operation system, the executable is for.
        
        parameters : `None`, `str`, Optional (Keyword only)
            The parameters to start the application with.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # launcher
        if launcher is ...:
            launcher = False
        else:
            launcher = validate_launcher(launcher)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # os
        if os is ...:
            os = OperationSystem.none
        else:
            os = validate_os(os)
        
        # parameters
        if parameters is ...:
            parameters = None
        else:
            parameters = validate_parameters(parameters)
        
        self = object.__new__(cls)
        self.launcher = launcher
        self.name = name
        self.os = os
        self.parameters = parameters
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new application executable with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Executable data.
        """
        self = object.__new__(cls)
        self.launcher = parse_launcher(data)
        self.name = parse_name(data)
        self.os = parse_os(data)
        self.parameters = parse_parameters(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the application executable to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        put_launcher_into(self.launcher, data, defaults)
        put_name_into(self.name, data, defaults)
        put_os_into(self.os, data, defaults)
        put_parameters_into(self.parameters, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the executable's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' ',
            repr(self.name),
        ]
        
        repr_parts.append(', os = ')
        repr_parts.append(repr(self.os))
        
        parameters = self.parameters
        if (parameters is not None):
            repr_parts.append(', parameters = ')
            repr_parts.append(repr(parameters))
        
        if self.launcher:
            repr_parts.append(', launcher = True')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two executables are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # launcher
        if self.launcher != other.launcher:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # os
        if self.os is not other.os:
            return False
        
        # parameters
        if self.parameters != other.parameters:
            return False
        
        return True
    
    
    def __gt__(self, other):
        """Returns whether self is greater than other executable."""
        if type(self) is not type(other):
            return NotImplemented
        
        # name
        self_name = self.name
        other_name = other.name
        if self_name > other_name:
            return True
        
        if self_name < other_name:
            return False
        
        # os
        self_os = self.os
        other_os = other.os
        if self_os > other_os:
            return True
        
        if self_os < other_os:
            return False
        
        # launcher
        self_launcher = self.launcher
        other_launcher = other.launcher
        if self_launcher > other_launcher:
            return True
        
        if self_launcher < other_launcher:
            return False
        
        # parameters
        self_parameters = self.parameters
        other_parameters = other.parameters
        
        if self_parameters is None:
            if (other_parameters is not None):
                return False
        
        else:
            if other_parameters is None:
                return True
            
            if self_parameters > other_parameters:
                return True
        
        return False
    
    
    def __hash__(self):
        """Returns the executable's hash."""
        hash_value = 0
        
        # launcher
        if self.launcher:
            hash_value ^= (1 << 15)
        
        # name
        hash_value ^= hash(self.name)
        
        # os
        hash_value ^= hash(self.os)
        
        # parameters
        parameters = self.parameters
        if (parameters is not None):
            hash_value ^= hash(parameters)
        
        return hash_value
    
    
    @property
    def is_launcher(self):
        """
        Deprecated and will be removed in 2023 Marc. Please use ``.launcher`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_launcher` is deprecated and will be removed in 2023 Marc. '
                f'Please use `.launcher` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.launcher
    
    
    def copy(self):
        """
        Copies the application executable.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.launcher = self.launcher
        new.name = self.name
        new.os = self.os
        new.parameters = self.parameters
        return new
    
    
    def copy_with(self, *, launcher = ..., name = ..., os = ..., parameters = ...):
        """
        Copies the application executable with the given fields.
        
        Parameters
        ----------
        launcher : `bool`, Optional (Keyword only)
            Whether the application is a launcher.
        
        name : `str`, Optional (Keyword only)
            The executable's name.
        
        os : ``OperationSystem``, `str`, Optional (Keyword only)
            The operation system, the executable is for.
        
        parameters : `None`, `str`, Optional (Keyword only)
            The parameters to start the application with.
        
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
        # launcher
        if launcher is ...:
            launcher = self.launcher
        else:
            launcher = validate_launcher(launcher)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # os
        if os is ...:
            os = self.os
        else:
            os = validate_os(os)
        
        # parameters
        if parameters is ...:
            parameters = self.parameters
        else:
            parameters = validate_parameters(parameters)
        
        new = object.__new__(type(self))
        new.launcher = launcher
        new.name = name
        new.os = os
        new.parameters = parameters
        return new
