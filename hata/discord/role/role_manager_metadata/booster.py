__all__ = ('RoleManagerMetadataBooster',)

from scarletio import copy_docs

from .base import RoleManagerMetadataBase
from .constants import BOOSTER_KEY


class RoleManagerMetadataBooster(RoleManagerMetadataBase):
    """
    Role manager metadata of a booster role.
    """
    __slots__ = ()
    
    @copy_docs(RoleManagerMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        return {BOOSTER_KEY: None}
