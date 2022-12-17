__all__ = ('ChannelMetadataBase',)

from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from scarletio import RichAttributeErrorBaseType, include

from ...bases import Icon, IconType, PlaceHolder, IconSlot
from ...http import urls as module_urls
from ...permission.permission import PERMISSION_NONE
from ...utils import id_to_datetime

from .constants import AUTO_ARCHIVE_DEFAULT, NAME_DEFAULT
from .flags import ChannelFlag
from .preinstanced import ForumLayout, SortOrder, VideoQualityMode, VoiceRegion


Client = include('Client')


CHANNEL_METADATA_ICON_SLOT = IconSlot(
    'icon',
    'icon',
    module_urls.channel_group_icon_url,
    module_urls.channel_group_icon_url_as,
)


class ChannelMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for channel metadatas.
    
    Class Attributes
    ----------------
    order_group: `int` = `0`
        The channel's order group used when sorting channels.
    """
    __slots__ = ()
    
    order_group = 0
    
    def __new__(cls, keyword_parameters):
        """
        Creates a new partially channel metadata.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to work with.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        self = cls._create_empty()
        self._set_attributes_from_keyword_parameters(keyword_parameters)
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creating channel metadatas.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        
        Returns
        -------
        self : instance<cls>
        """
        self = object.__new__(cls)
        
        self._update_attributes(data)
        
        return self
    
    
    def __repr__(self):
        """Returns the channel metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __hash__(self):
        """Returns the channel metadata's hash value"""
        return 0
    
    
    def __eq__(self, other):
        """Returns whether the two channel metadatas are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Compares the channel metadata's attributes to the other one's.
        
        Parameters
        ----------
        other : `instance<type<self>>`
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
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Serialises the channel metadata to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether we want to include identifiers as well.
        
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
            

            +---------------------------------------+-----------------------------------------------------------+
            | Keys                                  | Values                                                    |
            +=======================================+===========================================================+
            | applied_tag_ids                       | `None`, `tuple` of `int`                                  |
            +---------------------------------------+-----------------------------------------------------------+
            | archived                              | `bool`                                                    |
            +---------------------------------------+-----------------------------------------------------------+
            | archived_at                           | `None`, `datetime`                                        |
            +---------------------------------------+-----------------------------------------------------------+
            | auto_archive_after                    | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | available_tags                        | `None`, `tuple` of ``ForumTag``                           |
            +---------------------------------------+-----------------------------------------------------------+
            | bitrate                               | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | default_forum_layout                  | ``ForumLayout``                                           |
            +---------------------------------------+-----------------------------------------------------------+
            | default_sort_order                    | ``SortOrder``                                             |
            +---------------------------------------+-----------------------------------------------------------+
            | default_thread_auto_archive_after     | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | default_thread_reaction               | `None`, ``Emoji``                                         |
            +---------------------------------------+-----------------------------------------------------------+
            | default_thread_slowmode               | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | flags                                 | ``ChannelFlag``                                           |
            +---------------------------------------+-----------------------------------------------------------+
            | icon                                  | ``Icon``                                                  |
            +---------------------------------------+-----------------------------------------------------------+
            | invitable                             | `bool`                                                    |
            +---------------------------------------+-----------------------------------------------------------+
            | metadata                              | ``ChannelMetadataBase``                                   |
            +---------------------------------------+-----------------------------------------------------------+
            | name                                  | `str`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | nsfw                                  | `bool`                                                    |
            +---------------------------------------+-----------------------------------------------------------+
            | open                                  | `bool`                                                    |
            +---------------------------------------+-----------------------------------------------------------+
            | owner_id                              | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | parent_id                             | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | permission_overwrites                 | `None`, `dict` of (`int`, ``PermissionOverwrite``) items  |
            +---------------------------------------+-----------------------------------------------------------+
            | position                              | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | region                                | `None`, ``VoiceRegion``                                   |
            +---------------------------------------+-----------------------------------------------------------+
            | slowmode                              | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | topic                                 | `None`, `str`                                             |
            +---------------------------------------+-----------------------------------------------------------+
            | type                                  | ``ChannelType``                                           |
            +---------------------------------------+-----------------------------------------------------------+
            | user_limit                            | `int`                                                     |
            +---------------------------------------+-----------------------------------------------------------+
            | video_quality_mode                    | ``VideoQualityMode``                                      |
            +---------------------------------------+-----------------------------------------------------------+
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
        self : `instance<cls>`
        """
        return cls._create_empty()
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates a partial channel from the given parameters.
        
        Returns
        -------
        self : `instance<cls>`
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
            The parent client entity.
        """
        pass
    
    
    def _iter_delete(self, channel_entity, client):
        """
        Called when the channel is deleted. This method also applies deletion of other related channels too, invoking
        their ``._delete` technically.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        client : `None`, ``Client``
            The parent client entity.
        
        Yields
        ------
        channel : ``Channel``
        """
        self._delete(channel_entity, client)
        yield channel_entity
    
    
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
        
        This method is an iterable generator.
        
        Parameters
        ----------
        channel_entity : ``Channel``
            The channel entity owning the metadata.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        return
        yield
    
    
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
    
    
    @classmethod
    def precreate(cls, keyword_parameters):
        """
        Precreates the channel metadata. Each channel type exhaust it's own specific attributes from
        `keyword_parameters`.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters passed to ``Channel.precreate``
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            . If an parameter's value is incorrect.
        """
        self = cls._create_empty()
        self._set_attributes_from_keyword_parameters(keyword_parameters)
        return self
    
    
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
    
    
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        """
        Sets shared parameters used by ``.__new__` and ``._precreate˙`.
        
        Parameters
        ----------
        keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to work with.
        """
        pass
    
    # Slot place holders
    
    applied_tag_ids = PlaceHolder(
        None,
        """
        Returns the tags' identifier which have been applied to the thread. Applicable for threads of a forum.
        
        Returns
        -------
        applied_tag_ids : `None`, `tuple` of `int`
        """
    )
    
    
    archived = PlaceHolder(
        False,
        """
        Returns whether the thread is archived.
        
        If the channel is not a thread, then returns `False`.
        
        Returns
        -------
        archived : `bool`
        """
    )
    
    
    archived_at = PlaceHolder(
        None,
        """
        Returns when the thread was archived.
        
        Returns `None` if the the channel is not a thread one or if it is not archived.
        
        Returns
        -------
        archived_at : `None`, `datetime`
        """
    )
    
    
    auto_archive_after = PlaceHolder(
        0,
        """
        Returns the duration in seconds to automatically archive the thread after recent activity. Can be one of:
        `3600`, `86400`, `259200`, `604800`.
        
        Returns `3600` if the channel is not a thread one.
        
        Returns
        -------
        auto_archive_after : `int`
        """
    )
    
    
    available_tags = PlaceHolder(
        None,
        """
        Returns the available tags to assign to the child-thread channels.
        
        If the channel is not a forum channel, then returns `None`.
        
        Returns
        -------
        available_tags : `None`, `tuple` of ``ForumTag``
        """
    )
    
    
    bitrate = PlaceHolder(
        0,
        """
        Returns the bitrate (in bits) of the voice channel.
        
        If the channel has no bitrate, returns `0`.
        
        Returns
        -------
        bitrate : `int`
        """
    )
    
    
    default_forum_layout = PlaceHolder(
        ForumLayout.none,
        """
        The default layout used to display threads of the forum.
        
        Returns
        -------
        default_forum_layout : ``ForumLayout``
        """
    )
    
    default_sort_order = PlaceHolder(
        SortOrder.latest_activity,
        """
        The default thread ordering of the forum.
        
        Returns
        -------
        default_sort_order : ``SortOrder``
        """
    )
    
    
    default_thread_auto_archive_after = PlaceHolder(
        AUTO_ARCHIVE_DEFAULT,
        """
        Returns the default duration in seconds to automatically archive the channel's thread after recent activity.
        
        Returns
        -------
        default_thread_auto_archive_after : `int`
        """
    )
    
    
    default_thread_reaction = PlaceHolder(
        None,
        """
        Returns the emoji to show in the add reaction button on a thread of the forum channel.
        
        Returns
        -------
        default_thread_reaction : ``Emoji``
        """
    )
    
    
    default_thread_slowmode = PlaceHolder(
        0,
        """
        Returns the default slowmode applied to the threads of the channel.
        
        Returns
        -------
        default_thread_slowmode : `int`
        """
    )
    
    
    flags = PlaceHolder(
        ChannelFlag(0),
        """
        Returns the channel's flags.
        
        Returns empty channel flags by default.
        
        Returns
        -------
        flags : ``ChannelFlag``
        """
    )
    
    
    icon = PlaceHolder(
        Icon(IconType.none, 0),
        """
        Returns the channel's icon.
        
        Returns
        -------
        icon : ``Icon``
        """
    )
    
    
    invitable = PlaceHolder(
        True,
        """
        Whether non-moderators can invite other non-moderators to the threads. Only applicable for private threads.
        
        Returns `True` by default.
        
        Returns
        -------
        invitable : `bool`
        """
    )
    

    name = PlaceHolder(
        NAME_DEFAULT,
        """
        Returns the channel's name.
        
        Returns
        -------
        name : `str`
        """
    )
    
    
    nsfw = PlaceHolder(
        False,
        """
        Returns whether the channel is not safe for work.
        
        Defaults to `False`.
        
        Returns
        -------
        nsfw : `bool`
        """
    )
    
    
    open = PlaceHolder(
        True,
        """
        Returns whether the thread channel is open.
        
        If the channel is not a thread one, will return `True`.
        
        Returns
        -------
        open : `bool`
        """
    )
    
    
    owner_id = PlaceHolder(
        0,
        """
        Returns the channel's owner's identifier.
        
        If the channel has no owner, then returns `0`.
        
        Returns
        -------
        owner_id : `int`
        """
    )
    
    
    parent_id = PlaceHolder(
        0,
        """
        Returns the channel's parent's identifier.
        
        If the channel has no parent, or if not applicable for the specific channel type returns `0`.
        
        Returns
        -------
        parent_id : `int`
        """
    )
    
    
    permission_overwrites = PlaceHolder(
        None,
        """
        Returns the channel's permission overwrites.
        
        If the channel has no permission overwrites returns `None`.
        
        Returns
        -------
        permission_overwrites : `None`, `dict` of (`int`, ``PermissionOverwrite``) items
        """
    )
    
    
    position = PlaceHolder(
        0,
        """
        Returns the channel's position.
        
        If the channel has no position, returns `0`.
        
        Returns
        -------
        position : `int`
        """
    )
    
    
    region = PlaceHolder(
        VoiceRegion.unknown,
        """
        Returns the voice region of the channel.
        
        If the channel has no voice region, returns `None`.
        
        Returns
        -------
        region : ``VoiceRegion``
        """
    )
    
    
    slowmode = PlaceHolder(
        0,
        """
        Returns the slowmode of the channel.
        
        If the channel has no slowmode, returns `0`.
        
        Returns
        -------
        slowmode : `int`
        """
    )
    
    
    thread_users = PlaceHolder(
        None,
        """
        Returns the users inside of the thread if any.
        
        If the channel has no users, or if it is not a thread channel, will return `None`.
        
        Returns
        -------
        thread_users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        """
    )
    
    
    topic = PlaceHolder(
        None,
        """
        Returns the channel's topic.
        
        If the channel has no topic, returns `None`.
        
        Returns
        -------
        topic : `None`, `str`
        """
    )
    
    
    user_limit = PlaceHolder(
        0,
        """
        Returns the maximal amount of users, who can join the voice channel
        
        If the channel has not user limit, returns `0`.
        
        Returns
        -------
        user_limit : `int`
        """
    )
    
    
    video_quality_mode = PlaceHolder(
        VideoQualityMode.none,
        """
        Returns the video quality of the voice channel.
        
        If the channel has no video quality mode, returns `VideoQualityMode.none`.
        
        Returns
        -------
        video_quality_mode : ``VideoQualityMode``
        """
    )
