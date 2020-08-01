# -*- coding: utf-8 -*-
__all__ = ('Invite', 'InviteTargetType')

from .others import parse_time, DISCORD_EPOCH_START
from .http import URLS
from .client_core import GUILDS, CHANNELS
from .user import User, ZEROUSER
from .guild import PartialGuild
from .channel import PartialChannel

class InviteTargetType(object):
    """
    Represents an ``Invite``'s target's type.
    
    Attributes
    ----------
    name : `str`
        The name of the target type.
    value : `int`
        The Discord side identificator value of the target type.
    
    Class Attributes
    ----------------
    INSTANCES : `list` of ``InviteTargetType``
        Stores the predefined ``InviteTargetType`` instances. These can be accessed with their `value` as index.
    
    Every predefind invite target type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | NONE                  | NONE      | 0     |
    +-----------------------+-----------+-------+
    | STREAM                | STREAM    | 1     |
    +-----------------------+-----------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 2
    
    # object related
    __slots__=('name', 'value')
    
    def __init__(self, value, name):
        """
        Creates an ``InviteTargetType`` and stores it at the classe's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identificator value of the invite target type.
        name : `str`
            The name of invite target type.
        """
        self.value=value
        self.name=name
        
        self.INSTANCES[value]=self
    
    def __str__(self):
        """Returns the ivnite target type's name."""
        return self.name
    
    def __int__(self):
        """Returns the invite target type's value."""
        return self.value
    
    def __repr__(self):
        """Returns the invite target type's representation."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r})'
    
    # predefined
    NONE    = NotImplemented
    STREAM  = NotImplemented

InviteTargetType.NONE   = InviteTargetType(0,'NONE')
InviteTargetType.STREAM = InviteTargetType(1,'STREAM')

class Invite(object):
    """
    Represents a Discord Invite.
    
    Attributes
    ---------
    channel : `None`, ``ChannelText``, ``ChannelVoice``, ``ChannelStore`` or ``ChannelGroup``
        The channel where the invite redirects. If it is announcements or store channe, then the invite is a lurk
        invite. If channel data was not sent with the invite's, then this attribute is set as `None`.
    code : `str`
        The invite's unique identificator.
    created_at : `datetime`
        When the invite was created.
    guild : `None` or ``Guild``
        The guild this invite is for. If not included or if the invite's channel is a group channel, then set as
        `None`.
    inviter : ``Client`` or ``User``
        The creator of the invite. If not included, then set as `ZEROUSER`.
    max_age : `None` or `int`
        The time in seconds after the invite will expire. If not included, then set as `None`.
        > If the invite was created with max age as `0`, then this value will be negative instead of the expected `0`.
    max_uses : `None` or `int`
        How much times the invite can be used. If not included, then set as `None`.
        > If the invite has no use limit, then this value is set as `0`.
    online_count : `int`
        The amount of online users at the respective guild (or group channel). If not included, then set as `0`.
    target_type : ``InviteTargetType``
        The invite's target type.
    target_user : ``Client`` or ``User``
        The target of the invite if applicable. Defaults to `ZEROUSER`.
    temporary : `bool`
        Whether this invite only grants temporary membership.
        > When the user goes offline, they get kicked, execept if they got a role meanwhile.
    user_count : `int`
        The amount of users at the respective guild (or group channel). If not included, then set as `0`.
    uses : `None` or `int`
        The amount how much times the invite was used. If not included, set as `None`.
    """
    __slots__ = ('channel', 'code', 'created_at', 'guild', 'inviter', 'max_age', 'max_uses', 'online_count',
        'target_type', 'target_user', 'temporary', 'user_count', 'uses',)
    
    def __init__(self,data):
        """
        Creates an invite from the given invite data. The invite data can be requested or received through the gateway
        as well.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Invite data.
        """
        self.code = data['code']
        
        try:
            guild_data = data['guild']
        except KeyError:
            try:
                guild_id = data['guild_id']
            except KeyError:
                guild = None
            else:
                guild_id = int(guild_id)
                guild = GUILDS.get(guild_id,None)
        else:
            guild = PartialGuild(guild_data)
        
        self.guild = guild
        
        try:
            channel_data = data['channel']
        except KeyError:
            try:
                channel_id = data['channel_id']
            except KeyError:
                channel = None
            else:
                channel_id = int(channel_id)
                channel = CHANNELS.get(channel_id)
        else:
            channel = PartialChannel(channel_data, guild)
        self.channel = channel
        
        self.online_count = data.get('approximate_presence_count',0)
        self.user_count = data.get('approximate_member_count',0)
        
        try:
            inviter_data = data['inviter']
        except KeyError:
            inviter = ZEROUSER
        else:
            inviter = User(inviter_data)
        self.inviter = inviter
        
        self.uses = data.get('uses',None)
        self.max_age = data.get('max_age',None)
        self.max_uses = data.get('max_uses',None)
        self.temporary = data.get('temporary',True)
        
        try:
            created_at_data = data['created_at']
        except KeyError:
            created_at = DISCORD_EPOCH_START
        else:
            created_at = parse_time(created_at_data)
        self.created_at = created_at
        
        self.target_type = InviteTargetType.INSTANCES[data.get('target_user_type',0)]
        
        try:
            target_user_data=data['target_user']
        except KeyError:
            target_user=ZEROUSER
        else:
            target_user=User(target_user_data)
        self.target_user = target_user
        
    @classmethod
    def _create_vanity(cls ,guild, data):
        """
        Creates a vanity invite from the given guild and from the given invite data.
        
        Parameters
        ----------
        guild : ``Guild``
            The respective guild of the vanity invite.
        data : `dict` of (`str`, `Any`) items
            Invite data requested from Discord.
        
        Returns
        -------
        ivnite : ``Invite``
        """
        invite=object.__new__(cls)
        invite.code         = guild.vanity_code
        invite.inviter      = ZEROUSER
        invite.uses         = None
        invite.max_age      = None
        invite.max_uses     = None
        invite.temporary    = False
        invite.created_at   = None
        invite.guild        = guild
        try:
            channel_data = data['channel']
        except KeyError:
            channel = None
        else:
            channel = PartialChannel(channel_data, guild)
        invite.channel      = channel
        invite.online_count = 0
        invite.user_count   = 0
        invite.target_type  = InviteTargetType.NONE
        invite.target_user  = ZEROUSER
        
        return invite
    
    @property
    def partial(self):
        """
        Returns whether the integration is not fully loaded.
        
        Returns
        -------
        partial : `bool`
        """
        return bool(self.inviter.id)
    
    def __str__(self):
        """Returns the invite's url."""
        return self.url
    
    def __repr__(self):
        """Returns th represnetation of the invite."""
        return f'<{self.__class__.__name__} code={self.code!r}>'
    
    def __hash__(self):
        """Returns the invite's code's hash."""
        return hash(self.code)
    
    url = property(URLS.invite_url)
    if (__init__.__doc__ is not None):
        url.__doc__ = (
        """
        Returns the invite's url.
        
        Returns
        -------
        url : `str`
        """)
    
    # When we update it we get only a partial invite from Discord. So sad.
    def _update_no_return(self, data):
        """
        Updates the invite by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Requested invite data.
        """
        # Code can not change, I am pretty sure.
        try:
            self.online_count=data['approximate_presence_count']
            self.user_count=data['approximate_member_count']
        except KeyError:
            pass
    
    def _update(self, data):
        """
        Updates the invite and returns the changed attributes in a dictionary with `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Requested invite data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------+
        | Keys          | Values    |
        +===============+===========+
        | online_count  | `int`     |
        +---------------+-----------+
        | user_count    | `int`     |
        +---------------+-----------+
        """
        old_attributes = {}
        try:
            online_count=data['approximate_presence_count']
            if self.online_count!=online_count:
                old_attributes['online_count']=self.online_count
                self.online_count=online_count

            user_count=data['approximate_member_count']
            if self.user_count!=user_count:
                old_attributes['user_count']=self.user_count
                self.user_count=user_count
        except KeyError:
            pass
        
        return old_attributes

del URLS
