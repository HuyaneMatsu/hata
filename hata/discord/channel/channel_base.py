__all__ = ('ChannelBase',)

import re

from ...backend.export import export

from ..bases import DiscordEntity
from ..permission import Permission
from ..permission.permission import PERMISSION_NONE
from ..user import User
from ..utils import DATETIME_FORMAT_CODE

@export
class ChannelBase(DiscordEntity, immortal=True):
    """
    Base class for Discord channels.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the channel.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `0`
        The default type, what the channel represents.
    INTERCHANGE : `tuple` of `int` = `()`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    
    Notes
    -----
    Channels support weakreferencing.
    """
    DEFAULT_TYPE = 0
    INTERCHANGE = ()
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a new channel from the channel data received from Discord. If the channel already exists and if it
        is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        
        Raises
        -------
        RuntimeError
            The respective channel type cannot be instanced.
        """
        raise RuntimeError(f'`{cls.__name__}` cannot be instanced.')
    
    def __repr__(self):
        """Returns the representation of the channel."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.__str__()!r}>'
    
    def __str__(self):
        """Returns the channel's name."""
        return ''
    
    def __format__(self, code):
        """
        Formats the channel in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        channel : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import ChannelText, now_as_id
        >>> channel = ChannelText.precreate(now_as_id(), name='GENERAL')
        >>> channel
        <ChannelText id=710506058560307200, name='GENERAL'>
        >>> # no code stands for str(channel).
        >>> f'{channel}'
        'GENERAL'
        >>> # 'd' stands for display name.
        >>> f'{channel:d}'
        'general'
        >>> # 'm' stands for mention.
        >>> f'{channel:m}'
        '<#710506058560307200>'
        >>> # 'c' stands for created at.
        >>> f'{channel:c}'
        '2020.05.14-14:57:24'
        ```
        """
        if not code:
            return self.__str__()
        
        if code == 'm':
            return f'<#{self.id}>'
        
        if code == 'd':
            return self.display_name
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    @property
    def display_name(self):
        """
        The channel's display name.
        
        Returns
        -------
        display_name : `str`
        """
        return ''
    
    @property
    def mention(self):
        """
        The channel's mention.
        
        Returns
        -------
        mention : `str`
        """
        return f'<#{self.id}>'
    
    @property
    def partial(self):
        """
        Whether this channel is partial.
        
        A channel is partial if non of the running clients can see it.
        
        Returns
        -------
        is_partial : `bool`
        """
        return (not self.clients)
    
    def get_user(self, name, default=None):
        """
        Tries to find the a user with the given name at the channel. Returns the first matched one.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase`` or `None`
        """
        if (not 1 < len(name) < 38):
            return default
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if user.discriminator == discriminator and user.name == name_:
                        return user
        
        if len(name) > 32:
            return default
        
        for user in users:
            if user.name == name:
                return user
        
        return default
    
    def get_user_like(self, name, default=None):
        """
        Searches a user, who's name or nick starts with the given string and returns the first find.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        default : `Any`, Optional
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase`` or `default`
        """
        if (not 1 < len(name) < 38):
            return default
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if user.discriminator == discriminator and user.name == name_:
                        return user
        
        if len(name) > 32:
            return default
        
        pattern = re.compile(re.escape(name), re.I)
        for user in users:
            if pattern.match(user.name) is None:
                continue
            
            return user
        
        return default
    
    def get_users_like(self, name):
        """
        Searches the users, who's name or nick starts with the given string.
        
        Parameters
        ----------
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        result = []
        if (not 1 < len(name) < 38):
            return result
        
        users = self.users
        
        if len(name) > 6 and name[-5] == '#':
            try:
                discriminator = int(name[-4:])
            except ValueError:
                pass
            else:
                name_ = name[:-5]
                for user in users:
                    if user.discriminator == discriminator and user.name == name_:
                        result.append(user)
                        break
        
        if len(name) > 32:
            return result
        
        pattern = re.compile(re.escape(name), re.I)
        for user in users:
            if pattern.match(user.name) is None:
                continue
            
            result.append(user)
        
        return result
    
    @property
    def users(self):
        """
        The users who can see this channel.
        
        Returns
        -------
        users : `list` of (``Client`` or ``User``)
        """
        return []
    
    def iter_users(self):
        """
        Iterates over the users who can see the channel.
        
        This method is a generator.
        
        Yields
        ------
        user : ``Client`` or ``User``
        """
        yield from self.users
    
    @property
    def clients(self):
        """
        The clients, who can access this channel.
        
        Returns
        -------
        clients : `list` of ``Client`` objects
        """
        result = []
        for user in self.users:
            if type(user) is User:
                continue
            
            result.append(user)
        
        return result
    
    # for sorting channels
    def __gt__(self, other):
        """Returns whether this channel's id is greater than the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id > other.id
        
    
    def __ge__(self, other):
        """Returns whether this channel's id is greater or equal than the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id >= other.id
        
    
    def __eq__(self, other):
        """Returns whether this channel's id is equal to the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id == other.id
        
    
    def __ne__(self,other):
        """Returns whether this channel's id is not equal to the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id != other.id
        
    
    def __le__(self, other):
        """Returns whether this channel's id is less or equal than the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id <= other.id
        
    
    def __lt__(self, other):
        """Returns whether this channel's id is less than the other's."""
        if not isinstance(other, ChannelBase):
            return NotImplemented
        
        return self.id < other.id
        
    
    @property
    def name(self):
        """
        Returns the channel's name.
        
        Subclasses should overwrite it.
        
        Returns
        -------
        name : `str`
        """
        return self.__class__.__name__
    
    def has_name_like(self, name):
        """
        Returns whether the channel's name is like the given string.
        
        Parameters
        ----------
        name : `str`
            The name of the channel
        
        Returns
        -------
        channel : ``ChannelBase`` instance
        """
        if name.startswith('#'):
            name = name[1:]
        
        target_name_length = len(name)
        if target_name_length<2 or target_name_length>100:
            return False
        
        if re.match(re.escape(name), self.name, re.I) is None:
            return False
        
        return True
    
    def permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        user : ``UserBase`` instance
            The user, who's permissions will be returned.
        
        Returns
        -------
        permission : ``Permission``
        
        See Also
        --------
        ``.cached_permissions_for`` : Cached permission calculator.
        
        Notes
        -----
        Always return empty permissions. Subclasses should implement this method.
        """
        return PERMISSION_NONE
    
    def cached_permissions_for(self, user):
        """
        Returns the permissions for the given user at the channel. If the user's permissions are not cached, calculates
        and stores them first.
        
        Parameters
        ----------
        user : ``UserBase`` instance
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Mainly designed for getting clients' permissions and stores only their as well. Do not caches other user's
        permissions.
        
        Always return empty permissions. Subclasses should implement this method.
        """
        return PERMISSION_NONE
    
    def permissions_for_roles(self, *roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        *roles : ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        permission : ``Permission``
        
        Notes
        -----
        Partial roles and roles from other guilds as well are ignored.
        
        Always return empty permissions. Subclasses should implement this method.
        """
        return PERMISSION_NONE
    
    
    @property
    def guild(self):
        """
        Returns the channel's guild. At the case of private channels this is always `None`.
        
        Returns
        -------
        guild : `None`
        """
        return None
    
    
    def _update_no_return(self, data):
        """
        Updates the channel with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        pass

    def _update(self, data):
        """
        Updates the channel and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        """
        return {}
    
    def _delete(self):
        """
        Removes the channel's references.
        
        Used when the channel is deleted.
        """
        pass

    
    @classmethod
    def _from_partial_data(cls, data, channel_id, partial_guild):
        """
        Creates a channel from partial data. Called by ``create_partial_channel_from_data`` when a new
        partial channel is needed to be created.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Partial channel data.
        channel_id : `int`
            The channel's id.
        partial_guild : ``Guild`` or `None`
            The channel's guild if applicable.
        
        Returns
        -------
        channel : ``ChannelBase``
        """
        try:
            channel_type = data['type']
        except KeyError:
            channel_type = cls.DEFAULT_TYPE
        
        self = cls._create_empty(channel_id, channel_type, partial_guild)
        
        return self
    
    @classmethod
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        """
        Creates a partial channel from the given parameters.
        
        Parameters
        ----------
        channel_id : `int`
            The channel's identifier.
        channel_type : `int`
            The channel's type identifier.
        partial_guild : `None` or ``Guild``
            A partial guild for the created channel.
        
        Returns
        -------
        channel : ``ChannelBase`` instance
            The created partial channel.
        """
        self = object.__new__(cls)
        self.id = channel_id
        return self

