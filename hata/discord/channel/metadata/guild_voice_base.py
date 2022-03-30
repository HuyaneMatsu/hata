__all__ = ('ChannelMetadataGuildVoiceBase',)

from scarletio import copy_docs, include

from ...preconverters import preconvert_int, preconvert_preinstanced_type

from .guild_main_base import ChannelMetadataGuildMainBase


VoiceRegion = include('VoiceRegion')


class ChannelMetadataGuildVoiceBase(ChannelMetadataGuildMainBase):
    """
    Guild voice channel metadata base.
    
    Attributes
    ----------
    _permission_cache : `None`, `dict` of (`int`, ``Permission``) items
        A `user_id` to ``Permission`` relation mapping for caching permissions. Defaults to `None`.
    parent_id : `int`
        The channel's parent's identifier.
    name : `str`
        The channel's name.
    permission_overwrites : `dict` of (`int`, ``PermissionOverwrite``) items
        The channel's permission overwrites.
    position : `int`
        The channel's position.
    bitrate : `int`
        The bitrate (in bits) of the voice channel.
    region : `None`, ``VoiceRegion``
        The voice region of the channel.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    
    Class Attributes
    ----------------
    type : `int` = `-1`
        The channel's type.
    order_group: `int` = `2`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('bitrate', 'region', 'user_limit')
    
    order_group = 2
    

    @copy_docs(ChannelMetadataGuildMainBase._compare_attributes_to)
    def _compare_attributes_to(self, other):
        if not ChannelMetadataGuildMainBase._compare_attributes_to(self, other):
            return False
        
        if self.bitrate != other.bitrate:
            return False
        
        if self.region is not other.region:
            return False
        
        if self.user_limit != other.user_limit:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildVoiceBase, cls)._create_empty()
        
        self.bitrate = 0
        self.region = None
        self.user_limit = 0
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildMainBase._update_attributes(self, data)
        
        self.bitrate = data['bitrate']
        self.user_limit = data['user_limit']
        
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        self.region = region
    
    
    @copy_docs(ChannelMetadataGuildMainBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildMainBase._difference_update_attributes(self, data)
        
        bitrate = data['bitrate']
        if self.bitrate != bitrate:
            old_attributes['bitrate'] = self.bitrate
            self.bitrate = bitrate
        
        user_limit = data['user_limit']
        if self.user_limit != user_limit:
            old_attributes['user_limit'] = self.user_limit
            self.user_limit = user_limit
        
        region = data.get('rtc_region', None)
        if (region is not None):
            region = VoiceRegion.get(region)
        if self.region is not region:
            old_attributes['region'] = self.region
            self.region = region
        
        return old_attributes
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase._precreate)
    def _precreate(cls, keyword_parameters):
        self = super(ChannelMetadataGuildVoiceBase, cls)._precreate(keyword_parameters)
        
        try:
            bitrate = keyword_parameters.pop('bitrate')
        except KeyError:
            pass
        else:
            bitrate = preconvert_int(bitrate, 'bitrate', 8000, 384000)
            self.bitrate = bitrate
            
        try:
            user_limit = keyword_parameters.pop('user_limit')
        except KeyError:
            pass
        else:
            user_limit = preconvert_int(user_limit, 'user_limit', 0, 99)
            self.user_limit = user_limit
        
        try:
            region = keyword_parameters.pop('region')
        except KeyError:
            pass
        else:
            region = preconvert_preinstanced_type(region, 'region', VoiceRegion)
            self.region = region
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase._to_data)
    def _to_data(self):
        data = ChannelMetadataGuildMainBase._to_data(self)
        
        data['bitrate'] = self.bitrate
        data['user_limit'] = self.user_limit
        
        region = self.region
        if (region is not None):
            region = region.value
        
        data['rtc_region'] = region
        
        return data
