__all__ = ('IntegrationDetail', )

from ..utils import parse_time, DISCORD_EPOCH_START
from ..role import create_partial_role_from_id

class IntegrationDetail:
    """
    Details about a non discord integration.
    
    expire_behaviour : `int`
        The behavior of expiring subscription. `0` for kick or `1` for remove role. Might be set as `-1`, if not
        applicable.
    expire_grace_period : `int`
        The grace period in days for expiring subscribers. Can be `1`, `3`, `7`, `14` or `30`. If the integration is
        partial, or is not applicable for it, then is set as `-1`.
    role : `None` or ``Role``
        The role what the integration uses for subscribers.
    subscriber_count : `int`
        How many subscribers the integration has. Defaults to `0`.
    synced_at : `datetime`
        When the integration was last synced.
    syncing : `bool`
        Whether the integration syncing.
    """
    __slots__ = ('expire_behavior', 'expire_grace_period', 'role', 'subscriber_count', 'synced_at', 'syncing', )
    
    def __init__(self, data):
        """
        Fills up the integration detail from the respective integration's data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received integration data.
        """
        self.syncing = data.get('syncing', False)
        
        try:
            role_id = data['role_id']
        except KeyError:
            role = None
        else:
            role = create_partial_role_from_id(int(role_id))
        self.role = role
        
        self.expire_behavior = data.get('expire_behavior', -1)
        
        self.expire_grace_period = data.get('expire_grace_period', -1)
        
        try:
            synced_at = data['synced_at']
        except KeyError:
            synced_at = DISCORD_EPOCH_START
        else:
            synced_at = parse_time(synced_at)
        self.synced_at = synced_at
        
        self.subscriber_count = data.get('subscriber_count', 0)
    
    @classmethod
    def from_role(cls, role):
        """
        Creates a partial integration detail with the given role.
        
        Parameters
        ----------
        role : ``Role``
            The respective role.
        
        Returns
        -------
        self : ``IntegrationDetail``
            The created integration detail.
        """
        self = object.__new__(cls)
        self.syncing = False
        self.role = role
        self.expire_behavior = -1
        self.expire_grace_period = -1
        self.synced_at = DISCORD_EPOCH_START
        self.subscriber_count = 0
        return self
    
    def __repr__(self):
        """Returns the integration detail's representation."""
        return f'<{self.__class__.__name__} role={self.role!r}>'
