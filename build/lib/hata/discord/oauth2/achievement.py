__all__ = ('Achievement', )

from ..bases import DiscordEntity, IconSlot
from ..utils import DATETIME_FORMAT_CODE

from ..http import urls as module_urls

class Achievement(DiscordEntity):
    """
    Represents a Discord achievement created at Developer portal.
    
    Attributes
    ----------
    id : `int`
        The achievement's unique identifier number.
    application_id : `int`
        The achievement's respective application's id.
    description : `str`
        The description of the achievement.
    name : `str`
        The name of the achievement.
    secret : `bool`
        Secret achievements will *not* be shown to the user until they've unlocked them.
    secure : `bool`
        Secure achievements can only be set via HTTP calls from your server, not by a game client using the SDK.
    icon_hash : `int`
        The achievement's icon's hash. Achievements always have icon.
    icon_type : ``IconType``
        The achievement's icon's type.
    """
    __slots__ = ('application_id', 'description', 'name', 'secret', 'secure',)
    
    icon = IconSlot('icon', 'icon_hash', module_urls.achievement_icon_url, module_urls.achievement_icon_url_as)
    
    def __init__(self, data):
        """
        Creates an achievement with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received achievement data.
        """
        self.application_id = int(data['application_id'])
        self.id = int(data['id'])
        
        self._update_attributes(data)
    
    def __repr__(self):
        """Returns the achievement's representation."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}>'
    
    
    def __format__(self,code):
        if not code:
            return self.name
        
        if code=='c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
    def _difference_update_attributes(self, data):
        """
        Updates the achievement and returns it's overwritten attributes as a `dict` with a `attribute-name` -
        `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Achievement data received from Discord.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-----------+
        | Keys          | Values    |
        +===============+===========+
        | name          | `str`     |
        +---------------+-----------+
        | description   | `str`     |
        +---------------+-----------+
        | secret        | `bool`    |
        +---------------+-----------+
        | secure        | `bool`    |
        +---------------+-----------+
        | icon          | ``Icon``  |
        +---------------+-----------+
        """
        old_attributes = {}
        
        name = data['name']['default']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        description = data['description']['default']
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        secret = data['secret']
        if self.secret != secret:
            old_attributes['secret'] = self.secret
            self.secret = secret
        
        secure = data['secure']
        if self.secure != secure:
            old_attributes['secure'] = self.secure
            self.secure = secure
        
        self._update_icon(data, old_attributes)
        
        return old_attributes
    
    def _update_attributes(self, data):
        """
        Updates the achievement with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Achievement data received from Discord.
        """
        self.name = data['name']['default']
        self.description = data['description']['default']
        
        self.secret = data['secret']
        self.secure = data['secure']
        
        self._set_icon(data)
