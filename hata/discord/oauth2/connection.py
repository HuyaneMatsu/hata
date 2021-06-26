__all__ = ('Connection', )

from ..integration import Integration
from ..bases import DiscordEntity


class Connection(DiscordEntity):
    """
    A connection object that a user is attached to.
    
    Attributes
    ----------
    id : `int`
        The unique identifier value of the connection.
    friend_sync : `bool`
        Whether the user has friend sync enabled for the connection.
    integrations : `None` or (`list` of ``Integration``)
        A list (if any) of guild integrations which are attached to the connection.
    name : `str`
        The username of the connected account.
    revoked : `bool`
        Whether the connection is revoked.
    show_activity : `bool`
        Whether activity related to this connection will be shown in presence updates.
    type : `str`
        The service of the connection. (Like `'twitch'` or `'youtube'`.)
    verified : `bool`
        Whether the connection is verified.
    visibility : `int`
        For who is the connection visible for.
        
        Possible visibility values
        +-------+-------------------------------+
        | value | description                   |
        +=======+===============================+
        | 0     | Visible only for the user.    |
        +-------+-------------------------------+
        | 1     | Visible to everyone.          |
        +-------+-------------------------------+
    """
    __slots__ = ('friend_sync', 'integrations', 'name', 'revoked', 'show_activity', 'type', 'verified', 'visibility',)
    
    def __init__(self, data):
        """
        Creates a connection object from received connection data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`)
            Received connection data.
        """
        self.name = data['name']
        self.type = data['type']
        self.id = int(data['id'])
        self.revoked = data.get('revoked', False)
        self.verified = data.get('verified', False)
        self.show_activity = data.get('show_activity', False)
        self.friend_sync = data.get('friend_sync', False)
        self.visibility = data.get('visibility', 0)
        
        try:
            integration_datas = data['integrations']
        except KeyError:
            integrations = None
        else:
            if integration_datas:
                integrations = [Integration(integration_data) for integration_data in integration_datas]
            else:
                integrations = None
        self.integrations = integrations
