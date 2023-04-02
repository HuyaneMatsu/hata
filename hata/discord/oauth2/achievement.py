# Achievements are deprecated on discord side, no need to update them.
__all__ = ('Achievement', )

from ...env import API_VERSION

from ..bases import DiscordEntity, IconSlot
from ..http import urls as module_urls
from ..localization.utils import build_locale_dictionary
from ..utils import DATETIME_FORMAT_CODE


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
    description_localizations : `None`, `dict` of (`str`, `str`) items
        Localized descriptions of the achievement.
    icon_hash : `int`
        The achievement's icon's hash. Achievements always have icon.
    icon_type : ``IconType``
        The achievement's icon's type.
    name : `str`
        The name of the achievement.
    name_localizations : `None`, `dict` of (`str`, `str`) items
        Localized names of the achievement.
    secret : `bool`
        Secret achievements will *not* be shown to the user until they've unlocked them.
    secure : `bool`
        Secure achievements can only be set via HTTP calls from your server, not by a game client using the SDK.
    """
    __slots__ = (
        'application_id', 'description', 'description_localizations', 'name', 'name_localizations', 'secret', 'secure'
    )
    
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
        return f'<{self.__class__.__name__} id = {self.id}, name = {self.name!r}>'
    
    
    def __format__(self, code):
        """Formats the achievement with the given format code."""
        if not code:
            return self.name
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}.'
        )
    
    
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
        
        +---------------------------+-------------------------------------------+
        | Keys                      | Values                                    |
        +===========================+===========================================+
        | description               | `str`                                     |
        +---------------------------+-------------------------------------------+
        | description_localizations | `None`, `dict` of (`str`, `str`) items    |
        +---------------------------+-------------------------------------------+
        | icon                      | ``Icon``                                  |
        +---------------------------+-------------------------------------------+
        | name                      | `str`                                     |
        +---------------------------+-------------------------------------------+
        | name_localizations        | `None`, `dict` of (`str`, `str`) items    |
        +---------------------------+-------------------------------------------+
        | secret                    | `bool`                                    |
        +---------------------------+-------------------------------------------+
        | secure                    | `bool`                                    |
        +---------------------------+-------------------------------------------+
        """
        old_attributes = {}
        
        if API_VERSION >= 10:
            name_localizations = data['name_localizations']
            if not name_localizations:
                name_localizations = None
            
            name = data['name']
            
            description_localizations = data['description_localizations']
            if not description_localizations:
                description_localizations = None
            
            description = data['description']
        
        else:
            name_localizations = data['name']
            name = data.pop('default')
            if not name_localizations:
                name_localizations = None
            
            description_localizations = data['description']
            description = description_localizations.pop('default')
            if not description_localizations:
                description_localizations = None
        
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        
        if self.description != description:
            old_attributes['description'] = self.description
            self.description = description
        
        
        if self.name_localizations != name_localizations:
            old_attributes['name_localizations'] = self.name_localizations
            self.name_localizations = build_locale_dictionary(name_localizations)
        
        
        if self.description_localizations != description_localizations:
            old_attributes['description_localizations'] = self.description_localizations
            self.description_localizations = build_locale_dictionary(description_localizations)
        
        
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
        if API_VERSION >= 10:
            name_localizations = data['name_localizations']
            if not name_localizations:
                name_localizations = None
            
            name = data['name']
            
            description_localizations = data['description_localizations']
            if not description_localizations:
                description_localizations = None
            
            description = data['description']
        
        else:
            name_localizations = data['name']
            name = data.pop('default')
            if not name_localizations:
                name_localizations = None
            
            description_localizations = data['description']
            description = description_localizations.pop('default')
            if not description_localizations:
                 description_localizations = None
        
        
        self.name = name
        self.description = description
        
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        
        self.secret = data['secret']
        self.secure = data['secure']
        
        self._set_icon(data)
