__all__ = ('UserBase', )

import warnings
from re import I as re_ignore_case, escape as re_escape, search as re_search

from scarletio import export, include

from ..bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ..color import Color
from ..core import GUILDS
from ..http import urls as module_urls
from ..utils import DATETIME_FORMAT_CODE

from .flags import UserFlag
from .helpers import get_banner_color_from_data
from .preinstanced import DefaultAvatar, Status


create_partial_role_from_id = include('create_partial_role_from_id')
Client = include('Client')
Guild = include('Guild')

@export
def _try_get_guild_id(guild):
    """
    Tries to get the guild's identifier.
    
    Parameters
    ----------
    guild : `None`, `int`, ``Guild``
        The guild or it's identifier.
    
    Returns
    -------
    guild_id : `int`
        The guild's identifier. Defaults to `0`.
    """
    if isinstance(guild, int):
        guild_id = guild
    elif guild is None:
        guild_id = 0
    elif isinstance(guild, Guild):
        guild_id = guild.id
    else:
        guild_id = 0
    
    return guild_id


def _try_get_guild_and_id(guild):
    """
    Tries to get the guild and it's identifier.
    
    Parameters
    ----------
    guild : `None`, `int`, ``Guild``
        The guild or it's identifier.
    
    Returns
    -------
    guild : `None`, ``Guild``
        The guild if found.
    guild_id : `int`
        The guild's identifier. Defaults to `0`.
    """
    if isinstance(guild, int):
        guild_id = guild
        guild = GUILDS.get(guild_id)
    elif guild is None:
        guild_id = 0
    elif isinstance(guild, Guild):
        guild_id = guild.id
    else:
        guild_id = 0
        guild = None
    
    return guild, guild_id


class UserBase(DiscordEntity, immortal = True):
    """
    Base class for user instances.
    
    Attributes
    ----------
    id : `int`
        The client's unique identifier number.
    name : str
        The client's username.
    discriminator : `int`
        The client's discriminator. Given to avoid overlapping names.
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The user's avatar's type.
    banner_color : `None`, ``Color``
        The user's banner color if has any.
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    banner_type : ``IconType``
        The user's banner's type.
    
    Notes
    -----
    Instances of this class are weakreferable.
    """
    __slots__ = ('banner_color', 'name', 'discriminator', )
    
    avatar = IconSlot('avatar', 'avatar', module_urls.user_avatar_url, module_urls.user_avatar_url_as)
    banner = IconSlot('banner', 'banner', module_urls.user_banner_url, module_urls.user_banner_url_as)
    
    
    def __new__(cls, *positional_parameters, **keyword_parameters):
        raise NotImplementedError
    
    
    def _update_attributes(self, data):
        """
        Updates the user with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            User data received from Discord.
        """
        try:
            name = data['username']
        except KeyError:
            # Webhook?
            name = data.get('name', None)
            if (name is None):
                name = ''
        
        self.name = name
        
        try:
            discriminator = data['discriminator']
        except KeyError:
            discriminator = 0
        else:
            discriminator = int(discriminator)
        self.discriminator = discriminator
        
        self._set_avatar(data)
        self._set_banner(data)
        
        self.banner_color = get_banner_color_from_data(data)
    
    
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
        | banner_color  | `None`, ``Color``     |
        +---------------+-----------------------+
        | discriminator | `int`                 |
        +---------------+-----------------------+
        | name          | `str`                 |
        +---------------+-----------------------+
        """
        old_attributes = {}
        
        try:
            name = data['username']
        except KeyError:
            # Webhook?
            name = data.get('name', None)
            if (name is None):
                name = ''
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        
        discriminator = int(data['discriminator'])
        if self.discriminator != discriminator:
            old_attributes['discriminator'] = self.discriminator
            self.discriminator = discriminator
        
        
        self._update_avatar(data, old_attributes)
        self._update_banner(data, old_attributes)
        
        
        banner_color = get_banner_color_from_data(data)
        if self.banner_color != banner_color:
            old_attributes['banner_color'] = self.banner_color
            self.banner_color = banner_color
        
        return old_attributes
    
    
    def __repr__(self):
        """Returns the user's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        repr_parts.append(' id=')
        repr_parts.append(repr(self.id))
        
        if self.partial:
            repr_parts.append(' (partial)')
        else:
            repr_parts.append(', name=')
            repr_parts.append(repr(self.full_name))
        
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
        >>> # no code stands for `user.name`.
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
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"f"!r}, {"m"!r}.'
        )
    
    
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
    
    @activities.setter
    def activities(self, value):
        pass
    
    
    def iter_activities(self):
        """
        Iterates over the user's activities.
        
        This method is an iterable generator.
        
        Yields
        ------
        activity : ``Activity``
        """
        activities = self.activities
        if (activities is not None):
            yield from activities
    
    
    @property
    def status(self):
        """
        Returns the user's display status.
        
        Returns
        -------
        status  ``Status``
        """
        return Status.offline
    
    @status.setter
    def status(self, value):
        pass
    
    
    @property
    def statuses(self):
        """
        Returns the user's statuses for each platform.
        
        Returns
        -------
        statuses : `dict` of (`str`, `str`) items
        """
        return {}
    
    @statuses.setter
    def statuses(self, value):
        pass
    
    
    @property
    def guild_profiles(self):
        """
        Returns a dictionary, which contains the user's guild profiles. If the user is member of a guild, then it should
        have a respective guild profile accordingly.
        
        Returns
        -------
        guild_profiles : `dict` of (`int`, ``GuildProfile``) items
        """
        return {}
    
    @guild_profiles.setter
    def guild_profiles(self, value):
        pass
    
    
    @property
    def thread_profiles(self):
        """
        A Dictionary which contains the thread profiles for the user in thread channel - thread profile relation.
        Defaults to `None`.
        
        Returns
        -------
        thread_profiles : `None`, `dict` (``Channel``, ``ThreadProfile``) items
        """
        return None
    
    @thread_profiles.setter
    def thread_profiles(self, value):
        pass
    
    
    @property
    def is_bot(self):
        """
        Returns whether the user is a bot or a user account.
        
        This property is deprecated and will be removed in 2023 August.
        
        Returns
        -------
        bot : `bool`
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_bot` is deprecated and will be removed in 2023 August.'
                f'Please use `.bot` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.bot
    
    
    @property
    def bot(self):
        """
        Returns whether the user is a bot or a user account.
        
        Returns
        -------
        bot : `bool`
        """
        return False
    
    @bot.setter
    def bot(self, value):
        pass
    
    
    @property
    def flags(self):
        """
        Returns the user's flags.
        
        Returns
        -------
        flags : ``UserFlag``
        """
        return UserFlag()
    
    @flags.setter
    def flags(self, value):
        pass
    
    
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
        activity : ``Activity``, `None`
        """
        return None
    
    
    @property
    def custom_activity(self):
        """
        Returns the user's custom activity if applicable.
        
        Returns
        -------
        activity : ``Activity``, `None`
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
        guild : `None`, ``Guild``, `int`
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
        guild : `None`, ``Guild``, `int`
            The guild, where the user's nick will be checked.
            
            Can be given as `None`.

        Returns
        -------
        name : `str`
        """
        return self.name
    
    
    def has_name_like(self, name):
        """
        Returns whether the user's name is like the given string.
        
        Parameters
        ----------
        name : `str`
            The name of the user.
        
        Returns
        -------
        has_name_like : `bool`
        """
        if name.startswith('@'):
            name = name[1:]
        
        name_length = len(name)
        if name_length < 1:
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
        
        if re_search(re_escape(name), self.name, re_ignore_case) is None:
            return False
        
        return True
    
    
    def has_name_like_at(self, name, guild):
        """
        Returns whether the user's name is like the given string.
        
        Parameters
        ----------
        name : `str`
            The name of the user.
        
        guild : `None`, ``Guild``, `int`
            The guild, where the user's nick will be also checked.
            
            Can be given as `None`.
        
        Returns
        -------
        has_name_like : `bool`
        """
        return self.has_name_like(name)
    
    
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
            guild_id = message.guild_id
            if guild_id:
                try:
                    guild_profile = self.guild_profiles[guild_id]
                except KeyError:
                    pass
                else:
                    roles = guild_profile.roles
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
    
    
    def top_role_at(self, guild, default = None):
        """
        Returns the top role of the user at the given guild.
        
        Parameters
        ----------
        guild : `None`, ``Guild``, `int`
            The guild where the user's top role will be looked up.
        
        default : `Any` = `None`, Optional
            If the user is not a member of the guild, or if has no roles there, then the given default value is returned.
            Defaults to `None`.
        
        Returns
        -------
        top_role ``Role``, `default`
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
        guild : ``Guild``, `None`, `int`
            The guild where the users' top roles will be checked.
            
            Can be given as `None`.
        
        Returns
        -------
        has_higher_role_than_at : `bool`
        """
        return False
    
    
    def get_guild_profile_for(self, guild):
        """
        Returns the user's guild profile for the given guild.
        
        Parameters
        ----------
        guild : `None`, ``Guild``, `int`
            The guild to get guild profile for.
        
        Returns
        -------
        guild_profile : `None`, ``Guild``
        """
        return None
    
    
    def iter_guild_profiles(self):
        """
        Iterates over the guild profiles of the user.
        
        This method is an iterable generator.
        
        Yields
        ------
        guild : ``Guild``
            The guild profile's guild.
        guild_profile : ``GuildProfile``
            The user's guild profile in the guild.
        """
        return
        yield
    
    
    def is_boosting(self, guild):
        """
        Returns whether the user is boosting the given guild.
        
        Parameters
        ----------
        guild : `None`, ``Guild``, `int`
            The guild to get whether the user is booster of.
        
        Returns
        -------
        is_boosting : `bool`
        """
        return False
    
    
    avatar_url_for = module_urls.user_avatar_url_for
    avatar_url_for_as = module_urls.user_avatar_url_for_as
    avatar_url_at = module_urls.user_avatar_url_at
    avatar_url_at_as = module_urls.user_avatar_url_at_as
    
    
    @classmethod
    def _create_empty(cls, user_id):
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
        self.banner_color = None
        self.banner_hash = 0
        self.banner_type = ICON_TYPE_NONE
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Tries to convert the user back to a json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = {}
        
        # id
        data['id'] = str(self.id)
        
        # name
        data['name'] = self.name
        
        # discriminator
        data['discriminator'] = str(self.discriminator)
        
        # avatar
        data['avatar'] = self.avatar.as_base_16_hash
        
        # banner
        data['banner'] = self.banner.as_base_16_hash
        
        # banner color
        banner_color = self.banner_color
        if (banner_color is not None):
            banner_color = int(banner_color)
        data['accent_color'] = banner_color
        
        # bot
        if self.bot:
            data['bot'] = True
        
        # flags
        data['flags'] = int(self.flags)
        
        return data
    
    
    def copy(self):
        """
        Copies the user. (Not implemented)
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return self
