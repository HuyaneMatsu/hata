__all__ = ('EmbeddedActivityUserState',)

from scarletio import RichAttributeErrorBaseType

from ...user import ZEROUSER

from .fields import (
    parse_nonce, parse_session_id, parse_user, put_nonce_into, put_session_id_into, put_user_into, validate_nonce,
    validate_session_id, validate_user
)


class EmbeddedActivityUserState(RichAttributeErrorBaseType):
    """
    A user's state in an embedded activity.
    
    Attributes
    ----------
    nonce : `None | str`
        Can be used to identify the state on creation.
    
    session_id : `str`
        The state's session's identifier.
    
    user : ``ClientUserBase``
        The represented user.
    """
    __slots__ = ('nonce', 'session_id', 'user')
    
    def __new__(cls, *, nonce = ..., session_id = ..., user = ...):
        """
        Creates a new embedded user state instance.
        
        Parameters
        ----------
        nonce : `None | str`, Optional (Keyword only)
            Can be used to identify the state on creation.
        
        session_id : `None | str`, Optional (Keyword only)
            The state's session's identifier.
        
        user : `None | ClientUserBase`, Optional (Keyword only)
            The represented user.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - if a parameter's value is incorrect.
        """
        # nonce
        if nonce is ...:
            nonce = None
        else:
            nonce = validate_nonce(nonce)
        
        # session_id
        if session_id is ...:
            session_id = ''
        else:
            session_id = validate_session_id(session_id)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        # Construct
        self = object.__new__(cls)
        self.nonce = nonce
        self.session_id = session_id
        self.user = user
        return self
    
    
    def __repr__(self):
        """Returns the embedded activity user state's representation"""
        repr_parts = ['<', type(self).__name__]
        
        # user
        repr_parts.append(' user = ')
        repr_parts.append(repr(self.user))
        
        # session_id
        repr_parts.append(', session_id = ')
        repr_parts.append(repr(self.session_id))
        
        # nonce
        nonce = self.nonce
        if (nonce is not None):
            repr_parts.append(', nonce = ')
            repr_parts.append(repr(nonce))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the embedded activity user state's hash value"""
        hash_value = 0
        
        # nonce
        nonce = self.nonce
        if (nonce is not None):
            hash_value ^= hash(nonce)
        
        # session_id
        hash_value ^= hash(self.session_id)
        
        # user
        hash_value ^= hash(self.user)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two embedded activity user state's are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # nonce
        if self.nonce != other.nonce:
            return False
        
        # session_id
        if self.session_id != other.session_id:
            return False
        
        # user
        if self.user is not other.user:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates a new embedded activity user state from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to create instance from.
        
        guild_id : `int` = `0`
            The respective guild's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.nonce = parse_nonce(data)
        self.session_id = parse_session_id(data)
        self.user = parse_user(data, guild_id)
        return self
    
    
    def to_data(self, *, defaults = False, guild_id = 0):
        """
        Serialises the embedded activity user state.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        guild_id : `int` = `0`, Optional (Keyword only)
            The respective guild's identifier.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_nonce_into(self.nonce, data, defaults)
        put_session_id_into(self.session_id, data, defaults)
        put_user_into(self.user, data, defaults, guild_id = guild_id)
        return data
    
    
    def copy(self):
        """
        Copies the embedded activity user state.
        
        Returns
        -------
        new : `instance<type<cls>>`
        """
        new = object.__new__(type(self))
        new.nonce = self.nonce
        new.session_id = self.session_id
        new.user = self.user
        return new
        
    
    def copy_with(self, *, nonce = ..., session_id = ..., user = ...):
        """
        Copies the embedded activity user state with the given fields.
        
        Parameters
        ----------
        nonce : `None | str`, Optional (Keyword only)
            Can be used to identify the state on creation.
        
        session_id : `None | str`, Optional (Keyword only)
            The state's session's identifier.
        
        user : `None | ClientUserBase`, Optional (Keyword only)
            The represented user.
        
        Returns
        -------
        new : `instance<type<cls>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - if a parameter's value is incorrect.
        """
        # nonce
        if nonce is ...:
            nonce = self.nonce
        else:
            nonce = validate_nonce(nonce)
        
        # session_id
        if session_id is ...:
            session_id = self.session_id
        else:
            session_id = validate_session_id(session_id)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        # Construct
        new = object.__new__(type(self))
        new.nonce = nonce
        new.session_id = session_id
        new.user = user
        return new
    
    
    @property
    def user_id(self):
        """
        Returns the represented user's identifier.
        
        Returns
        -------
        user_id : `int`
        """
        return self.user.id
