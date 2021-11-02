__all__ = ('ClientUserBase', 'ClientUserPBase',)

from ...backend.utils import copy_docs

from ..core import USERS, GUILDS

from ..color import Color
from ..activity import create_activity_from_data, ActivityRich, ActivityCustom

from .preinstanced import Status

from .user_base import UserBase
from .flags import UserFlag
from .guild_profile import GuildProfile
from .activity_change import ActivityChange, ActivityUpdate


class ClientUserBase(UserBase):
    """
    Base class for discord users and clients.
    
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
    thread_profiles : `None` or `dict` (``ChannelThread``, ``ThreadProfile``) items
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
    """
    __slots__ = ('guild_profiles', 'is_bot', 'flags', 'thread_profiles')
    
    @copy_docs(UserBase._update_attributes)
    def _update_attributes(self, data):
        """
        Updates the user with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            User data received from Discord.
        """
        UserBase._update_attributes(self, data)
        
        self.flags = UserFlag(data.get('public_flags', 0))
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the user and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            User data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +---------------+-----------------------+
        | Keys          | Values                |
        +===============+=======================+
        | avatar        | ``Icon``              |
        +---------------+-----------------------+
        | banner        | ``Icon``              |
        +---------------+-----------------------+
        | banner_color  | `None` or ``Color``   |
        +---------------+-----------------------+
        | discriminator | `int`                 |
        +---------------+-----------------------+
        | flags         | ``UserFlag``          |
        +---------------+-----------------------+
        | name          | `str`                 |
        +---------------+-----------------------+
        """
        old_attributes = UserBase._difference_update_attributes(self, data)
        
        flags = data.get('public_flags', 0)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = UserFlag(flags)
        
        return old_attributes
    
    
    @classmethod
    def _difference_update_profile(cls, data, guild):
        """
        First tries to find the user, then it's respective guild profile for the given guild to update it.
        
        If the method cannot find the user, or the respective guild profile, then creates them.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild member data.
        guild : ``Guild``
            The respective guild of the profile to update.

        Returns
        -------
        user : ``user`` or ``Client``
            The respective user.
        old_attributes : `dict` of (`str`, `Any`) items
            The changed attributes of the respective guild profile as a `dict` with `attribute-name` - `old-attribute`
            relation.
            
            The possible keys and values within `old_attributes` are all optional and they can be any of the following:
            +-------------------+-------------------------------+
            | Keys              | Values                        |
            +===================+===============================+
            | avatar            | ``Icon``                      |
            +-------------------+-------------------------------+
            | boosts_since      | `None` or `datetime`          |
            +-------------------+-------------------------------+
            | nick              | `None` or `str`               |
            +-------------------+-------------------------------+
            | pending           | `bool`                        |
            +-------------------+-------------------------------+
            | role_ids          | `None` or `tuple` of `int`    |
            +-------------------+-------------------------------+
        """
        user_id = int(data['user']['id'])
        
        try:
            user = USERS[user_id]
        except KeyError:
            user = cls(data, guild)
            return user, {}
        
        try:
            guild_profile = user.guild_profiles[guild.id]
        except KeyError:
            user.guild_profiles[guild.id] = GuildProfile(data)
            guild.users[user_id] = user
            return user, {}
        
        guild_profile._set_joined(data)
        return user, guild_profile._difference_update_attributes(data)
    
    
    @classmethod
    def _update_profile(cls, data, guild):
        """
        First tries to find the user, then it's respective guild profile for the given guild to update it.
        
        If the method cannot find the user, or the respective guild profile, then creates them.
        
        Not like ``._difference_update_profile``, this method not calculates changes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild member data.
        guild : ``Guild``
            The respective guild of the profile to update.
        
        Returns
        -------
        user : ``UserBase``
            The updated user.
        """
        user_id = int(data['user']['id'])
        
        try:
            user = USERS[user_id]
        except KeyError:
            user = cls(data, guild)
        else:
            try:
                guild_profile = user.guild_profiles[guild.id]
            except KeyError:
                user.guild_profiles[guild.id] = GuildProfile(data)
            else:
                guild_profile._update_attributes(data)
        
        return user
    
    
    @staticmethod
    def _bypass_no_cache(data, guild):
        """
        Sets a ``Client``'s guild profile.
        
        > Only available when user or presence caching is disabled.
        
        Parameters
        ----------
        data : `dict`
            Received user data.
        guild : ``Guild``
            A respective guild from where the user data was received. Picked up if the given data includes
            guild member data as well.
        """
        user_data = data['user']
        guild_profile_data = data
        
        user_id = int(user_data['id'])
        
        try:
            user = USERS[user_id]
        except KeyError:
            return
        
        try:
            guild_profile = user.guild_profiles[guild.id]
        except KeyError:
            guild.users[user_id] = user
            user.guild_profiles[guild.id] = GuildProfile(guild_profile_data)
        else:
            guild_profile._set_joined(guild_profile_data)
            guild_profile._update_attributes(guild_profile_data)

    
    @classmethod
    def _from_client(cls, client):
        """
        Creates a client alter ego.
        
        Parameters
        ----------
        client : ``Client``
            The client to copy.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        self = object.__new__(cls)
        self.id = client.id
        self.discriminator = client.discriminator
        self.name = client.name
        
        self.guild_profiles = client.guild_profiles.copy()
        self.is_bot = client.is_bot
        self.flags = client.flags
        self.thread_profiles = client.thread_profiles.copy()
        
        self.avatar_hash = client.avatar_hash
        self.avatar_type = client.avatar_type
        
        self.banner_hash = client.banner_hash
        self.banner_type = client.banner_type
        
        return self
    
    
    @copy_docs(UserBase._set_default_attributes)
    def _set_default_attributes(self):
        UserBase._set_default_attributes(self)
        
        self.is_bot = False
        self.flags = UserFlag()
        
        self.guild_profiles = {}
        self.thread_profiles = None
    
    # if CACHE_PRESENCE is False, this should be never called from this class
    def _difference_update_presence(self, data):
        """
        Updates the user's presence and returns it's overwritten attributes as a `dict` with a `attribute-name` -
        `old-value` relation. An exception from this is `activities`, because that's a ``ActivityChange`` instance
        containing all the changes of the user's activities.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild member data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------------------------------+
        | Keys          | Values                            |
        +===============+===================================+
        | activities    | ``ActivityChange``                |
        +---------------+-----------------------------------+
        | status        | ``Status``                        |
        +---------------+-----------------------------------+
        | statuses      | `dict` of (`str`, `str`) items    |
        +---------------+-----------------------------------+
        """
        return {}
    
    
    def _update_presence(self, data):
        """
        Updates the user's presences with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild member data.
        """
        pass

    
    def _delete(self):
        """
        Deletes the user from it's guilds.
        """
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
    
    
    @copy_docs(UserBase.color_at)
    def color_at(self, guild):
        if (guild is not None):
            try:
                guild_profile = self.guild_profiles[guild.id]
            except KeyError:
                pass
            else:
                return guild_profile.color
        
        return Color()
    
    
    @copy_docs(UserBase.name_at)
    def name_at(self, guild):
        if (guild is not None):
            try:
                guild_profile = self.guild_profiles[guild.id]
            except KeyError:
                pass
            else:
                nick = guild_profile.nick
                if (nick is not None):
                    return nick
        
        return self.name
    
    
    @copy_docs(UserBase.has_role)
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
    
    
    @copy_docs(UserBase.top_role_at)
    def top_role_at(self, guild, default=None):
        if (guild is not None):
            try:
                guild_profile = self.guild_profiles[guild.id]
            except KeyError:
                pass
            else:
                return guild_profile.get_top_role(default)
        
        return default
    
    
    @copy_docs(UserBase.can_use_emoji)
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
        
        emoji_role_ids = emoji.roles
        if (emoji_role_ids is None):
            return True
        
        guild_profile_role_ids = guild_profile.role_ids
        if (guild_profile_role_ids is None):
            return False
        
        if emoji_role_ids.isdisjoint(guild_profile_role_ids):
            return False
        
        return True
    
    
    @copy_docs(UserBase.has_higher_role_than)
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
    
    
    @copy_docs(UserBase.has_higher_role_than_at)
    def has_higher_role_than_at(self, user, guild):
        if (guild is None):
            return False
        
        try:
            own_profile = self.guild_profiles[guild.id]
        except KeyError:
            return False
        
        if guild.owner_id == self.id:
            return True
        
        try:
            other_profile = user.guild_profiles[guild.id]
        except KeyError:
            # We always have higher permissions if the other user is not in the guild or if it is a webhook.
            return True
        
        if guild.owner_id == user.id:
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
    
    
    @copy_docs(UserBase.get_guild_profile_for)
    def get_guild_profile_for(self, guild):
        if (guild is not None):
            return self.guild_profiles.get(guild.id, None)
    
    
    @copy_docs(UserBase.iter_guild_profiles)
    def iter_guild_profiles(self):
        for guild_id, guild_profile in self.guild_profiles.items():
            try:
                guild = GUILDS[guild_id]
            except KeyError:
                continue
            
            yield guild, guild_profile
    
    
    @property
    @copy_docs(UserBase.partial)
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


class ClientUserPBase(ClientUserBase):
    """
    Base class for discord users and clients. This class is used as ``user`` superclass only if presence is enabled,
    so by default.
    
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
    thread_profiles : `None` or `dict` (``ChannelThread``, ``ThreadProfile``) items
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
    activities : `None` or `list` of ``ActivityBase`` instances
        A list of the client's activities. Defaults to `None`
    status : `Status`
        The user's display status.
    statuses : `dict` of (`str`, `str`) items
        The user's statuses for each platform.
    """
    __slots__ = ('activities', 'status', 'statuses')
    
    @classmethod
    @copy_docs(ClientUserBase._from_client)
    def _from_client(cls, client):
        self = super(ClientUserPBase, cls)._from_client(client)
        
        activities = client.activities
        if (activities is not None):
            activities = activities.copy()
        self.activities = activities
        self.status = client.status
        statuses = client.statuses
        if (statuses is not None):
            statuses = statuses.copy()
        self.statuses = statuses
        
        return self
    
    
    @copy_docs(ClientUserBase._set_default_attributes)
    def _set_default_attributes(self):
        ClientUserBase._set_default_attributes(self)
        
        self.status = Status.offline
        self.statuses = {}
        self.activities = None
    
    
    @copy_docs(ClientUserBase._difference_update_presence)
    def _difference_update_presence(self, data):
        old_attributes = {}
        
        statuses = data['client_status']
        if self.statuses != statuses:
            old_attributes['statuses'] = self.statuses
            self.statuses = statuses
            
            status = data['status']
            if self.status.value != status:
                old_attributes['status'] = self.status
                self.status = Status.get(status)
        
        activity_datas = data['activities']
        
        old_activities = self.activities
        new_activities = None
        
        if activity_datas:
            if old_activities is None:
                for activity_data in activity_datas:
                    activity = create_activity_from_data(activity_data)
                    
                    if new_activities is None:
                        new_activities = []
                    
                    new_activities.append(activity)
                
                activity_change = ActivityChange(new_activities, None, None)
                
            else:
                added_activities = None
                updated_activities = None
                removed_activities = old_activities.copy()
                
                for activity_data in activity_datas:
                    activity_type = activity_data['type']
                    for index in range(len(removed_activities)):
                        activity = removed_activities[index]
                        
                        if activity_type != activity.type:
                            continue
                            
                        if activity_data['id'] != activity.discord_side_id:
                            continue
                        
                        del removed_activities[index]
                        
                        activity_old_attributes = activity._difference_update_attributes(activity_data)
                        if activity_old_attributes:
                            activity_update = ActivityUpdate(activity, activity_old_attributes)
                            
                            if updated_activities is None:
                                updated_activities = []
                            
                            updated_activities.append(activity_update)
                        
                        if new_activities is None:
                            new_activities = []
                        
                        new_activities.append(activity)
                        break
                    else:
                        activity = create_activity_from_data(activity_data)
                        
                        if new_activities is None:
                            new_activities = []
                        
                        new_activities.append(activity)
                        
                        if added_activities is None:
                            added_activities = []
                        
                        added_activities.append(activity)
                
                if not removed_activities:
                    removed_activities = None
                
                if None is added_activities is updated_activities is removed_activities:
                    activity_change = None
                else:
                    activity_change = ActivityChange(added_activities, updated_activities, removed_activities)
        
        else:
            if old_activities is None:
                activity_change = None
            else:
                activity_change = ActivityChange(None, None, old_activities)
        
        if (activity_change is not None):
            old_attributes['activities'] = activity_change
        
        self.activities = new_activities
        
        return old_attributes
    
    
    @copy_docs(ClientUserBase._update_presence)
    def _update_presence(self, data):
        self.status = Status.get(data['status'])
        
        try:
            # not included sometimes
            self.statuses = data['client_status']
        except KeyError:
            pass
        
        activity_datas = data['activities']
        if activity_datas:
            new_activities = [create_activity_from_data(activity_data) for activity_data in activity_datas]
        else:
            new_activities = None
        
        self.activities = new_activities
    
    
    @property
    @copy_docs(UserBase.activity)
    def activity(self):
        activities = self.activities
        if activities is None:
            activity = None
        else:
            for activity in activities:
                if isinstance(activity, ActivityRich):
                    break
            else:
                activity = None
        
        return activity
    
    
    @property
    @copy_docs(UserBase.custom_activity)
    def custom_activity(self):
        activities = self.activities
        if activities is None:
            activity = None
        else:
            for activity in activities:
                if isinstance(activity, ActivityCustom):
                    break
            else:
                activity = None
        
        return activity
    
    
    @property
    @copy_docs(UserBase.platform)
    def platform(self):
        statuses = self.statuses
        if statuses:
            status = self.status.value
            for platform, l_status in statuses.items():
                if l_status == status:
                    return platform
        return ''

