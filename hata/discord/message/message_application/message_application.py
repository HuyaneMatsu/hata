__all__ = ('MessageApplication',)

from ...bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ...http import urls as module_urls
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_description, parse_id, parse_name, put_description_into, put_id_into, put_name_into,
    validate_description, validate_id, validate_name
)

APPLICATION_COVER = IconSlot(
    'cover',
    'cover_image',
    module_urls.application_cover_url,
    module_urls.application_cover_url_as,
    add_updater = False,
)

APPLICATION_ICON = IconSlot(
    'icon',
    'icon',
    module_urls.application_icon_url,
    module_urls.application_icon_url_as,
    add_updater = False,
)

PRECREATE_FIELDS = {
    'cover': ('cover', APPLICATION_COVER.validate_icon),
    'description': ('description', validate_description),
    'icon': ('icon', APPLICATION_ICON.validate_icon),
    'name': ('name', validate_name),
}


class MessageApplication(DiscordEntity):
    """
    Might be sent with a ``Message`` if it has rich presence-related chat embeds.
    
    Attributes
    ----------
    cover_hash : `int`
        The respective application's store cover image's hash in `uint128`. If the application is sold at Discord,
        this image will be used at the store.
    cover_type : ``IconType``
        The respective application's store cover image's type.
    description : `None` `str`
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
    __slots__ = ('description', 'name', )
    
    cover = APPLICATION_COVER
    icon = APPLICATION_ICON
    
    def __new__(cls, *, cover = ..., description = ..., icon = ..., name = ...):
        """
        Creates a new message application from the given keyword parameters.
        
        Parameters
        ----------
        cover : `None`, `bytes`, `bytearray`, `memoryview`, ``Icon``, Optional (Keyword only)
            The cover of the message application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        icon : `None`, `bytes`, `bytearray`, `memoryview`, ``Icon``, Optional (Keyword only)
            The icon of the message application.
        
        name : `None, `str`, Optional (Keyword only)
            The name of the application.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # cover
        if cover is ...:
            cover = None
        else:
            cover = cls.cover.validate_icon(cover, allow_data = True)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon, allow_data = True)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # Construct
        self = object.__new__(cls)
        self.cover = cover
        self.description = description
        self.icon = icon
        self.id = 0
        self.name = name
        return self
    
    
    @classmethod
    def precreate(cls, message_application_id, **keyword_parameters):
        """
        Creates a new message application with the given predefined fields.
        
        > Since message applications are not globally cached, this method is only used for testing.
        
        Parameters
        ----------
        message_application_id : `int`
            The message application's id.
        
        **keyword_parameters : Keyword parameters
            The attributes to set.
        
        Other Parameters
        ----------------
        cover : `None`, ``Icon``, Optional (Keyword only)
            The cover of the message application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        icon : `None`, ``Icon``, Optional (Keyword only)
            The icon of the message application.
        
        name : `None, `str`, Optional (Keyword only)
            The name of the application.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        message_application_id = validate_id(message_application_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        self = cls._create_empty(message_application_id)
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, message_application_id):
        """
        Creates a new message application with it's defaults attributes set.
        
        Parameters
        ----------
        message_application_id : `int`
            The message application's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.cover_type = ICON_TYPE_NONE
        self.cover_hash = 0
        self.description = None
        self.icon_type = ICON_TYPE_NONE
        self.icon_hash = 0
        self.id = message_application_id
        self.name = ''
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message application instance with the given application data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application data included within message payload.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._set_cover(data)
        self.description = parse_description(data)
        self._set_icon(data)
        self.id = parse_id(data)
        self.name = parse_name(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the message application to json serializable data.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        type(self).cover.put_into(self.cover, data, defaults, as_data = not include_internals)
        put_description_into(self.description, data, defaults)
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        put_name_into(self.name, data, defaults)
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        return data
    
    
    @property
    def partial(self):
        """
        Returns whether the message application is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return (self.id == 0)
    
    
    def __eq__(self, other):
        """Returns whether the two message applications are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two message applications not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id
        self_id = self.id
        other_id = other.id
        if (self_id and other_id) and (self_id != other_id):
            return False
        
        # cover_hash
        if self.cover_hash != other.cover_hash:
            return False
        
        # cover_type
        if self.cover_type != other.cover_type:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # icon_hash
        if self.icon_hash != other.icon_hash:
            return False
        
        # icon_type
        if self.icon_type != other.icon_type:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the message application's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        message_application_id = self.id
        if message_application_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(message_application_id))
        else:
            repr_parts.append(' (partial)')
        
        name = self.name
        if name:
            repr_parts.append(', name = ')
            repr_parts.append(repr(name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the message application's hash value."""
        # These entities are not cached, so we wont use their `id` if applicable.
        hash_value = 0
        
        # cover
        hash_value ^= hash(self.cover)
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # icon
        hash_value ^= hash(self.icon)
        
        # id
        hash_value ^= self.id
        
        # name
        name = self.name
        if (description is None) or (description != name):
            hash_value ^= hash(name)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the message application returning a new partial one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.cover_hash = self.cover_hash
        new.cover_type = self.cover_type
        new.description = self.description
        new.icon_hash = self.icon_hash
        new.icon_type = self.icon_type
        new.id = 0
        new.name = self.name
        return new


    def copy_with(self, *, cover = ..., description = ..., icon = ..., name = ...):
        """
        Copies the message application with the given fields returning a new partial one.
        
        Parameters
        ----------
        cover : `None`, `bytes`, `bytearray`, `memoryview`, ``Icon``, Optional (Keyword only)
            The cover of the message application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        icon : `None`, `bytes`, `bytearray`, `memoryview`, ``Icon``, Optional (Keyword only)
            The icon of the message application.
        
        name : `None, `str`, Optional (Keyword only)
            The name of the application.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # cover
        if cover is ...:
            cover = self.cover
        else:
            cover = type(self).cover.validate_icon(cover, allow_data = True)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon, allow_data = True)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # Construct
        new = object.__new__(type(self))
        new.cover = cover
        new.description = description
        new.icon = icon
        new.id = 0
        new.name = name
        return new
