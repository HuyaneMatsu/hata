__all__ = ('PollVoteAddEvent',)

from scarletio import copy_docs

from ...bases import EventBase
from ...user import create_partial_user_from_id

from .fields import (
    parse_answer_id, parse_message, parse_user_id, put_answer_id, put_message, put_user_id,
    validate_answer_id, validate_message, validate_user_id
)


class PollVoteAddEvent(EventBase):
    """
    Represents a processed `MESSAGE_POLL_VOTE_ADD` dispatch event.
    
    Attributes
    ----------
    answer_id : `int`
        The voted answer's identifier.
    message : ``Message``
        The message on what the vote is added.
    user_id : `int`
        The user's identifier who voted
    """
    __slots__ = ('answer_id', 'message', 'user_id')
    
    def __new__(cls, message, answer_id, user_id):
        """
        Creates a new vote add (or delete) instance.
        
        Parameters
        ----------
        message : ``Message``
            The respective message.
        answer_id : `int`
            The answer_id used.
        user_id : `int`
            The user_id who reacted.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # answer_id
        answer_id = validate_answer_id(answer_id)
        
        # message
        message = validate_message(message)
        
        # user_id
        user_id = validate_user_id(user_id)
        
        # Construct
        self = object.__new__(cls)
        self.answer_id = answer_id
        self.message = message
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new vote add (or delete) event instance.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Vote event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.answer_id = parse_answer_id(data)
        self.message = message = parse_message(data)
        self.user_id = parse_user_id(data)
        return self
    
    
    @classmethod
    def from_fields(cls, message, answer_id, user_id):
        """
        Creates a new vote add (or delete) instance.
        
        Parameters
        ----------
        message : ``Message``
            The respective message.
        answer_id : `int`
            The answer_id used.
        user_id : `int`
            The user_id who reacted.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.answer_id = answer_id
        self.message = message
        self.user_id = user_id
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the vote add (or delete) event into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_answer_id(self.answer_id, data, defaults)
        put_message(self.message, data, defaults)
        put_user_id(self.user_id, data, defaults)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' message = ')
        repr_parts.append(repr(self.message))
        
        repr_parts.append(', answer_id = ')
        repr_parts.append(repr(self.answer_id))
        
        repr_parts.append(', user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.message
        yield self.answer_id
        yield self.user_id
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.answer_id != other.answer_id:
            return False
        
        if self.message is not other.message:
            return False
        
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # answer_id
        hash_value ^= self.answer_id
        
        # message
        hash_value ^= hash(self.message)
        
        # user_id
        hash_value ^= self.user_id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the vote add (or remove) event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.answer_id = self.answer_id
        new.message = self.message
        new.user_id = self.user_id
        return new
    
    
    def copy_with(self, *, answer_id = ..., message = ..., user_id = ...):
        """
        Copies the vote add (or remove) event with the given fields.
        
        Parameters
        ----------
        answer_id : `int`, Optional (Keyword only)
            The answer_id used.
        message : ``Message``, Optional (Keyword only)
            The respective message.
        user_id : `int`, Optional (Keyword only)
            The user_id who reacted.
        
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
        # answer_id
        if answer_id is ...:
            answer_id = self.answer_id
        else:
            answer_id = validate_answer_id(answer_id)
        
        # message
        if message is ...:
            message = self.message
        else:
            message = validate_message(message)
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        new = object.__new__(type(self))
        new.answer_id = answer_id
        new.message = message
        new.user_id = user_id
        return new
    
    
    @property
    def user(self):
        """
        Returns the user who voted (removed their vote).
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)
