__all__ = ('ActivityChange', 'ActivityUpdate', 'ClientUserBase', 'ClientUserPBase', 'GuildProfile', 'PurchasedFlag',
    'ThreadProfile', 'ThreadProfileFlag', 'User', 'UserBase', 'UserFlag', 'VoiceState', 'ZEROUSER')

from datetime import datetime

from ..env import CACHE_USER, CACHE_PRESENCE

from ..backend.utils import DOCS_ENABLED, copy_docs, set_docs
from ..backend.export import export, include

from .bases import DiscordEntity, FlagBase, IconSlot, ICON_TYPE_NONE
from .core import USERS
from .utils import parse_time, DISCORD_EPOCH_START, DATETIME_FORMAT_CODE
from .color import Color
from .activity import create_activity, ActivityRich, ActivityCustom
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_bool, preconvert_discriminator, \
    preconvert_flag
from .preinstanced import Status, DefaultAvatar

from . import urls as module_urls

create_partial_role_from_id = include('create_partial_role_from_id')
Client = include('Client')


class UserFlag(FlagBase):
    """
    Represents a user's flags.
    
    The implemented user flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | staff                         | 0                 |
    +-------------------------------+-------------------+
    | partner                       | 1                 |
    +-------------------------------+-------------------+
    | hypesquad                     | 2                 |
    +-------------------------------+-------------------+
    | bug_hunter_level_1            | 3                 |
    +-------------------------------+-------------------+
    | mfa_sms                       | 4                 |
    +-------------------------------+-------------------+
    | premium_promo_dismissed       | 5                 |
    +-------------------------------+-------------------+
    | hypesquad_bravery             | 6                 |
    +-------------------------------+-------------------+
    | hypesquad_brilliance          | 7                 |
    +-------------------------------+-------------------+
    | hypesquad_balance             | 8                 |
    +-------------------------------+-------------------+
    | early_supporter               | 9                 |
    +-------------------------------+-------------------+
    | team_user                     | 10                |
    +-------------------------------+-------------------+
    | team_pseudo_user              | 11                |
    +-------------------------------+-------------------+
    | system                        | 12                |
    +-------------------------------+-------------------+
    | has_unread_urgent_messages    | 13                |
    +-------------------------------+-------------------+
    | bug_hunter_level_2            | 14                |
    +-------------------------------+-------------------+
    | underage_deleted              | 15                |
    +-------------------------------+-------------------+
    | verified_bot                  | 16                |
    +-------------------------------+-------------------+
    | early_verified_developer      | 17                |
    +-------------------------------+-------------------+
    | certified_moderator           | 18                |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'staff': 0,
        'partner': 1,
        'hypesquad': 2,
        'bug_hunter_level_1': 3,
        'mfa_sms': 4,
        'premium_promo_dismissed': 5,
        'hypesquad_bravery': 6,
        'hypesquad_brilliance': 7,
        'hypesquad_balance': 8,
        'early_supporter': 9,
        'team_user': 10,
        'team_pseudo_user': 11,
        'system': 12,
        'has_unread_urgent_messages': 13,
        'bug_hunter_level_2': 14,
        'underage_deleted': 15,
        'verified_bot': 16,
        'early_verified_developer': 17,
        'certified_moderator': 18,
    }


class ThreadProfileFlag(FlagBase):
    """
    Represents a ``ThreadProfile``'s user specific bitwise flag based settings.
    """
    __keys__ = {}


class PurchasedFlag(FlagBase):
    """
    A user's purchase flags.
    
    The implemented purchased flags are the following:
    
    +-------------------------------+-------------------+
    | Respective name               | Bitwise position  |
    +===============================+===================+
    | premium_tier_1                | 1                 |
    +-------------------------------+-------------------+
    | premium_tier_2                | 2                 |
    +-------------------------------+-------------------+
    | premium_guild                 | 4                 |
    +-------------------------------+-------------------+
    """
    __keys__ = {
        'premium_tier_1': 1,
        'premium_tier_2': 2,
        'premium_guild': 4,
    }


@export
def create_partial_user_from_id(user_id):
    """
    Creates a partial user from the given `user_id`. If the user already exists returns that instead.
    
    Parameters
    ----------
    user_id : `int`
        The unique identifier number of the user.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    try:
        return USERS[user_id]
    except KeyError:
        pass
    
    return User._create_empty(user_id)


class GuildProfile:
    """
    Represents a user's profile at a guild.
    
    Attributes
    ----------
    boosts_since : `None` or `datetime`
        Since when the user uses it's Nitro to boost the respective guild. If the user does not boost the guild, this
        attribute is set to `None`.
    joined_at : `None` or `datetime`
        The date, since the user is the member of the guild. If this field was not included with the initial data, then
        it is set to `None`.
    nick : `None` or `str`
        The user's nick at the guild if it has.
    pending : `bool`
        Whether the user has not yet passed the guild's membership screening requirements. Defaults to `False`.
    roles : `None` or `list` of ``Role``
        The user's roles at the guild.
        
        Feel free to use `.sort()` on it.
    """
    __slots__ = ('boosts_since', 'joined_at', 'nick', 'pending', 'roles',)
    
    @property
    def created_at(self):
        """
        Returns ``.joined_at`` if set, else the Discord epoch in datetime.
        
        Returns
        -------
        created_at : `datetime`
        """
        created_at = self.joined_at
        if created_at is None:
            created_at = DISCORD_EPOCH_START
        
        return created_at
    
    def __init__(self, data):
        """
        Creates a ``GuildProfile`` instance from the received guild profile data and from it's respective guild.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        """
        try:
            joined_at_data = data['joined_at']
        except KeyError:
            joined_at = None
        else:
            joined_at = parse_time(joined_at_data)
        
        self.joined_at = joined_at
        
        self._update_no_return(data)
    
    def __repr__(self):
        """Returns the representation of the guild profile."""
        return f'<{self.__class__.__name__}>'
    
    def _set_joined(self, data):
        """
        Sets ``.joined_at`` of the guild profile if it is not set yet.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        """
        if self.joined_at is None:
            try:
                joined_at_data = data['joined_at']
            except KeyError:
                joined_at = None
            else:
                joined_at = parse_time(joined_at_data)
            
            self.joined_at = joined_at
    
    def _update_no_return(self, data):
        """
        Updates the guild profile with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        """
        self.nick = data.get('nick', None)
        
        role_ids = data['roles']
        if role_ids:
            roles = []
            for role_id in role_ids:
                role_id = int(role_id)
                try:
                    role = create_partial_role_from_id(role_id)
                except KeyError:
                    continue
                
                roles.append(role)
            
            if (not roles):
                roles = None
        else:
            roles = None
        
        self.roles = roles
        
        boosts_since = data.get('premium_since', None)
        if (boosts_since is not None):
            boosts_since = parse_time(boosts_since)
        self.boosts_since = boosts_since
        
        self.pending = data.get('pending', None)
    
    def _update(self, data):
        """
        Updates the guild profile and returns it's changed attributes in a `dict` within `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | boosts_since      | `None` or `datetime`          |
        +-------------------+-------------------------------+
        | nick              | `None` or `str`               |
        +-------------------+-------------------------------+
        | pending           | `bool`                        |
        +-------------------+-------------------------------+
        | roles             | `None` or `list` of ``Role``  |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        nick = data.get('nick', None)
        if self.nick != nick:
            old_attributes['nick'] = self.nick
            self.nick = nick
        
        role_ids = data['roles']
        if role_ids:
            roles = []
            for role_id in role_ids:
                role_id = int(role_id)
                role = create_partial_role_from_id(role_id)
                roles.append(role)
            
            if (not roles):
                roles = None
        else:
            roles = None
        
        own_roles = self.roles
        if roles is None:
            if (own_roles is not None):
                old_attributes['roles'] = self.roles
                self.roles = None
        else:
            if own_roles is None:
                old_attributes['roles'] = None
                self.roles = roles
            else:
                own_roles.sort()
                roles.sort()
                
                if own_roles != roles:
                    old_attributes['roles'] = self.roles
                    self.roles = roles
        
        boosts_since = data.get('premium_since', None)
        if (boosts_since is not None):
            boosts_since = parse_time(boosts_since)
        if self.boosts_since != boosts_since:
            old_attributes['boosts_since'] = self.boosts_since
            self.boosts_since = boosts_since
        
        pending = data.get('pending', False)
        if pending != self.pending:
            old_attributes['pending'] = self.pending
            self.pending = pending
        
        return old_attributes
    
    def get_top_role(self, default=None):
        """
        Returns the top role of the guild profile. If the profile has no roles, then returns the `default`'s value.
        
        Parameters
        ----------
        default : `Any`, Optional
            Default value to return if the respective user has no roles at the respective guild. Defaults to `None`.
        
        Returns
        -------
        top_role : ``Role`` or `default`
        """
        roles = self.roles
        if roles is None:
            return default
        
        roles.sort()
        return roles[-1]
    
    @property
    def color(self):
        """
        Returns the color of the respective user at the respective guild.
        
        Returns
        -------
        color : ``Color``
        """
        roles = self.roles
        if (roles is not None):
            roles.sort()
            for role in reversed(roles):
                color = role.color
                if color:
                    return color
        
        return Color()
    


def thread_user_create(thread_channel, user, thread_user_data):
    """
    Resolves the given thread user data.
    
    Parameters
    ----------
    thread_channel : ``ChannelThread``
        The respective thread.
    user : ``ClientUserBase``
        The respective user to add or update in the thread.
    thread_user_data : `dict` of (`str`, `Any`) items
        Received thread user data.
    
    Returns
    -------
    created : `bool`
        Whether a new thread profile was created.
    """
    thread_users = thread_channel.thread_users
    if thread_users is None:
        thread_users = thread_channel.thread_users = {}
    thread_users[user.id] = user
    
    thread_profiles = user.thread_profiles
    if thread_profiles is None:
        thread_profiles = user.thread_profiles = {}
    
    try:
        thread_profile = thread_profiles[thread_channel]
    except KeyError:
        thread_profiles[thread_channel] = ThreadProfile(thread_user_data)
        created = True
    else:
        thread_profile._update_no_return(thread_user_data)
        created = False
    
    return created

def thread_user_update(thread_channel, user, thread_user_data):
    """
    Resolves the given thread user update.
    
    Parameters
    ----------
    thread_channel : ``ChannelThread``
        The respective thread.
    user : ``ClientUserBase``
        The respective user to add or update in the thread.
    thread_user_data : `dict` of (`str`, `Any`) items
        Received thread user data.
    
    Returns
    -------
    old_attributes : `None` or `dict` of (`str`, `Any`) items
    """
    thread_users = thread_channel.thread_users
    if thread_users is None:
        thread_users = thread_channel.thread_users = {}
    thread_users[user.id] = user
    
    thread_profiles = user.thread_profiles
    if thread_profiles is None:
        thread_profiles = user.thread_profiles = {}
    
    try:
        thread_profile = thread_profiles[thread_channel]
    except KeyError:
        thread_profiles[thread_channel] = ThreadProfile(thread_user_data)
        return None
    
    old_attributes = thread_profile._update_no_return(thread_user_data)
    if not old_attributes:
        old_attributes = None
    
    return old_attributes


def thread_user_delete(thread_channel, user_id):
    """
    Removes the user for the given id from the thread's users.
    
    Parameters
    ----------
    thread_channel : ``ChannelThread``
        The respective thread.
    user_id : `int`
        The respective user's identifier.
    """
    thread_users = thread_channel.thread_users
    if (thread_users is not None):
        try:
            user = thread_users.pop(user_id)
        except KeyError:
            pass
        else:
            if not thread_users:
                thread_channel.thread_users = None
            
            thread_profiles = user.thread_profiles
            if (thread_profiles is not None):
                try:
                    del thread_profiles[thread_channel]
                except KeyError:
                    pass
                else:
                    if not thread_profiles:
                        user.thread_profiles = None


def thread_user_pop(thread_channel, user_id, me):
    """
    Removes and returns the user for the given id from the thread's users.
    
    Parameters
    ----------
    thread_channel : ``ChannelThread``
        The respective thread.
    user_id : `int`
        The respective user's identifier.
    me : ``Client``
        The client who pops the user.
    
    Returns
    -------
    popped : `None` or `tuple` (``ClientUserBase``, ``ThreadProfile``) item
        The removed user and it's profile if any.
    """
    thread_users = thread_channel.thread_users
    if (thread_users is not None):
        try:
            user = thread_users.pop(user_id)
        except KeyError:
            pass
        else:
            if not thread_users:
                thread_channel.thread_users = None
            
            thread_profiles = user.thread_profiles
            if (thread_profiles is not None):
                if isinstance(user, Client) and (user is not me):
                    thread_profile = thread_profiles.get(thread_channel, None)
                else:
                    try:
                        thread_profile = thread_profiles.pop(thread_channel)
                    except KeyError:
                        thread_profile = None
                    else:
                        if not thread_profiles:
                            user.thread_profiles = None
                        
                if (thread_profile is not None):
                    return user, thread_profile


class ThreadProfile:
    """
    Represents an user's profile inside of a thread channel.
    
    Attributes
    ----------
    joined_at : `datetime`
        The date when the user joined the thread.
    flags : ``ThreadProfileFlag``
        user specific settings of the profile.
    """
    __slots__ = ('joined_at', 'flags',)
    
    @property
    def created_at(self):
        """
        Returns ``.joined_at`` if set.
        
        Returns
        -------
        created_at : `datetime`
        """
        return self.joined_at
    
    def __init__(self, data):
        """
        Creates a new ``ThreadProfile`` instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received thread profile data.
        """
        self.joined_at = parse_time(data['join_timestamp'])
        
        self._update_no_return(data)
    
    def __repr__(self):
        """Returns the thread profile's representation."""
        return f'<{self.__class__.__name__}>'
    
    def _update_no_return(self, data):
        """
        Updates the thread profile with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received thread profile data.
        """
        self.flags = ThreadProfileFlag(data['flags'])
    
    def _update(self, data):
        """
        Updates the thread profile and returns it's changed attributes in a `dict` within `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | flags             | ``ThreadProfileFlag``         |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        
        flags = data.get('flags', 0)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = ThreadProfileFlag(flags)
        
        return old_attributes


class UserBase(DiscordEntity, immortal=True):
    """
    Base class for user instances.
    
    id : `int`
        The client's unique identifier number.
    name : str
        The client's username.
    discriminator : `int`
        The client's discriminator. Given to avoid overlapping names.
    avatar_hash : `int`
        The client's avatar's hash in `uint128`.
    avatar_type : `bool`
        The client's avatar's type.
    
    Notes
    -----
    Instances of this class are weakreferable.
    """
    __slots__ = ('name', 'discriminator', )
    
    avatar = IconSlot('avatar', 'avatar', module_urls.user_avatar_url, module_urls.user_avatar_url_as)
    
    def __str__(self):
        """Returns the user's name."""
        return self.name
    
    def __repr__(self):
        """Returns the user's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        if self.partial:
            repr_parts.append(' partial')
        else:
            repr_parts.append(' name=')
            repr_parts.append(repr(self.full_name))
        
        repr_parts.append(', id=')
        repr_parts.append(repr(self.id))
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def __format__(self, code):
        """
        Formats the user in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        user : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import User, now_as_id
        >>> user = User.precreate(now_as_id(), name='Neko', discriminator=2012)
        >>> user
        <User partial, id=730233383967260672>
        >>> # no code stands for str(user).
        >>> f'{user}'
        'Neko'
        >>> # 'f' stands for full name
        >>> f'{user:f}'
        'Neko#2012'
        >>> # 'm' stands for mention.
        >>> f'{user:m}'
        '<@730233383967260672>'
        >>> # 'c' stands for created at.
        >>> f'{user:c}'
        '2020.07.08-01:26:45'
        ```
        """
        if not code:
            return self.name
        
        if code == 'f':
            return self.full_name
        
        if code == 'm':
            return self.mention
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    @property
    def full_name(self):
        """
        The user's name with it's discriminator.
        
        Returns
        -------
        full_name : `str`
        """
        return f'{self.name}#{self.discriminator:0>4}'
    
    @property
    def mention(self):
        """
        The mention of the user.
        
        Returns
        -------
        mention : `str`
        """
        return f'<@{self.id}>'
    
    @property
    def mention_nick(self):
        """
        The mention to the user's nick.
        
        Returns
        -------
        mention : `str`
        
        Notes
        -----
        It actually has nothing to do with the user's nickname > <.
        """
        return f'<@!{self.id}>'
    
    @property
    def default_avatar_url(self):
        """
        Returns the user's default avatar's url.
        
        Returns
        -------
        default_avatar_url : `str`
        """
        return DefaultAvatar.for_(self).url
    
    @property
    def default_avatar(self):
        """
        Returns the user's default avatar.
        
        Returns
        -------
        default_avatar : ``DefaultAvatar``
        """
        return DefaultAvatar.for_(self)
    
    # for sorting users
    def __gt__(self, other):
        """Returns whether the user's id is greater than the other's."""
        if isinstance(other, UserBase):
            return self.id > other.id
        return NotImplemented
    
    def __ge__(self, other):
        """Returns whether the user's id is greater or equal to the other."""
        if isinstance(other, UserBase):
            return self.id >= other.id
        return NotImplemented
    
    def __eq__(self, other):
        """Return whether the user's id is equal to the other."""
        if isinstance(other, UserBase):
            return self.id == other.id
        return NotImplemented
    
    def __ne__(self, other):
        """Returns whether the user's id is different as the other's."""
        if isinstance(other, UserBase):
            return self.id != other.id
        return NotImplemented
    
    def __le__(self, other):
        """Returns whether the user's id is less or equal to the other."""
        if isinstance(other,UserBase):
            return self.id <= other.id
        return NotImplemented
    
    def __lt__(self, other):
        """Returns whether the user's id is less than the other's."""
        if isinstance(other, UserBase):
            return self.id < other.id
        return NotImplemented
    
    @property
    def activities(self):
        """
        Returns the user's activities.
        
        Returns
        -------
        activities : `None`
        """
        return None
    
    @property
    def status(self):
        """
        Returns the user's display status.
        
        Returns
        -------
        status  ``Status``
        """
        return Status.offline
    
    @property
    def statuses(self):
        """
        Returns the user's statuses for each platform.
        
        Returns
        -------
        statuses : `dict` of (`str`, `str`) items
        """
        return {}
    
    @property
    def guild_profiles(self):
        """
        Returns a dictionary, which contains the user's guild profiles. If the user is member of a guild, then it should
        have a respective guild profile accordingly.
        
        Returns
        -------
        guild_profiles : `dict` of (``Guild``, ``GuildProfile``) items
        """
        return {}
    
    @property
    def thread_profiles(self):
        """
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
        
        Returns
        -------
        thread_profiles : `None` or `dict` (``ChannelThread``, ``ThreadProfile``) items
        """
        return None
    
    @property
    def is_bot(self):
        """
        Returns whether the user is a bot or a user account.
        
        Returns
        -------
        is_bot : `bool`
        """
        return False
    
    @property
    def flags(self):
        """
        Returns the user's flags.
        
        Returns
        -------
        flags : ``UserFlag``
        """
        return UserFlag()
    
    @property
    def partial(self):
        """
        Returns whether the user is partial. Partial users have only their ``.id`` set and every other field might not
        reflect the reality.
        
        Returns
        -------
        partial : `bool`
        """
        return True
    
    @property
    def activity(self):
        """
        Returns the user's top activity if applicable. If not.
        
        Returns
        -------
        activity : ``ActivityRich`` or `None`
        """
        return None
    
    @property
    def custom_activity(self):
        """
        Returns the user's custom activity if applicable.
        
        Returns
        -------
        activity : ``ActivityCustom`` or `None`
        """
        return None
    
    @property
    def platform(self):
        """
        Returns the user's top status's platform. If the user is offline it will return an empty string.
        
        Returns
        -------
        platform : `str`
        """
        return ''
    
    
    def color_at(self, guild):
        """
        Returns the user's color at the given guild.
        
        Parameters
        ----------
        guild : `None` or ``Guild``
            The guild, where the user's color will be checked.
            
            Can be given as `None`.

        Returns
        -------
        color : ``Color``
        """
        return Color()
    
    
    def name_at(self, guild):
        """
        Returns the user's name at the given guild.
        
        Parameters
        ----------
        guild : `None` or ``Guild``
            The guild, where the user's nick will be checked.
            
            Can be given as `None`.

        Returns
        -------
        name : `str`
        """
        return self.name
    
    
    def mentioned_in(self, message):
        """
        Returns whether the user is mentioned at a given message.
        
        Parameters
        ----------
        message : ``Message``
            The message, what's mentions will be checked.
        
        Returns
        -------
        mentioned : `bool`
        """
        if message.everyone_mention:
            return True
        
        user_mentions = message.user_mentions
        if (user_mentions is not None) and (self in user_mentions):
            return True
        
        role_mentions = message.role_mentions
        if (role_mentions is not None):
            guild = message.channel.guild
            if (guild is not None):
                try:
                    profile = self.guild_profiles[guild]
                except KeyError:
                    pass
                else:
                    roles = profile.roles
                    if (roles is not None):
                        for role in roles:
                            if role in role_mentions:
                                return True
        
        return False
    
    
    def has_role(self, role):
        """
        Returns whether the user has the given role.
        
        Parameters
        ----------
        role : ``Role``
            The role what will be checked.

        Returns
        -------
        has_role : `bool`
        """
        return False
    
    
    def top_role_at(self, guild, default=None):
        """
        Returns the top role of the user at the given guild.
        
        Parameters
        ----------
        guild : ``Guild`` or `None`
            The guild where the user's top role will be looked up.
            
            Can be given as `None`.
        default : `Any`
            If the user is not a member of the guild, or if has no roles there, then the given default value is returned.
            Defaults to `None`.
        
        Returns
        -------
        top_role ``Role`` or `default`
        """
        return default
    
    
    def can_use_emoji(self, emoji):
        """
        Returns whether the user can use the given emoji.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to check.
        
        Returns
        -------
        can_use_emoji : `bool`
        """
        if emoji.is_unicode_emoji():
            return True
        
        return False
    
    
    def has_higher_role_than(self, role):
        """
        Returns whether the user has higher role than the given role at it's respective guild.
        
        If the user is the owner of the guild, then returns `True` even if it has lower role.
        
        Parameters
        ----------
        role : ``Role``
            The role to check.
        
        Returns
        -------
        has_higher_role_than : `bool`
        """
        return False
    
    
    def has_higher_role_than_at(self, user, guild):
        """
        Returns whether the user has higher role as the other one at the given guild.
        
        Parameters
        ----------
        user : ``User``
            The other user to check.
        guild : ``Guild`` or `None`
            The guild where the users' top roles will be checked.
            
            Can be given as `None`.
        
        Returns
        -------
        has_higher_role_than_at : `bool`
        """
        return False


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
    avatar_type : `bool`
        The user's avatar's type.
    guild_profiles : `dict` of (``Guild``, ``GuildProfile``) items
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
    """
    __slots__ = ('guild_profiles', 'is_bot', 'flags', 'partial', 'thread_profiles')
    
    def _update_no_return(self, data):
        """
        Updates the user with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            User data received from Discord.
        """
        self.name = data['username']
        self.discriminator = int(data['discriminator'])
        
        self._set_avatar(data)
        
        self.flags = UserFlag(data.get('public_flags', 0))
        self.thread_profiles = None
    
    def _update(self, data):
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
        
        +---------------+---------------+
        | Keys          | Values        |
        +===============+===============+
        | avatar        | ``Icon``      |
        +---------------+---------------+
        | discriminator | `int          |
        +---------------+---------------+
        | flags         | ``UserFlag``  |
        +---------------+---------------+
        | name          | `str`         |
        +---------------+---------------+
        """
        old_attributes = {}
        
        name = data['username']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        discriminator = int(data['discriminator'])
        if self.discriminator != discriminator:
            old_attributes['discriminator'] = self.discriminator
            self.discriminator = discriminator
        
        self._update_avatar(data, old_attributes)
        
        flags = data.get('public_flags', 0)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = UserFlag(flags)
        
        return old_attributes
    
    
    @classmethod
    def _update_profile(cls, data, guild):
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
            +-------------------+-----------------------+
            | Keys              | Values                |
            +===================+=======================+
            | boosts_since      | `None` or `datetime`  |
            +-------------------+-----------------------+
            | nick              | `None` or `str`       |
            +-------------------+-----------------------+
            | roles             | `list` of ``Role``    |
            +-------------------+-----------------------+
        """
        user_id = int(data['user']['id'])
        
        try:
            user = USERS[user_id]
        except KeyError:
            user = cls(data, guild)
            return user,{}
        
        try:
            profile = user.guild_profiles[guild]
        except KeyError:
            user.guild_profiles[guild] = GuildProfile(data)
            guild.users[user_id] = user
            return user, {}

        profile._set_joined(data)
        return user, profile._update(data)
    
    
    @classmethod
    def _update_profile_no_return(cls, data, guild):
        """
        First tries to find the user, then it's respective guild profile for the given guild to update it.
        
        If the method cannot find the user, or the respective guild profile, then creates them.
        
        Not like ``._update_profile``, this method not calculates changes.
        
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
                profile = user.guild_profiles[guild]
            except KeyError:
                user.guild_profiles[guild] = GuildProfile(data)
            else:
                profile._update_no_return(data)
        
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
            profile = user.guild_profiles[guild]
        except KeyError:
            guild.users[user_id] = user
            user.guild_profiles[guild] = GuildProfile(guild_profile_data)
        else:
            profile._set_joined(guild_profile_data)
            profile._update_no_return(guild_profile_data)

    
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
        
        guild_profiles = client.guild_profiles
        if (guild_profiles is not None):
            guild_profiles = guild_profiles.copy()
        
        self.guild_profiles = guild_profiles
        self.is_bot = client.is_bot
        self.flags = client.flags
        self.partial = client.partial
        self.thread_profiles = client.thread_profiles.copy()
        
        return self
    
    
    @classmethod
    def _create_empty(cls, user_id):
        """
        Creates a user instance with the given `user_id` and with the default user attributes.
        
        Parameters
        ----------
        user_id : `int`
            The user's id.
        
        Returns
        -------
        self : ``ClientUserBase``
        """
        self = object.__new__(cls)
        self.id = user_id
        self._set_default_attributes()
        return self
    
    
    def _set_default_attributes(self):
        """
        Sets the user's attribute's to their default.
        """
        self.name = ''
        self.discriminator = 0
        self.avatar_hash = 0
        self.avatar_type = ICON_TYPE_NONE
        self.is_bot = False
        self.flags = UserFlag()
        
        self.guild_profiles = {}
        self.partial = True
        self.thread_profiles = None
    
    # if CACHE_PRESENCE is False, this should be never called from this class
    def _update_presence(self, data):
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
    
    
    def _update_presence_no_return(self, data):
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
            guild, profile = guild_profiles.popitem()
            try:
                del guild.users[self.id]
            except KeyError:
                pass
    
    
    @copy_docs(UserBase.color_at)
    def color_at(self, guild):
        if (guild is not None):
            try:
                profile = self.guild_profiles[guild]
            except KeyError:
                pass
            else:
                return profile.color
        
        return Color()
    
    
    @copy_docs(UserBase.name_at)
    def name_at(self, guild):
        if (guild is not None):
            try:
                profile = self.guild_profiles[guild]
            except KeyError:
                pass
            else:
                nick = profile.nick
                if nick is not None:
                    return nick
        
        return self.name
    
    
    @copy_docs(UserBase.has_role)
    def has_role(self, role):
        # if role is deleted, it's guild is None
        guild = role.guild
        if guild is None:
            return False
        
        try:
            profile = self.guild_profiles[guild]
        except KeyError:
            return False
        
        roles = profile.roles
        if roles is None:
            return False
        
        return (role in profile.roles)
    
    
    @copy_docs(UserBase.top_role_at)
    def top_role_at(self, guild, default=None):
        if (guild is not None):
            try:
                profile = self.guild_profiles[guild]
            except KeyError:
                pass
            else:
                return profile.get_top_role(default)
        
        return default
    
    
    @copy_docs(UserBase.can_use_emoji)
    def can_use_emoji(self, emoji):
        if emoji.is_unicode_emoji():
            return True
        
        guild = emoji.guild
        if guild is None:
            return False
        
        try:
            profile = self.guild_profiles[guild]
        except KeyError:
            return False
        
        emoji_roles = emoji.roles
        if (emoji_roles is None):
            return True
        
        if guild.owner_id == self.id:
            return True
        
        profile_roles = profile.roles
        if (profile_roles is None):
            return False
        
        if emoji_roles.isdisjoint(profile_roles):
            return False
        
        return True
    
    
    @copy_docs(UserBase.has_higher_role_than)
    def has_higher_role_than(self, role):
        guild = role.guild
        if guild is None:
            return False
        
        try:
            profile = self.guild_profiles[guild]
        except KeyError:
            return False
        
        if guild.owner_id == self.id:
            return True
        
        top_role = profile.get_top_role()
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
            own_profile = self.guild_profiles[guild]
        except KeyError:
            return False
        
        if guild.owner_id == self.id:
            return True
        
        try:
            other_profile = user.guild_profiles[guild]
        except KeyError:
            # We always have higher permissions if the other user is not in the guild or if it is a webhook.
            # webhook_guild = getattr(user, 'guild', None)
            # if (webhook_guild is not guild):
            #     return True
            #
            # if (own_profile.roles is not None):
            #    return True
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
    avatar_type : `bool`
        The user's avatar's type.
    guild_profiles : `dict` of (``Guild``, ``GuildProfile``) items
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
    
    @copy_docs(ClientUserBase._update_presence)
    def _update_presence(self, data):
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
                    activity = create_activity(activity_data)
                    
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
                        
                        activity_old_attributes = activity._update(activity_data)
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
                        activity = create_activity(activity_data)
                        
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
    
    @copy_docs(ClientUserBase._update_presence_no_return)
    def _update_presence_no_return(self, data):
        self.status = Status.get(data['status'])
        
        try:
            # not included sometimes
            self.statuses = data['client_status']
        except KeyError:
            pass
        
        activity_datas = data['activities']
        if activity_datas:
            new_activities = [create_activity(activity_data) for activity_data in activity_datas]
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
    avatar_type : `bool`
        The user's avatar's type.
    guild_profiles : `dict` of (``Guild``, ``GuildProfile``) items
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
    status : `Status`
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
                self.status = Status.offline
                self.statuses = {}
                self.activities = None
                update = True
                
                USERS[user_id] = self
            else:
                update = self.partial
            
            if update:
                self.partial = False
                self.is_bot = user_data.get('bot', False)
                self._update_no_return(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                try:
                    profile = self.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id] = self
                    self.guild_profiles[guild] = GuildProfile(guild_profile_data)
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
                update = True
                
                USERS[user_id] = self
            else:
                update = self.partial
            
            if update:
                self.partial = False
                self.is_bot = user_data.get('bot', False)
                self._update_no_return(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                try:
                    profile = self.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id] = self
                    self.guild_profiles[guild] = GuildProfile(guild_profile_data)
                else:
                    profile._set_joined(guild_profile_data)
                    
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
                
                USERS[user_id] = self
            
            self.partial = False
            self.is_bot = user_data.get('bot', False)
            self._update_no_return(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                self.guild_profiles[guild] = GuildProfile(guild_profile_data)
            
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
        user : ``User`` or ``Client``
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
        **kwargs : keyword arguments
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
        flags : ``UserFlag`` or `int` instance, Optional (Keyword only)
            The user's ``.flags``. If not passed as ``UserFlag``, then will be converted to it.
        
        Returns
        -------
        user : ``User`` or ``Client``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
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
                user = USERS[user_id]
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = {}
                user.status = Status.offline
                user.statuses = {}
                user.activities = None
                
                USERS[user_id] = user
            
            user.partial = False
            user.is_bot = user_data.get('bot', False)
            user._update_no_return(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                try:
                    profile = user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id] = user
                    user.guild_profiles[guild] = GuildProfile(guild_profile_data)
                else:
                    profile._set_joined(guild_profile_data)
                    profile._update_no_return(guild_profile_data)
            
            return user
        
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
                user = USERS[user_id]
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = {}
                
                USERS[user_id] = user
            
            user.partial = False
            user.is_bot = user_data.get('bot', False)
            user._update_no_return(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                try:
                    profile = user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id] = user
                    user.guild_profiles[guild] = GuildProfile(guild_profile_data)
                else:
                    profile._set_joined(guild_profile_data)
                    profile._update_no_return(guild_profile_data)
            
            return user
        
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
                user = USERS[user_id]
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = {}
                
                USERS[user_id] = user
            
            user.partial = False
            user.is_bot = user_data.get('bot', False)
            user._update_no_return(user_data)
            
            if (guild_profile_data is not None) and (guild is not None):
                user.guild_profiles[guild] = GuildProfile(guild_profile_data)
            
            return user
    
    if DOCS_ENABLED:
        _create_and_update.__doc__ = (
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
        user : ``User`` or ``Client``
        """)


class ActivityChange:
    """
    Represents a user's changed activities.
    
    Attributes
    ----------
    added : `None` or `list` of ``ActivityBase``
        The added activities to the respective user. Defaults to `None`.
    updated : `None` or `list` of ``ActivityUpdate``
        The updated activities of the respective user. Defaults to `None`.
    removed: `None` or `list` of ``ActivityBase``
        The removed activities from the respective user. Defaults to `None`.
    """
    __slots__ = ('added', 'updated', 'removed',)
    
    def __init__(self, added, updated, removed):
        """
        Creates a new activity change with the given parameters.
        
        added : `None` or `list` of ``ActivityBase``
            The added activities to the user.
        updated : `None` or `list` of ``ActivityUpdate``
            The updated activities of the user.
        removed: `None` or `list` of ``ActivityBase``
            The removed activities from the user.
        """
        self.added = added
        self.updated = updated
        self.removed = removed
    
    def __repr__(self):
        """Returns the representation of the activity change."""
        result = ['<',
            self.__class__.__name__,
        ]
        
        added = self.added
        if added is None:
            put_comma = False
        else:
            result.append(' added=')
            result.append(repr(added))
            put_comma = True
        
        updated = self.updated
        if (updated is not None):
            if put_comma:
                result.append(',')
            else:
                put_comma = True
            
            result.append(' updated=')
            result.append(repr(updated))
        
        removed = self.removed
        if (removed is not None):
            if put_comma:
                result.append(',')
            
            result.append(' removed=')
            result.append(repr(removed))
        
        result.append('>')
        
        return ''.join(result)
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 3
    
    def __iter__(self):
        """
        Unpacks the activity change.
        
        This method is a generator.
        """
        yield self.added
        yield self.updated
        yield self.removed

class ActivityUpdate:
    """
    Represents an updated activity with storing the activity and it's old updated attributes in a `dict`.
    
    Attributes
    ----------
    activity : ``ActivityBase`` instance
        The updated activity.
    old_attributes : `dict` of (`str`, `Any`) items
        The changed attributes of the activity in `attribute-name` - `old-value` relation. Can contain any of the
        following items:
        
        +-------------------+-----------------------------------+
        | Keys              | Values                            |
        +===================+===================================+
        | application_id    | `int`                             |
        +-------------------+-----------------------------------+
        | assets            | `None` or ``ActivityAssets``      |
        +-------------------+-----------------------------------+
        | created           | `int`                             |
        +-------------------+-----------------------------------+
        | details           | `None` or `str`                   |
        +-------------------+-----------------------------------+
        | emoji             | `None` or ``Emoji``               |
        +-------------------+-----------------------------------+
        | flags             | ``ActivityFlag``                  |
        +-------------------+-----------------------------------+
        | name              | `str`                             |
        +-------------------+-----------------------------------+
        | party             | `None` or ``ActivityParty``       |
        +-------------------+-----------------------------------+
        | secrets           | `None` or ``ActivitySecrets``     |
        +-------------------+-----------------------------------+
        | session_id        | `None` or `str`                   |
        +-------------------+-----------------------------------+
        | state             | `None` or `str`                   |
        +-------------------+-----------------------------------+
        | sync_id           | `None` or `str`                   |
        +-------------------+-----------------------------------+
        | timestamps        | `None` or `ActivityTimestamps``   |
        +-------------------+-----------------------------------+
        | url               | `None` or `str`                   |
        +-------------------+-----------------------------------+
    """
    __slots__ = ('activity', 'old_attributes',)
    
    def __init__(self, activity, old_attributes):
        """
        Creates a new activity change instance with the given parameters.
        
        activity : ``ActivityBase`` instance
            The updated activity.
        old_attributes : `dict` of (`str`, `Any`) items
            The changed attributes of the activity.
        """
        self.activity = activity
        self.old_attributes = old_attributes
    
    def __repr__(self):
        """Returns the representation of the activity update."""
        return f'<{self.__class__.__name__} activity={self.activity!r} changes count={len(self.old_attributes)}>'
    
    def __len__(self):
        """Helper for unpacking if needed."""
        return 2
    
    def __iter__(self):
        """
        Unpacks the activity update.
        
        This method is a generator.
        """
        yield self.activity
        yield self.old_attributes


class VoiceState:
    """
    Represents a user at a ``ChannelVoice``.
    
    Attributes
    ----------
    channel : ``ChannelVoice``
        The channel to where the user is connected to.
    deaf : `bool`
        Whether the user is deafen.
    is_speaker : `bool`
        Whether the user is suppressed inside of the voice channel.
        
        If the channel is a ``ChannelVoice``, it is always `False`, meanwhile it ``ChannelStage`` it can vary.
    mute : `bool`
        Whether the user is muted.
    requested_to_speak_at : `None` or `datetime`
        When the user requested to speak.
        
        Only applicable for ``ChannelStage``-s.
    self_deaf : `bool`
        Whether the user muted everyone else.
    self_mute : `bool`
        Whether the user muted itself.
    self_stream : `bool`
        Whether the user screen shares with the go live option.
    self_video : `bool`
        Whether the user sends video from a camera source.
    session_id : `str`
        The user's voice session id.
    user : ``User`` or ``Client``
        The voice state's respective user. If user caching is disabled it will be set as a partial user.
    """
    __slots__ = ('channel', 'deaf', 'is_speaker', 'mute', 'requested_to_speak_at', 'self_deaf', 'self_mute', 'self_stream',
        'self_video', 'session_id', 'user', )
    def __init__(self, data, channel):
        """
        Creates a ``VoiceState`` object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        channel : ``ChannelVoiceBase``
            The channel of the voice state.
        """
        self.channel = channel
        self.user = create_partial_user_from_id(int(data['user_id']))
        self.session_id = data['session_id']
        self.mute = data['mute']
        self.deaf = data['deaf']
        self.self_deaf = data['self_deaf']
        self.self_mute = data['self_mute']
        self.self_stream = data.get('self_stream', False)
        self.self_video = data['self_video']
        
        requested_to_speak_at = data.get('request_to_speak_timestamp', None)
        if (requested_to_speak_at is not None):
            requested_to_speak_at = parse_time(requested_to_speak_at)
        
        self.is_speaker = not data.get('suppress', False)
        
        self.requested_to_speak_at = requested_to_speak_at
    
    @property
    def guild(self):
        """
        Returns the voice state's respective guild.
        
        Returns
        -------
        guild : `None` or ``Guild``
        """
        return self.channel.guild
    
    def _update(self, data, channel):
        """
        Updates the voice state and returns it's overwritten attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        channel : ``ChannelVoice``
            The channel of the voice state.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dictionary is optional.
        
        Returned Data Structure
        -----------------------
        +-----------------------+-----------------------+
        | Keys                  | Values                |
        +=======================+=======================+
        | channel               | ``ChannelVoice``      |
        +-----------------------+-----------------------+
        | deaf                  | `str`                 |
        +-----------------------+-----------------------+
        | is_speaker            | `bool`                |
        +-----------------------+-----------------------+
        | mute                  | `bool`                |
        +-----------------------+-----------------------+
        | requested_to_speak_at | `None` or `datetime`  |
        +-----------------------+-----------------------+
        | self_deaf             | `bool`                |
        +-----------------------+-----------------------+
        | self_mute             | `bool`                |
        +-----------------------+-----------------------+
        | self_stream           | `bool`                |
        +-----------------------+-----------------------+
        | self_video            | `bool`                |
        +-----------------------+-----------------------+
        """
        old_attributes = {}
        
        if (self.channel is not channel):
            old_attributes['channel'] = self.channel
            self.channel = channel
        
        deaf = data['deaf']
        if self.deaf != deaf:
            old_attributes['deaf'] = self.deaf
            self.deaf = deaf
        
        mute = data['mute']
        if self.mute != mute:
            old_attributes['mute'] = self.mute
            self.mute = mute
        
        self_deaf = data['self_deaf']
        if self.self_deaf != self_deaf:
            old_attributes['self_deaf'] = self.self_deaf
            self.self_deaf = self_deaf
        
        self_video = data['self_video']
        if self.self_video != self_video:
            old_attributes['self_video'] = self.self_video
            self.self_video = self_video
        
        self_stream = data.get('self_stream', False)
        if self.self_stream != self_stream:
            old_attributes['self_stream'] = self.self_stream
            self.self_stream = self_stream
        
        self_mute = data['self_mute']
        if self.self_mute != self_mute:
            old_attributes['self_mute'] = self.self_mute
            self.self_mute = self_mute
        
        requested_to_speak_at = data.get('request_to_speak_timestamp', None)
        if (requested_to_speak_at is not None):
            requested_to_speak_at = parse_time(requested_to_speak_at)
        
        if self.requested_to_speak_at != requested_to_speak_at:
            old_attributes['requested_to_speak_at'] = self.requested_to_speak_at
            self.requested_to_speak_at = requested_to_speak_at
        
        is_speaker = not data.get('suppress', False)
        if self.is_speaker != is_speaker:
            old_attributes['is_speaker'] = self.is_speaker
            self.is_speaker = is_speaker
        
        return old_attributes
    
    def _update_no_return(self, data, channel):
        """
        Updates the voice state with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        channel : ``ChannelVoice``
            The channel of the voice state.
        """
        self.channel = channel
        self.deaf = data['deaf']
        self.mute = data['mute']
        self.self_deaf = data['self_deaf']
        self.self_mute = data['self_mute']
        self.self_stream = data.get('self_stream', False)
        self.self_video = data['self_video']
        
        requested_to_speak_at = data.get('request_to_speak_timestamp', None)
        if (requested_to_speak_at is not None):
            requested_to_speak_at = parse_time(requested_to_speak_at)
        
        self.requested_to_speak_at = requested_to_speak_at
        
        self.is_speaker = not data.get('suppress', False)
    
    def __repr__(self):
        """Returns the voice state's representation."""
        return f'<{self.__class__.__name__} user={self.user.full_name!r}, channel={self.channel!r}>'

ZEROUSER = User._create_empty(0)
