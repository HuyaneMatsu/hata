__all__ = ('StatusByPlatform',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_desktop, parse_embedded, parse_mobile, parse_web, put_desktop, put_embedded, put_mobile, put_web,
    validate_desktop, validate_embedded, validate_mobile, validate_platform, validate_web
)
from .preinstanced import SessionPlatformType, Status


class StatusByPlatform(RichAttributeErrorBaseType):
    """
    Represents an user's status by platform.
    
    Attributes
    ----------
    desktop : ``Status``
        The user's status on your average shitty electron application.
    
    embedded : ``Status``
        The user's status on an embedded platform.
    
    mobile : ``Status``
        The user's status on a mobile device.
    
    web : ``Status``
        The user's status in a web browser (excluding electron).
    """
    __slots__ = ('desktop', 'embedded', 'mobile', 'web')
    
    
    def __new__(cls, *, desktop = ..., embedded = ..., mobile = ..., web = ...):
        """
        Creates a new status by platform with the given parameters.
        
        Parameters
        ----------
        desktop : ``Status``, Optional (Keyword only)
            The user's status on your average shitty electron application.
        
        embedded : ``Status``
            The user's status on an embedded platform.
        
        mobile : ``Status``
            The user's status on a mobile device.
        
        web : ``Status``
            The user's status in a web browser (excluding electron).
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        """
        # desktop
        if desktop is ...:
            desktop = Status.offline
        else:
            desktop = validate_desktop(desktop)
        
        # embedded
        if embedded is ...:
            embedded = Status.offline
        else:
            embedded = validate_embedded(embedded)
        
        # mobile
        if mobile is ...:
            mobile = Status.offline
        else:
            mobile = validate_mobile(mobile)
        
        # web
        if web is ...:
            web = Status.offline
        else:
            web = validate_web(web)
        
        # Construct
        self = object.__new__(cls)
        self.desktop = desktop
        self.embedded = embedded
        self.mobile = mobile
        self.web = web
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # desktop
        desktop = self.desktop
        if (desktop is Status.offline):
            field_added = False
        
        else:
            field_added = True
            
            repr_parts.append(' desktop = ')
            repr_parts.append(desktop.name)
        
        # embedded
        embedded = self.embedded
        if (embedded is not Status.offline):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' embedded = ')
            repr_parts.append(embedded.name)
        
        # mobile
        mobile = self.mobile
        if (mobile is not Status.offline):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' mobile = ')
            repr_parts.append(mobile.name)
        
        # web
        web = self.web
        if (web is not Status.offline):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' web = ')
            repr_parts.append(web.name)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # desktop
        hash_value ^= hash(self.desktop)
        
        # embedded
        hash_value ^= hash(self.embedded) << 8
        
        # mobile
        hash_value ^= hash(self.mobile) << 16
        
        # web
        hash_value ^= hash(self.web) << 24
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # desktop
        if self.desktop is not other.desktop:
            return False
        
        # embedded
        if self.embedded is not other.embedded:
            return False
        
        # mobile
        if self.mobile is not other.mobile:
            return False
        
        # web
        if self.web is not other.web:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a status by platform from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received status by platform data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.desktop = parse_desktop(data)
        self.embedded = parse_embedded(data)
        self.mobile = parse_mobile(data)
        self.web = parse_web(data)
        return self
    
    
    def to_data(self, *, defaults = False,):
        """
        Converts the status by platform to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_desktop(self.desktop, data, defaults)
        put_embedded(self.embedded, data, defaults)
        put_mobile(self.mobile, data, defaults)
        put_web(self.web, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the status by platform.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.desktop = self.desktop
        new.embedded = self.embedded
        new.mobile = self.mobile
        new.web = self.web
        return new
    
    
    def copy_with(self, *, desktop = ..., embedded = ..., mobile = ..., web = ...):
        """
        Copies the status by platform and modifies the defined the defined fields of it.
        
        Parameters
        ----------
        desktop : ``Status``, Optional (Keyword only)
            The user's status on your average shitty electron application.
        
        embedded : ``Status``
            The user's status on an embedded platform.
        
        mobile : ``Status``
            The user's status on a mobile device.
        
        web : ``Status``
            The user's status in a web browser (excluding electron).
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        # desktop
        if desktop is ...:
            desktop = self.desktop
        else:
            desktop = validate_desktop(desktop)
        
        # embedded
        if embedded is ...:
            embedded = self.embedded
        else:
            embedded = validate_embedded(embedded)
        
        # mobile
        if mobile is ...:
            mobile = self.mobile
        else:
            mobile = validate_mobile(mobile)
        
        # web
        if web is ...:
            web = self.web
        else:
            web = validate_web(web)
        
        # construct
        new = object.__new__(type(self))
        new.desktop = desktop
        new.embedded = embedded
        new.mobile = mobile
        new.web = web
        return new
    
    
    def __getitem__(self, platform):
        """
        Returns the status for the given platform.
        
        Parameters
        ----------
        platform : ``None | str | Platform``
            Platform to return status for.
        
        Returns
        -------
        status : ``Status``
        """
        platform = validate_platform(platform)
        
        try:
            slot = STATUS_BY_PLATFORM_SLOT_BY_PLATFORM[platform]
        except KeyError:
            status = Status.offline
        else:
            status = slot.__get__(self, type(self))
        
        return status
    
    
    def iter_status_by_platform(self):
        """
        Iterates over the platforms and their statuses.
        
        This function is an iterable generator.
        
        Yields
        ------
        item : ``(SessionPlatformType, Status)``
        """
        yield SessionPlatformType.desktop, self.desktop
        yield SessionPlatformType.embedded, self.embedded
        yield SessionPlatformType.mobile, self.mobile
        yield SessionPlatformType.web, self.web
    

STATUS_BY_PLATFORM_SLOT_BY_PLATFORM = {
    SessionPlatformType.desktop : StatusByPlatform.desktop,
    SessionPlatformType.embedded : StatusByPlatform.embedded,
    SessionPlatformType.mobile : StatusByPlatform.mobile,
    SessionPlatformType.web : StatusByPlatform.web,
}
