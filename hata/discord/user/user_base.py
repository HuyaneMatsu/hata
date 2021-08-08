__all__ = ('UserBase', )

from ...backend.export import include

from ..bases import DiscordEntity, IconSlot, ICON_TYPE_NONE
from ..utils import DATETIME_FORMAT_CODE
from ..color import Color

from ..http import urls as module_urls

from .preinstanced import Status, DefaultAvatar
from .flags import UserFlag
from .helpers import get_banner_color_from_data

create_partial_role_from_id = include('create_partial_role_from_id')
Client = include('Client')


class UserBase(DiscordEntity, immortal=True):
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
    banner_color : `None` or ``Color``
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
        | banner_color  | `None` or ``Color``   |
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
        guild_profiles : `dict` of (`int`, ``GuildProfile``) items
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
            guild = message.guild
            if (guild is not None):
                try:
                    guild_profile = self.guild_profiles[guild.id]
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
    
    
    def get_guild_profile_for(self, guild):
        """
        Returns the user's guild profile for the given guild.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild to get guild profile for.
        
        Returns
        -------
        guild_profile : `None` or ``Guild``
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
    
    
    avatar_url_for = property(module_urls.user_avatar_url_for)
    avatar_url_for_as = module_urls.user_avatar_url_for_as
    avatar_url_at = property(module_urls.user_avatar_url_at)
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
