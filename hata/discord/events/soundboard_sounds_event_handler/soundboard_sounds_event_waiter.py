__all__ = ()

from scarletio import Future, RichAttributeErrorBaseType

from ..core import KOKORO


class SoundboardSoundsEventWaiter(RichAttributeErrorBaseType):
    """
    Soundboard sounds event waiter.
    
    Attributes
    ----------
    counter : `int`
        Counter how much times the event is waited on.
    future : ``Future``
        The waiter future.
    """
    __slots__ = ('counter', 'future')
    
    
    def __new__(cls):
        """
        Creates a new event waiter.
        """
        self = object.__new__(cls)
        self.counter = 1
        self.future = Future(KOKORO)
        return self
    
    
    def __repr__(self):
        """Returns the event waiter's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' counter = ')
        repr_parts.append(repr(self.counter))
        
        repr_parts.append(', future = ')
        repr_parts.append(repr(self.future))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
