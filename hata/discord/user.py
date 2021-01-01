# -*- coding: utf-8 -*-
__all__ = ('ActivityChange', 'ActivityUpdate', 'GuildProfile', 'User', 'UserBase', 'UserFlag', 'VoiceState', 'ZEROUSER')

from datetime import datetime

from ..env import CACHE_USER, CACHE_PRESENCE

from ..backend.utils import DOCS_ENABLED, WeakKeyDictionary

from .bases import DiscordEntity, FlagBase, IconSlot, ICON_TYPE_NONE
from .client_core import USERS
from .utils import parse_time, DISCORD_EPOCH_START, DATETIME_FORMAT_CODE
from .color import Color
from .activity import ActivityUnknown, create_activity
from .http import URLS
from .preconverters import preconvert_snowflake, preconvert_str, preconvert_bool, preconvert_discriminator, \
    preconvert_flag
from .preinstanced import Status, DefaultAvatar

from . import utils as module_utils

create_partial_role = NotImplemented

if CACHE_USER:
    GUILD_PROFILES_TYPE = dict
else:
    GUILD_PROFILES_TYPE = WeakKeyDictionary

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
    """
    __keys__ = {
        'staff'                     :  0,
        'partner'                   :  1,
        'hypesquad'                 :  2,
        'bug_hunter_level_1'        :  3,
        'mfa_sms'                   :  4,
        'premium_promo_dismissed'   :  5,
        'hypesquad_bravery'         :  6,
        'hypesquad_brilliance'      :  7,
        'hypesquad_balance'         :  8,
        'early_supporter'           :  9,
        'team_user'                 : 10,
        'team_pseudo_user'          : 11,
        'system'                    : 12,
        'has_unread_urgent_messages': 13,
        'bug_hunter_level_2'        : 14,
        'underage_deleted'          : 15,
        'verified_bot'              : 16,
        'early_verified_developer'  : 17,
            }

def create_partial_user(user_id):
    try:
        return USERS[user_id]
    except KeyError:
        pass
    
    return User._create_empty(user_id)

if DOCS_ENABLED:
    create_partial_user.__doc__ = (
    """
    Creates a partial user from the given `user_id`. If the user already exists returns that instead.
    
    Parameters
    ----------
    user_id : `int`
        The unique identifier number of the user.
    
    Returns
    -------
    user : ``Client`` or ``User``
    """)

class GuildProfile(object):
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
    
    def __init__(self, data, guild):
        """
        Creates a ``GuildProfile`` instance from the received guild profile data and from it's respective guild.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        guild : ``Guild``
            The guild profile's respective guild.
        """
        try:
            joined_at_data = data['joined_at']
        except KeyError:
            joined_at = None
        else:
            joined_at = parse_time(joined_at_data)
        
        self.joined_at = joined_at
        
        self._update_no_return(data, guild)
    
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
    
    def _update_no_return(self, data, guild):
        """
        Updates the guild profile with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        guild : ``Guild``
            The guild profile's respective guild.
        """
        self.nick = data.get('nick')
        
        role_ids = data['roles']
        if role_ids:
            guild_roles = guild.roles
            roles = []
            for role_id in role_ids:
                role_id = int(role_id)
                try:
                    role = guild_roles[role_id]
                except KeyError:
                    continue
                
                roles.append(role)
            
            if (not roles):
                roles = None
        else:
            roles = None
        
        self.roles = roles
        
        boosts_since = data.get('premium_since')
        if (boosts_since is not None):
            boosts_since = parse_time(boosts_since)
        self.boosts_since = boosts_since
        
        self.pending = data.get('pending')
    
    def _update(self, data, guild):
        """
        Updates the guild profile and returns it's changed attributes in a `dict` within `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        guild : ``Guild``
            The owner guild of the role.
        
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
        nick = data.get('nick')
        if self.nick != nick:
            old_attributes['nick'] = self.nick
            self.nick = nick
        
        role_ids = data['roles']
        if role_ids:
            guild_roles = guild.roles
            roles = []
            for role_id in role_ids:
                role_id = int(role_id)
                role = create_partial_role(role_id)
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
        
        boosts_since = data.get('premium_since')
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
    
    avatar = IconSlot('avatar', 'avatar', URLS.user_avatar_url, URLS.user_avatar_url_as)
    
    def __init_subclass__(cls):
        """Replaces some methods of the subclasses depending on their instance attributes."""
        rich = cls.__rich__
        if 'guild_profiles' in cls.__slots__:
            cls.color_at = rich.color_at
            cls.name_at = rich.name_at
            cls.has_role = rich.has_role
            cls.top_role_at = rich.top_role_at
            cls.can_use_emoji = rich.can_use_emoji
            cls.has_higher_role_than = rich.has_higher_role_than
            cls.has_higher_role_than_at = rich.has_higher_role_than_at
        
        if 'activities' in cls.__slots__:
            cls.activity = rich.activity
        
        if 'statuses' in cls.__slots__:
            cls.platform = rich.platform
        
        # webhook type
        if hasattr(cls, 'guild'):
            cls.can_use_emoji = rich.can_use_emoji__w_guild
    
    def __str__(self):
        """Returns the user's name."""
        return self.name
    
    def __repr__(self):
        """Returns the user's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        if self.partial:
            result.append(' partial')
        else:
            result.append(' name=')
            result.append(repr(self.full_name))
        
        result.append(', id=')
        result.append(repr(self.id))
        result.append('>')
        
        return ''.join(result)
    
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
        ```
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
        guild_profiles : `dict` or ``WeakKeyDictionary`` of (``Guild``, ``GuildProfile``) items
        """
        return GUILD_PROFILES_TYPE()
    
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
        Returns the user's top activity if applicable. If not, returns ``ActivityUnknown``.
        
        Returns
        -------
        activity : ``ActivityBase`` instance
        """
        return ActivityUnknown
    
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
    
    class __rich__:
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
            if (guild is not None):
                try:
                    profile = self.guild_profiles[guild]
                except KeyError:
                    pass
                else:
                    return profile.color
            
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
        
        @property
        def activity(self):
            """
            Returns the user's top activity if applicable. If not, returns ``ActivityUnknown``.
            
            Returns
            -------
            activity : ``ActivityBase`` instance
            """
            activities = self.activities
            if activities is None:
                activity = ActivityUnknown
            else:
                activity = activities[0]
            return activity
        
        @property
        def platform(self):
            """
            Returns the user's top status's platform. If the user is offline it will return `an empty string.
            
            Returns
            -------
            platform : `str`
            """
            statuses = self.statuses
            if statuses:
                status = self.status.value
                for platform, l_status in statuses.items():
                    if l_status == status:
                        return platform
            return ''
        
        def has_role(self,role):
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
        
        def top_role_at(self, guild, default=None):
            """
            Returns the top role of the user at the given guild.
            
            Parameters
            ----------
            guild : ``Guild`` or `None`
                The guild where the user's top role will be looked up.
                
                Can be given as `None`.
            default : `Any`
                If the user is not a member of the guild, or if has no roles there, the given default value is returned.
                Defaults to `None`.
            
            Returns
            -------
            top_role ``Role`` or `default`
            """
            if (guild is not None):
                try:
                    profile = self.guild_profiles[guild]
                except KeyError:
                    pass
                else:
                    return profile.get_top_role(default)
            
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
        
        # For ``UserBase`` subclasses with `.guild` instance attribute
        def can_use_emoji__w_guild(self, emoji):
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
            
            guild = emoji.guild
            if guild is None:
                return False
            
            webhook_guild = self.guild
            if webhook_guild is None:
                return False
            
            emoji_roles = emoji.emoji_roles
            if (emoji_roles is None):
                return True
            
            return False
        
        def has_higher_role_than(self, role):
            """
            Returns whether the user has higher role than the given role at it's respective guild.
            
            If the user is the owner of the guild, then returns `True` even if the role check fails.
            
            Parameters
            ----------
            role : ``Role``
                The role to check.
            
            Returns
            -------
            has_higher_role_than : `bool`
            """
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
            
            if top_role>role:
                return True
            
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
                # Is the other user a Webhook?
                webhook_guild = getattr(user, 'guild', None)
                if (webhook_guild is not guild):
                    # Not webhook or partial webhook, or a webhook of a different guild
                    return False
                
                # If we have any roles, we have more role than a webhook with 0
                if (own_profile.roles is not None):
                    return True
                
                return False
            
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

class User(UserBase):
    if DOCS_ENABLED: __doc__ = ''.join([
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
    guild_profiles : `dict` or ``WeakKeyDictionary`` of (``Guild``, ``GuildProfile``) items
        A dictionary, which contains the user's guild profiles. If a user is member of a guild, then it should
        have a respective guild profile accordingly.
    is_bot : `bool`
        Whether the user is a bot or a user account.
    flags : ``UserFlag``
        The user's user flags.
    partial : `bool`
        Partial users have only their `.id` set and every other field might not reflect the reality.""", """
    activities : `None` or `list` of ``ActivityBase`` instances
        A list of the client's activities. Defaults to `None`
    status : `Status`
        The user's display status.
    statuses : `dict` of (`str`, `str`) items
        The user's statuses for each platform.
    """ if CACHE_PRESENCE else "", """
    
    Notes
    -----
    Instances of this class are weakreferable.
    """])
    
    if CACHE_PRESENCE:
        __slots__ = ('guild_profiles', 'is_bot', 'flags', 'partial', #default User
            'activities', 'status', 'statuses', ) #Presence
    else:
        __slots__ = ('guild_profiles', 'is_bot', 'flags', 'partial', ) #default User
    
    if CACHE_PRESENCE:
        def __new__(cls, data, guild=None):
            try:
                user_data = data['user']
            except KeyError:
                user_data = data
                member_data = data.get('member')
            else:
                member_data = data
            
            user_id = int(user_data['id'])
            
            try:
                user = USERS[user_id]
                update = user.partial
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = GUILD_PROFILES_TYPE()
                user.status = Status.offline
                user.statuses = {}
                user.activities = None
                update = True
                
                USERS[user_id] = user
            
            if update:
                user.partial = False
                user.is_bot = user_data.get('bot', False)
                user._update_no_return(user_data)
            
            if (member_data is not None) and (guild is not None):
                try:
                    profile = user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id] = user
                    user.guild_profiles[guild] = GuildProfile(member_data, guild)
                else:
                    profile._set_joined(member_data)
            
            return user
            
    elif CACHE_USER:
        def __new__(cls, data, guild=None):
            try:
                user_data = data['user']
                member_data = data
            except KeyError:
                user_data = data
                member_data = data.get('member')
                
            user_id = int(user_data['id'])

            try:
                user = USERS[user_id]
                update = user.partial
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = GUILD_PROFILES_TYPE()
                update = True
                
                USERS[user_id] = user

            if update:
                user.partial = False
                user.is_bot = user_data.get('bot', False)
                user._update_no_return(user_data)

            if (member_data is not None) and (guild is not None):
                try:
                    profile = user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id] = user
                    user.guild_profiles[guild] = GuildProfile(member_data, guild)
                else:
                    profile._set_joined(member_data)
                    
            return user
    
    else:
        def __new__(cls, data, guild=None):
            try:
                user_data = data['user']
                member_data = data
            except KeyError:
                user_data = data
                member_data = data.get('member')
            
            user_id = int(user_data['id'])
            
            try:
                user = USERS[user_id]
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = GUILD_PROFILES_TYPE()
                
                USERS[user_id] = user
            
            user.partial = False
            user.is_bot = user_data.get('bot', False)
            user._update_no_return(user_data)
            
            if (member_data is not None) and (guild is not None):
                user.guild_profiles[guild] = GuildProfile(member_data, guild)
            
            return user
    
    if DOCS_ENABLED:
        __new__.__doc__ = (
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
    
    if (not CACHE_PRESENCE):
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
            member_data = data
            
            user_id = int(user_data['id'])
            
            try:
                user = USERS[user_id]
            except KeyError:
                return
            
            try:
                profile = user.guild_profiles[guild]
            except KeyError:
                guild.users[user_id] = user
                user.guild_profiles[guild] = GuildProfile(member_data, guild)
            else:
                profile._set_joined(member_data)
                profile._update_no_return(member_data, guild)
    
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
        name : `str`, Optional
            The user's ``.name``.
        discriminator : `int` or `str` instance, Optional
            The user's ``.discriminator``. Is accepted as `str` instance as well and will be converted to `int`.
        avatar : `None`, ``Icon`` or `str`, Optional
            The user's avatar. Mutually exclusive with `avatar_type` and `avatar_hash`.
        avatar_type : ``IconType``, Optional
            The user's avatar's type. Mutually exclusive with `avatar_type`.
        avatar_hash : `int`, Optional
            The user's avatar hash. Mutually exclusive with `avatar`.
        flags : ``UserFlag`` or `int` instance, Optional
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
                processable.append(('name',name))
            
            try:
                discriminator = kwargs.pop('discriminator')
            except KeyError:
                pass
            else:
                discriminator = preconvert_discriminator(discriminator)
                processable.append(('discriminator',discriminator))
            
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
        
        user = create_partial_user(user_id)
        if not user.partial:
            return user
        
        if (processable is not None):
            for item in processable:
                setattr(user, *item)
        
        return user
    
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
    
    if CACHE_PRESENCE:
        @classmethod
        def _create_and_update(cls, data, guild=None):
            try:
                user_data = data['user']
                member_data = data
            except KeyError:
                user_data = data
                member_data = None
            
            user_id = int(user_data['id'])
            
            try:
                user = USERS[user_id]
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = GUILD_PROFILES_TYPE()
                user.status = Status.offline
                user.statuses = {}
                user.activities = None
                
                USERS[user_id] = user
            
            user.partial = False
            user.is_bot = user_data.get('bot', False)
            user._update_no_return(user_data)
            
            if (member_data is not None) and (guild is not None):
                try:
                    profile = user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id] = user
                    user.guild_profiles[guild] = GuildProfile(member_data, guild)
                else:
                    profile._set_joined(member_data)
                    profile._update_no_return(member_data, guild)
            
            return user
        
    elif CACHE_USER:
        @classmethod
        def _create_and_update(cls, data, guild=None):
            try:
                user_data = data['user']
                member_data = data
            except KeyError:
                user_data = data
                member_data = None
            
            user_id = int(user_data['id'])
            
            try:
                user = USERS[user_id]
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = GUILD_PROFILES_TYPE()
                
                USERS[user_id] = user
            
            user.partial = False
            user.is_bot = user_data.get('bot', False)
            user._update_no_return(user_data)
            
            if (member_data is not None) and (guild is not None):
                try:
                    profile = user.guild_profiles[guild]
                except KeyError:
                    guild.users[user_id] = user
                    user.guild_profiles[guild] = GuildProfile(member_data, guild)
                else:
                    profile._set_joined(member_data)
                    profile._update_no_return(member_data, guild)
            
            return user
        
    else:
        @classmethod
        def _create_and_update(cls, data, guild=None):
            try:
                user_data = data['user']
            except KeyError:
                user_data = data
                member_data = None
            else:
                member_data = data
            
            user_id = int(user_data['id'])
            
            try:
                user = USERS[user_id]
            except KeyError:
                user = object.__new__(cls)
                user.id = user_id
                user.guild_profiles = GUILD_PROFILES_TYPE()
                
                USERS[user_id] = user
            
            user.partial = False
            user.is_bot = user_data.get('bot', False)
            user._update_no_return(user_data)
            
            if (member_data is not None) and (guild is not None):
                user.guild_profiles[guild] = GuildProfile(member_data, guild)
            
            return user
    
    if DOCS_ENABLED:
        __new__.__doc__ = (
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
    
    def _delete(self):
        """
        Deletes the user from it's guilds.
        """
        #we cannot full delete a user, because of the mentions, so we delete it only from the guilds
        guild_profiles = self.guild_profiles
        while guild_profiles:
            guild, profile = guild_profiles.popitem()
            try:
                del guild.users[self.id]
            except KeyError:
                pass
    
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
    
    def _update_presence_no_return(self, data):
        """
        Updates the user's presences with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild member data.
        """
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
            user.guild_profiles[guild] = GuildProfile(data, guild)
            guild.users[user_id] = user
            return user, {}

        profile._set_joined(data)
        return user, profile._update(data, guild)
    
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
                user.guild_profiles[guild] = GuildProfile(data, guild)
            else:
                profile._update_no_return(data, guild)
        
        return user
    
    if CACHE_PRESENCE:
        @classmethod
        def _create_empty(cls, user_id):
            user = object.__new__(cls)
            user.id = user_id
            
            user.name = ''
            user.discriminator = 0
            user.avatar_hash = 0
            user.avatar_type = ICON_TYPE_NONE
            user.is_bot = False
            user.flags = UserFlag()
            
            user.guild_profiles = GUILD_PROFILES_TYPE()
            user.partial = True
            
            user.status = Status.offline
            user.statuses = {}
            user.activities = None
            
            return user
    
    else:
        @classmethod
        def _create_empty(cls, user_id):
            user = object.__new__(cls)
            user.id = user_id
            
            user.name = ''
            user.discriminator = 0
            user.avatar_hash = 0
            user.avatar_type = ICON_TYPE_NONE
            user.is_bot = False
            user.flags = UserFlag()
            
            user.guild_profiles = GUILD_PROFILES_TYPE()
            user.partial = True
            
            return user
    
    if DOCS_ENABLED:
        _create_empty.__doc__ = (
        """
        Creates a user instance with the given `user_id` and with the default user attributes.
        
        Parameters
        ----------
        user_id : `int`
            The user's id.
        """)

class ActivityChange(object):
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

class ActivityUpdate(object):
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


class VoiceState(object):
    """
    Represents a user at a ``ChannelVoice``.
    
    Attributes
    ----------
    channel : ``ChannelVoice``
        The channel to where the user is connected to.
    deaf : `bool`
        Whether the user is deafen.
    mute : `bool`
        Whether the user is muted.
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
    __slots__ = ('channel', 'deaf', 'mute', 'self_deaf', 'self_mute', 'self_stream', 'self_video', 'session_id', 'user')
    def __init__(self, data, channel):
        """
        Creates a ``VoiceState`` object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice state data received from Discord.
        channel : ``ChannelVoice``
            The channel of the voice state.
        """
        self.channel = channel
        self.user = create_partial_user(int(data['user_id']))
        self.session_id = data['session_id']
        self.mute = data['mute']
        self.deaf = data['deaf']
        self.self_deaf = data['self_deaf']
        self.self_mute = data['self_mute']
        self.self_stream = data.get('self_stream', False)
        self.self_video = data['self_video']
    
    @property
    def guild(self):
        """
        Returns the voice state's respective guild
        
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
        +---------------+-------------------+
        | Keys          | Values            |
        +===============+===================+
        | channel       | ``ChannelVoice``  |
        +---------------+-------------------+
        | deaf          | `str`             |
        +---------------+-------------------+
        | mute          | `bool`            |
        +---------------+-------------------+
        | self_deaf     | `bool`            |
        +---------------+-------------------+
        | self_mute     | `bool`            |
        +---------------+-------------------+
        | self_stream   | `bool`            |
        +---------------+-------------------+
        | self_video    | `bool`            |
        +---------------+-------------------+
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
    
    def __repr__(self):
        """Returns the voice state's representation."""
        return f'<{self.__class__.__name__} user={self.user.full_name!r}, channel={self.channel!r}>'

ZEROUSER = User._create_empty(0)

module_utils.create_partial_user = create_partial_user

del URLS
del CACHE_USER
del CACHE_PRESENCE
del DiscordEntity
del FlagBase
del IconSlot
del module_utils
del DOCS_ENABLED
