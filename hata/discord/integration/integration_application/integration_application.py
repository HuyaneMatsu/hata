__all__ = ('IntegrationApplication',)

from ...bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ...http import urls as module_urls
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import ZEROUSER

from .fields import (
    parse_bot, parse_description, parse_id, parse_name, put_bot_into, put_description_into, put_id_into, put_name_into,
    validate_bot, validate_description, validate_id, validate_name
)

application_icon = IconSlot('icon', 'icon', module_urls.application_icon_url, module_urls.application_icon_url_as)


PRECREATE_FIELDS = {
    'bot': ('bot', validate_bot),
    'description': ('description', validate_description),
    'icon': ('icon', application_icon.validate_icon),
    'name': ('name', validate_name),
}


class IntegrationApplication(DiscordEntity):
    """
    Represents a Discord ``Application`` received with Integration data.
    
    Attributes
    ----------
    id : `int`
        The application's id.
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    icon_type : `IconType`
        The application's icon's type.
    bot : ``ClientUserBase``
        The application's bot if applicable.
    description : `None` `str`
        The description of the application. Defaults to empty string.
    name : `str`
        The name of the application. Defaults to empty string.
    """
    __slots__ = ('bot', 'description', 'name', )
    
    icon = application_icon
    
    def __new__(cls, *, bot = ..., description = ..., icon = ..., name = ...):
        """
        Creates a new integration application from the given keyword parameters.
        
        Parameters
        ----------
        bot : `None`, ``ClientUserBase``, Optional (Keyword only)
            The application's bot if applicable.
        
        icon : `None`, `bytes`, `bytearray`, `memoryview`, ``Icon``, Optional (Keyword only)
            The icon of the integration application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        name : `None, `str`, Optional (Keyword only)
            The name of the application.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # bot
        if bot is ...:
            bot = ZEROUSER
        else:
            bot = validate_bot(bot)
        
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
        
        self = object.__new__(cls)
        self.bot = bot
        self.description = description
        self.icon = icon
        self.id = 0
        self.name = name
        return self
    
    
    @classmethod
    def precreate(cls, integration_application_id, **keyword_parameters):
        """
        Creates a new integration application with the given predefined fields.
        
        > Since integration applications are not globally cached, this method is only used for testing.
        
        Parameters
        ----------
        integration_application_id : `int`
            The integration application's id.
        **keyword_parameters : Keyword parameters
            The attributes to set.
        
        Other Parameters
        ----------------
        bot : `None`, ``ClientUserBase``, Optional (Keyword only)
            The application's bot if applicable.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        icon : `None`, ``Icon``, Optional (Keyword only)
            The icon of the integration application.
        
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
        integration_application_id = validate_id(integration_application_id)
        

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        self = cls._create_empty(integration_application_id)
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, integration_application_id):
        """
        Creates a new integration application with it's defaults attributes set.
        
        Parameters
        ----------
        integration_application_id : `int`
            The integration application's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.bot = ZEROUSER
        self.description = None
        self.icon_type = ICON_TYPE_NONE
        self.icon_hash = 0
        self.id = integration_application_id
        self.name = ''
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new integration application instance with the given application data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Application data included within integration payload.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = parse_id(data)
        self._set_icon(data)
        self.bot = parse_bot(data)
        self.description = parse_description(data)
        self.name = parse_name(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the integration application to json serializable data.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        put_bot_into(self.bot, data, defaults, include_internals = include_internals)
        put_description_into(self.description, data, defaults)
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        put_name_into(self.name, data, defaults)
        
        return data
    
    
    @property
    def partial(self):
        """
        Returns whether the integration application is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return (self.id == 0)
    
    
    def __eq__(self, other):
        """Returns whether the two integration applications are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two integration applications not equal."""
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
        
        # bot
        if self.bot != other.bot:
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
        """Returns the integration application's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        integration_application_id = self.id
        if integration_application_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(integration_application_id))
        else:
            repr_parts.append(' (partial)')
        
        name = self.name
        if name:
            repr_parts.append(', name = ')
            repr_parts.append(repr(name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the integration application's hash value."""
        # These entities are not cached, so we wont use their `id` if applicable.
        hash_value = 0
        
        # bot
        hash_value ^= hash(self.bot)
        
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
        Copies the integration application returning a new partial one.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        new.bot = self.bot
        new.description = self.description
        new.icon_hash = self.icon_hash
        new.icon_type = self.icon_type
        new.id = 0
        new.name = self.name
        return new


    def copy_with(self, *, bot = ..., description = ..., icon = ..., name = ...):
        """
        Copies the integration application with the given fields returning a new partial one.
        
        Parameters
        ----------
        bot : `None`, ``ClientUserBase``, Optional (Keyword only)
            The application's bot if applicable.
        
        icon : `None`, `bytes`, `bytearray`, `memoryview`, ``Icon``, Optional (Keyword only)
            The icon of the integration application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        name : `None, `str`, Optional (Keyword only)
            The name of the application.
        
        Returns
        -------
        new : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # bot
        if bot is ...:
            bot = self.bot
        else:
            bot = validate_bot(bot)
        
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
        
        new = object.__new__(type(self))
        new.bot = bot
        new.description = description
        new.icon = icon
        new.id = 0
        new.name = name
        return new
