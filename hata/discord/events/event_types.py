__all__ = ('GuildUserChunkEvent', )

from ..bases import EventBase
from ..user import User
from ..guild import Guild


class GuildUserChunkEvent(EventBase):
    """
    Represents a processed `GUILD_MEMBERS_CHUNK` dispatch event.
    
    Attributes
    ----------
    guild : ``Guild``
        The guild what received the user chunk.
    users : `list` of (``User`` or ``Client``)
        The received users.
    nonce : `None` or `str`
        A nonce to identify guild user chunk response.
    index : `int`
        The index of the received chunk response (0 <= index < count).
    count : `int`
        The total number of chunk responses what Discord sends for the respective gateway.
    """
    __slots__ = ('guild', 'users', 'nonce', 'index', 'count')
    
    def __repr__(self):
        """Returns the representation of the guild user chunk event."""
        return f'<{self.__class__.__name__} guild={self.guild}, users={len(self.users)}, nonce={self.nonce!r}, index={self.index}, count={self.count}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 5
    
    def __iter__(self):
        """
        Unpacks the guild user chunk event.
        
        This method is a generator.
        """
        yield self.guild
        yield self.users
        yield self.nonce
        yield self.index
        yield self.count
