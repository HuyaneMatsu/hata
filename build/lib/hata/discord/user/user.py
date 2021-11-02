__all__ = ('User', 'ZEROUSER')

from ...env import CACHE_USER, CACHE_PRESENCE

from ...backend.utils import set_docs
from ...backend.export import include

from ..core import USERS

from ..preconverters import preconvert_snowflake, preconvert_str, preconvert_bool, preconvert_discriminator, \
    preconvert_flag, preconvert_color
from .preinstanced import Status
from .guild_profile import GuildProfile
from .client_user_base import ClientUserPBase, ClientUserBase
from .flags import UserFlag

create_partial_role_from_id = include('create_partial_role_from_id')
create_partial_user_from_id = include('create_partial_user_from_id')

if CACHE_PRESENCE:
    USER_BASE_CLASS = ClientUserPBase
else:
    USER_BASE_CLASS = ClientUserBase


class User(USER_BASE_CLASS):
    """
    Represents a Discord user.
    
    Attributes
    ----------
    id : `int`
        The user's unique identifier number.
    name : str
        The user's name.
    discriminator : `int`
        The user's discriminator. Given to avoid overlapping names.
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The user's avatar's type.
    banner_color : `None` or ``Color``
        The user's banner color if has any.
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    banner_type : ``IconType``
        The user's banner's type.
    guild_profiles : `dict` of (`int`, ``GuildProfile``) items
        A dictionary, which contains the user's guild profiles. If a user is member of a guild, then it should
        have a respective guild profile accordingly.
    is_bot : `bool`
        Whether the user is a bot or a user account.
    flags : ``UserFlag``
        The user's user flags.
    partial : `bool`
        Partial users have only their `.id` set and every other field might not reflect the reality.
    thread_profiles : `None` or `dict` (``ChannelThread``, ``ThreadProfile``) items
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
    activities : `None` or `list` of ``ActivityBase`` instances
        A list of the client's activities. Defaults to `None`
        
        > Only available if presence caching is enabled.
    status : ``Status``
        The user's display status.
        
        > Only available if presence caching is enabled.
    statuses : `dict` of (`str`, `str`) items
        The user's statuses for each platform.
        
        > Only available if presence caching is enabled.
    
    Notes
    -----
    Instances of this class are weakreferable.
    """
    __slots__ = ()
    
    if CACHE_PRESENCE:
        def __new__(cls, data, guild=None):
            try:
                user_data = data['user']
            except KeyError:
                user_data = data
                guild_profile_data = data.get('member', None)
            else:
                guild_profile_data = data
            
            user_id = int(user_data['id'])
            
            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                self.thread_profiles = None
                self.status = Status.offline
                self.statuses = {}
                self.activities = None
                update = True
                
                USERS[user_id] = self
            else:
                update = self.partial
            
            if update:
                self.is_bot = user_data.get('bot', False)
                self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                try:
                    profile = self.guild_profiles[guild.id]
                except KeyError:
                    guild.users[user_id] = self
                    self.guild_profiles[guild.id] = GuildProfile(guild_profile_data)
                else:
                    profile._set_joined(guild_profile_data)
            
            return self
    
    elif CACHE_USER:
        def __new__(cls, data, guild=None):
            try:
                user_data = data['user']
                guild_profile_data = data
            except KeyError:
                user_data = data
                guild_profile_data = data.get('member', None)
                
            user_id = int(user_data['id'])

            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                self.thread_profiles = None
                update = True
                
                USERS[user_id] = self
            else:
                update = self.partial
            
            if update:
                self.is_bot = user_data.get('bot', False)
                self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                try:
                    guild_profile = self.guild_profiles[guild.id]
                except KeyError:
                    guild.users[user_id] = self
                    self.guild_profiles[guild.id] = GuildProfile(guild_profile_data)
                else:
                    guild_profile._set_joined(guild_profile_data)
                    
            return self
    
    else:
        def __new__(cls, data, guild=None):
            try:
                user_data = data['user']
                guild_profile_data = data
            except KeyError:
                user_data = data
                guild_profile_data = data.get('member', None)
            
            user_id = int(user_data['id'])
            
            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                self.thread_profiles = None
                
                USERS[user_id] = self
            
            self.is_bot = user_data.get('bot', False)
            self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                self.guild_profiles[guild.id] = GuildProfile(guild_profile_data)
            
            return self
    
    set_docs(__new__,
        """
        First tries to find the user by id. If fails, then creates a new ``User`` object. If guild was given
        and the given data contains member data as well, then it will create a respective guild profile for the user
        too.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received user data.
        guild : ``Guild`` or `None`, Optional
            A respective guild from where the user data was received. It is picked up if the given data includes
            guild member data as well.
        
        Returns
        -------
        user : ``ClientUserBase``
        """)
    
    
    @classmethod
    def precreate(cls, user_id, **kwargs):
        """
        Precreates a user by creating a partial one with the given parameters. When the user is loaded, the precreated
        one is picked up and is updated. If an already existing user would be precreated, returns that instead of
        creating a new one, and updates it only, if it is still a partial one.
        
        Parameters
        ----------
        user_id : `int` or `str`
            The user's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the user.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The user's ``.name``.
        discriminator : `int` or `str` instance, Optional (Keyword only)
            The user's ``.discriminator``. Is accepted as `str` instance as well and will be converted to `int`.
        
        avatar : `None`, ``Icon`` or `str`, Optional (Keyword only)
            The user's avatar.
            
            > Mutually exclusive with `avatar_type` and `avatar_hash`.
        
        avatar_type : ``IconType``, Optional (Keyword only)
            The user's avatar's type.
            
            > Mutually exclusive with `avatar_type`.
        
        avatar_hash : `int`, Optional (Keyword only)
            The user's avatar's hash.
            
            > Mutually exclusive with `avatar`.
        
        banner : `None`, ``Icon`` or `str`, Optional (Keyword only)
            The user's banner.
            
            > Mutually exclusive with `banner_type` and `banner_hash`.
        
        banner_color : `None` or ``Color``
            The user's banner color.
        
        banner_type : ``IconType``, Optional (Keyword only)
            The user's banner's type.
            
            > Mutually exclusive with `banner_type`.
        
        banner_hash : `int`, Optional (Keyword only)
            The user's banner hash.
            
            > Mutually exclusive with `banner`.
        
        flags : ``UserFlag`` or `int` instance, Optional (Keyword only)
            The user's ``.flags``. If not passed as ``UserFlag``, then will be converted to it.
        
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
        user_id = preconvert_snowflake(user_id, 'user_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 32)
                processable.append(('name', name))
            
            try:
                discriminator = kwargs.pop('discriminator')
            except KeyError:
                pass
            else:
                discriminator = preconvert_discriminator(discriminator)
                processable.append(('discriminator', discriminator))
            
            cls.avatar.preconvert(kwargs, processable)
            cls.banner.preconvert(kwargs, processable)
            
            try:
                is_bot = kwargs.pop('is_bot')
            except KeyError:
                pass
            else:
                is_bot = preconvert_bool(is_bot, 'is_bot')
                processable.append(('is_bot', is_bot))
            
            try:
                flags = kwargs.pop('flags')
            except KeyError:
                pass
            else:
                flags = preconvert_flag(flags, 'flags', UserFlag)
                processable.append(('flags', flags))
            
            try:
                banner_color = kwargs.pop('banner_color')
            except KeyError:
                pass
            else:
                banner_color = preconvert_color(banner_color, 'banner_color', True)
                processable.append(('banner_color', banner_color))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}.')
        
        else:
            processable = None
        
        self = create_partial_user_from_id(user_id)
        if not self.partial:
            return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    if CACHE_PRESENCE:
        @classmethod
        def _create_and_update(cls, data, guild=None):
            try:
                user_data = data['user']
                guild_profile_data = data
            except KeyError:
                user_data = data
                guild_profile_data = None
            
            user_id = int(user_data['id'])
            
            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                self.status = Status.offline
                self.statuses = {}
                self.activities = None
                
                USERS[user_id] = self
            
            self.is_bot = user_data.get('bot', False)
            self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                try:
                    guild_profile = self.guild_profiles[guild.id]
                except KeyError:
                    guild.users[user_id] = self
                    self.guild_profiles[guild.id] = GuildProfile(guild_profile_data)
                else:
                    guild_profile._set_joined(guild_profile_data)
                    guild_profile._update_attributes(guild_profile_data)
            
            return self
        
    elif CACHE_USER:
        @classmethod
        def _create_and_update(cls, data, guild=None):
            try:
                user_data = data['user']
                guild_profile_data = data
            except KeyError:
                user_data = data
                guild_profile_data = None
            
            user_id = int(user_data['id'])
            
            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                
                USERS[user_id] = self
            
            self.is_bot = user_data.get('bot', False)
            self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                try:
                    guild_profile = self.guild_profiles[guild.id]
                except KeyError:
                    guild.users[user_id] = self
                    self.guild_profiles[guild.id] = GuildProfile(guild_profile_data)
                else:
                    guild_profile._set_joined(guild_profile_data)
                    guild_profile._update_attributes(guild_profile_data)
            
            return self
        
    else:
        @classmethod
        def _create_and_update(cls, data, guild=None):
            try:
                user_data = data['user']
            except KeyError:
                user_data = data
                guild_profile_data = None
            else:
                guild_profile_data = data
            
            user_id = int(user_data['id'])
            
            try:
                self = USERS[user_id]
            except KeyError:
                self = object.__new__(cls)
                self.id = user_id
                self.guild_profiles = {}
                
                USERS[user_id] = self
            
            self.is_bot = user_data.get('bot', False)
            self._update_attributes(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                self.guild_profiles[guild.id] = GuildProfile(guild_profile_data)
            
            return self
    
    set_docs(_create_and_update,
        """
        Creates a user with the given data. If the user already exists, updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received user data.
        guild : ``Guild`` or `None`, Optional
            A respective guild from where the user data was received. Picked up if the given data includes
            guild member data as well.
        
        Returns
        -------
        user : ``ClientUserBase``
        """)


ZEROUSER = User._create_empty(0)
