__all__ = ('AUTO_ARCHIVE_DEFAULT', 'AUTO_ARCHIVE_OPTIONS', 'ChannelThread', )

from ...backend.utils import copy_docs
from ...backend.export import export

from ..core import CHANNELS
from ..permission.permission import PERMISSION_NONE
from ..user import ZEROUSER, create_partial_user_from_id
from ..user.thread_profile import thread_user_create
from ..preconverters import preconvert_snowflake, preconvert_str, preconvert_int, preconvert_int_options
from ..utils import parse_time

from .channel_base import ChannelBase
from .channel_guild_base import ChannelGuildBase
from .channel_text_base import ChannelTextBase


AUTO_ARCHIVE_DEFAULT = 3600
AUTO_ARCHIVE_OPTIONS = frozenset((3600, 86400, 259200, 604800))

CHANNEL_THREAD_NAMES = {
     9: None,
    10: 'announcements',
    11: 'public',
    12: 'private',
}

@export
class ChannelThread(ChannelGuildBase, ChannelTextBase):
    """
    Represents a ``Guild`` thread channel
    
    Attributes
    ----------
    id : `int`
        The unique identifier of the channel.
    parent : `None` or ``ChannelText``
        The text channel from where the thread is created from.
    name : `str`
        The channel's name.
    _message_keep_limit : `int`
        The channel's own limit of how much messages it should keep before removing their reference.
    _turn_message_keep_limit_on_at : `float`
        The LOOP_TIME time, when the channel's message history should be turned back to limited. Defaults `0.0`.
    message_history_reached_end : `bool`
        Whether the channel's message's are loaded till their end. If the channel's message history reached it's end
        no requests will be requested to get older messages.
    messages : `deque` of ``Message`` objects
        The channel's message history.
    archived : `bool`
        Whether the thread s archived.
    archived_at : `None` or `datetime`
        When the thread's archive status was last changed.
    auto_archive_after : `int`
        Duration in seconds to automatically archive the thread after recent activity. Can be one of: `3600`, `86400`,
        `259200`, `604800`.
    open : `bool`
        Whether the thread channel is open.
    slowmode : `int`
        The amount of time in seconds what a user needs to wait between it's each message. Bots and user accounts with
        `manage_messages` or `manage_channel` permissions are unaffected.
    thread_users : `None` or `dict` of (`int`, ``ClientUserBase``) items
        The users inside of the thread if any.
    type : `int` = `12`
        The channel's Discord side type.
    owner_id : `int`
        The channel's creator's identifier. Defaults to `0`.
    
    Class Attributes
    ----------------
    DEFAULT_TYPE : `int` = `12`
        The preferred channel type, if there is no channel type included.
    INTERCHANGE : `tuple` of `int` = `(10, 11, 12,)`
        Defines to which channel type this channel's type can be interchanged. The channel's direct type must be of
        them.
    ORDER_GROUP : `int` = `9`
        An order group what defined which guild channel type comes after the other one.
    MESSAGE_KEEP_LIMIT : `int` = `10`
        The default amount of messages to store at `.messages`.
    REPRESENTED_TYPES : `tuple` = (`10`, `11`, `12`,)
        The type values which ``ChannelThread`` might represent.
    """
    __slots__ = ('archived', 'archived_at', 'auto_archive_after', 'open', 'owner_id', 'slowmode',
        'thread_users', 'type')
    
    DEFAULT_TYPE = 12
    ORDER_GROUP = 9
    INTERCHANGE = ()
    REPRESENTED_TYPES = (10, 11, 12,)
    
    def __new__(cls, data, client=None, guild=None):
        """
        Creates a guild thread channel from the channel data received from Discord. If the channel already exists and
        if it is partial, then updates it.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data receive from Discord.
        client : `None` or ``Client``, Optional
            The client, who received the channel's data, if any.
        guild : `None` or ``Guild``, Optional
            The guild of the channel.
        """
        channel_id = int(data['id'])
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = channel_id
            CHANNELS[channel_id] = self
            self._messageable_init()
            self.thread_users = None
            update = True
        else:
            if self.clients:
                update = False
            else:
                update = True
        
        if update:
            self.type = data['type']
            self._init_parent(data, guild)
            self._update_no_return(data)
        
        if (client is not None):
            try:
                thread_user_data = data['member']
            except KeyError:
                pass
            else:
                thread_user_create(self, client, thread_user_data)
        
        return self
    
    @copy_docs(ChannelBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        try:
            type_name = CHANNEL_THREAD_NAMES[self.type]
        except KeyError:
            type_name = repr(self.type)
        
        if (type_name is not None):
            repr_parts.append(' (')
            repr_parts.append(type_name)
            repr_parts.append(')')
            
        repr_parts.append(' id=')
        repr_parts.append(repr(self.id))
        repr_parts.append(', name=')
        repr_parts.append(repr(self.__str__()))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    @property
    def owner(self):
        """
        Returns the thread threads's creator.
        
        Returns
        -------
        owner : ``UserClientBase``
            If user the guild has no owner, returns `ZEROUSER`.
        """
        owner_id = self.owner_id
        if owner_id:
            owner = create_partial_user_from_id(owner_id)
        else:
            owner = ZEROUSER
        
        return owner
    
    def is_announcements(self):
        """
        Returns whether the thread channel is bound to an announcements channel.
        
        Returns
        -------
        is_announcements : `bool`
        """
        return self.type == 10
    
    def is_public(self):
        """
        Returns whether the thread channel is public.
        
        Returns
        -------
        is_public : `bool`
        """
        return self.type == 11
    
    def is_private(self):
        """
        Returns whether the thread channel is private.
        
        Returns
        -------
        is_private : `bool`
        """
        return self.type == 12
    
    def _init_parent(self, data, guild):
        """
        Initializes the `.parent` attribute of the channel. If a channel is under the ``Guild``, and not in a parent
        (parent channels are all like these), then their `.parent` is the ``Guild`` itself.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Channel data received from Discord.
        guild : ``Guild``
            The guild of the channel.
        """
        self.guild = guild
        
        if (guild is not None):
            guild.threads[self.id] = self
        
        parent_id = data.get('parent_id', None)
        if (parent_id is None):
            parent = None
        else:
            parent_id = int(parent_id)
            
            if guild is None:
                parent = CHANNELS.get(parent_id, None)
            else:
                parent = guild.channels.get(parent_id, None)
        
        self.parent = parent
    
    
    @classmethod
    @copy_docs(ChannelBase._create_empty)
    def _create_empty(cls, channel_id, channel_type, partial_guild):
        self = super(ChannelThread, cls)._create_empty(channel_id, channel_type, partial_guild)
        self._messageable_init()
        
        self.archived = False
        self.archived_at = None
        self.auto_archive_after = AUTO_ARCHIVE_DEFAULT
        self.open = False
        self.owner_id = 0
        self.slowmode = 0
        self.type = channel_type
        
        return self
    
    @property
    @copy_docs(ChannelBase.display_name)
    def display_name(self):
        return self.name.lower()
    
    
    @property
    @copy_docs(ChannelBase.users)
    def users(self):
        thread_users = self.thread_users
        if thread_users is None:
            users = []
        else:
            users = list(thread_users.values())
        
        return users
    
    @copy_docs(ChannelBase.iter_users)
    def iter_users(self):
        thread_users = self.thread_users
        if (thread_users is not None):
            yield from thread_users.values()
    
    
    @copy_docs(ChannelBase._update_no_return)
    def _update_no_return(self, data):
        self.name = data['name']
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        self.slowmode = slowmode
        
        # Move to sub data
        data = data['thread_metadata']
        
        self.archived = data.get('archived', False)
        
        
        self.auto_archive_after = data['auto_archive_duration']*60
        
        archived_at_data = data.get('archive_timestamp', None)
        if archived_at_data is None:
            archived_at = None
        else:
            archived_at = parse_time(archived_at_data)
        self.archived_at = archived_at
        
        self.open = not data.get('locked', True)
    
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
        
        Returned Data Structure
        -----------------------
        
        +-----------------------+-----------------------------------+
        | Keys                  | Values                            |
        +=======================+===================================+
        | archived              | `bool`                            |
        +-----------------------+-----------------------------------+
        | archived_at           | `None` or `datetime`              |
        +-----------------------+-----------------------------------+
        | auto_archive_after    | `int`                             |
        +-----------------------+-----------------------------------+
        | name                  | `str`                             |
        +-----------------------+-----------------------------------+
        | open                  | `bool`                            |
        +-----------------------+-----------------------------------+
        | slowmode              | `int`                             |
        +-----------------------+-----------------------------------+
        """
        old_attributes = {}
        
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        slowmode = data.get('rate_limit_per_user', None)
        if slowmode is None:
            slowmode = 0
        if self.slowmode != slowmode:
            old_attributes['slowmode'] = self.slowmode
            self.slowmode = slowmode
        
        
        # Move to sub data
        data = data['thread_metadata']
        
        
        archived = data.get('archived', False)
        if (self.archived != archived):
            old_attributes['archived'] = self.archived
            self.archived = archived
        
        
        auto_archive_after = data['auto_archive_duration']*60
        if (self.auto_archive_after != auto_archive_after):
            old_attributes['auto_archive_after'] = self.auto_archive_after
            self.auto_archive_after = auto_archive_after
        
        
        archived_at_data = data.get('archive_timestamp', None)
        if archived_at_data is None:
            archived_at = None
        else:
            archived_at = parse_time(archived_at_data)
        if (self.archived_at != archived_at):
            old_attributes['archived_at'] = self.archived_at
            self.archived_at = archived_at
        
        open_ = not data.get('locked', True)
        if (self.open != open_):
            old_attributes['open'] = self.open
            self.open = open_
        
        return old_attributes
    
    
    @copy_docs(ChannelBase._delete)
    def _delete(self):
        parent = self.parent
        if parent is None:
            return
        
        self.parent = None
        
        guild = self.guild
        if (guild is not None):
            self.guild = None
            del guild.threads[self.id]
        
        thread_users = self.thread_users
        if (thread_users is not None):
            self.thread_users = None
            for user in thread_users.values():
                thread_profiles = user.thread_profiles
                if (thread_profiles is not None):
                    try:
                        del thread_profiles[self]
                    except KeyError:
                        pass
                    else:
                        if (not thread_profiles):
                            user.thread_profiles = None
    
    @copy_docs(ChannelBase.permissions_for)
    def permissions_for(self, user):
        parent = self.parent
        if parent is None:
            return PERMISSION_NONE
        
        return parent.permissions_for(user)

    @copy_docs(ChannelBase.cached_permissions_for)
    def cached_permissions_for(self, user):
        parent = self.parent
        if parent is None:
            return PERMISSION_NONE
        
        return parent.cached_permissions_for(user)
    
    @copy_docs(ChannelBase.permissions_for_roles)
    def permissions_for_roles(self, *roles):
        parent = self.parent
        if parent is None:
            return PERMISSION_NONE
        
        return parent.permissions_for_roles(*roles)
    
    @classmethod
    def precreate(cls, channel_id, **kwargs):
        """
        Precreates the channel by creating a partial one with the given parameters. When the channel is loaded
        the precrated channel will be picked up. If an already existing channel would be precreated, returns that
        instead and updates that only, if that is a partial channel.
        
        Parameters
        ----------
        channel_id : `int` or `str`
            The channel's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the channel.
        
        Other Parameters
        ----------------
        auto_archive_after: `int`, Optional (Keyword only)
            The channel's ``.auto_archive_after``.
        name : `str`, Optional (Keyword only)
            The channel's ``.name``.
        slowmode : `int`, Optional (Keyword only)
            The channel's ``.slowmode``.
        type : `int`, Optional (Keyword only)
            The channel's ``.type``.
        
        Returns
        -------
        channel : ``ChannelThread``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        channel_id = preconvert_snowflake(channel_id, 'channel_id')
        
        if kwargs:
            processable = []
            
            try:
                value = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(value, 'name', 1, 100)
                processable.append(('name', name))
            
            
            try:
                slowmode = kwargs.pop('slowmode')
            except KeyError:
                pass
            else:
                slowmode = preconvert_int(slowmode, 'slowmode', 0, 21600)
                processable.append(('slowmode', slowmode))
            
            
            try:
                auto_archive_after = kwargs.pop('auto_archive_after')
            except KeyError:
                pass
            else:
                auto_archive_after = preconvert_int_options(auto_archive_after, 'auto_archive_after',
                    AUTO_ARCHIVE_OPTIONS)
                processable.append(('auto_archive_after', auto_archive_after))
            
            
            try:
                type_ = kwargs.pop('type')
            except KeyError:
                pass
            else:
                type_ = preconvert_int(type_, 'type', 0, 256)
                if (type_ not in cls.REPRESENTED_TYPES):
                    raise ValueError(f'`type` should be one of: {cls.REPRESENTED_TYPES!r}')
                
                processable.append(('type', type_))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            self = CHANNELS[channel_id]
        except KeyError:
            self = cls._create_empty(channel_id, cls.DEFAULT_TYPE, None)
            CHANNELS[channel_id] = self
        
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
