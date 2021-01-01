# -*- coding: utf-8 -*-
__all__ = ('Invite', )

from datetime import datetime

from ..backend.utils import DOCS_ENABLED

from .bases import DiscordEntity, instance_or_id_to_instance
from .preconverters import preconvert_str, preconvert_int, preconvert_bool, preconvert_preinstanced_type
from .utils import parse_time, DISCORD_EPOCH_START
from .http import URLS
from .client_core import GUILDS, CHANNELS, INVITES
from .user import User, ZEROUSER
from .guild import create_partial_guild, Guild
from .channel import create_partial_channel, ChannelText, ChannelGroup, ChannelVoice, ChannelStore
from .preinstanced import InviteTargetType

Client = NotImplemented

class Invite(DiscordEntity, immortal=True):
    """
    Represents a Discord Invite.
    
    Attributes
    ---------
    channel : `None`, ``ChannelText``, ``ChannelVoice``, ``ChannelStore`` or ``ChannelGroup``
        The channel where the invite redirects. If it is announcements or store channel, then the invite is a lurk
        invite. If channel data was not sent with the invite's, then this attribute is set as `None`.
    code : `str`
        The invite's unique identifier.
    created_at : `datetime`
        When the invite was created. Defaults to Discord epoch.
    guild : `None` or ``Guild``
        The guild the invite is for. If not included or if the invite's channel is a group channel, then set as
        `None`.
    inviter : ``Client`` or ``User``
        The creator of the invite. If not included, then set as `ZEROUSER`.
    max_age : `None` or `int`
        The time in seconds after the invite will expire. If not included, then set as `None`.
        
        If the invite was created with max age as `0`, then this value will be negative instead of the expected `0`.
    max_uses : `None` or `int`
        How much times the invite can be used. If not included, then set as `None`.
        
        If the invite has no use limit, then this value is set as `0`.
    online_count : `int`
        The amount of online users at the respective guild (or group channel). If not included, then set as `0`.
    partial : `bool`
        Whether the invite is only partially loaded.
    target_type : ``InviteTargetType``
        The invite's target type.
    target_user : ``Client`` or ``User``
        The target of the invite if applicable. Defaults to `ZEROUSER`.
    temporary : `bool`
        Whether this invite only grants temporary membership.
        
        When the user goes offline, they get kicked, except if they got a role meanwhile.
    user_count : `int`
        The amount of users at the respective guild (or group channel). If not included, then set as `0`.
    uses : `None` or `int`
        The amount how much times the invite was used. If not included, set as `None`.
    """
    __slots__ = ('channel', 'code', 'created_at', 'guild', 'inviter', 'max_age', 'max_uses', 'online_count', 'partial',
        'target_type', 'target_user', 'temporary', 'user_count', 'uses',)
    
    def __new__(cls, data, data_partial):
        """
        Creates an invite from the given invite data. The invite data can be requested or received through the gateway
        as well.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Invite data.
        """
        code = data['code']
        
        try:
            invite = INVITES[code]
        except KeyError:
            invite = object.__new__(cls)
            invite.code = code
            invite.partial = data_partial
            updater = cls._set_attributes
        else:
            if invite.partial:
                if data_partial:
                    updater = cls._update_attributes
                else:
                    updater = cls._set_attributes
                    invite.partial = False
            else:
                if data_partial:
                    updater = cls._update_counts_only
                else:
                    updater = cls._update_attributes
        
        updater(invite, data)
        return invite
    
    @classmethod
    def _create_vanity(cls, guild, data):
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
        invite : ``Invite``
        """
        code = guild.vanity_code
        try:
            invite = INVITES[code]
        except KeyError:
            invite = object.__new__(cls)
        
        invite.code = code
        invite.inviter = ZEROUSER
        invite.uses = None
        invite.max_age = None
        invite.max_uses = None
        invite.temporary = False
        invite.created_at = DISCORD_EPOCH_START
        invite.guild = guild
        try:
            channel_data = data['channel']
        except KeyError:
            channel = None
        else:
            channel = create_partial_channel(channel_data, guild)
        invite.channel = channel
        invite.online_count = 0
        invite.user_count = 0
        invite.target_type = InviteTargetType.NONE
        invite.target_user = ZEROUSER
        invite.partial = True
        
        return invite
    
    def __str__(self):
        """Returns the invite's url."""
        return self.url
    
    def __repr__(self):
        """Returns the representation of the invite."""
        return f'<{self.__class__.__name__} code={self.code!r}>'
    
    def __hash__(self):
        """Returns the invite's code's hash."""
        return hash(self.code)
    
    url = property(URLS.invite_url)
    if DOCS_ENABLED:
        url.__doc__ = (
        """
        Returns the invite's url.
        
        Returns
        -------
        url : `str`
        """)
    
    @property
    def id(self):
        """
        Compatibility property with other Discord entities.
        
        Returns
        -------
        id : `int` = `0`
        """
        return 0
    
    # When we update it we get only a partial invite from Discord. So sad.
    def _set_attributes(self, data):
        """
        Updates the invite by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Invite data.
        """
        try:
            guild_data = data['guild']
        except KeyError:
            try:
                guild_id = data['guild_id']
            except KeyError:
                guild = None
            else:
                guild_id = int(guild_id)
                guild = GUILDS.get(guild_id, None)
        else:
            guild = create_partial_guild(guild_data)
        
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
            channel = create_partial_channel(channel_data, guild)
        self.channel = channel
        
        self.online_count = data.get('approximate_presence_count', 0)
        self.user_count = data.get('approximate_member_count', 0)
        
        try:
            inviter_data = data['inviter']
        except KeyError:
            inviter = ZEROUSER
        else:
            inviter = User(inviter_data)
        self.inviter = inviter
        
        self.uses = data.get('uses', None)
        self.max_age = data.get('max_age', None)
        self.max_uses = data.get('max_uses', None)
        self.temporary = data.get('temporary', True)
        
        try:
            created_at_data = data['created_at']
        except KeyError:
            created_at = DISCORD_EPOCH_START
        else:
            created_at = parse_time(created_at_data)
        self.created_at = created_at
        
        self.target_type = InviteTargetType.get(data.get('target_user_type', 0))
        
        try:
            target_user_data = data['target_user']
        except KeyError:
            target_user = ZEROUSER
        else:
            target_user = User(target_user_data)
        
        self.target_user = target_user
    
    def _update_attributes(self, data):
        """
        Updates the invite with the given data. Only updates the attributes, which's respective value is included.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Invite data.
        """
        guild = self.guild
        if guild is None:
            try:
                guild_data = data['guild']
            except KeyError:
                try:
                    guild_id = data['guild_id']
                except KeyError:
                    guild = None
                else:
                    guild_id = int(guild_id)
                    guild = GUILDS.get(guild_id, None)
            else:
                guild = create_partial_guild(guild_data)
            
            self.guild = guild
        
        if self.channel is None:
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
                channel = create_partial_channel(channel_data, guild)
            
            self.channel = channel
        
        try:
            self.online_count = data['approximate_presence_count']
        except KeyError:
            pass
        
        try:
            self.user_count = data['approximate_member_count']
        except KeyError:
            pass
        
        try:
            inviter_data = data['inviter']
        except KeyError:
            pass
        else:
            self.inviter = User(inviter_data)
        
        try:
            self.uses = data['uses']
        except KeyError:
            pass
        
        try:
            self.max_age = data['max_age']
        except KeyError:
            pass
        
        try:
            self.max_uses = data['max_uses']
        except KeyError:
            pass
        
        try:
            self.temporary = data['temporary']
        except KeyError:
            pass
        
        try:
            created_at_data = data['created_at']
        except KeyError:
            pass
        else:
            self.created_at = parse_time(created_at_data)
        
        try:
            target_type_value = data['target_user_type']
        except KeyError:
            pass
        else:
            self.target_type = InviteTargetType.get(target_type_value)
        
        try:
            target_user_data = data['target_user']
        except KeyError:
            pass
        else:
            self.target_user = User(target_user_data)
    
    def _update_counts_only(self, data):
        """
        Updates the invite's counts if given.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received invite data.
        """
        try:
            self.online_count = data['approximate_presence_count']
        except KeyError:
            pass
        
        try:
            self.user_count = data['approximate_member_count']
        except KeyError:
            pass
    
    @classmethod
    def precreate(cls, code, **kwargs):
        """
        Precreates an invite object with the given parameters.
        
        Parameters
        ----------
        code : `str`
            The invite's code.
        **kwargs : keyword arguments
            Additional predefined attributes for the invite.
        
        Other Parameters
        ----------------
        channel : `None`, ``ChannelText``, ``ChannelVoice``, ``ChannelStore`` or ``ChannelGroup``
            The channel where the invite redirects.
        created_at : `datetime`
            When the invite was created.
        guild : `None` or ``Guild``
            The guild the invite is for.
        inviter : `int`, `str`, ``Client`` or ``User``
            The creator of the invite.
        max_age : `None` or `int`
            The time in seconds after the invite will expire.
        max_uses : `None` or `int`
            How much times the invite can be used.
        online_count : `int`
            The amount of online users at the respective guild (or group channel).
        target_type : `int` or ``InviteTargetType``
            The invite's target type.
        target_user : `int`, `str`, ``Client`` or ``User``
            The target of the invite.
        temporary : `bool`
            Whether this invite only grants temporary membership.
        user_count : `int`
            The amount of users at the respective guild (or group channel).
        uses : `None` or `int`
            The amount how much times the invite was used.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
        """
        code = preconvert_str(code, 'code', 2, 32)

        if kwargs:
            processable = []
            for key in ('uses', 'max_age', 'max_uses' ):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    if (value is not None):
                        value = preconvert_int(value, key, 0, (1<<64)-1)
                        processable.append((key, value))
            
            try:
                temporary = kwargs.pop('temporary')
            except KeyError:
                pass
            else:
                temporary = preconvert_bool(temporary, 'temporary')
                processable.append(('temporary', temporary))
            
            try:
                created_at = kwargs.pop('created_at')
            except KeyError:
                pass
            else:
                created_at_type = created_at.__class__
                if (created_at_type is not datetime):
                    raise TypeError(f'`\'created_at\'` can be `int` instance, got {created_at_type.__name__}.')
                processable.append(('created_at', created_at))
            
            for key in ('inviter', 'target_user',):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = instance_or_id_to_instance(value, (User, Client), key)
                    processable.append((key, value))
            
            for key in ('online_count', 'user_count',):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_int(value, key, 0, (1<<64)-1)
                    processable.append((key, value))
            
            for key, type_ in (
                    ('guild', Guild),
                    ('channel', (ChannelText, ChannelGroup, ChannelVoice, ChannelStore)),
                        ):
                
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    if (value is not None):
                        value = instance_or_id_to_instance(value, type_, key)
                        processable.append((key, value))
                    
            try:
                target_type = kwargs.pop('target_type')
            except KeyError:
                pass
            else:
                target_type = preconvert_preinstanced_type(target_type, InviteTargetType, 'target_type')
                processable.append(('target_type', target_type))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}.')
        
        else:
            processable = None
        
        try:
            invite = INVITES[code]
        except KeyError:
            invite = object.__new__(cls)
            invite.code = code
            invite.inviter = ZEROUSER
            invite.uses = None
            invite.max_age = None
            invite.max_uses = None
            invite.temporary = False
            invite.created_at = DISCORD_EPOCH_START
            invite.guild = None
            invite.channel = None
            invite.online_count = 0
            invite.user_count = 0
            invite.target_type = InviteTargetType.NONE
            invite.target_user = ZEROUSER
            invite.partial = True
            
            INVITES[code] = invite
        else:
            if not invite.partial:
                return invite
        
        if (processable is not None):
            for item in processable:
                setattr(invite, *item)
        
        return invite

del URLS
del DOCS_ENABLED
