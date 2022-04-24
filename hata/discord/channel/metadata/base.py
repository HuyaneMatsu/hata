__all__ = ('ChannelMetadataBase',)

from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from scarletio import RichAttributeErrorBaseType, include

from ...bases import Icon, IconType
from ...permission import Permission
from ...permission.permission import PERMISSION_NONE
from ...utils import id_to_datetime

from ..constants import AUTO_ARCHIVE_DEFAULT
from ..flags import ChannelFlag
from ..preinstanced import VideoQualityMode


Client = include('Client')

CHANNEL_DEFAULT_ATTRIBUTES = {
    'archived': False,
    'archived_at': None,
    'auto_archive_after': AUTO_ARCHIVE_DEFAULT,
    'bitrate': 0,
    'default_auto_archive_after': AUTO_ARCHIVE_DEFAULT,
    'flags': ChannelFlag(0),
    'icon': Icon(IconType.none, 0),
    'invitable': True,
    'nsfw': False,
    'open': False,
    'owner_id': 0,
    'parent_id': 0,
    'permission_overwrites': None,
    'position': 0,
    'region': None,
    'slowmode': 0,
    'thread_users': None,
    'topic': None,
    'user_limit': 0,
    'video_quality_mode': VideoQualityMode.none,
}


class ChannelMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for channel metadatas.
    
    Class Attributes
    ----------------
    type : `int` = `-1`
        The channel's type.
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ()
    
    type = -1
    order_group = 0
    
    def __new__(cls, data):
        """
        Creating channel metadatas.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        """
        self = object.__new__(cls)
        
        self._update_attributes(data)
        
        return self
    
    
    def __repr__(self):
        """Returns the channel metadata's representation."""
        return f'<{self.__class__.__name__} type={self.type}>'
    
    
    def __eq__(self, other):
        """Returns whether the two channel metadatas are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._compare_attributes_to(other)
    
    
    def _compare_attributes_to(self, other):
        """
        Compares the channel metadata's attributes to the other one's.
        
        Parameters
        ----------
        other : ``ChannelMetadataBase``
            The other channel metadata to compare self to.
            
            > Must have the same type as self.
        
        Returns
        -------
        equal : `bool`
            Whether both metadata has the same attributes.
        """
        return True
    
    
    def _created(self, channel_entity, client):
        """
        Called when the channel entity is initialized.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The parent channel entity.
        client : `None`, ``Client``
            The client who received the channel payload.
        """
        pass
    
    
    def _to_data(cls):
        """
        Serialises the channel metadata to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) Items
        """
        return {}
    

    def _update_attributes(self, data):
        """
        Updates the channel metadata with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        """
        pass
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the channel metadata and returns it's overwritten attributes as a `dict` with a
        `attribute-name` - `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
            
            Might contain the following items:
            
            +-------------------------------+-----------------------------------------------------------+
            | Keys                          | Values                                                    |
            +===============================+===========================================================+
            | archived                      | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | archived_at                   | `None`, `datetime`                                        |
            +-------------------------------+-----------------------------------------------------------+
            | auto_archive_after            | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | bitrate                       | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | default_auto_archive_after    | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | flags                         | ``ChannelFlag``                                           |
            +-------------------------------+-----------------------------------------------------------+
            | icon                          | ``Icon``                                                  |
            +-------------------------------+-----------------------------------------------------------+
            | invitable                     | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | name                          | `str`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | nsfw                          | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | open                          | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | owner_id                      | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | parent_id                     | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | permission_overwrites         | `None`, `dict` of (`int`, ``PermissionOverwrite``) items  |
            +-------------------------------+-----------------------------------------------------------+
            | position                      | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | region                        | `None`, ``VoiceRegion``                                   |
            +-------------------------------+-----------------------------------------------------------+
            | slowmode                      | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | topic                         | `None`, `str`                                             |
            +-------------------------------+-----------------------------------------------------------+
            | type                          | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | user_limit                    | `int`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | video_quality_mode            | ``VideoQualityMode``                                      |
            +-------------------------------+-----------------------------------------------------------+
        """
        return {}
    
    
    @classmethod
    def _from_partial_data(cls, data):
        """
        Creates a channel metadata from the given partial data. Called by ``Channel._from_partial_data`` when a
        new partial channel is needed to be created.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `Any`) items
            Partial channel data.
        
        Returns
        -------
        self : ``ChannelMetadataBase``
        """
        return cls._create_empty()
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates a partial channel from the given parameters.
        
        Returns
        -------
        self : ``ChannelMetadataBase``
        """
        return object.__new__(cls)
    
    
    def _delete(self, channel_entity, client):
        """
        Called when the channel is deleted.
        
        Removes the channel's references.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        client : `None`, ``Client``
            The parent client entity,
        """
        pass
    
    
    def _get_users(self, channel_entity):
        """
        The users who can see this channel.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        return []
    
    
    def _iter_users(self, channel_entity):
        """
        Iterates over the users who can see the channel.
        
        This method is a generator.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        yield from self.users
    
    
    def _get_clients(self, channel_entity):
        """
        Helper class to get the channel's clients.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        
        Returns
        -------
        clients : `list` of ``Client``
        """
        clients = []
        for user in self._get_users(channel_entity):
            if isinstance(user, Client):
                clients.append(user)
        
        return clients
    
    
    def _get_user(self, channel_entity, name, default):
        """
        Tries to find the a user with the given name at the channel. Returns the first matched one.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        name : `str`
            The name to search for.
        default : `Any`
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase``, `default`
        """
        if (not 1 < len(name) < 38):
            return default
        
        users = self._get_users(channel_entity)
        
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
    
    
    def _get_user_like(self, channel_entity, name, default):
        """
        Searches a user, who's name or nick starts with the given string and returns the first find.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        name : `str`
            The name to search for.
        default : `Any`
            The value what is returned when no user was found. Defaults to `None`.
        
        Returns
        -------
        user : ``ClientUserBase``, `default`
        """
        name_length = len(name)
        if name_length < 1:
            return default
        
        users = self._get_users(channel_entity)
        
        if name_length > 6:
            if name_length > 37:
                return default
            
            if name[-5] == '#':
                try:
                    discriminator = int(name[-4:])
                except ValueError:
                    pass
                else:
                    stripped_name = name[:-5]
                    for user in users:
                        if user.discriminator == discriminator and user.name == stripped_name:
                            return user
        
        if name_length > 32:
            return default
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        for user in users:
            if pattern.search(user.name) is None:
                continue
            
            return user
        
        return default
    
    
    def _get_users_like(self, channel_entity, name):
        """
        Searches the users, who's name or nick starts with the given string.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        name : `str`
            The name to search for.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        result = []
        
        name_length = len(name)
        if name_length < 1:
            return result
        
        users = self._get_users(channel_entity)
        
        if name_length > 6:
            if name_length > 37:
                return result
            
            if name[-5] == '#':
                try:
                    discriminator = int(name[-4:])
                except ValueError:
                    pass
                else:
                    stripped_name = name[:-5]
                    for user in users:
                        if user.discriminator == discriminator and user.name == stripped_name:
                            result.append(user)
                            break
        
        if name_length > 32:
            return result
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        for user in users:
            if pattern.search(user.name) is None:
                continue
            
            result.append(user)
        
        return result
    
    
    @property
    def name(self):
        """
        Returns the channel's name.
        
        Returns
        -------
        name : `str`
        """
        return 'channel'
    
    
    def _get_processed_name(self):
        """
        Returns the channel's name.
        
        Returns
        -------
        name : `str`
        """
        return self.name
    
    
    def _get_display_name(self):
        """
        Returns channel's display name.
        
        Returns
        -------
        display_name : `str`
        """
        return self.name
    

    def _get_permissions_for(self, channel_entity, user):
        """
        Returns the permissions for the given user at the channel.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        user : ``UserBase``
            The user to calculate it's permissions of.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
            
        
        See Also
        --------
        ``.cached_permissions_for`` : Cached permission calculator.
        """
        return PERMISSION_NONE
    
    
    def _get_cached_permissions_for(self, channel_entity, user):
        """
        Returns the permissions for the given user at the channel. If the user's permissions are not cached, calculates
        and stores them first.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        user : ``UserBase``
            The user to calculate it's permissions of.
        
        Returns
        -------
        permissions : ``Permission``
            The calculated permissions.
        """
        return self._get_permissions_for(channel_entity, user)
    
    
    def _get_permissions_for_roles(self, channel_entity, roles):
        """
        Returns the channel permissions of an imaginary user who would have the listed roles.
        
        Parameters
        ----------
        roles : `tuple` of ``Role``
            The roles to calculate final permissions from.
        
        Returns
        -------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        permissions : ``Permission``
            The calculated permissions.
        """
        return PERMISSION_NONE
    
    
    def __dir__(self):
        """Returns the attributes of the channel."""
        return sorted(set(object.__dir__(self))|set(CHANNEL_DEFAULT_ATTRIBUTES.keys()))
    
    
    def __getattr__(self, attribute_name):
        """Returns the channel metadata's attribute if found."""
        try:
            return CHANNEL_DEFAULT_ATTRIBUTES[attribute_name]
        except KeyError:
            pass
        
        return RichAttributeErrorBaseType.__getattr__(self, attribute_name)
    
    
    @classmethod
    def _precreate(cls, keyword_parameters):
        """
        Precreates the channel metadata. Each channel type exhaust it's own specific attributes from
        `keyword_parameters`.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters passed to ``Channel.precreate``
        
        Returns
        -------
        self : ``ChannelMetadataBase``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        return cls._create_empty()
    
    
    def _get_created_at(self, channel_entity):
        """
        Returns when the channel was created.
        
        Returns
        -------
        created_at : `datetime`
        """
        return id_to_datetime(channel_entity.id)
    
    
    def _invalidate_permission_cache(self):
        """
        Invalidates the cached permissions of the channel.
        
        This method is only applicable for channel types with permission cache.
        """
        pass
