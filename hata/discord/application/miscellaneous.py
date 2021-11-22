__all__ = ('ApplicationExecutable', 'ApplicationInstallParameters', 'ApplicationSubEntity', 'EULA', 'ThirdPartySKU', )

from ..bases import DiscordEntity
from ..core import EULAS
from ..permission import Permission

class ApplicationSubEntity(DiscordEntity):
    """
    An un-typed entity stored inside of an ``Application``, as one of it's `.developers`, or `.publishers`.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the entity.
    name : `str`
        The name of the entity.
    """
    __slots__ = ('name', )
    
    def __init__(self, data):
        """
        Creates a new ``ApplicationSubEntity`` instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Developers or Publisher data.
        """
        self.id = int(data['id'])
        self.name = data['name']
    
    def __repr__(self):
        """Returns the entity's representation."""
        return f'<{self.__class__.__name__} {self.name!r}, id={self.id}>'
    
    def __eq__(self, other):
        """Returns whether the two entities equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.id != other.id:
            return False
        
        if self.name != other.name:
            return False
        
        return True


class ApplicationExecutable:
    """
    Represents a game's executable.
    
    Attributes
    ----------
    parameters : `None` or `str`
        The parameters to start the application with. Defaults to `None`.
    is_launcher : `bool`
        Whether the application is a launcher. Defaults to `False`.
    name : `str`
        The executable's name.
    os : `str`
        The operation system, the executable is for.
    """
    __slots__ = ('parameters', 'is_launcher', 'name', 'os')
    
    def __init__(self, data):
        """
        Creates a new application executable with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Executable data.
        """
        self.name = data['name']
        self.os = data['os']
        self.parameters = data.get('parameters', None)
        self.is_launcher = data.get('is_launcher', False)
    
    def __repr__(self):
        """Returns the executable's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' ',
            repr(self.name),
            ', os=',
            repr(self.os),
        ]
        
        parameters = self.parameters
        if (parameters is not None):
            repr_parts.append(', parameters=')
            repr_parts.append(repr(parameters))
        
        is_launcher = self.is_launcher
        if is_launcher:
            repr_parts.append(', is_launcher=True')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def __eq__(self, other):
        """Returns whether the two executables are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.os != other.os:
            return False
        
        if self.parameters != other.parameters:
            return False
        
        if self.is_launcher != other.is_launcher:
            return False
        
        return True
    
    def __hash__(self):
        """Returns the entity's hash."""
        result = hash(self.name) ^ hash(self.os)
        
        parameters = self.parameters
        if (parameters is not None):
            result ^= hash(parameters)
        
        if self.is_launcher:
            result ^= (1<<15)
        
        return result

class ThirdPartySKU:
    """
    Represents a third party Stock Keeping Unit.
    
    distributor : `str`
        The distributor of the SKU.
    id : `str`
        The identifier of the third party SKU.
    sku : `str`
        Might be same as `.id`.
    """
    __slots__ = ('distributor', 'id', 'sku',)
    
    def __init__(self, data):
        """
        creates a new third party SKU object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            SKU data.
        """
        self.distributor = data['distributor']
        self.id = data['id']
        self.sku = data['sku']
    
    def __repr__(self):
        """Returns the SKU's representation."""
        return f'<{self.__class__.__name__} distributor={self.distributor!r}, id={self.id!r}, sku={self.sku!r}>'
    
    def __eq__(self, other):
        """Returns whether the two SKU-s are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.distributor != other.distributor:
            return False
        
        if self.id != other.id:
            return False
        
        if self.sku != other.sku:
            return False
        
        return True
    
    def __hash__(self):
        """Returns the sku's hash."""
        result = hash(self.distributor)
        
        id_ = self.id
        result ^= hash(id_)
        
        sku = self.sku
        if sku != id_:
            result ^= hash(sku)
        
        return result

class EULA(DiscordEntity, immortal=True):
    """
    Represents a Discord end-user license agreement
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the eula.
    content : `str`
        The eula's content.
    name : `str`
        The eula's name.
    
    Notes
    -----
    The instances of the class support weakreferencing.
    """
    __slots__ = ('id', 'content', 'name')
    
    def __new__(cls, data):
        """
        Creates a new eula instance from the given data.
        
        If the eula already exists, returns that instead.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Eula data.
        """
        eula_id = int(data['id'])
        
        try:
            self = EULAS[eula_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = eula_id
            self._update_attributes(data)
            
            EULAS[eula_id] = self
        
        return self
    
    def _update_attributes(self, data):
        """
        Updates the eula with the received data from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        """
        self.content = data['content']
        self.name = data['name']
    
    def __repr__(self):
        """Returns the eula's representation"""
        return f'<{self.__class__.__name__} {self.name!r}, id={self.id}>'


class ApplicationInstallParameters:
    """
    Parameters for inviting a bot.
    
    Attributes
    ----------
    permissions : ``Permission``
        The permissions to invite the bot with.
    scopes : `None` or `tuple` of `str`
        Oauth2 scopes to invite the bot with.
    """
    __slots__ = ('permissions', 'scopes')
    
    def __new__(cls, data):
        """
        Creates a application installation parameters instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application installation parameters data.
        """
        self = object.__new__(cls)
        scopes = data.get('scopes', None)
        if (scopes is None) or (not scopes):
            scopes = tuple(sorted(scopes))
        else:
            scopes = None
        self.scopes = scopes
        
        self.permissions = Permission(data.get('permissions', 0))
        
        return self
    
    def __repr__(self):
        """Returns the application install parameters' representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' scopes=[')
        
        scopes = self.scopes
        if (scopes is not None):
            length = len(scopes)
            index = 0
            
            while True:
                scope = scopes[index]
                repr_parts.append(repr(scope))
                
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(', permissions=')
        repr_parts.append(format(self.permissions, 'd'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the application install parameters' hash value."""
        hash_value = 0
        
        scopes = self.scopes
        if (scopes is not None):
            hash_value ^= hash(scopes)
        
        hash_value ^ hash(self.permissions)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two application install parameters are equal."""
        if type(other) is not ApplicationInstallParameters:
            return NotImplemented
        
        if self.permissions != other.permissions:
            return False
        
        if self.scopes != other.scopes:
            return False
        
        return True
