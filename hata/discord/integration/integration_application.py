__all__ = ('IntegrationApplication',)

import warnings

from ..bases import DiscordEntity, IconSlot
from ..http import urls as module_urls
from ..user import User, ZEROUSER


class IntegrationApplication(DiscordEntity):
    """
    Represents a Discord ``Application`` received with Integration data.
    
    Attributes
    ----------
    bot : ``ClientUserBase``
        The application's bot if applicable.
    description : `str`
        The description of the application. Defaults to empty string.
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    icon_type : `IconType`
        The application's icon's type.
    id : `int`
        The application's id.
    name : `str`
        The name of the application. Defaults to empty string.
    """
    __slots__ = ('bot', 'description', 'name', )
    
    icon = IconSlot('icon', 'icon', module_urls.application_icon_url, module_urls.application_icon_url_as,)
    
    def __init__(self, data):
        """
        Creates a new integration application instance with the given application data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application data included within integration payload.
        """
        self.id = int(data['id'])
        self.name = data['name']
        self.description = data['description']
        self._set_icon(data)
        
        bot_data = data.get('bot', None)
        if bot_data is None:
            bot = ZEROUSER
        else:
            bot = User.from_data(bot_data)
        
        self.bot = bot
    
    
    @property
    def summary(self):
        """
        `.summary` is deprecated and will be removed in 2022 Jun. Please use `.description` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.summary` is deprecated and will be removed in 2022 Jun. '
                f'Please use `.description` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return ''
