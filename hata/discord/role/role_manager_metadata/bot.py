__all__ = ('RoleManagerMetadataBot',)

from scarletio import copy_docs

from ...user import User, ZEROUSER

from .base import RoleManagerMetadataBase
from .fields import parse_bot_id, put_bot_id_into, validate_bot_id


class RoleManagerMetadataBot(RoleManagerMetadataBase):
    """
    Role manager metadata of a role managed by a bot.
    
    Attributes
    ----------
    bot_id : `int`
        The manager bot's identifier.
    """
    __slots__ = ('bot_id', )
    
    def __new__(cls, *, bot_id = ...):
        """
        Creates a new role manager.
        
        Parameters
        ----------
        bot_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The manager bot's identifier.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # bot_id
        if bot_id is ...:
            bot_id = 0
        else:
            bot_id = validate_bot_id(bot_id)
        
        self = object.__new__(cls)
        self.bot_id = bot_id
        return self
    
    
    @classmethod
    @copy_docs(RoleManagerMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.bot_id = parse_bot_id(data)
        return self
    
    
    @copy_docs(RoleManagerMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_bot_id_into(self.bot_id, data, defaults)
        return data
    
    
    @copy_docs(RoleManagerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' bot_id = ')
        repr_parts.append(repr(self.bot_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(RoleManagerMetadataBase.__hash__)
    def __hash__(self):
        return self.bot_id
    
    
    @copy_docs(RoleManagerMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.bot_id == other.bot_id
    
    
    @copy_docs(RoleManagerMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.bot_id = self.bot_id
        return new
    
    
    def copy_with(self, *, bot_id = ...):
        """
        Copies the role manager metadata with the given fields.
        
        Parameters
        ----------
        bot_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The manager bot's identifier.
        
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
        # bot_id
        if bot_id is ...:
            bot_id = self.bot_id
        else:
            bot_id = validate_bot_id(bot_id)
        
        new = object.__new__(type(self))
        new.bot_id = bot_id
        return new
    
    
    @property
    @copy_docs(RoleManagerMetadataBase.manager_id)
    def manager_id(self):
        return self.bot_id
    
    
    @property
    @copy_docs(RoleManagerMetadataBase.manager)
    def manager(self):
        bot_id = self.bot_id
        if bot_id:
            return User.precreate(self.manager_id, bot = True)
        
        return ZEROUSER
