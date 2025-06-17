__all__ = ('GuildProfile', )

from scarletio import include

from ...bases import IconSlot, IconType, Slotted
from ...color import Color
from ...core import ROLES
from ...utils import DISCORD_EPOCH_START

from .fields import (
    parse_avatar_decoration, parse_boosts_since, parse_flags, parse_joined_at, parse_nick, parse_pending,
    parse_role_ids, parse_timed_out_until, put_avatar_decoration, put_boosts_since, put_flags,
    put_joined_at, put_nick, put_pending, put_role_ids, put_timed_out_until,
    validate_avatar_decoration, validate_boosts_since, validate_flags, validate_joined_at, validate_nick,
    validate_pending, validate_role_ids, validate_timed_out_until
)
from .flags import GuildProfileFlag


create_partial_role_from_id = include('create_partial_role_from_id')


GUILD_PROFILE_AVATAR = IconSlot('avatar', 'avatar')
GUILD_PROFILE_BANNER = IconSlot('banner', 'banner')


class GuildProfile(metaclass = Slotted):
    """
    Represents a user's profile at a guild.
    
    Attributes
    ----------
    avatar_decoration : ``None | AvatarDecoration``
        The guild profile's avatar decorations.
    
    avatar_hash : `int`
        The respective user's avatar hash at the guild in `uint128`.
    
    avatar_type : ``IconType``
        The respective user's avatar type at the guild.
    
    banner_hash : `int`
        The respective user's banner hash at the guild in `uint128`.
    
    banner_type : ``IconType``
        The respective user's banner type at the guild.
    
    boosts_since : `None | DateTime`
        Since when the user uses it's Nitro to boost the respective guild.
        If the user does not boost the guild then is set as `None`.
    
    flags : ``GuildProfileFlag``
        The guild profile's flags.
    
    joined_at : `None | DateTime`
        The date, since the user is the member of the guild.
        If this field was not included with the initial data, then it is set to `None`.
    
    nick : `None`, `str`
        The user's nick at the guild if it has.
    
    pending : `bool`
        Whether the user has not yet passed the guild's membership screening requirements.
        Defaults to `False`.
    
    role_ids : `None`, `tuple` of ``int``
        The user's roles at the guild.
    
    timed_out_until : `None | DateTime`
        Till when the user is timed out, and cannot interact with the guild.
    """
    __slots__ = (
        'avatar_decoration', 'boosts_since', 'flags', 'joined_at', 'nick', 'pending', 'role_ids', 'timed_out_until'
    )
    
    avatar = GUILD_PROFILE_AVATAR
    banner = GUILD_PROFILE_BANNER
    
    def __new__(
        cls,
        *,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        boosts_since = ...,
        flags = ...,
        joined_at = ...,
        nick = ...,
        pending = ...,
        role_ids = ...,
        timed_out_until = ...,
    ):
        """
        Creates a new guild profile instance from the given parameters.
        
        Parameters
        ----------
        avatar : ``None | str | Icon``, Optional (Keyword only)
            The guild profile's avatar.
        
        avatar_decoration : ``None | AvatarDecoration``, Optional (Keyword only)
            The guild profile's avatar decoration.
        
        banner : ``None | str | Icon``, Optional (Keyword only)
            The guild profile's banner.
        
        boosts_since : `None | DateTime`, Optional (Keyword only)
            Since when the user uses it's Nitro to boost the respective guild.
        
        flags : `int`, ``GuildProfileFlag``, Optional (Keyword only)
            The guild profile's flags.
            
        joined_at : `None | DateTime`, Optional (Keyword only)
            The date, since the user is the member of the guild.
        
        nick : `None`, `str`, Optional (Keyword only)
            The user's nick at the guild if it has.
        
        pending : `bool`, Optional (Keyword only)
            Whether the user has not yet passed the guild's membership screening requirements.
        
        role_ids : `None`, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            The user's roles at the guild.
        
        timed_out_until : `None | DateTime`, Optional (Keyword only)
            Till when the user is timed out, and cannot interact with the guild.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # avatar
        if avatar is ...:
            avatar = None
        else:
            avatar = cls.avatar.validate_icon(avatar, allow_data = True)
        
        # banner
        if banner is ...:
            banner = None
        else:
            banner = cls.banner.validate_icon(banner, allow_data = True)
        
        # avatar_decoration
        if avatar_decoration is ...:
            avatar_decoration = None
        else:
            avatar_decoration = validate_avatar_decoration(avatar_decoration)
        
        # boosts_since
        if boosts_since is ...:
            boosts_since = None
        else:
            boosts_since = validate_boosts_since(boosts_since)
        
        # flags
        if flags is ...:
            flags = GuildProfileFlag()
        else:
            flags = validate_flags(flags)
        
        # joined_at
        if joined_at is ...:
            joined_at = None
        else:
            joined_at = validate_joined_at(joined_at)
        
        # nick
        if nick is ...:
            nick = None
        else:
            nick = validate_nick(nick)
        
        # pending
        if pending is ...:
            pending = False
        else:
            pending = validate_pending(pending)
        
        # role_ids
        if role_ids is ...:
            role_ids = None
        else:
            role_ids = validate_role_ids(role_ids)
        
        # timed_out_until
        if timed_out_until is ...:
            timed_out_until = None
        else:
            timed_out_until = validate_timed_out_until(timed_out_until)
        
        # Construct
        self = object.__new__(cls)
        self.avatar = avatar
        self.avatar_decoration = avatar_decoration
        self.banner = banner
        self.boosts_since = boosts_since
        self.flags = flags
        self.joined_at = joined_at
        self.nick = nick
        self.pending = pending
        self.role_ids = role_ids
        self.timed_out_until = timed_out_until
        return self
    
    
    def __repr__(self):
        """Returns the representation of the guild profile."""
        return ''.join(['<', type(self).__name__, '>'])
    
    
    def __hash__(self):
        """Returns the guild profile's hash value."""
        hash_value = 0
        
        # avatar
        hash_value ^= hash(self.avatar)
        
        # avatar_decoration
        avatar_decoration = self.avatar_decoration
        if (avatar_decoration is not None):
            hash_value ^= hash(avatar_decoration)
        
        # banner
        hash_value ^= hash(self.banner)
        
        # boosts_since
        boosts_since = self.boosts_since
        if (boosts_since is not None):
            hash_value ^= hash(boosts_since)
        
        # flags
        hash_value ^= self.flags
        
        # joined_at
        joined_at = self.joined_at
        if (joined_at is not None):
            hash_value ^= hash(joined_at)
        
        # nick
        nick = self.nick
        if (nick is not None):
            hash_value ^= hash(nick)
        
        # pending
        hash_value ^= self.pending
        
        # role_ids
        role_ids = self.role_ids
        if (role_ids is not None):
            hash_value ^= len(role_ids) << 4
            for role_id in role_ids:
                hash_value ^= role_id
        
        # timed_out_until
        timed_out_until = self.timed_out_until
        if (timed_out_until is not None):
            hash_value ^= hash(timed_out_until)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two guild profiles are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # avatar
        if self.avatar != other.avatar:
            return False
        
        # avatar_decoration
        if self.avatar_decoration != other.avatar_decoration:
            return False
        
        # banner
        if self.banner != other.banner:
            return False
        
        # boosts_since
        if self.boosts_since != other.boosts_since:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # joined_at
        if self.joined_at != other.joined_at:
            return False
        
        # nick
        if self.nick != other.nick:
            return False
        
        # pending
        if self.pending != other.pending:
            return False
        
        # role_ids
        if self.role_ids != other.role_ids:
            return False
        
        # timed_out_until
        if self.timed_out_until != other.timed_out_until:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a guild profile from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received guild profile data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.joined_at = parse_joined_at(data)
        self._update_attributes(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the guild profile to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        type(self).avatar.put_into(self.avatar, data, defaults, as_data = not include_internals)
        put_avatar_decoration(self.avatar_decoration, data, defaults)
        type(self).banner.put_into(self.banner, data, defaults, as_data = not include_internals)
        put_nick(self.nick, data, defaults)
        put_role_ids(self.role_ids, data, defaults)
        put_timed_out_until(self.timed_out_until, data, defaults)
        
        if include_internals:
            put_boosts_since(self.boosts_since, data, defaults)
            put_flags(self.flags, data, defaults)
            put_joined_at(self.joined_at, data, defaults)
            put_pending(self.pending, data, defaults)
        
        return data
    
    
    def _set_joined(self, data):
        """
        Sets ``.joined_at`` of the guild profile if it is not set yet.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received guild profile data.
        """
        if self.joined_at is None:
            self.joined_at = parse_joined_at(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the guild profile with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received guild profile data.
        """
        self._set_avatar(data)
        self.avatar_decoration = parse_avatar_decoration(data)
        self._set_banner(data)
        self.boosts_since = parse_boosts_since(data)
        self.flags = parse_flags(data)
        self.nick = parse_nick(data)
        self.pending = parse_pending(data)
        self.role_ids = parse_role_ids(data)
        self.timed_out_until = parse_timed_out_until(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the guild profile and returns it's changed attributes in a `dict` within `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict<str, object>`
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | avatar            | ``Icon``                      |
        +-------------------+-------------------------------+
        | avatar_decoration | ``None | AvatarDecoration``   |
        +-------------------+-------------------------------+
        | banner            | ``Icon``                      |
        +-------------------+-------------------------------+
        | boosts_since      | `None | DateTime`             |
        +-------------------+-------------------------------+
        | flags             | `None`, ``GuildProfileFlags`` |
        +-------------------+-------------------------------+
        | nick              | `None`, `str`                 |
        +-------------------+-------------------------------+
        | pending           | `bool`                        |
        +-------------------+-------------------------------+
        | role_ids          | `None | tuple<int>`           |
        +-------------------+-------------------------------+
        | timed_out_until   | `None | DateTime`             |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        
        # avatar
        self._update_avatar(data, old_attributes)
        
        # avatar_decoration
        avatar_decoration = parse_avatar_decoration(data)
        if self.avatar_decoration != avatar_decoration:
            old_attributes['avatar_decoration'] = self.avatar_decoration
            self.avatar_decoration = avatar_decoration
        
        # banner
        self._update_banner(data, old_attributes)
        
        # boosts_since
        boosts_since = parse_boosts_since(data)
        if self.boosts_since != boosts_since:
            old_attributes['boosts_since'] = self.boosts_since
            self.boosts_since = boosts_since
        
        # flags
        flags = parse_flags(data)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = flags
            
        # nick
        nick = parse_nick(data)
        if self.nick != nick:
            old_attributes['nick'] = self.nick
            self.nick = nick
        
        # pending
        pending = parse_pending(data)
        if pending != self.pending:
            old_attributes['pending'] = self.pending
            self.pending = pending
        
        # role_ids
        role_ids = parse_role_ids(data)
        if role_ids != self.role_ids:
            old_attributes['role_ids'] = self.role_ids
            self.role_ids = role_ids
        
        # timed_out_until
        timed_out_until = parse_timed_out_until(data)
        if self.timed_out_until != timed_out_until:
            old_attributes['timed_out_until'] = self.timed_out_until
            self.timed_out_until = timed_out_until
        
        return old_attributes
    
    
    def copy(self):
        """
        Copies the guild profile.
        
        Returns
        -------
        new : `instance<type<self>>
        """
        new = object.__new__(type(self))
        
        avatar_decoration = self.avatar_decoration
        if (avatar_decoration is not None):
            avatar_decoration = avatar_decoration.copy()
        new.avatar_decoration = avatar_decoration
        
        new.avatar_hash = self.avatar_hash
        new.avatar_type = self.avatar_type
        
        new.banner_hash = self.banner_hash
        new.banner_type = self.banner_type
        
        new.boosts_since = self.boosts_since
        new.flags = self.flags
        new.joined_at = self.joined_at
        new.nick = self.nick
        new.pending = self.pending
        
        role_ids = self.role_ids
        if (role_ids is not None):
            role_ids = (*role_ids,)
        new.role_ids = role_ids
        
        new.timed_out_until = self.timed_out_until
        return new
    
    
    def copy_with(
        self, 
        *,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        boosts_since = ...,
        flags = ...,
        joined_at = ...,
        nick = ...,
        pending = ...,
        role_ids = ...,
        timed_out_until = ...,
    ):
        """
        Copies the guild profile and modifies the defined the defined fields of it.
        
        Parameters
        ----------
        avatar : ``None | str | Icon``, Optional (Keyword only)
            The guild profile's avatar.
        
        avatar_decoration : ``None | AvatarDecoration``, Optional (Keyword only)
            The guild profile's avatar decoration.
        
        banner : ``None | str | Icon``, Optional (Keyword only)
            The guild profile's banner.
        
        boosts_since : `None | DateTime`, Optional (Keyword only)
            Since when the user uses it's Nitro to boost the respective guild.
        
        flags : `int`, ``GuildProfileFlag``, Optional (Keyword only)
            The guild profile's flags.
        
        joined_at : `None | DateTime`, Optional (Keyword only)
            The date, since the user is the member of the guild.
        
        nick : `None`, `str`, Optional (Keyword only)
            The user's nick at the guild if it has.
        
        pending : `bool`, Optional (Keyword only)
            Whether the user has not yet passed the guild's membership screening requirements.
        
        role_ids : `None`, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            The user's roles at the guild.
        
        timed_out_until : `None | DateTime`, Optional (Keyword only)
            Till when the user is timed out, and cannot interact with the guild.
        
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
        # avatar
        if avatar is ...:
            avatar = self.avatar
        else:
            avatar = type(self).avatar.validate_icon(avatar, allow_data = True)
        
        # avatar_decoration
        if avatar_decoration is ...:
            avatar_decoration = self.avatar_decoration
            if (avatar_decoration is not None):
                avatar_decoration = avatar_decoration.copy()
        else:
            avatar_decoration = validate_avatar_decoration(avatar_decoration)
        
        # banner
        if banner is ...:
            banner = self.banner
        else:
            banner = type(self).banner.validate_icon(banner, allow_data = True)
        
        # boosts_since
        if boosts_since is ...:
            boosts_since = self.boosts_since
        else:
            boosts_since = validate_boosts_since(boosts_since)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # joined_at
        if joined_at is ...:
            joined_at = self.joined_at
        else:
            joined_at = validate_joined_at(joined_at)
        
        # nick
        if nick is ...:
            nick = self.nick
        else:
            nick = validate_nick(nick)
        
        # pending
        if pending is ...:
            pending = False
        else:
            pending = validate_pending(pending)
        
        # role_ids
        if role_ids is ...:
            role_ids = self.role_ids
            if (role_ids is not None):
                role_ids = (*role_ids,)
        else:
            role_ids = validate_role_ids(role_ids)
        
        # timed_out_until
        if timed_out_until is ...:
            timed_out_until = self.timed_out_until
        else:
            timed_out_until = validate_timed_out_until(timed_out_until)
        
        # Construct
        new = object.__new__(type(self))
        new.avatar = avatar
        new.avatar_decoration = avatar_decoration
        new.banner = banner
        new.boosts_since = boosts_since
        new.flags = flags
        new.joined_at = joined_at
        new.nick = nick
        new.pending = pending
        new.role_ids = role_ids
        new.timed_out_until = timed_out_until
        return new
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates a new guild profile with it's default attributes set.
        
        Returns
        -------
        self `instance<cls>`
        """
        self = object.__new__(cls)
        self.avatar_decoration = None
        self.avatar_hash = 0
        self.avatar_type = IconType.none
        self.banner_hash = 0
        self.banner_type = IconType.none
        self.boosts_since = None
        self.flags = GuildProfileFlag()
        self.joined_at = None
        self.nick = None
        self.pending = False
        self.role_ids = None
        self.timed_out_until = None
        return self
    
    
    def get_top_role(self, default = None):
        """
        Returns the top role of the guild profile. If the profile has no roles, then returns the `default`'s value.
        
        Parameters
        ----------
        default : `object` = `None`, Optional
            Default value to return if the respective user has no roles at the respective guild. Defaults to `None`.
        
        Returns
        -------
        top_role : ``Role``, `default`
        """
        top_role = default
        
        role_ids = self.role_ids
        if (role_ids is not None):
            role_found = False
            
            for role_id in role_ids:
                try:
                    role = ROLES[role_id]
                except KeyError:
                    continue
                
                if role_found:
                    if role > top_role:
                        top_role = role
                else:
                    top_role = role
                    role_found = True
            
            # If non of the roles is cached, create a partial role from the highest id.
            if not role_found:
                top_role = create_partial_role_from_id(role_ids[-1])
        
        return top_role
    
    
    def iter_role_ids(self):
        """
        Iterates over the role-ids of the guild profile.
        
        This method is an iterable generator.
        
        Yields
        ------
        role_id : `int`
        """
        role_ids = self.role_ids
        if (role_ids is not None):
            yield from role_ids
    
    
    def iter_roles(self):
        """
        Iterates over the roles of the guild profile. The roles are not sorted by position like at the case of
        ``.roles``, but based on `.id`.
        
        This method is an iterable generator.
        
        Yields
        ------
        role : ``Role``
        """
        role_ids = self.role_ids
        if (role_ids is not None):
            for role_id in role_ids:
                yield create_partial_role_from_id(role_id)
    
    
    @property
    def roles(self):
        """
        Returns the roles of the guild profile in sorted form.
        
        Returns
        -------
        roles : `None`, `list` of ``Role``
        """
        role_ids = self.role_ids
        if role_ids is None:
            roles = None
        else:
            roles = sorted(create_partial_role_from_id(role_id) for role_id in self.role_ids)
        
        return roles
    
    
    @property
    def color(self):
        """
        Returns the color of the respective user at the respective guild.
        
        Returns
        -------
        color : ``Color``
        """
        role_ids = self.role_ids
        if (role_ids is not None):
            for role in sorted((create_partial_role_from_id(role_id) for role_id in self.role_ids), reverse = True):
                color = role.color
                if color:
                    return color
        
        return Color()
    
    
    @property
    def created_at(self):
        """
        Returns ``.joined_at`` if set, else the Discord epoch.
        
        Returns
        -------
        created_at : `DateTime`
        """
        created_at = self.joined_at
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        
        return created_at
    
    
    @property
    def avatar_decoration_url(self):
        """
        Returns the guild profile's avatar decoration's url.
        If the guild profile has no avatar decoration then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        avatar_decoration = self.avatar_decoration
        if (avatar_decoration is not None):
            return avatar_decoration.url
    
    
    def avatar_decoration_url_as(self, ext = None, size = None):
        """
        Returns the guild profile's avatar decoration's url.
        If the guild profile has no avatar decoration then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        avatar_decoration = self.avatar_decoration
        if (avatar_decoration is not None):
            return avatar_decoration.url_as(ext = ext, size = size)
