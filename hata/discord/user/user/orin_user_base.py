__all__ = ('OrinUserBase',)

from scarletio import copy_docs

from ...bases import ICON_TYPE_ANIMATED_APNG, ICON_TYPE_NONE, IconSlot
from ...http import urls as module_urls

from .fields import (
    parse_banner_color, parse_discriminator, parse_display_name, parse_flags, validate_banner_color,
    validate_discriminator, validate_display_name, validate_flags
)
from .flags import UserFlag
from .user_base import UserBase


class OrinUserBase(UserBase):
    """
    Base class for actual user entities, like oauth2 user and normal users.
    
    Attributes
    ----------
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The user's avatar's type.
    avatar_decoration_hash : `int`
        The user's avatar decoration's hash in `uint128`.
    avatar_decoration_type : ``IconType``
        The user's avatar decoration's type.
    banner_color : `None`, ``Color``
        The user's banner color if has any.
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    banner_type : ``IconType``
        The user's banner's type.
    discriminator : `int`
        The client's discriminator. Given to avoid overlapping names.
    display_name : `None`, `str`
        The user's non-unique display name.
    id : `int`
        The client's unique identifier number.
    flags : ``UserFlag``
        The user's flags.
    name : str
        The client's username.
    """
    __slots__ = ('banner_color', 'discriminator', 'display_name', 'flags')
    
    banner = IconSlot('banner', 'banner', module_urls.user_banner_url, module_urls.user_banner_url_as)
    avatar_decoration = IconSlot(
        'avatar_decoration',
        'avatar_decoration',
        module_urls.user_avatar_decoration_url,
        module_urls.user_avatar_decoration_url_as,
        animated_icon_type = ICON_TYPE_ANIMATED_APNG,
    )
    
    def __new__(
        cls,
        *,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        banner_color = ...,
        discriminator = ...,
        display_name = ...,
        flags = ...,
        name = ...,
    ):
        """
        Creates a new partial user with the given fields.
        
        Parameters
        ----------
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        avatar_decoration : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar decoration.
        banner : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's banner.
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The user's banner color.
        discriminator : `str`, `int`, Optional (Keyword only)
            The user's discriminator.
        display_name : `None`, `str`, Optional (Keyword only)
            The user's non-unique display name.
        flags : `int`, ``UserFlag``, Optional (Keyword only)
            The user's flags.
        name : `str`, Optional (Keyword only)
            The user's name.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # avatar_decoration
        if avatar_decoration is ...:
            avatar_decoration = None
        else:
            avatar_decoration = cls.avatar_decoration.validate_icon(avatar_decoration, allow_data = True)
        
        # banner
        if banner is ...:
            banner = None
        else:
            banner = cls.banner.validate_icon(banner, allow_data = True)
        
        # banner_color
        if banner_color is ...:
            banner_color = None
        else:
            banner_color = validate_banner_color(banner_color)
        
        # discriminator
        if discriminator is ...:
            discriminator = 0
        else:
            discriminator = validate_discriminator(discriminator)
        
        # display_name
        if display_name is ...:
            display_name = None
        else:
            display_name = validate_display_name(display_name)
        
        # flags
        if flags is ...:
            flags = UserFlag()
        else:
            flags = validate_flags(flags)
        
        # Construct
        self = UserBase.__new__(
            cls,
            avatar = avatar,
            name = name,
        )
        self.avatar_decoration = avatar_decoration
        self.banner = banner
        self.banner_color = banner_color
        self.discriminator = discriminator
        self.display_name = display_name
        self.flags = flags
        return self
    
    
    @copy_docs(UserBase._update_attributes)
    def _update_attributes(self, data):
        UserBase._update_attributes(self, data)
        
        self._set_avatar_decoration(data)
        self._set_banner(data)
        self.banner_color = parse_banner_color(data)
        self.discriminator = parse_discriminator(data)
        self.display_name = parse_display_name(data)
        self.flags = parse_flags(data)
        
    
    @copy_docs(UserBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = UserBase._difference_update_attributes(self, data)
        
        # avatar_decoration
        self._update_avatar_decoration(data, old_attributes)
        
        # banner
        self._update_banner(data, old_attributes)
        
        # banner_color
        banner_color = parse_banner_color(data)
        if self.banner_color != banner_color:
            old_attributes['banner_color'] = self.banner_color
            self.banner_color = banner_color
        
        # discriminator
        discriminator = parse_discriminator(data)
        if self.discriminator != discriminator:
            old_attributes['discriminator'] = self.discriminator
            self.discriminator = discriminator
        
        # display_name
        display_name = parse_display_name(data)
        if self.display_name != display_name:
            old_attributes['display_name'] = self.display_name
            self.display_name = display_name
        
        # flags
        flags = parse_flags(data)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = flags
        
        return old_attributes
    
    
    @copy_docs(UserBase._set_default_attributes)
    def _set_default_attributes(self):
        UserBase._set_default_attributes(self)
        self.avatar_decoration_hash = 0
        self.avatar_decoration_type = ICON_TYPE_NONE
        self.banner_color = None
        self.banner_hash = 0
        self.banner_type = ICON_TYPE_NONE
        self.discriminator = 0
        self.display_name = None
        self.flags = UserFlag()
    
    
    @copy_docs(UserBase.copy)
    def copy(self):
        new = UserBase.copy(self)
        new.avatar_decoration = self.avatar_decoration
        new.banner = self.banner
        new.banner_color = self.banner_color
        new.discriminator = self.discriminator
        new.display_name = self.display_name
        new.flags = self.flags
        return new
    
    
    def copy_with(
        self,
        *,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        banner_color = ...,
        discriminator = ...,
        display_name = ...,
        flags = ...,
        name = ...,
    ):
        """
        Copies the user with the given fields.
        
        Parameters
        ----------
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        avatar_decoration : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar decoration.
        banner : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's banner.
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The user's banner color.
        discriminator : `str`, `int`, Optional (Keyword only)
            The user's discriminator.
        display_name : `None`, `str`, Optional (Keyword only)
            The user's non-unique display name.
        flags : `int`, ``UserFlag``, Optional (Keyword only)
            The user's flags.
        name : `str`, Optional (Keyword only)
            The user's name.
        
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
        # avatar_decoration
        if avatar_decoration is ...:
            avatar_decoration = self.avatar_decoration
        else:
            avatar_decoration = type(self).avatar_decoration.validate_icon(avatar_decoration, allow_data = True)
        
        # banner
        if banner is ...:
            banner = self.banner
        else:
            banner = type(self).banner.validate_icon(banner, allow_data = True)
        
        # banner_color
        if banner_color is ...:
            banner_color = self.banner_color
        else:
            banner_color = validate_banner_color(banner_color)
        
        # discriminator
        if discriminator is ...:
            discriminator = self.discriminator
        else:
            discriminator = validate_discriminator(discriminator)
        
        # display_name
        if display_name is ...:
            display_name = self.display_name
        else:
            display_name = validate_display_name(display_name)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # Construct
        new = UserBase.copy_with(
            self,
            avatar = avatar,
            name = name,
        )
        new.avatar_decoration = avatar_decoration
        new.banner = banner
        new.banner_color = banner_color
        new.discriminator = discriminator
        new.display_name = display_name
        new.flags = flags
        return new
    
    
    @copy_docs(UserBase._get_hash_partial)
    def _get_hash_partial(self):
        hash_value = UserBase._get_hash_partial(self)
        
        # avatar_decoration
        hash_value ^= hash(self.avatar_decoration)
        
        # banner
        hash_value ^= hash(self.banner)
        
        # banner_color
        banner_color = self.banner_color
        if (banner_color is not None):
            hash_value ^= 1 << 25
            hash_value ^= banner_color
        
        # discriminator
        hash_value ^= self.discriminator << 26
        
        # display_name
        display_name = self.display_name
        if (display_name is not None) and (display_name != self.name):
            hash_value ^= hash(display_name)
        
        # flags
        hash_value ^= self.flags
        
        return hash_value
