__all__ = ('ChannelMetadataGuildVoiceBase',)

from scarletio import copy_docs

from .constants import BITRATE_DEFAULT, USER_LIMIT_DEFAULT
from .fields import (
    parse_bitrate, parse_region, parse_user_limit, put_bitrate_into, put_region_into, put_user_limit_into,
    validate_bitrate, validate_region, validate_user_limit
)
from .preinstanced import VoiceRegion

from .guild_main_base import ChannelMetadataGuildMainBase


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
    region : ``VoiceRegion``
        The voice region of the channel.
    user_limit : `int`
        The maximal amount of users, who can join the voice channel, or `0` if unlimited.
    
    Class Attributes
    ----------------
    order_group: `int` = `2`
        The channel's order group used when sorting channels.
    """
    __slots__ = ('bitrate', 'region', 'user_limit')
    
    order_group = 2
    
    
    @copy_docs(ChannelMetadataGuildMainBase.__hash__)
    def __hash__(self):
        hash_value = ChannelMetadataGuildMainBase.__hash__(self)
        
        # bitrate
        hash_value ^= self.bitrate << 12
        
        # region
        hash_value ^= hash(self.region)
        
        # user_limit
        hash_value ^= self.user_limit << 15
        
        return hash_value
    
    
    @copy_docs(ChannelMetadataGuildMainBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not ChannelMetadataGuildMainBase._is_equal_same_type(self, other):
            return False
        
        # bitrate
        if self.bitrate != other.bitrate:
            return False
        
        # region
        if self.region is not other.region:
            return False
        
        # user_limit
        if self.user_limit != other.user_limit:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ChannelMetadataGuildMainBase._create_empty)
    def _create_empty(cls):
        self = super(ChannelMetadataGuildVoiceBase, cls)._create_empty()
        
        self.bitrate = BITRATE_DEFAULT
        self.region = VoiceRegion.unknown
        self.user_limit = USER_LIMIT_DEFAULT
        
        return self
    
    
    @copy_docs(ChannelMetadataGuildMainBase._update_attributes)
    def _update_attributes(self, data):
        ChannelMetadataGuildMainBase._update_attributes(self, data)
        
        # bitrate
        self.bitrate = parse_bitrate(data)
        
        # region
        self.region = parse_region(data)
        
        # user_limit
        self.user_limit = parse_user_limit(data)
    
    
    @copy_docs(ChannelMetadataGuildMainBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = ChannelMetadataGuildMainBase._difference_update_attributes(self, data)
        
        # bitrate
        bitrate = parse_bitrate(data)
        if self.bitrate != bitrate:
            old_attributes['bitrate'] = self.bitrate
            self.bitrate = bitrate
        
        # region
        region = parse_region(data)
        if self.region is not region:
            old_attributes['region'] = self.region
            self.region = region
        
        # user_limit
        user_limit = parse_user_limit(data)
        if self.user_limit != user_limit:
            old_attributes['user_limit'] = self.user_limit
            self.user_limit = user_limit
        
        return old_attributes
    
    
    @copy_docs(ChannelMetadataGuildMainBase._set_attributes_from_keyword_parameters)
    def _set_attributes_from_keyword_parameters(self, keyword_parameters):
        ChannelMetadataGuildMainBase._set_attributes_from_keyword_parameters(self, keyword_parameters)
        
        # bitrate
        try:
            bitrate = keyword_parameters.pop('bitrate')
        except KeyError:
            pass
        else:
            self.bitrate = validate_bitrate(bitrate)
        
        # region
        try:
            region = keyword_parameters.pop('region')
        except KeyError:
            pass
        else:
            self.region = validate_region(region)
        
        # user_limit
        try:
            user_limit = keyword_parameters.pop('user_limit')
        except KeyError:
            pass
        else:
            self.user_limit = validate_user_limit(user_limit)
    
    
    @copy_docs(ChannelMetadataGuildMainBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = ChannelMetadataGuildMainBase.to_data(self, defaults = defaults, include_internals = include_internals)
        
        # bitrate
        put_bitrate_into(self.bitrate, data, defaults)
        
        # region
        put_region_into(self.region, data, defaults)
        
        # user_limit
        put_user_limit_into(self.user_limit, data, defaults)
        
        return data
