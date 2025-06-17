__all__ = ('Invite',)

from datetime import datetime as DateTime

from scarletio import export

from ...bases import DiscordEntity
from ...core import INVITES
from ...http.urls import build_invite_url
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import ClientUserBase, ZEROUSER

from .fields import (
    parse_approximate_online_count, parse_approximate_user_count, parse_channel, parse_code, parse_created_at,
    parse_flags, parse_guild, parse_guild_activity_overview, parse_inviter, parse_max_age, parse_max_uses,
    parse_target_application, parse_target_type, parse_target_user, parse_temporary, parse_type, parse_uses,
    put_approximate_online_count, put_approximate_user_count, put_channel, put_code, put_created_at, put_flags,
    put_guild, put_guild_activity_overview, put_inviter, put_max_age, put_max_uses, put_target_application,
    put_target_application_id, put_target_type, put_target_user, put_target_user_id, put_temporary, put_type, put_uses,
    validate_approximate_online_count, validate_approximate_user_count, validate_channel, validate_code,
    validate_created_at, validate_flags, validate_guild, validate_guild_activity_overview, validate_inviter,
    validate_max_age, validate_max_uses, validate_target_application, validate_target_type, validate_target_user,
    validate_temporary, validate_type, validate_uses
)
from .flags import InviteFlag
from .preinstanced import InviteTargetType, InviteType


PRECREATE_FIELDS = {
    'approximate_user_count': ('approximate_user_count', validate_approximate_user_count),
    'approximate_online_count': ('approximate_online_count', validate_approximate_online_count),
    'channel': ('channel', validate_channel),
    'created_at': ('created_at', validate_created_at),
    'flags': ('flags', validate_flags),
    'guild': ('guild', validate_guild),
    'guild_activity_overview' : ('guild_activity_overview', validate_guild_activity_overview),
    'invite_type': ('type', validate_type),
    'inviter': ('inviter', validate_inviter),
    'max_age': ('max_age', validate_max_age),
    'max_uses': ('max_uses', validate_max_uses),
    'target_application': ('target_application', validate_target_application),
    'target_type': ('target_type', validate_target_type),
    'target_user': ('target_user', validate_target_user),
    'temporary': ('temporary', validate_temporary),
    'uses': ('uses', validate_uses),
}


@export
class Invite(DiscordEntity, immortal = True):
    """
    Represents a Discord Invite.
    
    Attributes
    ---------
    approximate_online_count : `int`
        The approximate amount of online users at the respective guild (or group channel).
        Defaults to `0`.
    
    approximate_user_count : `int`
        The approximate amount of users at the respective guild (or group channel).
        Defaults to `0`.
    
    channel : ``None | Channel``
        The channel where the invite redirects. If it is announcements or store channel, then the invite is a lurk
        invite. If channel data was not sent with the invite's, then this attribute is set as `None`.
    
    code : `str`
        The invite's unique identifier.
    
    created_at : `DateTime`
        When the invite was created. Defaults to Discord epoch.
    
    flags : ``InviteFlag``
        The invite's flags.
    
    guild : ``None | Guild``
        The guild the invite is for. If not included or if the invite's channel is a group channel, then set as
        `None`.
    
    guild_activity_overview : ``None | GuildActivityOverview``
        The guild's activity overview.
    
    inviter : ``ClientUserBase``
        The creator of the invite. If not included, then set as `ZEROUSER`.
    
    max_age : `None | int`
        The time in seconds after the invite will expire.
        Defaults to `None`.
        
        If the invite was created with max age as `0`, then this value will be negative instead of the expected `0`.
    
    max_uses : `None | int`
        How much times the invite can be used.
        Defaults to `None`.
        
        If the invite has no use limit, then this value is set as `0`.
    
    target_application : ``None | Application``
        The invite's target application.
    
    target_type : ``InviteTargetType``
        The invite's target type.
    
    target_user : ``None | ClientUserBase``
        The target of the invite if applicable.
    
    temporary : `bool`
        Whether this invite only grants temporary membership.
        
        When the user goes offline, they get kicked, except if they got a role meanwhile.
    
    type : ``InviteType``
        The invite's type.
    
    uses : `None | int`
        The amount how much times the invite was used.
        Defaults to `None`.
    """
    __slots__ = (
        'approximate_user_count', 'approximate_online_count', 'channel', 'code', 'created_at', 'flags', 'guild',
        'guild_activity_overview', 'inviter', 'max_age', 'max_uses', 'target_application', 'target_type',
        'target_user', 'temporary', 'type', 'uses'
    )
    
    
    def __new__(
        cls,
        *, 
        flags = ...,
        max_age = ...,
        max_uses = ...,
        target_application = ...,
        target_type = ...,
        target_user = ...,
        temporary = ...,
    ):
        """
        Creates a partial invite with the given fields.
        
        Parameters
        ----------
        flags : ``int | InviteFlag``, Optional (Keyword only)
            The invite's flags.
        
        max_age : `None | int`, Optional (Keyword only)
            The time in seconds after the invite will expire.
        
        max_uses : `None | int`, Optional (Keyword only)
            How much times the invite can be used.
        
        target_application : ``None | Application``, Optional (Keyword only)
            The invite's target application.
        
        target_type : ``None | int | InviteTargetType``, Optional (Keyword only)
            The invite's target type.
        
        target_user : ``None | ClientUserBase``, Optional (Keyword only)
            The target of the invite if applicable.
        
        temporary : `bool`, Optional (Keyword only)
            Whether this invite only grants temporary membership.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # flags
        if flags is ...:
            flags = InviteFlag()
        else:
            flags = validate_flags(flags)
        
        # max_age
        if max_age is ...:
            max_age = None
        else:
            max_age = validate_max_age(max_age)
        
        # max_uses
        if max_uses is ...:
            max_uses = None
        else:
            max_uses = validate_max_uses(max_uses)
        
        # target_application
        if target_application is ...:
            target_application = None
        else:
            target_application = validate_target_application(target_application)
        
        # target_type
        if target_type is ...:
            target_type = InviteTargetType.none
        else:
            target_type = validate_target_type(target_type)
        
        # target_user
        if target_user is ...:
            target_user = None
        else:
            target_user = validate_target_user(target_user)
        
        # temporary
        if temporary is ...:
            temporary = False
        else:
            temporary = validate_temporary(temporary)
        
        # Construct
        self = object.__new__(cls)
        
        self.approximate_online_count = 0
        self.approximate_user_count = 0
        self.channel = None
        self.code = ''
        self.created_at = None
        self.flags = flags
        self.guild = None
        self.guild_activity_overview = None
        self.inviter = ZEROUSER
        self.max_age = max_age
        self.max_uses = max_uses
        self.target_application = target_application
        self.target_type = target_type
        self.target_user = target_user
        self.temporary = temporary
        self.type = InviteType.guild
        self.uses = None
        
        return self
        
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an invite from the given invite data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Invite data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        code = parse_code(data)
        
        try:
            self = INVITES[code]
        except KeyError:
            self = object.__new__(cls)
            self.code = code
            self._set_attributes(data)
            INVITES[code] = self
        
        else:
            self._update_attributes(data)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the invite to json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields, like id-s should be present as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_flags(self.flags, data, defaults)
        put_max_age(self.max_age, data, defaults)
        put_max_uses(self.max_uses, data, defaults)
        put_target_type(self.target_type, data, defaults)
        put_temporary(self.temporary, data, defaults)
        
        if include_internals:
            put_approximate_user_count(self.approximate_user_count, data, defaults)
            put_approximate_online_count(self.approximate_online_count, data, defaults)
            put_channel(self.channel, data, defaults)
            put_code(self.code, data, defaults)
            put_created_at(self.created_at, data, defaults)
            put_guild(self.guild, data, defaults)
            put_guild_activity_overview(self.guild_activity_overview, data, defaults)
            put_inviter(self.inviter, data, defaults)
            put_target_application(self.target_application, data, defaults)
            put_target_user(self.target_user, data, defaults)
            put_type(self.type, data, defaults)
            put_uses(self.uses, data, defaults)
        
        else:
            put_target_application_id(self.target_application_id, data, defaults)
            put_target_user_id(self.target_user_id, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the representation of the invite."""
        return f'<{type(self).__name__} code = {self.code!r}>'
    
    
    def __hash__(self):
        """Returns the invite's code's hash."""
        code = self.code
        if code:
            return hash(code)
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns a partial invite's hash value.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # flags
        hash_value ^= self.flags
        
        # max_age
        hash_value ^= self.max_age << 4
        
        # max_uses
        hash_value ^= self.max_uses << 8
        
        # target_application
        target_application = self.target_application
        if (target_application is not None):
            hash_value ^= hash(target_application)
        
        # target_type
        hash_value ^= self.target_type.value << 12
        
        # target_user
        target_user = self.target_user
        if (target_user is not None):
            hash_value ^= hash(target_user)
        
        # temporary
        hash_value ^= self.temporary << 16
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two invites are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two invites are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two types are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # flags
        if self.flags != other.flags:
            return False
        
        # max_age
        if self.max_age != other.max_age:
            return False
        
        # max_uses
        if self.max_uses != other.max_uses:
            return False
        
        # target_application
        if self.target_application is not other.target_application:
            return False
        
        # target_type
        if self.target_type is not other.target_type:
            return False
        
        # target_user
        if self.target_user is not other.target_user:
            return False
        
        # temporary
        if self.temporary != other.temporary:
            return False
        
        return True
    
    
    def _set_attributes(self, data):
        """
        Sets the invite's attributes (except code).
        
        Parameters
        ----------
        data : `dict<str, object>`
            Invite data.
        """
        self._set_attributes_common(data)
        self._set_counts_only(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the invite with the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Invite data.
        """
        self._set_attributes_common(data)
        self._update_counts_only(data)
    
    
    def _update_attributes_partial(self, data):
        """
        Updates the invite's fields that are received with a partial data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Invite data.
        """
        self.channel = parse_channel(data)
        self.guild = parse_guild(data)
    
    
    def _set_attributes_common(self, data):
        """
        Sets the common attributes of the invite. Used both in ``._set_attributes`` and ``._update_attributes``.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Invite data.
        """
        self.channel = parse_channel(data)
        self.created_at = parse_created_at(data)
        self.flags = parse_flags(data)
        self.guild = parse_guild(data)
        self.guild_activity_overview = parse_guild_activity_overview(data)
        self.inviter = parse_inviter(data)
        self.max_age = parse_max_age(data)
        self.max_uses = parse_max_uses(data)
        self.target_application = parse_target_application(data)
        self.target_type = parse_target_type(data)
        self.target_user = parse_target_user(data)
        self.temporary = parse_temporary(data)
        self.type = parse_type(data)
        self.uses = parse_uses(data)
    
    
    def _set_counts_only(self, data):
        """
        Sets the invite's counts.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received invite data.
        """
        guild = self.guild
        
        self.approximate_online_count = approximate_online_count = parse_approximate_online_count(data)
        if approximate_online_count and (guild is not None):
            guild.approximate_online_count = approximate_online_count
        
        self.approximate_user_count = approximate_user_count = parse_approximate_user_count(data)
        if approximate_user_count and (guild is not None):
            guild.approximate_user_count = approximate_user_count
    
    
    def _update_counts_only(self, data):
        """
        Updates the invite's counts if given.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received invite data.
        """
        guild = self.guild
        
        approximate_online_count = parse_approximate_online_count(data)
        if approximate_online_count:
            self.approximate_online_count = approximate_online_count
            if (guild is not None):
                guild.approximate_online_count = approximate_online_count
        
        approximate_user_count = parse_approximate_user_count(data)
        if approximate_user_count:
            self.approximate_user_count = approximate_user_count
            if (guild is not None):
                guild.approximate_user_count = approximate_user_count
    
    
    @classmethod
    def precreate(cls, code, **keyword_parameters):
        """
        Precreates an invite object with the given parameters.
        
        Parameters
        ----------
        code : `str`
            The invite's code.
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the invite.
        
        Other Parameters
        ----------------
        approximate_online_count : `int`, Optional (Keyword only)
            The amount of online users at the respective guild (or group channel).
        
        approximate_user_count : `int`, Optional (Keyword only)
            The amount of users at the respective guild (or group channel).
        
        channel : ``None | Channel``, Optional (Keyword only)
            The channel where the invite redirects.
        
        created_at : `None | DateTime`, Optional (Keyword only)
            When the invite was created.
        
        flags : ``int | InviteFlag``, Optional (Keyword only)
            The invite's flags.
        
        guild : ``None | Guild``, Optional (Keyword only)
            The guild the invite is for.
        
        guild_activity_overview : ``None | GuildActivityOverview``, Optional (Keyword only)
            The guild's activity overview.
        
        invite_type : ``None | int | InviteType``, Optional (Keyword only)
            The invite's type.
        
        inviter : ``ClientUserBase``, Optional (Keyword only)
            The creator of the invite.
        
        max_age : `None | int`, Optional (Keyword only)
            The time in seconds after the invite will expire.
        
        max_uses : `None | int`, Optional (Keyword only)
            How much times the invite can be used.
        
        target_application : ``None | Application``, Optional (Keyword only)
            The target application of the invite.
        
        target_type : ``int | InviteTargetType`` Optional (Keyword only)
            The invite's target type.
        
        target_user : ``None | ClientUserBase``, Optional (Keyword only)
            The target user of the invite.
        
        temporary : `bool`, Optional (Keyword only)
            Whether this invite only grants temporary membership.
        
        uses : `None | int`, Optional (Keyword only)
            The amount how much times the invite was used.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        code = validate_code(code)

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = INVITES[code]
        except KeyError:
            self = cls._create_empty(code)
            INVITES[code] = self
        
        else:
            # Cannot detect if an invite is not partial -> do nothing
            pass
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, code):
        """
        Creates an empty invite with default attributes set.
        
        Parameters
        ----------
        code : `str`
            Unique identifier of the invite.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        
        self.approximate_online_count = 0
        self.approximate_user_count = 0
        self.channel = None
        self.code = code
        self.created_at = None
        self.flags = InviteFlag()
        self.guild = None
        self.guild_activity_overview = None
        self.inviter = ZEROUSER
        self.max_age = None
        self.max_uses = None
        self.target_application = None
        self.target_type = InviteTargetType.none
        self.target_user = None
        self.temporary = False
        self.type = InviteType.guild
        self.uses = None
        
        return self
    
    
    def copy(self):
        """
        Copies the invite returning a new partial one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        new.approximate_online_count = 0
        new.approximate_user_count = 0
        new.channel = None
        new.code = ''
        new.created_at = None
        new.flags = self.flags
        new.guild = None
        new.guild_activity_overview = None
        new.inviter = ZEROUSER
        new.max_age = self.max_age
        new.max_uses = self.max_uses
        new.target_application = self.target_application
        new.target_type = self.target_type
        new.target_user = self.target_user
        new.temporary = self.temporary
        new.type = InviteType.guild
        new.uses = None
        
        return new
    
    
    def copy_with(
        self,
        *, 
        flags = ...,
        max_age = ...,
        max_uses = ...,
        target_application = ...,
        target_type = ...,
        target_user = ...,
        temporary = ...,
    ):
        """
        Copies the invite with the given fields.
        
        Parameters
        ----------
        flags : ``int | InviteFlag``, Optional (Keyword only)
            The invite's flags.
        
        max_age : `None | int`, Optional (Keyword only)
            The time in seconds after the invite will expire.
        
        max_uses : `None | int`, Optional (Keyword only)
            How much times the invite can be used.
        
        target_application : ``None | Application``, Optional (Keyword only)
            The invite's target application.
        
        target_type : ``None | int | InviteTargetType``, Optional (Keyword only)
            The invite's target type.
        
        target_user : ``None | ClientUserBase``, Optional (Keyword only)
            The target of the invite if applicable.
        
        temporary : `bool`, Optional (Keyword only)
            Whether this invite only grants temporary membership.
        
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
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # max_age
        if max_age is ...:
            max_age = self.max_age
        else:
            max_age = validate_max_age(max_age)
        
        # max_uses
        if max_uses is ...:
            max_uses = self.max_uses
        else:
            max_uses = validate_max_uses(max_uses)
        
        # target_application
        if target_application is ...:
            target_application = self.target_application
        else:
            target_application = validate_target_application(target_application)
        
        # target_type
        if target_type is ...:
            target_type = self.target_type
        else:
            target_type = validate_target_type(target_type)
        
        # target_user
        if target_user is ...:
            target_user = self.target_user
        else:
            target_user = validate_target_user(target_user)
        
        # temporary
        if temporary is ...:
            temporary = self.temporary
        else:
            temporary = validate_temporary(temporary)
        
        # Construct
        new = object.__new__(type(self))
        
        new.approximate_online_count = 0
        new.approximate_user_count = 0
        new.channel = None
        new.code = ''
        new.created_at = None
        new.flags = flags
        new.guild = None
        new.guild_activity_overview = None
        new.inviter = ZEROUSER
        new.max_age = max_age
        new.max_uses = max_uses
        new.target_application = target_application
        new.target_type = target_type
        new.target_user = target_user
        new.temporary = temporary
        new.type = InviteType.guild
        new.uses = None
        
        return new
    
    
    @property
    def url(self):
        """
        Returns the invite's url.
        
        Returns
        -------
        url : `str`
        """
        return build_invite_url(self.code)
    
    
    @property
    def id(self):
        """
        Compatibility property with other Discord entities.
        
        Returns
        -------
        id : `int` = `0`
        """
        return 0
    
    
    @property
    def target_application_id(self):
        """
        Returns the invite's target application's identifier.
        
        Returns
        -------
        target_application_id : `int`
        """
        target_application = self.target_application
        if target_application is None:
            target_application_id = 0
        else:
            target_application_id = target_application.id
        
        return target_application_id
    
    
    @property
    def channel_id(self):
        """
        Returns the invite's channel's identifier.
        """
        channel = self.channel
        if channel is None:
            channel_id = 0
        else:
            channel_id = channel.id
        
        return channel_id
    
    
    @property
    def guild_id(self):
        """
        Returns the invite's guild's identifier.
        
        Returns
        -------
        guild_id : `int`
        """
        guild = self.guild
        if guild is None:
            guild_id = 0
        else:
            guild_id = guild.id
        
        return guild_id
    
    
    @property
    def inviter_id(self):
        """
        Returns the invite's creator's identifier.
        
        Returns
        -------
        user_id : `int`
        """
        return self.inviter.id
    
    
    @property
    def target_user_id(self):
        """
        Returns the invite's target user's identifier.
        
        Returns
        -------
        target_user_id : `int`
        """
        target_user = self.target_user
        if target_user is None:
            target_user_id = 0
        else:
            target_user_id = target_user.id
        
        return target_user_id
    
    
    @property
    def partial(self):
        """
        Returns whether the invite is partial.
        
        Since it is not possible to check whether the invite is up to date, it will always return `True` for
        non-template invites.
        
        Returns
        -------
        partial : `bool`
        """
        return False if self.code else True
