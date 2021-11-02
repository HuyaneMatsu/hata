__all__ = ('Invite',)

from datetime import datetime

from ..bases import DiscordEntity, instance_or_id_to_instance
from ..preconverters import preconvert_str, preconvert_int, preconvert_bool, preconvert_preinstanced_type
from ..utils import timestamp_to_datetime, DISCORD_EPOCH_START
from ..core import GUILDS, CHANNELS, INVITES
from ..user import User, ZEROUSER, ClientUserBase
from ..guild import create_partial_guild_from_data, Guild
from ..channel import create_partial_channel_from_data, ChannelText, ChannelGroup, ChannelVoice, ChannelStore, \
    ChannelDirectory
from ..application import Application
from ..http import urls as module_urls

from .preinstanced import InviteTargetType
from .invite_stage import InviteStage

# Experimental addition

EMBEDDED_ACTIVITY_NAME_TO_APPLICATION_ID = {
    'Betrayal.io': 773336526917861400,
    'Chess in The Park': 832012774040141894,
    'Fishington.io': 814288819477020702,
    'Poker Night': 755827207812677713,
    'YouTube Together': 755600276941176913,
}

EMBEDDED_ACTIVITY_APPLICATION_ID_TO_NAME = {
    value: key for key, value in EMBEDDED_ACTIVITY_NAME_TO_APPLICATION_ID.items()
}

class Invite(DiscordEntity, immortal=True):
    """
    Represents a Discord Invite.
    
    Attributes
    ---------
    approximate_online_count : `int`
        The approximate amount of online users at the respective guild (or group channel). If not included, then set
        as `0`.
    approximate_user_count : `int`
        The approximate amount of users at the respective guild (or group channel). If not included, then set as `0`.
    channel : `None`, ``ChannelText``, ``ChannelVoice``, ``ChannelStore``, ``ChannelGroup`` or ``ChannelDirectory``
        The channel where the invite redirects. If it is announcements or store channel, then the invite is a lurk
        invite. If channel data was not sent with the invite's, then this attribute is set as `None`.
    code : `str`
        The invite's unique identifier.
    created_at : `datetime`
        When the invite was created. Defaults to Discord epoch.
    guild : `None` or ``Guild``
        The guild the invite is for. If not included or if the invite's channel is a group channel, then set as
        `None`.
    inviter : ``ClientUserBase``
        The creator of the invite. If not included, then set as `ZEROUSER`.
    max_age : `None` or `int`
        The time in seconds after the invite will expire. If not included, then set as `None`.
        
        If the invite was created with max age as `0`, then this value will be negative instead of the expected `0`.
    max_uses : `None` or `int`
        How much times the invite can be used. If not included, then set as `None`.
        
        If the invite has no use limit, then this value is set as `0`.
    partial : `bool`
        Whether the invite is only partially loaded.
    stage : `None` or ``InviteStage``
        A invite stage instance representing the stage to which the invite is created to.
    target_type : ``InviteTargetType``
        The invite's target type.
    target_application : `None` or ``Application``
        The invite's target application.
    target_user : ``ClientUserBase``
        The target of the invite if applicable. Defaults to `ZEROUSER`.
    temporary : `bool`
        Whether this invite only grants temporary membership.
        
        When the user goes offline, they get kicked, except if they got a role meanwhile.
    uses : `None` or `int`
        The amount how much times the invite was used. If not included, set as `None`.
    """
    __slots__ = ('approximate_user_count', 'approximate_online_count', 'channel', 'code', 'created_at', 'guild',
        'inviter', 'max_age', 'max_uses', 'partial', 'target_application', 'stage', 'target_type', 'target_user',
        'temporary', 'uses',)
    
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
            self = INVITES[code]
        except KeyError:
            self = object.__new__(cls)
            self.code = code
            self.partial = data_partial
            INVITES[code] = self
            updater = cls._set_attributes
        else:
            if self.partial:
                if data_partial:
                    updater = cls._update_attributes
                else:
                    updater = cls._set_attributes
                    self.partial = False
            else:
                if data_partial:
                    updater = cls._update_counts_only
                else:
                    updater = cls._update_attributes
        
        updater(self, data)
        return self
    
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
            self = INVITES[code]
        except KeyError:
            self = object.__new__(cls)
        
        self.code = code
        self.inviter = ZEROUSER
        self.uses = None
        self.max_age = None
        self.max_uses = None
        self.temporary = False
        self.created_at = DISCORD_EPOCH_START
        self.guild = guild
        try:
            channel_data = data['channel']
        except KeyError:
            channel = None
        else:
            channel = create_partial_channel_from_data(channel_data, guild.id)
        self.channel = channel
        self.approximate_online_count = 0
        self.approximate_user_count = 0
        self.target_type = InviteTargetType.none
        self.target_user = ZEROUSER
        self.target_application = None
        self.partial = True
        self.stage = None
        
        return self
    
    def __repr__(self):
        """Returns the representation of the invite."""
        return f'<{self.__class__.__name__} code={self.code!r}>'
    
    def __hash__(self):
        """Returns the invite's code's hash."""
        return hash(self.code)
    
    url = property(module_urls.invite_url)
    
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
            guild = create_partial_guild_from_data(guild_data)
        
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
                channel = CHANNELS.get(channel_id, None)
        else:
            channel = create_partial_channel_from_data(channel_data, guild.id)
        self.channel = channel
        
        try:
            approximate_online_count = data['approximate_presence_count']
        except KeyError:
            approximate_online_count = 0
        else:
            if (guild is not None):
                guild.approximate_online_count = approximate_online_count
        
        self.approximate_online_count = approximate_online_count
        
        try:
            approximate_user_count = data['approximate_member_count']
        except KeyError:
            approximate_user_count = 0
        else:
            if (guild is not None):
                guild.approximate_user_count = approximate_user_count
            
        self.approximate_user_count = approximate_user_count
        
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
            created_at = timestamp_to_datetime(created_at_data)
        self.created_at = created_at
        
        self.target_type = InviteTargetType.get(data.get('target_type', 0))
        
        try:
            target_user_data = data['target_user']
        except KeyError:
            target_user = ZEROUSER
        else:
            target_user = User(target_user_data)
        
        self.target_user = target_user
        
        try:
            target_application_data = data['target_application']
        except KeyError:
            target_application = None
        else:
            target_application = Application(target_application_data)
        
        self.target_application = target_application
        
        try:
            invite_stage_data = data['stage_instance']
        except KeyError:
            invite_stage = None
        else:
            invite_stage = InviteStage(invite_stage_data, guild)
        self.stage = invite_stage
    
    
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
                guild = create_partial_guild_from_data(guild_data)
            
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
                    channel = CHANNELS.get(channel_id, None)
            else:
                channel = create_partial_channel_from_data(channel_data, guild.id)
            
            self.channel = channel
        
        self._update_counts_only(data)
        
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
            self.created_at = timestamp_to_datetime(created_at_data)
        
        try:
            target_type_value = data['target_type']
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
    
        try:
            target_application_data = data['target_application']
        except KeyError:
            pass
        else:
            self.target_application = Application(target_application_data)
        
        try:
            invite_stage_data = data['stage_instance']
        except KeyError:
            pass
        else:
            self.stage = InviteStage(invite_stage_data, guild)
    
    
    def _update_counts_only(self, data):
        """
        Updates the invite's counts if given.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received invite data.
        """
        guild = self.guild
        try:
            approximate_online_count = data['approximate_presence_count']
        except KeyError:
            pass
        else:
            self.approximate_online_count = approximate_online_count
            if (guild is not None):
                guild.approximate_online_count = approximate_online_count
        
        try:
            approximate_user_count = data['approximate_member_count']
        except KeyError:
            pass
        else:
            self.approximate_user_count = approximate_user_count
            if (guild is not None):
                guild.approximate_user_count = approximate_user_count
    
    
    @classmethod
    def precreate(cls, code, **kwargs):
        """
        Precreates an invite object with the given parameters.
        
        Parameters
        ----------
        code : `str`
            The invite's code.
        **kwargs : keyword parameters
            Additional predefined attributes for the invite.
        
        Other Parameters
        ----------------
        channel : `None`, ``ChannelText``, ``ChannelVoice``, ``ChannelStore``, ``ChannelGroup`` or
                ``ChannelDirectory``, Optional (Keyword only)
            The channel where the invite redirects.
        created_at : `datetime`, Optional (Keyword only)
            When the invite was created.
        guild : `None` or ``Guild``, Optional (Keyword only)
            The guild the invite is for.
        inviter : `int`, `str`, ``ClientUserBase``, Optional (Keyword only)
            The creator of the invite.
        max_age : `None` or `int`, Optional (Keyword only)
            The time in seconds after the invite will expire.
        max_uses : `None` or `int`, Optional (Keyword only)
            How much times the invite can be used.
        approximate_online_count : `int`, Optional (Keyword only)
            The amount of online users at the respective guild (or group channel).
        target_type : `int` or ``InviteTargetType``, Optional (Keyword only)
            The invite's target type.
        target_application : `int`, `str` or ``Application``, Optional (Keyword only)
            The target application of the invite.
        target_user : `int`, `str`, ``ClientUserBase``, Optional (Keyword only)
            The target user of the invite.
        temporary : `bool`, Optional (Keyword only)
            Whether this invite only grants temporary membership.
        approximate_user_count : `int`, Optional (Keyword only)
            The amount of users at the respective guild (or group channel).
        uses : `None` or `int`, Optional (Keyword only)
            The amount how much times the invite was used.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
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
                    value = instance_or_id_to_instance(value, ClientUserBase, key)
                    processable.append((key, value))
            
            for key in ('approximate_online_count', 'approximate_user_count',):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    pass
                else:
                    value = preconvert_int(value, key, 0, (1<<64)-1)
                    processable.append((key, value))
            
            for key, type_ in (
                    ('guild', Guild),
                    ('channel', (ChannelText, ChannelGroup, ChannelVoice, ChannelStore, ChannelDirectory)),
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
            
            try:
                target_application = kwargs.pop('target_application')
            except KeyError:
                pass
            else:
                value = instance_or_id_to_instance(target_application, Application, key)
                processable.append(('target_application', value))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}.')
        
        else:
            processable = None
        
        try:
            self = INVITES[code]
        except KeyError:
            self = object.__new__(cls)
            self.code = code
            self.inviter = ZEROUSER
            self.uses = None
            self.max_age = None
            self.max_uses = None
            self.temporary = False
            self.created_at = DISCORD_EPOCH_START
            self.guild = None
            self.channel = None
            self.approximate_online_count = 0
            self.approximate_user_count = 0
            self.target_type = InviteTargetType.none
            self.target_user = None
            self.target_user = ZEROUSER
            self.partial = True
            self.stage = None
            
            INVITES[code] = self
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
