__all__ = ('ApplicationEntity',)

from ...bases import DiscordEntity

from .fields import parse_id, parse_name, put_id_into, put_name_into, validate_id, validate_name


class ApplicationEntity(DiscordEntity):
    """
    An un-typed entity stored inside of an ``Application``, as one of it's `.developers`, `.publishers`.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the entity.
    name : `str`
        The name of the entity.
    """
    __slots__ = ('name', )
    
    
    def __new__(cls, *, name = ...):
        """
        Creates a new partial application entity.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The name of the entity.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        self = object.__new__(cls)
        self.id = 0
        self.name = name
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new application entity.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Developers or Publisher data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = parse_id(data)
        self.name = parse_name(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the application entity into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        put_name_into(self.name, data, defaults)
        
        return data
    
    
    @classmethod
    def _create_empty(cls, entity_id):
        """
        Creates a new application entity instance with it's attribute set to their default values.
        
        Parameters
        ----------
        entity_id : `int`
            The entity's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = entity_id
        self.name = ''
        return self
    

    @classmethod
    def precreate(cls, entity_id, **keyword_parameters):
        """
        Creates an application entity instance. Since these objects are not cached, the only advantage of using
        ``.precreate`` is that it allows setting ``.id``.
        
        Parameters
        ----------
        entity_id : `int`
            The entity's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The entity's name.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        entity_id = validate_id(entity_id)

        if keyword_parameters:
            processable = []
            
            try:
                name = keyword_parameters.pop('name')
            except KeyError:
                pass
            else:
                name = validate_name(name)
                processable.append(('name', name))
            
            if keyword_parameters:
                raise TypeError(
                    f'Unused or unsettable keyword parameters: {keyword_parameters!r}.'
                )
        
        else:
            processable = None
        
        
        self = cls._create_empty(entity_id)
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    def __repr__(self):
        """Returns the entity's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        entity_id = self.id
        if entity_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two application entities are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two application entities are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self.id != other.id:
                return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the application entity."""
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the application entity.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = 0
        new.name = self.name
        return new
    
    
    def copy_with(self, *, name = ...):
        """
        Copies the application entity with the defined fields.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The entity's name.
        
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
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        new = object.__new__(type(self))
        new.id = 0
        new.name = name
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether the entity is partial.
        
        Returns
        -------
        partial : `bool
        """
        return (self.id == 0)
