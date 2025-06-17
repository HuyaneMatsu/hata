__all__ = ('ClientUserBase',)

from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from scarletio import copy_docs, export

from ...color import Color
from ...core import GUILDS, USERS

from ..guild_profile import GuildProfile

from .fields import parse_id, validate_bot
from .flags import UserFlag
from .helpers import _try_get_guild_and_id, _try_get_guild_id
from .orin_user_base import OrinUserBase


@export
class ClientUserBase(OrinUserBase):
    """
    Base class for discord users and clients.
    
    Attributes
    ----------
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    
    avatar_type : ``IconType``
        The user's avatar's type.
    
    avatar_decoration : ``None | AvatarDecoration``
        The user's avatar decorations.
    
    banner_color : `None`, ``Color``
        The user's banner color if has any.
    
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    
    banner_type : ``IconType``
        The user's banner's type.
    
    bot : `bool`
        Whether the user is a bot or a user account.
    
    discriminator : `int`
        The user's discriminator. Given to avoid overlapping names.
    
    display_name : `None | str`
        The user's non-unique display name.
    
    flags : ``UserFlag``
        The user's user flags.
    
    guild_profiles : ``dict<int, GuildProfile>``
        A dictionary, which contains the user's guild profiles. If a user is member of a guild, then it should
        have a respective guild profile accordingly.
    
    id : `int`
        The user's unique identifier number.
    
    name : str
        The user's name.
    
    name_plate : ``None | NamePlate``
        The user's name plate.
    
    primary_guild_badge : `None | GuildBadge`
        The user's primary guild's badge.
    
    thread_profiles : `None`, `dict` (``Channel``, ``ThreadProfile``) items
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
    """
    __slots__ = ('bot', 'guild_profiles', 'thread_profiles')
    
    
    def __new__(
        cls,
        *,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        banner_color = ...,
        bot = ...,
        discriminator = ...,
        display_name = ...,
        flags = ...,
        name = ...,
        name_plate = ...,
        primary_guild_badge = ...,
    ):
        """
        Creates a new partial user with the given fields.
        
        Parameters
        ----------
        avatar : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The user's avatar.
        
        avatar_decoration : ``None | AvatarDecoration``, Optional (Keyword only)
            The user's avatar decoration.
        
        banner : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The user's banner.
        
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The user's banner color.
        
        bot : `bool`, Optional (Keyword only)
            Whether the user is a bot or a user account.
        
        discriminator : `str`, `int`, Optional (Keyword only)
            The user's discriminator.
        
        display_name : `None | str`, Optional (Keyword only)
            The user's non-unique display name.
        
        flags : `int`, ``UserFlag``, Optional (Keyword only)
            The user's flags.
        
        name : `str`, Optional (Keyword only)
            The user's name.
        
        name_plate : ``None | NamePlate``, Optional (Keyword only)
            The user's name plate.
        
        primary_guild_badge : `None | GuildBadge`, Optional (Keyword only)
            The user's primary guild's badge.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # bot
        if bot is ...:
            bot = False
        else:
            bot = validate_bot(bot)
        
        self = OrinUserBase.__new__(
            cls,
            avatar = avatar,
            avatar_decoration = avatar_decoration,
            banner = banner,
            banner_color = banner_color,
            discriminator = discriminator,
            display_name = display_name,
            flags = flags,
            name = name,
            name_plate = name_plate,
            primary_guild_badge = primary_guild_badge,
        )
        self.bot = bot
        self.guild_profiles = {}
        self.thread_profiles = None
        return self
    
    
    @classmethod
    def from_data(cls, user_data, guild_profile_data = None, guild_id = 0, *, strong_cache = True):
        """
        Creates a new user from the given data.
        
        Parameters
        ----------
        user_data : `dict<str, object>`
            User data.
        
        guild_profile_data : `None`, `dict<str, object>` = `None`, Optional
            Guild profile data.
        
        guild_id : `int` = `0`, Optional
            The guild's identifier to which the guild profile is bound to.
        
        strong_cache : `bool` = `True`, Optional (Keyword only)
            Whether the instance should be put into its strong cache.
        
        Returns
        -------
        self : `instance<cls>`
        """
        raise NotImplementedError(
            f'`{cls.__name__}` does not support `.from_data` operation, please call it on a sub-type of it.'
        )
    
    
    @classmethod
    @copy_docs(OrinUserBase._from_data_and_difference_update_profile)
    def _from_data_and_difference_update_profile(cls, data, guild):
        user_data = data['user']
        user_id = parse_id(user_data)
        
        self = USERS.get(user_id, None)
        if self is None:
            self = cls.from_data(user_data, data, guild.id)
            old_attributes = None
        
        else:
            old_attributes = self._difference_update_profile(data, guild)
        
        return self, old_attributes
    
    
    @copy_docs(OrinUserBase._difference_update_profile)
    def _difference_update_profile(self, data, guild):
        guild_profile = self.guild_profiles.get(guild.id, None)
        if guild_profile is None:
            self.guild_profiles[guild.id] = GuildProfile.from_data(data)
            guild.users[self.id] = self
            return None
        
        guild_profile._set_joined(data)
        return guild_profile._difference_update_attributes(data)
    
    
    @classmethod
    @copy_docs(OrinUserBase._from_data_and_update_profile)
    def _from_data_and_update_profile(cls, data, guild):
        user_data = data['user']
        user_id = parse_id(user_data)
        
        self = USERS.get(user_id, None)
        if self is None:
            self = cls.from_data(user_data, data, guild.id)
        else:
            self._update_profile(data, guild)
        
        return self
    
    
    @copy_docs(OrinUserBase._update_profile)
    def _update_profile(self, data, guild):
        guild_profile = self.guild_profiles.get(guild.id, None)
        if guild_profile is None:
            self.guild_profiles[guild.id] = GuildProfile.from_data(data)
            guild.users[self.id] = self
            return False
        
        guild_profile._set_joined(data)
        guild_profile._update_attributes(data)
        return True
    
    
    @staticmethod
    def _bypass_no_cache(data, guild_profile_data, guild_id):
        """
        Sets a ``Client``'s guild profile.
        
        > Only available when user or presence caching is disabled.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received user data.
        
        guild_profile_data : `dict<str, object>`
            The user's guild profile's data.
        
        guild_id : `int`
            A respective guild's identifier from where the user data was received.
            Picked up if the given data includes guild member data as well.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        user_id = parse_id(data)
        
        try:
            user = USERS[user_id]
        except KeyError:
            return
        
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            user.guild_profiles[guild_id] = GuildProfile.from_data(guild_profile_data)
        else:
            guild_profile._set_joined(guild_profile_data)
            guild_profile._update_attributes(guild_profile_data)
        
        return user
    
    
    @classmethod
    def _from_client(cls, client, include_internals):
        """
        Creates a client alter ego.
        
        Parameters
        ----------
        client : ``Client``
            The client to copy.
        include_internals : `bool`
            Whether internal fields should be copied as well.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        self = object.__new__(cls)
        self.avatar_hash = client.avatar_hash
        self.avatar_type = client.avatar_type
        
        # avatar_decoration
        avatar_decoration = client.avatar_decoration
        if (avatar_decoration is not None):
            avatar_decoration = avatar_decoration.copy()
        self.avatar_decoration = avatar_decoration
        
        self.banner_color = client.banner_color
        self.banner_hash = client.banner_hash
        self.banner_type = client.banner_type
        self.bot = client.bot
        self.discriminator = client.discriminator
        self.display_name = client.display_name
        self.flags = client.flags
        
        if include_internals:
            guild_profiles = client.guild_profiles
            if (guild_profiles is not None):
                guild_profiles = {guild_id: guild_profile.copy() for guild_id, guild_profile in guild_profiles.items()}
        else:
            guild_profiles = {}
        
        self.guild_profiles = guild_profiles
        
        if include_internals:
            user_id = client.id
        else:
            user_id = 0
        self.id = user_id
        self.name = client.name
        
        # name_plate
        name_plate = client.name_plate
        if (name_plate is not None):
            name_plate = name_plate.copy()
        self.name_plate = name_plate
        
        primary_guild_badge = client.primary_guild_badge
        if (primary_guild_badge is not None):
            primary_guild_badge = primary_guild_badge.copy()
        self.primary_guild_badge = primary_guild_badge
        
        if include_internals:
            thread_profiles = client.thread_profiles
            if (thread_profiles is not None):
                thread_profiles = {
                    channel_id: thread_profile.copy() for channel_id, thread_profile in thread_profiles.items()
                }
        else:
            thread_profiles = None
        self.thread_profiles = thread_profiles
        
        return self
    
    
    @copy_docs(OrinUserBase._set_default_attributes)
    def _set_default_attributes(self):
        OrinUserBase._set_default_attributes(self)
        
        self.bot = False
        self.guild_profiles = {}
        self.thread_profiles = None
    
    
    @copy_docs(OrinUserBase.copy)
    def copy(self):
        new = OrinUserBase.copy(self)
        new.bot = self.bot
        new.guild_profiles = {}
        new.thread_profiles = None
        return new
    
    
    def copy_with(
        self,
        *,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        banner_color = ...,
        bot = ...,
        discriminator = ...,
        display_name = ...,
        flags = ...,
        name = ...,
        name_plate = ...,
        primary_guild_badge = ...,
    ):
        """
        Copies the user with the given fields.
        
        Parameters
        ----------
        avatar : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The user's avatar.
        
        avatar_decoration : ``None | AvatarDecoration``, Optional (Keyword only)
            The user's avatar decoration.
        
        banner : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The user's banner.
        
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The user's banner color.
        
        bot : `bool`, Optional (Keyword only)
            Whether the user is a bot or a user account.
        
        discriminator : `str`, `int`, Optional (Keyword only)
            The user's discriminator.
        
        display_name : `None | str`, Optional (Keyword only)
            The user's non-unique display name.
        
        flags : `int`, ``UserFlag``, Optional (Keyword only)
            The user's flags.
        
        name : `str`, Optional (Keyword only)
            The user's name.
        
        name_plate : ``None | NamePlate``, Optional (Keyword only)
            The user's name plate.
        
        primary_guild_badge : `None | GuildBadge`, Optional (Keyword only)
            The user's primary guild's badge.
        
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
        # bot
        if bot is ...:
            bot = self.bot
        else:
            bot = validate_bot(bot)
        
        # Construct
        new = OrinUserBase.copy_with(
            self,
            avatar = avatar,
            avatar_decoration = avatar_decoration,
            banner = banner,
            banner_color = banner_color,
            discriminator = discriminator,
            display_name = display_name,
            flags = flags,
            name = name,
            name_plate = name_plate,
            primary_guild_badge = primary_guild_badge,
        )
        new.bot = bot
        new.guild_profiles = {}
        new.thread_profiles = None
        return new
    
    
    @copy_docs(OrinUserBase._get_hash_partial)
    def _get_hash_partial(self):
        hash_value = OrinUserBase._get_hash_partial(self)
        
        # bot
        hash_value ^= self.bot << 34
        
        # guild_profiles | internal -> ignore
        # thread_profiles | internal -> ignore
        
        return hash_value
    
    
    @copy_docs(OrinUserBase._delete)
    def _delete(self):
        # we cannot full delete a user, because of the mentions, so we delete it only from the guilds
        guild_profiles = self.guild_profiles
        while guild_profiles:
            guild_id, guild_profile = guild_profiles.popitem()
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                continue
            
            try:
                del guild.users[self.id]
            except KeyError:
                pass
        
        # TODO: Should we delete the user from threads too?
    
    
    @copy_docs(OrinUserBase.color_at)
    def color_at(self, guild):
        guild_id = _try_get_guild_id(guild)
        
        try:
            guild_profile = self.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            return guild_profile.color
        
        return Color()
    
    
    @copy_docs(OrinUserBase.name_at)
    def name_at(self, guild):
        guild_id = _try_get_guild_id(guild)
        
        try:
            guild_profile = self.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            nick = guild_profile.nick
            if (nick is not None):
                return nick
        
        display_name = self.display_name
        if (display_name is not None):
            return display_name
        
        return self.name
    
    
    @copy_docs(OrinUserBase.has_name_like_at)
    def has_name_like_at(self, name, guild):
        if name.startswith('@'):
            name = name[1:]
        
        name_length = len(name)
        if (name_length < 1):
            return False
        
        if name_length > 5:
            if name_length > 37:
                return False
            
            if name[-5] == '#':
                try:
                    discriminator = int(name[-4:])
                except ValueError:
                    pass
                else:
                    stripped_name = name[:-5]
                    if (self.discriminator == discriminator) and (self.name == stripped_name):
                        return True
        
        if name_length > 32:
            return False
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        
        if pattern.search(self.name) is not None:
            return True
        
        display_name = self.display_name
        if (display_name is not None) and (pattern.search(display_name) is not None):
            return True
        
        guild_id = _try_get_guild_id(guild)
        try:
            guild_profile = self.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            nick = guild_profile.nick
            if (nick is not None):
                if pattern.search(nick) is not None:
                    return True
        
        return False
    
    
    @copy_docs(OrinUserBase.has_role)
    def has_role(self, role):
        guild_id = role.guild_id
        
        try:
            guild_profile = self.guild_profiles[guild_id]
        except KeyError:
            return False
        
        role_id = role.id
        if guild_id == role_id:
            return True
        
        role_ids = guild_profile.role_ids
        if role_ids is None:
            return False
        
        if role_id in role_ids:
            return True
        
        return False
    
    
    @copy_docs(OrinUserBase.top_role_at)
    def top_role_at(self, guild, default = None):
        guild, guild_id = _try_get_guild_and_id(guild)
        
        try:
            guild_profile = self.guild_profiles[guild_id]
        except KeyError:
            pass
        else:
            top_role = guild_profile.get_top_role()
            if (top_role is not None):
                return top_role
            
            if (guild is not None):
                top_role = guild.default_role
                if (top_role is not None):
                    return top_role
        
        return default
    
    
    @copy_docs(OrinUserBase.can_use_emoji)
    def can_use_emoji(self, emoji):
        if emoji.is_unicode_emoji():
            return True
        
        guild_id = emoji.guild_id
        
        try:
            guild_profile = self.guild_profiles[guild_id]
        except KeyError:
            return False
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            if guild.owner_id == self.id:
                return True
        
        emoji_role_ids = emoji.role_ids
        if (emoji_role_ids is None):
            return True
        
        guild_profile_role_ids = guild_profile.role_ids
        if (guild_profile_role_ids is None):
            return False
        
        if {*emoji_role_ids} & {*guild_profile_role_ids}:
            return True
        
        return False
    
    
    @copy_docs(OrinUserBase.has_higher_role_than)
    def has_higher_role_than(self, role):
        guild_id = role.guild_id
        
        try:
            guild_profile = self.guild_profiles[guild_id]
        except KeyError:
            return False
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            pass
        else:
            if guild.owner_id == self.id:
                return True
        
        top_role = guild_profile.get_top_role()
        if top_role is None:
            return False
        
        if top_role > role:
            return True
        
        return False
    
    
    @copy_docs(OrinUserBase.has_higher_role_than_at)
    def has_higher_role_than_at(self, user, guild):
        if self is user:
            return False
        
        guild, guild_id = _try_get_guild_and_id(guild)
        if (not guild_id):
            return False
        
        try:
            own_profile = self.guild_profiles[guild_id]
        except KeyError:
            return False
        
        if (guild is not None) and (guild.owner_id == self.id):
            return True
        
        try:
            other_profile = user.guild_profiles[guild_id]
        except KeyError:
            # We always have higher permissions if the other user is not in the guild or if it is a webhook.
            return True
        
        if (guild is not None) and (guild.owner_id == user.id):
            return False
        
        own_top_role = own_profile.get_top_role()
        if own_top_role is None:
            return False
        
        other_top_role = other_profile.get_top_role()
        if other_top_role is None:
            return True
        
        if own_top_role > other_top_role:
            return True
        
        return False
    
    
    @copy_docs(OrinUserBase.get_guild_profile_for)
    def get_guild_profile_for(self, guild):
        guild_id = _try_get_guild_id(guild)
        return self.guild_profiles.get(guild_id, None)
    
    
    @copy_docs(OrinUserBase.iter_guilds_and_profiles)
    def iter_guilds_and_profiles(self):
        for guild_id, guild_profile in self.guild_profiles.items():
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                continue
            
            yield guild, guild_profile
    
    
    @copy_docs(OrinUserBase.iter_guilds)
    def iter_guilds(self):
        for guild_id in self.guild_profiles.keys():
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                continue
            
            yield guild
    
    
    @copy_docs(OrinUserBase.is_boosting)
    def is_boosting(self, guild):
        guild_id = _try_get_guild_id(guild)
        
        try:
            guild_profile = self.guild_profiles[guild_id]
        except KeyError:
            return False
        
        return (guild_profile.boosts_since is not None)
    
    
    @property
    @copy_docs(OrinUserBase.partial)
    def partial(self):
        for guild_id in self.guild_profiles.keys():
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                continue
            
            if guild.partial:
                continue
            
            return False
        
        return True
