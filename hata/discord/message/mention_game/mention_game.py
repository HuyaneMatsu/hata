__all__ = ('MentionGame',)


from ...bases import DiscordEntity, ICON_TYPE_NONE
from ...http.urls import build_application_icon_url, build_application_icon_url_as
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from ...application.application.application import APPLICATION_ICON_DETECTABLE
from ...core import MENTION_GAMES

from .fields import parse_id, parse_name, put_id, put_name, validate_id, validate_name


PRECREATE_FIELDS = {
    'icon': ('icon', APPLICATION_ICON_DETECTABLE.validate_icon),
    'name': ('name', validate_name),
}


class MentionGame(DiscordEntity, immortal = True):
    """
    A mention of a game.
    
    Attributes
    ----------
    application_id : `int`
        The application's identifier.
    
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    
    icon_type : ``IconType``
        The application's icon's type.
    
    name : `str`, Optional (Keyword only)
        The application's name.
    """
    __slots__ = ('name', )
    
    icon = APPLICATION_ICON_DETECTABLE
    
    def __new__(
        cls,
        *,
        icon = ...,
        name = ...,
    ):
        """
        Creates a mention of a game.
        
        Parameters
        ----------
        icon : ``None | str | Icon``, Optional (Keyword only)
            The application's icon.
        
        name : `str`, Optional (Keyword only)
            The application's name.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # Construct
        
        self = object.__new__(cls)
        self.icon = icon
        self.id = 0
        self.name = name
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new instance from the received data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Mention game data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        application_id = parse_id(data)
        
        try:
            self = MENTION_GAMES[application_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = application_id
            self._set_icon(data)
            self.name = parse_name(data)
            MENTION_GAMES[application_id] = self
        
        else:
            self._set_icon(data)
            self.name = parse_name(data)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the mention game to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        type(self).icon.put_into(self.icon, data, defaults)
        put_id(self.id, data, defaults)
        put_name(self.name, data, defaults)
        return data
    
    
    
    @classmethod
    def precreate(cls, application_id, **keyword_parameters):
        """
        Precreates the application game with the given parameters. When the application game is loaded, the precreated
        one will be picked up and its fields will be populated.
        
        > Mention games cannot determine whether they are already loaded, therefore they always set their attributes.
        Parameters
        ----------
        application_id : `int`
            The application's identifier.
        
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the application game.
        
        Other Parameters
        ----------------
        icon : ``None | str | Icon``, Optional (Keyword only)
            The application's icon.
        
        name : `str`, Optional (Keyword only)
            The application's name.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - A parameter's type is incorrect.
            - Extra parameters given.
        ValueError
            - A parameter's value is incorrect.
        """
        application_id = validate_id(application_id)

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = MENTION_GAMES[application_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = application_id
            self.icon_type = ICON_TYPE_NONE
            self.icon_hash = 0
            self.name = ''
            
            MENTION_GAMES[application_id] = self
        
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    def __repr__(self):
        """Returns the mention game's representation."""
        repr_parts = ['<', type(self).__name__]
        
        application_id = self.id
        if application_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two mention games are equal"""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two mention games are not equal"""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two mention games are equal. Type of `other` must match type of `self`.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other mention game.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return (self_id == other_id)
        
        if self.icon != other.icon:
            return False
        
        if self.name != other.name:
            return False
        
        return True

    
    def __hash__(self):
        """Returns the mention game's hash."""
        application_id = self.id
        if application_id:
            return application_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns a partial mention game's hash value.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # icon
        hash_value ^= hash(self.icon)
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value

    
    def copy(self):
        """
        Copies the mention game.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.id = 0
        new.icon = self.icon
        new.name = self.name
        return new
    
    
    def copy_with(
        self,
        *,
        icon = ...,
        name = ...,
    ):
        """
        Copies the mention game with the given fields.
        
        Parameters
        ----------
        icon : ``None | str | Icon``, Optional (Keyword only)
            The application's icon.
        
        name : `str`, Optional (Keyword only)
            The application's name.
        
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
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # Construct
        
        new = object.__new__(type(self))
        new.icon = icon
        new.id = 0
        new.name = name
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether self is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return self.id == 0
    
    
    @property
    def icon_url(self):
        """
        Returns the application's icon's url. If the application has no icon, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_application_icon_url(self.id, self.icon_type, self.icon_hash)
    
    
    def icon_url_as(self, ext = None, size = None):
        """
        Returns the application's icon's url. If the application has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the application has animated icon, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_application_icon_url_as(self.id, self.icon_type, self.icon_hash, ext, size)
