__all__ = ('GuildJoinRequest',)

import reprlib, warnings

from scarletio import copy_docs

from ...bases import EventBase
from ...core import GUILDS
from ...user import ZEROUSER
from ...utils import DATETIME_FORMAT_CODE

from .fields import (
    parse_actioned_at, parse_actioned_by, parse_created_at, parse_form_responses, parse_guild_id, parse_last_seen_at,
    parse_rejection_reason, parse_status, parse_user, put_actioned_at_into, put_actioned_by_into, put_created_at_into,
    put_form_responses_into, put_guild_id_into, put_last_seen_at_into, put_rejection_reason_into, put_status_into,
    put_user_id_into, put_user_into, validate_actioned_at, validate_actioned_by, validate_created_at,
    validate_form_responses, validate_guild_id, validate_last_seen_at, validate_rejection_reason, validate_status,
    validate_user
)
from .preinstanced import GuildJoinRequestStatus


class GuildJoinRequest(EventBase):
    """
    Guild join request received within both `GUILD_JOIN_REQUEST_CREATE` and `GUILD_JOIN_REQUEST_UPDATE` events.
    
    Attributes
    ----------
    actioned_by : `None`, ``ClientUserBase``
        The user who action the join request.
    actioned_at : `None`, `datetime`
        When the join request was actioned at.
    created_at : `None`, `datetime`
        When the join request was created.
    form_responses : `None`, `tuple` of ``GuildJoinRequestFormResponse``
        The responses the user submitted.
    guild_id : `int`
        The respective guild's identifier.
    last_seen_at : `None`, `datetime`
        When the user was last seen.
    rejection_reason : `None`, `str`
        The reason why the join request was rejected.
    status : ``GuildJoinRequestStatus``
        The join request's status.
    user : ``ClientUserBase``
        The user in context.
    """
    __slots__ = (
        'actioned_by', 'actioned_at', 'created_at', 'form_responses', 'guild_id', 'last_seen_at', 'rejection_reason',
        'status', 'user'
    )
    
    def __new__(
        cls,
        *,
        actioned_by = ...,
        actioned_at = ...,
        created_at = ...,
        form_responses = ...,
        guild_id = ...,
        last_seen_at = ...,
        rejection_reason = ...,
        status = ...,
        user = ...,
    ):
        """
        Creates a new guild join request.
        
        Parameters
        ----------
        actioned_by : `None`, ``ClientUserBase``, Optional (Keyword only)
            The user who action the join request.
        actioned_at : `None`, `datetime`, Optional (Keyword only)
            When the join request was actioned at.
        created_at : None`, `datetime`, Optional (Keyword only)
            When the join request was created.
        form_responses : `None`, `iterable` of ``GuildJoinRequestFormResponse``, Optional (Keyword only)
            The responses the user submitted.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The respective guild's identifier.
        last_seen_at : `None`, `datetime`, Optional (Keyword only)
            When the user was last seen.
        rejection_reason : `None`, `str`, Optional (Keyword only)
            The reason why the join request was rejected.
        status : ``GuildJoinRequestStatus``, Optional (Keyword only)
            The join request's status.
        user : ``ClientUserBase``, Optional (Keyword only)
            The user in context.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # actioned_by
        if actioned_by is ...:
            actioned_by = None
        else:
            actioned_by = validate_actioned_by(actioned_by)
        
        # actioned_at
        if actioned_at is ...:
            actioned_at = None
        else:
            actioned_at = validate_actioned_at(actioned_at)
        
        # created_at
        if created_at is ...:
            created_at = None
        else:
            created_at = validate_created_at(created_at)
        
        # form_responses
        if form_responses is ...:
            form_responses = None
        else:
            form_responses = validate_form_responses(form_responses)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # last_seen_at
        if last_seen_at is ...:
            last_seen_at = None
        else:
            last_seen_at = validate_last_seen_at(last_seen_at)
        
        # rejection_reason
        if rejection_reason is ...:
            rejection_reason = None
        else:
            rejection_reason = validate_rejection_reason(rejection_reason)
        
        # status
        if status is ...:
            status = GuildJoinRequestStatus.started
        else:
            status = validate_status(status)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        # Construct
        self = object.__new__(cls)
        self.actioned_by = actioned_by
        self.actioned_at = actioned_at
        self.created_at = created_at
        self.form_responses = form_responses
        self.guild_id = guild_id
        self.last_seen_at = last_seen_at
        self.rejection_reason = rejection_reason
        self.status = status
        self.user = user
        return self
    
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild join request from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.actioned_by = parse_actioned_by(data)
        self.actioned_at = parse_actioned_at(data)
        self.created_at = parse_created_at(data)
        self.form_responses = parse_form_responses(data)
        self.guild_id = parse_guild_id(data)
        self.last_seen_at = parse_last_seen_at(data)
        self.rejection_reason = parse_rejection_reason(data)
        self.status = parse_status(data)
        self.user = parse_user(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the guild join request.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_actioned_by_into(self.actioned_by, data, defaults)
        put_actioned_at_into(self.actioned_at, data, defaults)
        put_created_at_into(self.created_at, data, defaults)
        put_form_responses_into(self.form_responses, data, defaults)
        put_guild_id_into(self.guild_id, data, defaults)
        put_last_seen_at_into(self.last_seen_at, data, defaults)
        put_rejection_reason_into(self.rejection_reason, data, defaults)
        put_status_into(self.status, data, defaults)
        put_user_into(self.user, data, defaults)
        put_user_id_into(self.user_id, data, defaults)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        repr_parts.append(', user = ')
        repr_parts.append(repr(self.user))
        
        created_at = self.created_at
        if (created_at is not None):
            repr_parts.append(', created_at = ')
            repr_parts.append(format(created_at, DATETIME_FORMAT_CODE))
        
        repr_parts.append(', status = ')
        repr_parts.append(self.status.name)
        
        actioned_by = self.actioned_by
        if (actioned_by is not None):
            repr_parts.append(', actioned_by = ')
            repr_parts.append(repr(actioned_by))
        
        actioned_at = self.actioned_at
        if (actioned_at is not None):
            repr_parts.append(', actioned_at = ')
            repr_parts.append(format(actioned_at, DATETIME_FORMAT_CODE))
        
        last_seen_at = self.last_seen_at
        if (last_seen_at is not None):
            repr_parts.append(', last_seen_at = ')
            repr_parts.append(format(last_seen_at, DATETIME_FORMAT_CODE))
        
        form_responses = self.form_responses
        if (form_responses is not None):
            repr_parts.append(' form_responses = [')
            
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
            repr_parts.append(', rejection_reason = ')
            repr_parts.append(reprlib.repr(rejection_reason))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.user
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
        
        if self.last_seen_at != other.last_seen_at:
            return False
        
        if self.rejection_reason != other.rejection_reason:
            return False
        
        if self.status != other.status:
            return False
        
        if self.user is not other.user:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # actioned_by
        actioned_by = self.actioned_by
        if (actioned_by is not None):
            hash_value ^= hash(actioned_by)
        
        # actioned_at
        actioned_at = self.actioned_at
        if (actioned_at is not None):
            hash_value ^= hash(actioned_at)
        
        # created_at
        created_at = self.created_at
        if (created_at is not None):
            hash_value ^= hash(created_at)
        
        # form_responses
        form_responses = self.form_responses
        if (form_responses is not None):
            hash_value ^= len(form_responses)
            
            for form_response in form_responses:
                hash_value ^= hash(form_response)
        
        # guild_id
        hash_value ^= self.guild_id
        
        # last_seen_at
        last_seen_at = self.last_seen_at
        if (last_seen_at is not None):
            hash_value ^= hash(last_seen_at)
        
        # rejection_reason
        rejection_reason = self.rejection_reason
        if (rejection_reason is not None):
            hash_value += hash(rejection_reason)
        
        # status
        hash_value ^= hash(self.status)
        
        # user_id
        hash_value ^= hash(self.user)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the guild join request.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        # Construct
        new = object.__new__(type(self))
        new.actioned_by = self.actioned_by
        new.actioned_at = self.actioned_at
        new.created_at = self.created_at
        
        form_responses = self.form_responses
        if (form_responses is not None):
            form_responses = (*(form_response.copy() for form_response in form_responses),)
        new.form_responses = form_responses
        
        new.guild_id = self.guild_id
        new.last_seen_at = self.last_seen_at
        new.rejection_reason = self.rejection_reason
        new.status = self.status
        new.user = self.user
        return new
    
    
    def copy_with(
        self,
        *,
        actioned_by = ...,
        actioned_at = ...,
        created_at = ...,
        form_responses = ...,
        guild_id = ...,
        last_seen_at = ...,
        rejection_reason = ...,
        status = ...,
        user = ...,
    ):
        """
        Copies the guild join request with the given fields.
        
        Parameters
        ----------
        actioned_by : `None`, ``ClientUserBase``, Optional (Keyword only)
            The user who action the join request.
        actioned_at : `None`, `datetime`, Optional (Keyword only)
            When the join request was actioned at.
        created_at : None`, `datetime`, Optional (Keyword only)
            When the join request was created.
        form_responses : `None`, `iterable` of ``GuildJoinRequestFormResponse``, Optional (Keyword only)
            The responses the user submitted.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The respective guild's identifier.
        last_seen_at : `None`, `datetime`, Optional (Keyword only)
            When the user was last seen.
        rejection_reason : `None`, `str`, Optional (Keyword only)
            The reason why the join request was rejected.
        status : ``GuildJoinRequestStatus``, Optional (Keyword only)
            The join request's status.
        user : ``ClientUserBase``, Optional (Keyword only)
            The user in context.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # actioned_by
        if actioned_by is ...:
            actioned_by = self.actioned_by
        else:
            actioned_by = validate_actioned_by(actioned_by)
        
        # actioned_at
        if actioned_at is ...:
            actioned_at = self.actioned_at
        else:
            actioned_at = validate_actioned_at(actioned_at)
        
        # created_at
        if created_at is ...:
            created_at = self.created_at
        else:
            created_at = validate_created_at(created_at)
        
        # form_responses
        if form_responses is ...:
            form_responses = self.form_responses
            if (form_responses is not None):
                form_responses = (*(form_response.copy() for form_response in form_responses),)
        else:
            form_responses = validate_form_responses(form_responses)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # last_seen_at
        if last_seen_at is ...:
            last_seen_at = self.last_seen_at
        else:
            last_seen_at = validate_last_seen_at(last_seen_at)
        
        # rejection_reason
        if rejection_reason is ...:
            rejection_reason = self.rejection_reason
        else:
            rejection_reason = validate_rejection_reason(rejection_reason)
        
        # status
        if status is ...:
            status = self.status
        else:
            status = validate_status(status)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        # Construct
        new = object.__new__(type(self))
        new.actioned_by = actioned_by
        new.actioned_at = actioned_at
        new.created_at = created_at
        new.form_responses = form_responses
        new.guild_id = guild_id
        new.last_seen_at = last_seen_at
        new.rejection_reason = rejection_reason
        new.status = status
        new.user = user
        return new
    
    
    @property
    def guild(self):
        """
        Returns the guild join request delete event's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def user_id(self):
        """
        Returns the user's identifier who requested to join.
        
        Returns
        -------
        user_id : `int`
        """
        return self.user.id
    
    
    def iter_form_responses(self):
        """
        Iterates over the form responses of the guild join request.
        
        This method is an iterable generator.
        
        Yields
        ------
        form_response : ``GuildJoinRequestFormResponse``
        """
        form_responses = self.form_responses
        if (form_responses is not None):
            yield from form_responses
    
    
    @property
    def last_seen(self):
        """
        ``.last_seen`` is deprecated and will be removed in 2023 April. Please use ``.edited_at`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.last_seen` is deprecated and will be removed in 2023 November. '
                f'Please use `.last_seen_at` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.last_seen_at
