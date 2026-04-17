__all__ = ('InviteAllowedUserIdsStatus',)

from scarletio import RichAttributeErrorBaseType

from ...utils import DATETIME_FORMAT_CODE

from .fields import (
    parse_completed_at, parse_error_message, parse_processed, parse_started_at, parse_status, parse_total,
    put_completed_at, put_error_message, put_processed, put_started_at, put_status, put_total, validate_completed_at,
    validate_error_message, validate_processed, validate_started_at, validate_status, validate_total
)
from .preinstanced import InviteAllowedUserIdsStatusStatus


class InviteAllowedUserIdsStatus(RichAttributeErrorBaseType):
    """
    Represents the status of how allowed user ids processing.
    
    Attributes
    ----------
    completed_at : `None | Datetime`
        When the processing was completed.
    
    error_message : `None | str`
        Error message if processing failed.
    
    processed : `int`
        The amount of users processed.
    
    started_at : `None | DateTime`
        When the processing was started.
    
    status : ``InviteAllowedUserIdsStatusStatus``
        Processing status.
    
    total : `int`
        The total amount of users to process.
    """
    __slots__ = ('completed_at', 'error_message', 'processed', 'started_at', 'status', 'total')
    
    def __new__(
        cls,
        completed_at = ...,
        error_message = ...,
        processed = ...,
        started_at = ...,
        status = ...,
        total = ...,
    ):
        """
        Creates a new instance.
        
        Parameters
        ----------
        completed_at : `None | Datetime`, Optional (Keyword only)
            When the processing was completed.
        
        error_message : `None | str`, Optional (Keyword only)
            Error message if processing failed.
        
        processed : `None | int`, Optional (Keyword only)
            The amount of users processed.
        
        started_at : `None | DateTime`, Optional (Keyword only)
            When the processing was started.
        
        status : ``None | int | InviteAllowedUserIdsStatusStatus``, Optional (Keyword only)
            Processing status.
        
        total : `None | int`, Optional (Keyword only)
            The total amount of users to process.
        
        Raises
        ------
        TypeError
            . If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # completed_at
        if completed_at is ...:
            completed_at = None
        else:
            completed_at = validate_completed_at(completed_at)
        
        # error_message
        if error_message is ...:
            error_message = None
        else:
            error_message = validate_error_message(error_message)
        
        # processed
        if processed is ...:
            processed = 0
        else:
            processed = validate_processed(processed)
        
        # started_at
        if started_at is ...:
            started_at = None
        else:
            started_at = validate_started_at(started_at)
        
        # status
        if status is ...:
            status = InviteAllowedUserIdsStatusStatus.none
        else:
            status = validate_status(status)
        
        # total
        if total is ...:
            total = 0
        else:
            total = validate_total(total)
        
        # Construct
        self = object.__new__(cls)
        self.completed_at = completed_at
        self.error_message = error_message
        self.processed = processed
        self.started_at = started_at
        self.status = status
        self.total = total
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # status
        status = self.status
        repr_parts.append(', status = ')
        repr_parts.append(status.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(status.value))
        
        # processed
        repr_parts.append(', processed = ')
        repr_parts.append(repr(self.processed))
        
        # total
        repr_parts.append(', total = ')
        repr_parts.append(repr(self.total))
        
        # completed_at
        completed_at = self.completed_at
        if (completed_at is not None):
            repr_parts.append(', completed_at = ')
            repr_parts.append(format(completed_at, DATETIME_FORMAT_CODE))
        
        # started_at
        started_at = self.started_at
        if (started_at is not None):
            repr_parts.append(', started_at = ')
            repr_parts.append(repr(started_at))
        
        # error_message
        error_message = self.error_message
        if (error_message is not None):
            repr_parts.append(', error_message = ')
            repr_parts.append(repr(error_message))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # completed_at
        completed_at = self.completed_at
        if (completed_at is not None):
            hash_value ^= (1 << 5)
            hash_value ^= hash(completed_at)
        
        # error_message
        error_message = self.error_message
        if (error_message is not None):
            hash_value ^= (1 << 8)
            hash_value ^= hash(error_message)
        
        # processed
        hash_value ^= self.processed << 16
        
        # started_at
        started_at = self.started_at
        if (started_at is not None):
            hash_value ^= (1 << 7)
            hash_value ^= hash(started_at)
        
        # status
        hash_value ^= hash(self.status)
        
        # total
        hash_value ^= self.total << 24
        
        return hash_value
    
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # completed_at
        if self.completed_at != other.completed_at:
            return False
        
        # error_message
        if self.error_message != other.error_message:
            return False
        
        # processed
        if self.processed != other.processed:
            return False
        
        # started_at
        if self.started_at != other.started_at:
            return False
        
        # status
        if self.status is not other.status:
            return False
        
        # total
        if self.total != other.total:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new instance from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to create instance from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.completed_at = parse_completed_at(data)
        self.error_message = parse_error_message(data)
        self.processed = parse_processed(data)
        self.started_at = parse_started_at(data)
        self.status = parse_status(data)
        self.total = parse_total(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serialises self.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_completed_at(self.completed_at, data, defaults)
        put_error_message(self.error_message, data, defaults)
        put_processed(self.processed, data, defaults)
        put_started_at(self.started_at, data, defaults)
        put_status(self.status, data, defaults)
        put_total(self.total, data, defaults)
        return data
    
    
    def copy(self):
        """
        Copies self.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.completed_at = self.completed_at
        new.error_message = self.error_message
        new.processed = self.processed
        new.started_at = self.started_at
        new.status = self.status
        new.total = self.total
        return new
    
    
    def copy_with(
        self,
        completed_at = ...,
        error_message = ...,
        processed = ...,
        started_at = ...,
        status = ...,
        total = ...,
    ):
        """
        Copies self with the given fields.
        
        Parameters
        ----------
        completed_at : `None | Datetime`, Optional (Keyword only)
            When the processing was completed.
        
        error_message : `None | str`, Optional (Keyword only)
            Error message if processing failed.
        
        processed : `None | int`, Optional (Keyword only)
            The amount of users processed.
        
        started_at : `None | DateTime`, Optional (Keyword only)
            When the processing was started.
        
        status : ``None | int | InviteAllowedUserIdsStatusStatus``, Optional (Keyword only)
            Processing status.
        
        total : `None | int`, Optional (Keyword only)
            The total amount of users to process.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            . If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        """
        # completed_at
        if completed_at is ...:
            completed_at = self.completed_at
        else:
            completed_at = validate_completed_at(completed_at)
        
        # error_message
        if error_message is ...:
            error_message = self.error_message
        else:
            error_message = validate_error_message(error_message)
        
        # processed
        if processed is ...:
            processed = self.processed
        else:
            processed = validate_processed(processed)
        
        # started_at
        if started_at is ...:
            started_at = self.started_at
        else:
            started_at = validate_started_at(started_at)
        
        # status
        if status is ...:
            status = self.status
        else:
            status = validate_status(status)
        
        # total
        if total is ...:
            total = self.total
        else:
            total = validate_total(total)
        
        # Construct
        new = object.__new__(type(self))
        new.completed_at = completed_at
        new.error_message = error_message
        new.processed = processed
        new.started_at = started_at
        new.status = status
        new.total = total
        return new
