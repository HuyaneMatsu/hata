__all__ = ('User',)

from scarletio import copy_docs

from ....env import CACHE_PRESENCE, CACHE_USER

from ...core import GUILDS, USERS
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from ..guild_profile import GuildProfile

from .client_user_base import ClientUserBase
from .client_user_presence_base import ClientUserPBase
from .fields import (
    parse_bot, parse_id, validate_activities, validate_banner_color, validate_bot, validate_discriminator,
    validate_display_name, validate_flags, validate_id, validate_name, validate_status, validate_statuses
)
from .flags import UserFlag
from .preinstanced import Status


PRECREATE_FIELDS = {
    'avatar': ('avatar', ClientUserBase.avatar.validate_icon),
    'avatar_decoration': ('avatar_decoration', ClientUserBase.avatar_decoration.validate_icon),
    'banner': ('banner', ClientUserBase.banner.validate_icon),
    'banner_color': ('banner_color', validate_banner_color),
    'bot': ('bot', validate_bot),
    'discriminator': ('discriminator', validate_discriminator),
    'display_name': ('display_name', validate_display_name),
    'flags': ('flags', validate_flags),
    'name': ('name', validate_name),
}

if not CACHE_PRESENCE:
    USER_BASE_TYPE = ClientUserBase

else:
    USER_BASE_TYPE = ClientUserPBase
    
    PRECREATE_FIELDS = {
        **PRECREATE_FIELDS,
        'activities': ('activities', validate_activities),
        'status': ('status', validate_status),
        'statuses': ('statuses', validate_statuses),
    }


class User(USER_BASE_TYPE):
    """
    Represents a Discord user.
    
    Attributes
    ----------
    activities : `None`, `list` of ``Activity``
        A list of the client's activities. Defaults to `None`
        
        > Only available if presence caching is enabled.
    
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    
    avatar_type : ``IconType``
        The user's avatar's type.
    
    avatar_decoration_hash : `int`
        The user's avatar decoration's hash in `uint128`.
    
    avatar_decoration_type : ``IconType``
        The user's avatar decoration's type.
    
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
    
    display_name : `None`, `str`
        The user's non-unique display name.
    
    flags : ``UserFlag``
        The user's user flags.
    
    guild_profiles : `dict` of (`int`, ``GuildProfile``) items
        A dictionary, which contains the user's guild profiles. If a user is member of a guild, then it should
        have a respective guild profile accordingly.
    
    id : `int`
        The user's unique identifier number.
    
    name : str
        The user's name.
    
    status : `Status`
        The user's display status.
        
        > Only available if presence caching is enabled.
    
    statuses : `None`, `dict` of (`str`, `str`) items
        The user's statuses for each platform.
        
        > Only available if presence caching is enabled.
    
    thread_profiles : `None`, `dict` (``Channel``, ``ThreadProfile``) items
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
    
    Notes
    -----
    Instances of this class are weakreferable.
    """
    __slots__ = ()
    
    if CACHE_PRESENCE:
        @classmethod
        @copy_docs(USER_BASE_TYPE.from_data)
        def from_data(cls, user_data, guild_profile_data = None, guild_id = 0, *, strong_cache = True):
            user_id = parse_id(user_data)
            
            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                self.thread_profiles = None
                self.status = Status.offline
                self.statuses = None
                self.activities = None
                
                USERS[user_id] = self
            
            self.bot = parse_bot(user_data)
            self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and guild_id:
                try:
                    guild_profile = self.guild_profiles[guild_id]
                except KeyError:
                    self.guild_profiles[guild_id] = GuildProfile.from_data(guild_profile_data)
                else:
                    guild_profile._set_joined(guild_profile_data)
                    guild_profile._update_attributes(guild_profile_data)
                
                if strong_cache:
                    try:
                        guild = GUILDS[guild_id]
                    except KeyError:
                        pass
                    else:
                        guild.users[user_id] = self
            
            return self
    
    elif CACHE_USER:
        @classmethod
        @copy_docs(USER_BASE_TYPE.from_data)
        def from_data(cls, user_data, guild_profile_data = None, guild_id = 0, *, strong_cache = True):
            user_id = parse_id(user_data)

            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                self.thread_profiles = None
                
                USERS[user_id] = self
            
            self.bot = parse_bot(user_data)
            self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and guild_id:
                try:
                    guild_profile = self.guild_profiles[guild_id]
                except KeyError:
                    self.guild_profiles[guild_id] = GuildProfile.from_data(guild_profile_data)
                else:
                    guild_profile._set_joined(guild_profile_data)
                    guild_profile._update_attributes(guild_profile_data)
                
                if strong_cache:
                    try:
                        guild = GUILDS[guild_id]
                    except KeyError:
                        pass
                    else:
                        guild.users[user_id] = self
            
            return self
    
    else:
        @classmethod
        @copy_docs(USER_BASE_TYPE.from_data)
        def from_data(cls, user_data, guild_profile_data = None, guild_id = 0, strong_cache = True):
            user_id = parse_id(user_data)
            
            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                self.thread_profiles = None
                
                USERS[user_id] = self
            
            self.bot = parse_bot(user_data)
            self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and guild_id:
                self.guild_profiles[guild_id] = GuildProfile.from_data(guild_profile_data)
            
            # Do we want to strong cache at this case?
            # if strong_cache:
            #     try:
            #         guild = GUILDS[guild_id]
            #     except KeyError:
            #         pass
            #     else:
            #         guild.users[user_id] = self
            
            return self
    
    
    @classmethod
    def precreate(cls, user_id, **keyword_parameters):
        """
        Precreates a user by creating a partial one with the given parameters. When the user is loaded, the precreated
        one is picked up and is updated. If an already existing user would be precreated, returns that instead of
        creating a new one, and updates it only, if it is still a partial one.
        
        Parameters
        ----------
        user_id : `int`, `str`
            The user's id.
        
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the user.
        
        Other Parameters
        ----------------
        activities : `iterable`, `list` of ``Activity``, Optional (Keyword only)
            A list of the client's activities.
            
            > Only available if presence caching is enabled.
        
        avatar : `None`, ``Icon``, `str`, Optional (Keyword only)
            The user's avatar.
        
        avatar_decoration : `None`, ``Icon``, `str`, Optional (Keyword only)
            The user's avatar decoration.
        
        banner : `None`, ``Icon``, `str`, Optional (Keyword only)
            The user's banner.
            
            > Mutually exclusive with `banner_type` and `banner_hash`.
        
        banner_color : `None`, ``Color``
            The user's banner color.
        
        bot : `bool`, Optional (Keyword only)
            Whether the user is a bot account.
        
        flags : ``UserFlag``, `int`, Optional (Keyword only)
            The user's ``.flags``. If not passed as ``UserFlag``, then will be converted to it.
        
        name : `str`, Optional (Keyword only)
            The user's ``.name``.
        
        discriminator : `int`, `str`, Optional (Keyword only)
            The user's discriminator.
        
        display_name : `None`, `str`, Optional (Keyword only)
            The user's non-unique display name.
        
        status : `Status`, `str`, Optional (Keyword only)
            The user's display status.
        
            > Only available if presence caching is enabled.
        
        statuses : `None`, `dict` of (`str`, `str`) items, Optional (Keyword only)
            The user's statuses for each platform.
        
            > Only available if presence caching is enabled.
        
        Returns
        -------
        user : ``ClientUserBase``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        user_id = validate_id(user_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = USERS[user_id]
        except KeyError:
            self = cls._create_empty(user_id)
            USERS[user_id] = self
        
        else:
            if not self.partial:
                return self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
