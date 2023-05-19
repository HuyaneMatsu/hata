__all__ = ('GuildWidgetUser',)

import warnings

from ...bases import DiscordEntity
from ...user import Status

from .fields import (
    parse_activity_name, parse_avatar_url, parse_discriminator, parse_id, parse_name, parse_status,
    put_activity_name_into, put_avatar_url_into, put_discriminator_into, put_id_into, put_name_into, put_status_into,
    validate_activity_name, validate_avatar_url, validate_discriminator, validate_id, validate_name, validate_status
)


class GuildWidgetUser(DiscordEntity):
    """
    Represents an user object sent with a ``GuildWidget``'s data.
    
    Attributes
    ----------
    activity_name : `None`, `str`
        The guild widget user's activity's name if applicable.
    avatar_url : `str`
        The guild widget user's avatar url.
    discriminator : `int`
        The guild widget user's discriminator.
    id : `int`
        The unique identifier number of the guild widget user. Can be between `0` and `99`.
    name : `str`
        The guild widget user's name.
    status : ``Status``
        The guild widget user's status.
    """
    __slots__ = ('activity_name', 'avatar_url', 'discriminator', 'name', 'status')
    
    
    def __new__(
        cls,
        *,
        activity_name = ...,
        avatar_url = ...,
        discriminator = ...,
        name = ...,
        status = ...,
        user_id = ...,
    ):
        """
        Creates a new guild widget user with the given parameters.
        
        Parameters
        ----------
        activity_name : `None`, `str`, Optional (Keyword only)
            The guild widget user's activity's name if applicable.
        avatar_url : `str`, Optional (Keyword only)
            The guild widget user's avatar url.
        discriminator : `int`, Optional (Keyword only)
            The guild widget user's discriminator.
        name : `str`, Optional (Keyword only)
            The guild widget user's name.
        status : ``Status``, `str`, Optional (Keyword only)
            The guild widget user's status.
        user_id : `int`, Optional (Keyword only)
            The unique identifier number of the guild widget user. Can be between `0` and `99`.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # activity_name
        if activity_name is ...:
            activity_name = None
        else:
            activity_name = validate_activity_name(activity_name)
        
        # avatar_url
        if avatar_url is ...:
            avatar_url = ''
        else:
            avatar_url = validate_avatar_url(avatar_url)
        
        # discriminator
        if discriminator is ...:
            discriminator = 0
        else:
            discriminator = validate_discriminator(discriminator)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # status
        if status is ...:
            status = Status.offline
        else:
            status = validate_status(status)
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_id(user_id)
        
        # Construct
        self = object.__new__(cls)
        self.activity_name = activity_name
        self.avatar_url = avatar_url
        self.discriminator = discriminator
        self.id = user_id
        self.name = name
        self.status = status
        return self
        
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild widget user from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Guild widget user data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.activity_name = parse_activity_name(data)
        self.avatar_url = parse_avatar_url(data)
        self.discriminator = parse_discriminator(data)
        self.id = parse_id(data)
        self.name = parse_name(data)
        self.status = parse_status(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the guild widget user.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_activity_name_into(self.activity_name, data, defaults)
        put_avatar_url_into(self.avatar_url, data, defaults)
        put_discriminator_into(self.discriminator, data, defaults)
        put_id_into(self.id, data, defaults)
        put_name_into(self.name, data, defaults)
        put_status_into(self.status, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the representation of the guild widget user."""
        return f'<{self.__class__.__name__} id = {self.id}, name = {self.full_name!r}>'
    
    
    def __hash__(self):
        """Returns the guild widget user's hash value."""
        hash_value = 0
        
        # activity_name
        activity_name = self.activity_name
        if (activity_name is not None):
            hash_value ^= hash(activity_name)
        
        # avatar_url
        hash_value ^= hash(self.avatar_url)
        
        # discriminator
        hash_value ^= self.discriminator
        
        # id
        hash_value ^= self.id << 6
        
        # name
        hash_value ^= hash(self.name)
        
        # status
        hash_value ^= hash(self.status)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two guild widget users are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two guild widget users are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two types are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # activity_name
        if self.activity_name != other.activity_name:
            return False
        
        # avatar_url
        if self.avatar_url != other.avatar_url:
            return False
        
        # discriminator
        if self.discriminator != other.discriminator:
            return False
        
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # status
        if self.status is not other.status:
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the guild widget user.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.activity_name = self.activity_name
        new.avatar_url = self.avatar_url
        new.discriminator = self.discriminator
        new.id = self.id
        new.name = self.name
        new.status = self.status
        return new
    
    
    def copy_with(
        self,
        *,
        activity_name = ...,
        avatar_url = ...,
        discriminator = ...,
        name = ...,
        status = ...,
        user_id = ...,
    ):
        """
        Copies the guild widget user with the given fields.
        
        Parameters
        ----------
        activity_name : `None`, `str`, Optional (Keyword only)
            The guild widget user's activity's name if applicable.
        avatar_url : `None`, `str`, Optional (Keyword only)
            The guild widget user's avatar url.
        discriminator : `int`, Optional (Keyword only)
            The guild widget user's discriminator.
        name : `str`, Optional (Keyword only)
            The guild widget user's name.
        status : ``Status``, `str`, Optional (Keyword only)
            The guild widget user's status.
        user_id : `int`, Optional (Keyword only)
            The unique identifier number of the guild widget user. Can be between `0` and `99`.
        
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
        # activity_name
        if activity_name is ...:
            activity_name = self.activity_name
        else:
            activity_name = validate_activity_name(activity_name)
        
        # avatar_url
        if avatar_url is ...:
            avatar_url = self.avatar_url
        else:
            avatar_url = validate_avatar_url(avatar_url)
        
        # discriminator
        if discriminator is ...:
            discriminator = self.discriminator
        else:
            discriminator = validate_discriminator(discriminator)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # status
        if status is ...:
            status = self.status
        else:
            status = validate_status(status)
        
        # user_id
        if user_id is ...:
            user_id = self.id
        else:
            user_id = validate_id(user_id)
        
        # Construct
        new = object.__new__(type(self))
        new.activity_name = activity_name
        new.avatar_url = avatar_url
        new.discriminator = discriminator
        new.id = user_id
        new.name = name
        new.status = status
        return new
        
        
    @property
    def full_name(self):
        """
        The user's name with it's discriminator (if applicable).
        
        Returns
        -------
        full_name : `str`
        """
        discriminator = self.discriminator
        if discriminator:
            return f'{self.name}#{discriminator:0>4}'
        
        return self.name
    
    
    @property
    def mention(self):
        """
        The mention of the user.
        
        Returns
        -------
        mention : `str`
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.mention` is deprecated and will be removed in 2023 November. '
                f'This property actually never returned the correct value, that is why.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return f'<@{self.id}>'
    
    
    @property
    def mention_nick(self):
        """
        The mention to the user's nick.
        
        Returns
        -------
        mention : `str`
        
        Notes
        -----
        It actually has nothing to do with the user's nickname > <.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.mention_nick` is deprecated and will be removed in 2023 November. '
                f'This property actually never returned the correct value, that is why.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return f'<@!{self.id}>'
