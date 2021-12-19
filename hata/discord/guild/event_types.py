"""
Koishi#8708 ignores occurred exception at DiscordGateway._received_message
Unknown dispatch event GUILD_JOIN_REQUEST_UPDATE
Data:
{
    'status': 'APPROVED',
    'request': {
        'user_id': '885003167509651486',
        'user': {
            'username': 'Tabi',
            'public_flags': 64,
            'id': '885003167509651486',
            'discriminator': '1730',
            'avatar': '701457c5a35ae4fd24d350fd0dd876bf'
        },
        'rejection_reason': None,
        'last_seen': None,
        'guild_id': '912478352823181312',
        'form_responses': [],
        'created_at': '2021-12-19T09:38:11.989000+00:00',
        'application_status': 'APPROVED',
        'actioned_by_user': {
            'username': 'YAGPDB.xyz',
            'public_flags': 65536,
            'id': '204255221017214977',
            'discriminator': '8760',
            'bot': True,
            'avatar': '2fa57b425415134d4f8b279174131ad6'
        },
        'actioned_at': '2021-12-19T09:38:12.142900+00:00'
        },
    'guild_id': '912478352823181312'
}
"""
__all__ = ('GuildJoinRequest', 'GuildJoinRequestUpdateEvent',)

import reprlib

from scarletio import copy_docs

from ..bases import EventBase
from ..core import GUILDS
from ..user import User

from .preinstanced import GuildJoinRequestStatus

class GuildJoinRequest:
    """
    
    Attributes
    ----------
    user : ``ClientUserBase``
        The user in context.
    """
    __slots__ = ('user',)
    
    def __new__(cls, data):
        """
        Creates a new guild join request.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
        """
        user = User(data['user'])
        
        self = object.__new__(cls)
        self.user = user
        return self
    
    
    def __repr__(self):
        """Returns the guild join request's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' user=')
        repr_parts.append(repr(self.user))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two guild join requests are the same"""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.user is not other.user:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the guild join request."""
        hash_value = 0
        
        # user
        hash_value ^= self.user.id
        
        return hash_value


class GuildJoinRequestUpdateEvent(EventBase):
    """
    Represents a guild join request update event.
    
    Attributes
    ----------
    guild_id : `int`
        The respective guild's identifier.
    request : ``GuildJoinRequest``
        The request.
    status : ``GuildJoinRequestStatus``
        The guild join request's status.
    """
    __slots__ = ('guild_id', 'request', 'status',)
    
    def __new__(cls, data):
        """
        Creates a new guild join request event.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Guild join request update event.
        """
        guild_id = int(data['guild_id'])
        request = GuildJoinRequest(data['request'])
        status = GuildJoinRequestStatus.get(data['status'])
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.request = request
        self.status = status
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<', self.__class__.__name__,
            ' guild_id=', repr(self.guild_id),
            ', request=', repr(self.request),
            ', status=', repr(self.status),
            '>',
        ]
        
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.request
        yield self.status
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.request != other.request:
            return False
        
        if self.status is not other.status:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return self.guild_id^hash(self.request)^hash(self.status)
    
    
    @property
    def guild(self):
        """
        Returns the guild join request update's guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        return GUILDS.get(self.guild_id, None)
