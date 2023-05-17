__all__ = ('GuildJoinRequestStatus',)

from ...bases import Preinstance as P, PreinstancedBase


class GuildJoinRequestStatus(PreinstancedBase):
    """
    Represents the status of a ``GuildJoinRequest``.
    
    Attributes
    ----------
    name : `str`
        The name of the guild join request status.
    value : `str`
        The Discord side identifier value of the guild join request status.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``GuildJoinRequestStatus``) items
        Stores the predefined ``GuildJoinRequestStatus``-s.
    VALUE_TYPE : `type` = `str`
        The guild join request statuses' values' type.
    DEFAULT_NAME : `str` = `''`
        The default name of the guild join request statuses. Guild join request statuses have their name generated from
        their value, so at their case it is not applicable.
    
    Every predefined guild join request status can be accessed as class attribute as well:
    
    +-----------------------+-----------+-----------+
    | Class attribute names | Name      | Value     |
    +=======================+===========+===========+
    | approved              | approved  | APPROVED  |
    +-----------------------+-----------+-----------+
    | pending               | pending   | PENDING   |
    +-----------------------+-----------+-----------+
    | rejected              | rejected  | REJECTED  |
    +-----------------------+-----------+-----------+
    | started               | started   | STARTED   |
    +-----------------------+-----------+-----------+
    """
    
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    
    __slots__ = ()
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new guild join request status from the given value.
        
        Parameters
        ----------
        value : `str`
            The guild join request status's identifier value.
        
        Returns
        -------
        self : ``GuildJoinRequestStatus``
            The guild join request status.
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value.lower().replace('_', ' ')
        self.INSTANCES[value] = self
        return self
    
    def __repr__(self):
        """Returns the representation of the guild join request status."""
        return f'{self.__class__.__name__}(value = {self.value!r})'
    
    approved = P('APPROVED', 'approved')
    pending = P('PENDING', 'pending')
    rejected = P('REJECTED', 'rejected')
    started = P('STARTED', 'started')

