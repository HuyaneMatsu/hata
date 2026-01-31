__all__ = ('MessageSearchResponse',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_analytics_id, parse_deep_historical_indexing_in_progress, parse_messages, parse_result_count, parse_threads,
    put_analytics_id, put_deep_historical_indexing_in_progress, put_messages, put_result_count, put_threads,
    validate_analytics_id, validate_deep_historical_indexing_in_progress, validate_messages, validate_result_count,
    validate_threads
)


class MessageSearchResponse(RichAttributeErrorBaseType):
    """
    Response of a message search.
    
    Attributes
    ----------
    analytics_id : `int`
        Analytics identifier.
    
    deep_historical_indexing_in_progress : `bool`
        Whether deep historical indexing is in progress.
    
    messages : ``None | tuple<Messages>``
        The search result messages.
    
    result_count : `int`
        The total amount of messages matched.
    
    threads : ``None | tuple<Channel>``
        Additional threads to keep cached for channel resolution.
    """
    __slots__ = ('analytics_id', 'deep_historical_indexing_in_progress', 'messages', 'result_count', 'threads')
    
    def __new__(
        cls,
        *,
        analytics_id = ...,
        deep_historical_indexing_in_progress = ...,
        messages = ...,
        result_count = ...,
        threads = ...,
    ):
        """
        Creates a new message search response with the given fields.
        
        Parameters
        ----------
        analytics_id : `None | int`, Optional (Keyword only)
            Analytics identifier.
        
        deep_historical_indexing_in_progress : `None | bool`, Optional (Keyword only)
            Whether deep historical indexing is in progress.
        
        messages : ``None | iterable<Messages>``, Optional (Keyword only)
            The search result messages.
        
        result_count : `None | int`, Optional (Keyword only)
            The total amount of messages matched.
        
        threads : ``None | iterable<Channel>``, Optional (Keyword only)
            Additional threads to keep cached for channel resolution.
        
        Raises
        ------
        ValueError
            - If a parameter's value is incorrect.
        TypeError
            - If a parameter's type is incorrect.
        """
        # analytics_id
        if (analytics_id is ...):
            analytics_id = 0
        else:
            analytics_id = validate_analytics_id(analytics_id)
        
        # deep_historical_indexing_in_progress
        if (deep_historical_indexing_in_progress is ...):
            deep_historical_indexing_in_progress = False
        else:
            deep_historical_indexing_in_progress = validate_deep_historical_indexing_in_progress(
                deep_historical_indexing_in_progress,
            )
        
        # messages
        if (messages is ...):
            messages = None
        else:
            messages = validate_messages(messages)
        
        # result_count
        if (result_count is ...):
            result_count = 0
        else:
            result_count = validate_result_count(result_count)
        
        # threads
        if (threads is ...):
            threads = None
        else:
            threads = validate_threads(threads)
        
        # Construct
        self = object.__new__(cls)
        self.analytics_id = analytics_id
        self.deep_historical_indexing_in_progress = deep_historical_indexing_in_progress
        self.messages = messages
        self.result_count = result_count
        self.threads = threads
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # analytics_id
        repr_parts.append(' analytics_id = ')
        repr_parts.append(repr(self.analytics_id))
        
        # deep_historical_indexing_in_progress
        repr_parts.append(', deep_historical_indexing_in_progress = ')
        repr_parts.append(repr(self.deep_historical_indexing_in_progress))
        
        # messages
        repr_parts.append(', messages = ')
        repr_parts.append(repr(self.messages))
        
        # result_count
        repr_parts.append(', result_count = ')
        repr_parts.append(repr(self.result_count))
        
        # threads
        repr_parts.append(', threads = ')
        repr_parts.append(repr(self.threads))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # analytics_id
        analytics_id = self.analytics_id
        hash_value ^= (analytics_id & 0xffffffffffffffff) ^ (analytics_id >> 64)
        
        # deep_historical_indexing_in_progress
        hash_value ^= self.deep_historical_indexing_in_progress
        
        # messages
        messages = self.messages
        if (messages is not None):
            hash_value ^= len(messages) << 1
            
            for message in messages:
                hash_value ^= hash(message)
        
        # result_count
        hash_value ^= self.result_count << 6
        
        # threads
        threads = self.threads
        if (threads is not None):
            hash_value ^= len(threads) << 23
            
            for message in threads:
                hash_value ^= hash(message)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # analytics_id
        if self.analytics_id != other.analytics_id:
            return False
        
        # deep_historical_indexing_in_progress
        if self.deep_historical_indexing_in_progress != other.deep_historical_indexing_in_progress:
            return False
        
        # messages
        if self.messages != other.messages:
            return False
        
        # result_count
        if self.result_count != other.result_count:
            return False
        
        # threads
        if self.threads != other.threads:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a message search response from the given data.
        
        Parameters
        ----------
        data : `dict<st, object>`
            Data to parse from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.analytics_id = parse_analytics_id(data)
        self.deep_historical_indexing_in_progress = parse_deep_historical_indexing_in_progress(data)
        self.messages = parse_messages(data)
        self.result_count = parse_result_count(data)
        self.threads = parse_threads(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serialises the message search response.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_analytics_id(self.analytics_id, data, defaults)
        put_deep_historical_indexing_in_progress(self.deep_historical_indexing_in_progress, data, defaults)
        messages = self.messages
        put_messages(messages, data, defaults)
        put_result_count(self.result_count, data, defaults)
        put_threads(self.threads, data, defaults, messages = messages)
        return data
    
    
    def copy(self):
        """
        Copies the message search response.
        
        Returns
        -------
        new : `instance<type<self>>˙
        """
        new = object.__new__(type(self))
        
        # analytics_id
        new.analytics_id = self.analytics_id
        
        # deep_historical_indexing_in_progress
        new.deep_historical_indexing_in_progress = self.deep_historical_indexing_in_progress
        
        # messages
        messages = self.messages
        if (messages is not None):
            messages = (*messages,)
        new.messages = messages
        
        # result_count
        new.result_count = self.result_count
        
        # threads
        threads = self.threads
        if (threads is not None):
            threads = (*threads,)
        new.threads = threads
        
        return new

    
    def copy_with(
        self,
        *,
        analytics_id = ...,
        deep_historical_indexing_in_progress = ...,
        messages = ...,
        result_count = ...,
        threads = ...,
    ):
        """
        Copies the message search response with the given fields..
        
        Parameters
        ----------
        analytics_id : `None | int`, Optional (Keyword only)
            Analytics identifier.
        
        deep_historical_indexing_in_progress : `None | bool`, Optional (Keyword only)
            Whether deep historical indexing is in progress.
        
        messages : ``None | iterable<Messages>``, Optional (Keyword only)
            The search result messages.
        
        result_count : `None | int`, Optional (Keyword only)
            The total amount of messages matched.
        
        threads : ``None | iterable<Channel>``, Optional (Keyword only)
            Additional threads to keep cached for channel resolution.
        
        Returns
        -------
        new : `instance<type<self>>˙
        
        Raises
        ------
        ValueError
            - If a parameter's value is incorrect.
        TypeError
            - If a parameter's type is incorrect.
        """
        # analytics_id
        if (analytics_id is ...):
            analytics_id = self.analytics_id
        else:
            analytics_id = validate_analytics_id(analytics_id)
        
        # deep_historical_indexing_in_progress
        if (deep_historical_indexing_in_progress is ...):
            deep_historical_indexing_in_progress = self.deep_historical_indexing_in_progress
        else:
            deep_historical_indexing_in_progress = validate_deep_historical_indexing_in_progress(
                deep_historical_indexing_in_progress
            )
        
        # messages
        if (messages is ...):
            messages = self.messages
            if (messages is not None):
                messages = (*messages,)
        else:
            messages = validate_messages(messages)
        
        # result_count
        if (result_count is ...):
            result_count = self.result_count
        else:
            result_count = validate_result_count(result_count)
        
        # threads
        if (threads is ...):
            threads = self.threads
            if (threads is not None):
                threads = (*threads,)
        else:
            threads = validate_threads(threads)
        
        # Construct
        new = object.__new__(type(self))
        new.analytics_id = analytics_id
        new.deep_historical_indexing_in_progress = deep_historical_indexing_in_progress
        new.messages = messages
        new.result_count = result_count
        new.threads = threads
        return new
