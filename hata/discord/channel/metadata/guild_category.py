__all__ = ('ChannelMetadataGuildCategory',)

from scarletio import copy_docs

from .guild_main_base import ChannelMetadataGuildMainBase


class ChannelMetadataGuildCategory(ChannelMetadataGuildMainBase):
    """
    Guild category channel metadata.
    
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
    
    Class Attributes
    ----------------
    order_group: `int` = `4`
        The channel's order group used when sorting channels.
    """
    __slots__ = ()
    
    order_group = 4
    
    @copy_docs(ChannelMetadataGuildMainBase._get_display_name)
    def _get_display_name(self):
        return self.name.upper()
