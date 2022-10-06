__all__ = ('MessageApplication', )

from ..bases import DiscordEntity, IconSlot
from ..http import urls as module_urls


class MessageApplication(DiscordEntity):
    """
    Might be sent with a ``Message``, if it has rich presence-related chat embeds.
    
    Attributes
    ----------
    id : `int`
        Unique identifier of the respective application.
    cover_hash : `int`
        The respective application's store cover image's hash in `uint128`. If the application is sold at Discord,
        this image will be used at the store.
    cover_type : ``IconType``
        The respective application's store cover image's type.
    description : `str`
        The respective application's description.
    icon_hash : `int`
        The respective application's icon's hash as `uint128`.
    icon_type : ``IconType``
        The respective application's icon's type.
    name : `str`
        The respective application's name.
    """
    __slots__ = ('description', 'name',)
    
    cover = IconSlot(
        'cover',
        'cover_image',
        module_urls.application_cover_url,
        module_urls.application_cover_url_as,
        add_updater = False,
    )
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.application_icon_url,
        module_urls.application_icon_url_as,
        add_updater = False,
    )
    
    def __init__(self, data):
        """
        Creates a new ``MessageApplication`` from message application data included inside of a ``Message``'s data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message application data.
        """
        self._set_cover(data)
        self.description = data['description']
        self._set_icon(data)
        self.id = int(data['id'])
        self.name = data['name']
    
    
    def __repr__(self):
        """Returns the representation of the message application."""
        return f'<{self.__class__.__name__} name={self.name!r}, id={self.id}>'
    
    
    def to_data(self):
        """
        Tries to convert the message application back to json serializable dictionary.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        return {
            'cover': self.cover.as_base_16_hash,
            'description': self.description,
            'icon': self.icon.as_base_16_hash,
            'id': str(self.id),
            'name': self.name,
        }
