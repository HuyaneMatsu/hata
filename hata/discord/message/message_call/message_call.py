__all__ = ('MessageCall', )

from scarletio import RichAttributeErrorBaseType

from ...user import create_partial_user_from_id
from ...utils import DATETIME_FORMAT_CODE
from .fields import (
    parse_ended_at, parse_user_ids, put_ended_at_into, put_user_ids_into, validate_ended_at, validate_user_ids
)


class MessageCall(RichAttributeErrorBaseType):
    """
    Contained by messages with message type `call`.
    
    Attributes
    ----------
    ended_at : `None`, `datetime`
        When the call ended. Set as `None` if it is still ongoing.
    user_ids : `None`, `tuple` of `int`
        The users' identifiers participating the call.
    """
    __slots__ = ('ended_at', 'user_ids',)
    
    def __new__(cls, *, ended_at = ..., user_ids = ...):
        """
        Creates a new message call from the given parameters.
        
        Parameters
        ----------
        ended_at : `None`, `datetime`, Optional (Keyword only)
            When the call ended.
        user_ids : `None`, `iterable` of (`ClientUserBase`, `int`), Optional (Keyword only)
            The users' identifiers participating the call.
        
        Raises
        ------
        TypeError
            - If a parameter's user_ids is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # ended_at
        if ended_at is ...:
            ended_at = None
        else:
            ended_at = validate_ended_at(ended_at)
        
        # user_ids
        if user_ids is ...:
            user_ids = None
        else:
            user_ids = validate_user_ids(user_ids)
        
        # Construct
        self = object.__new__(cls)
        self.ended_at = ended_at
        self.user_ids = user_ids
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message call instance instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Message call data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.ended_at = parse_ended_at(data)
        self.user_ids = parse_user_ids(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the message call back to json a serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`)
        """
        data = {}
        put_ended_at_into(self.ended_at, data, defaults)
        put_user_ids_into(self.user_ids, data, defaults)
        return data
    
    
    def __eq__(self, other):
        """Returns whether the two message calls are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # ended_at
        if self.ended_at != other.ended_at:
            return False
        
        # user_ids
        if self.user_ids != other.user_ids:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the message call's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        user_ids = self.user_ids
        repr_parts.append(' user_ids = [')
        
        if (user_ids is not None):
            index = 0
            length = len(user_ids)
            
            while True:
                user_id = user_ids[index]
                repr_parts.append(repr(user_id))
                index += 1
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']')
        
        ended_at = self.ended_at
        if (ended_at is not None):
            repr_parts.append(', ended_at = ')
            repr_parts.append(format(ended_at, DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the message call's hash value."""
        hash_value = 0
        
        # ended_at
        ended_at = self.ended_at
        if (ended_at is not None):
            hash_value ^= hash(ended_at)
        
        # user_ids
        user_ids = self.user_ids
        if (user_ids is not None):
            hash_value ^= len(user_ids)
            
            for user_id in user_ids:
                hash_value ^= user_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the message call.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.ended_at = self.ended_at
        
        user_ids = self.user_ids
        if (user_ids is not None):
            user_ids = (*user_ids,)
        new.user_ids = user_ids
        
        return new
    
    
    def copy_with(self, *, user_ids = ..., ended_at = ...):
        """
        Copies the message call with the given fields.
        
        Parameters
        ----------
        ----------
        ended_at : `None`, `datetime`, Optional (Keyword only)
            When the call ended.
        user_ids : `None`, `iterable` of (`ClientUserBase`, `int`), Optional (Keyword only)
            The users' identifiers participating the call.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's user_ids is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # ended_at
        if ended_at is ...:
            ended_at = self.ended_at
        else:
            ended_at = validate_ended_at(ended_at)
        
        # user_ids
        if user_ids is ...:
            user_ids = self.user_ids
            if (user_ids is not None):
                user_ids = (*user_ids,)
        else:
            user_ids = validate_user_ids(user_ids)
        
        # Construct
        new = object.__new__(type(self))
        new.ended_at = ended_at
        new.user_ids = user_ids
        return new
    
    
    def iter_user_ids(self):
        """
        Iterates over the users' identifiers who participate (or participated) in the call.
        
        This method is an iterable generator.
        
        Yields
        ------
        user_id : `int`
        """
        user_ids = self.user_ids
        if (user_ids is not None):
            yield from user_ids
    
    
    def users(self):
        """
        Returns the users who participate (or participated) in the call.
        
        Returns
        -------
        users : `None`, `tuple` of ``ClientUserBase``
        """
        user_ids = self.user_ids
        if (user_ids is not None):
            return (*(create_partial_user_from_id(user_id) for user_id in user_ids),)
    
    
    def iter_users(self):
        """
        Iterates over the users who participate (or participated) in the call.
        
        This method is an iterable generator.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        user_ids = self.user_ids
        if (user_ids is not None):
            for user_id in user_ids:
                yield create_partial_user_from_id(user_id)
