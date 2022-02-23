__all__ = ('GuildJoinRequest', 'GuildJoinRequestDeleteEvent', 'GuildRequestFormResponse',)

import reprlib

from scarletio import copy_docs

from ..bases import EventBase
from ..core import GUILDS
from ..user import User, create_partial_user_from_id
from ..utils import DATETIME_FORMAT_CODE, timestamp_to_datetime

from .preinstanced import GuildJoinRequestStatus


class GuildRequestFormResponse:
    """
    Form response of a guild join request.
    
    Attributes
    ----------
    """
    def __new__(cls, data):
        """
        Creates a new guild request form response instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items.
        """
        
        # Nothing yet
        
        self = object.__new__(cls)
        return self
    
    
    def __repr__(self):
        """Returns the guild join request form response's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        # nothing yet
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two join requests responses are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        # Nothing yet
        
        return True
    
    
    def __hash__(self):
        """Returns the guild join request form response's hash value."""
        return 0


class GuildJoinRequestDeleteEvent(EventBase):
    """
    Represents a guild join request delete event.
    
    Attributes
    ----------
    guild_id : `int`
        The respective guild's identifier.
    user_id : `int`
        The respective user's identifier.
    """
    __slots__ = ('guild_id', 'user_id',)
    
    def __new__(cls, data):
        """
        Creates a new  guild join request delete event from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received data.
        """
        guild_id = int(data['guild_id'])
        user_id = int(data['user_id'])
        
        self = object.__new__(cls)
        self.guild_id = guild_id
        self.user_id = user_id
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<', self.__class__.__name__,
            ' guild_id=', repr(self.guild_id),
            ', user_id=', repr(self.user_id),
            '>',
        ]
        
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 2
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.user_id
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        return self.guild_id ^ self.user_id
    
    
    @property
    def guild(self):
        """
        Returns the respective guild of the join request. The guild must be cached.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        return GUILDS.get(self.guild_id)
    
    
    @property
    def user(self):
        """
        Returns the respective user. Might return a partial user if not cached.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)


class GuildJoinRequest(GuildJoinRequestDeleteEvent):
    """
    Guild join request received withing guild join request events.
    
    Attributes
    ----------
    guild_id : `int`
        The respective guild's identifier.
    actioned_by : `None`, ``ClientUserBase``
        The user who action the join request.
    actioned_at : `None`, `datetime`
        When the join request was actioned at.
    created_at : `datetime`
        When the join request was created.
    last_seen : `None`, `datetime`
        When the user was last seen.
    rejection_reason : `None`, `str`
        The reason why the join request was rejected.
    status : ``GuildJoinRequestStatus``
        The join request's status.
    user : ``ClientUserBase``
        The user in context.
    """
    __slots__ = (
        'actioned_by', 'actioned_at', 'created_at', 'form_responses', 'last_seen', 'rejection_reason', 'status', 'user'
    )
    
    def __new__(cls, data):
        """
        Creates a new guild join request.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received data.
        """
        actioned_by = data.get('actioned_by_user', None)
        if (actioned_by is not None):
            actioned_by = User.from_data(actioned_by)
        
        actioned_at = data.get('actioned_at', None)
        if (actioned_at is not None):
            actioned_at = timestamp_to_datetime(actioned_at)
        
        created_at = timestamp_to_datetime(data['created_at'])
        
        form_response_datas = data['form_responses']
        if form_response_datas:
            form_responses = tuple(
                GuildRequestFormResponse(form_response_data) for form_response_data in form_response_datas
            )
        else:
            form_responses = None
        

        last_seen = data.get('last_seen', None)
        if (last_seen is not None):
            last_seen = timestamp_to_datetime(last_seen)
        
        status = GuildJoinRequestStatus.get(data['application_status'])
        
        user = User.from_data(data['user'])
        
        self = GuildJoinRequestDeleteEvent.__new__(cls, data)
        self.actioned_by = actioned_by
        self.actioned_at = actioned_at
        self.created_at = created_at
        self.form_responses = form_responses
        self.last_seen = last_seen
        self.rejection_reason = data.get('rejection_reason', None)
        self.status = status
        self.user = user
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' guild_id=')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', user=')
        repr_parts.append(repr(self.user))
        
        repr_parts.append(', created_at=')
        repr_parts.append(format(self.created_at, DATETIME_FORMAT_CODE))
        
        repr_parts.append(', status=')
        repr_parts.append(self.status.name)
        
        actioned_by = self.actioned_by
        if (actioned_by is not None):
            repr_parts.append(', actioned_by=')
            repr_parts.append(repr(actioned_by))
        
        actioned_at = self.actioned_at
        if (actioned_at is not None):
            repr_parts.append(', actioned_at=')
            repr_parts.append(format(actioned_at, DATETIME_FORMAT_CODE))
        
        last_seen = self.last_seen
        if (last_seen is not None):
            repr_parts.append(', last_seen=')
            repr_parts.append(format(last_seen, DATETIME_FORMAT_CODE))
        
        form_responses = self.form_responses
        if (form_responses is not None):
            repr_parts.append(' form_responses=[')
            
            form_response_count = len(form_responses)
            index = 0
            while True:
                form_response = form_responses[index]
                repr_parts.append(repr(form_response))
                
                index += 1
                if index == form_response_count:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        rejection_reason = self.rejection_reason
        if (rejection_reason is not None):
            repr_parts.append(', rejection_reason=')
            repr_parts.append(reprlib.repr(rejection_reason))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.user_id
        yield self.status
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.actioned_by is not other.actioned_by:
            return False
        
        if self.actioned_at != other.actioned_at:
            return False
        
        if self.created_at != other.created_at:
            return False
        
        if self.form_responses != other.form_responses:
            return False
        
        if self.guild_id != other.guild_id:
            return False
        
        if self.last_seen != other.last_seen:
            return False
        
        if self.rejection_reason != other.rejection_reason:
            return False
        
        if self.status != other.status:
            return False
        
        # user ignored in favor of using `user_id`
        
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # actioned_by
        actioned_by = self.actioned_by
        if (actioned_by is not None):
            hash_value ^= actioned_by.id
        
        # actioned_at
        actioned_at = self.actioned_at
        if (actioned_at is not None):
            hash_value ^= hash(actioned_at)
        
        # created_at
        hash_value ^= hash(self.created_at)
        
        # form_responses
        form_responses = self.form_responses
        if (form_responses is not None):
            hash_value ^= len(form_responses)
            
            for form_response in form_responses:
                hash_value ^= hash(form_response)
        
        # guild_id
        hash_value ^= self.guild_id
        
        # last_seen
        last_seen = self.last_seen
        if (last_seen is not None):
            hash_value ^= hash(last_seen)
        
        # rejection_reason
        rejection_reason = self.rejection_reason
        if (rejection_reason is not None):
            hash_value += hash(rejection_reason)
        
        # status
        hash_value ^= hash(self.status)
        
        # user
        # Ignored in favor of using `user_id`
        
        # user_id
        hash_value ^= self.user_id
        
        return hash_value
