__all__ = ('ClientUserPBase',)

from itertools import count

from scarletio import copy_docs

from ...activity import Activity, ActivityType

from ..activity_change import ActivityChange
from ..activity_update import ActivityUpdate

from .client_user_base import ClientUserBase
from .fields import (
    parse_activities, parse_status, parse_statuses, validate_activities, validate_status, validate_statuses
)
from .flags import UserFlag
from .preinstanced import Status


ACTIVITY_TYPE_CUSTOM = ActivityType.custom


class ClientUserPBase(ClientUserBase):
    """
    Base class for discord users and clients. This class is used as ``User`` superclass only if presence is enabled,
    so by default.
    
    Attributes
    ----------
    activities : `None`, `list` of ``Activity``
        A list of the client's activities. Defaults to `None`
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
    statuses : `None`, `dict` of (`str`, `str`) items
        The user's statuses for each platform.
    thread_profiles : `None`, `dict` (``Channel``, ``ThreadProfile``) items
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
    """
    __slots__ = ('activities', 'status', 'statuses')
    
    def __new__(
        cls,
        *,
        activities = ...,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        banner_color = ...,
        bot = ...,
        discriminator = ...,
        display_name = ...,
        flags = ...,
        name = ...,
        status = ...,
        statuses = ...,
    ):
        """
        Creates a new partial user with the given fields.
        
        Parameters
        ----------
        activities : `iterable`, `list` of ``Activity``, Optional (Keyword only)
            A list of the client's activities.
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        avatar_decoration : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar decoration.
        banner : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's banner.
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The user's banner color.
        bot : `bool`, Optional (Keyword only)
            Whether the user is a bot or a user account.
        discriminator : `str`, `int`, Optional (Keyword only)
            The user's discriminator.
        display_name : `None`, `str`, Optional (Keyword only)
            The user's non-unique display name.
        flags : `int`, ``UserFlag``, Optional (Keyword only)
            The user's flags.
        name : `str`, Optional (Keyword only)
            The user's name.
        status : `Status`, `str`, Optional (Keyword only)
            The user's display status.
        statuses : `None`, `dict` of (`str`, `str`) items, Optional (Keyword only)
            The user's statuses for each platform.
        
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
        # activities
        if activities is ...:
            activities = None
        else:
            activities = validate_activities(activities)
        
        # status
        if status is ...:
            status = Status.offline
        else:
            status = validate_status(status)
        
        # statuses
        if statuses is ...:
            statuses = None
        else:
            statuses = validate_statuses(statuses)
        
        self = ClientUserBase.__new__(
            cls,
            avatar = avatar,
            avatar_decoration = avatar_decoration,
            banner = banner,
            banner_color = banner_color,
            bot = bot,
            discriminator = discriminator,
            display_name = display_name,
            flags = flags,
            name = name,
        )
        
        self.activities = activities
        self.status = status
        self.statuses = statuses
        return self
        
    
    @classmethod
    @copy_docs(ClientUserBase._from_client)
    def _from_client(cls, client, include_internals):
        self = super(ClientUserPBase, cls)._from_client(client, include_internals)
        
        # activities
        activities = client.activities
        if (activities is not None):
            activities = [activity.copy() for activity in activities]
        self.activities = activities
        
        # status
        self.status = client.status
        
        # statuses
        statuses = client.statuses
        if (statuses is not None):
            statuses = statuses.copy()
        self.statuses = statuses
        
        return self
    
    
    @copy_docs(ClientUserBase._set_default_attributes)
    def _set_default_attributes(self):
        ClientUserBase._set_default_attributes(self)
        
        self.status = Status.offline
        self.statuses = None
        self.activities = None
    
    
    @copy_docs(ClientUserBase._update_presence)
    def _update_presence(self, data):
        self.activities = parse_activities(data)
        self.status = parse_status(data)
        self.statuses = parse_statuses(data)
    
    
    @copy_docs(ClientUserBase._difference_update_presence)
    def _difference_update_presence(self, data):
        old_attributes = {}
        
        statuses = parse_statuses(data)
        if self.statuses != statuses:
            old_attributes['statuses'] = self.statuses
            self.statuses = statuses
            
        status = parse_status(data)
        if self.status is not status:
            old_attributes['status'] = self.status
            self.status = status
        
        activity_datas = data['activities']
        
        old_activities = self.activities
        new_activities = None
        
        if activity_datas:
            if old_activities is None:
                for activity_data in activity_datas:
                    activity = Activity.from_data(activity_data)
                    
                    if new_activities is None:
                        new_activities = []
                    
                    new_activities.append(activity)
                
                activity_change = ActivityChange.from_fields(new_activities, None, None)
                
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
                            activity_update = ActivityUpdate.from_fields(activity, activity_old_attributes)
                            
                            if updated_activities is None:
                                updated_activities = []
                            
                            updated_activities.append(activity_update)
                        
                        if new_activities is None:
                            new_activities = []
                        
                        new_activities.append(activity)
                        break
                    else:
                        activity = Activity.from_data(activity_data)
                        
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
                    activity_change = ActivityChange.from_fields(
                        added_activities, updated_activities, removed_activities
                    )
        
        else:
            if old_activities is None:
                activity_change = None
            else:
                activity_change = ActivityChange.from_fields(None, None, old_activities)
        
        if (activity_change is not None):
            old_attributes['activities'] = activity_change
        
        self.activities = new_activities
        
        return old_attributes
    
    
    @copy_docs(ClientUserBase.copy)
    def copy(self):
        new = ClientUserBase.copy(self)
        
        # activities
        activities = self.activities
        if (activities is not None):
            activities = [activity.copy() for activity in activities]
        new.activities = activities
        
        # status
        new.status = self.status
        
        # statuses
        statuses = self.statuses
        if (statuses is not None):
            statuses = statuses.copy()
        new.statuses = statuses
        
        return new
    
    
    def copy_with(
        self,
        *,
        activities = ...,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        banner_color = ...,
        bot = ...,
        discriminator = ...,
        display_name = ...,
        flags = ...,
        name = ...,
        status = ...,
        statuses = ...,
    ):
        """
        Copies the user with the given fields.
        
        Parameters
        ----------
        activities : `iterable`, `list` of ``Activity``, Optional (Keyword only)
            A list of the client's activities.
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        avatar_decoration : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar decoration.
        banner : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's banner.
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The user's banner color.
        bot : `bool`, Optional (Keyword only)
            Whether the user is a bot or a user account.
        discriminator : `str`, `int`, Optional (Keyword only)
            The user's discriminator.
        display_name : `None`, `str`, Optional (Keyword only)
            The user's non-unique display name.
        flags : `int`, ``UserFlag``, Optional (Keyword only)
            The user's flags.
        name : `str`, Optional (Keyword only)
            The user's name.
        status : `Status`, `str`, Optional (Keyword only)
            The user's display status.
        statuses : `None`, `dict` of (`str`, `str`) items, Optional (Keyword only)
            The user's statuses for each platform.
        
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
        # activities
        if activities is ...:
            activities = self.activities
            if (activities is not None):
                activities = [activity.copy() for activity in activities]
        else:
            activities = validate_activities(activities)
        
        # status
        if status is ...:
            status = self.status
        else:
            status = validate_status(status)
        
        # statuses
        if statuses is ...:
            statuses = self.statuses
            if (statuses is not None):
                statuses = statuses.copy()
        else:
            statuses = validate_statuses(statuses)
        
        new = ClientUserBase.copy_with(
            self,
            avatar = avatar,
            avatar_decoration = avatar_decoration,
            banner = banner,
            banner_color = banner_color,
            bot = bot,
            discriminator = discriminator,
            display_name = display_name,
            flags = flags,
            name = name,
        )
        
        new.activities = activities
        new.status = status
        new.statuses = statuses
        return new
    
    
    @copy_docs(ClientUserBase._get_hash_partial)
    def _get_hash_partial(self):
        hash_value = ClientUserBase._get_hash_partial(self)
        
        # activities
        activities = self.activities
        if (activities is not None):
            hash_value ^= len(activities) << 2
            
            for mask_shift, activity in zip(count(4, 4), activities):
                hash_value ^= hash(activity) | (0xf << mask_shift)
        
        # status
        hash_value ^= hash(self.status)
        
        # statuses
        statuses = self.statuses
        if (statuses is not None):
            hash_value ^= hash(tuple(statuses.items()))
        
        return hash_value
    
    
    @property
    @copy_docs(ClientUserBase.activity)
    def activity(self):
        activities = self.activities
        if activities is None:
            activity = None
        else:
            for activity in activities:
                if activity.type is not ACTIVITY_TYPE_CUSTOM:
                    break
            else:
                activity = None
        
        return activity
    
    
    @property
    @copy_docs(ClientUserBase.custom_activity)
    def custom_activity(self):
        activities = self.activities
        if activities is None:
            activity = None
        else:
            for activity in activities:
                if activity.type is ACTIVITY_TYPE_CUSTOM:
                    break
            else:
                activity = None
        
        return activity
    
    
    @property
    @copy_docs(ClientUserBase.platform)
    def platform(self):
        statuses = self.statuses
        if (statuses is not None):
            actual_status_value = self.status.value
            for platform, status_value in statuses.items():
                if actual_status_value == status_value:
                    return platform
        
        return ''
    
    
    @copy_docs(ClientUserBase.get_status_by_platform)
    def get_status_by_platform(self, platform):
        statuses = self.statuses
        if (statuses is not None):
            try:
                status_value = statuses[platform]
            except KeyError:
                pass
            else:
                return Status.get(status_value)
        
        return Status.offline
