# -*- coding: utf-8 -*-
__all__ = ('Color', 'DefaultAvatar', )

from .http import URLS

class Color(int):
    """
    A Color object represents a RGB color. Using int instead of Color is completely fine.
    """
    __slots__ = ()
    
    def __repr__(self):
        """Returns the color's representation."""
        return f'<{self.__class__.__name__} #{self:06X}>'
    
    @property
    def as_html(self):
        """
        Returns the color in HTML format.
        
        Returns
        -------
        color : `str`
        """
        return f'#{self:06X}'
    
    @classmethod
    def from_html(cls, value):
        """
        Converts a HTML color code to a ``Color`` object.
        
        Parameters
        ----------
        value : `str`
            HTML color code.

        Returns
        -------
        color : ``Color``
        
        Raises
        ------
        ValueError
            If the conversion failed.
        """
        if len(value) != 7:
            raise ValueError(f'The passed string\'s length must be 7, got {value!r}.')
        
        if value[0] != '#':
            raise ValueError(f'The passed string\'s first character must be \'#\', got {value!r}.')
        
        return cls(value[1:], base=16)
    
    @classmethod
    def from_tuple(cls, value):
        """
        Converts a tuple of ints to a Color object.
        
        Does not checks if each element of the tuple is in 0-255, so inputting bad values can yield any error.
        
        Parameters
        ----------
        value : `tuple` of 3 `int`-s
            A tuple of `3` 0-255 `int`-s.

        Returns
        -------
        color : ``Color``
        """
        return cls((value[0]<<16)|(value[1]<<8)|value[2])
    
    @property
    def as_tuple(self):
        """
        Returns the color's Red, Green and Blue value.
        
        Returns
        -------
        tuple_value : `tuple` of 3 `int`-s
        """
        return (self>>16, (self>>8)&0x00ff, self&0x0000ff)
    
    @classmethod
    def from_rgb(cls, r, g, b):
        """
        Converts red, green and blue to a Color object.
        
        Does not checks if each element of the tuple is in 0-255, so inputting bad values can yield any error.

        Parameters
        ----------
        r : `int`
            Red value.
        g : `int`
            Green value.
        b : `int`
            Blue value.

        Returns
        -------
        color : ``Color``
        """
        return cls((r<<16)|(g<<8)|b)
    
    @property
    def red(self):
        """
        Returns the color's red value.
        
        Returns
        -------
        red_value : `int`
        """
        return self>>16
    
    @property
    def green(self):
        """
        Returns the color's green value.
        
        Returns
        -------
        green_value : `int`
        """
        return (self>>8)&0x0000ff
    
    @property
    def blue(self):
        """
        Returns the color's blue value.
        
        Returns
        -------
        blue_value : `int`
        """
        return self&0x0000ff


class DefaultAvatar(object):
    """
    Represents a default avatar of a user. Default avatar is used, when the user has no avatar set.

    There are some predefined default avatars and there should be no more instances created.
    
    +-----------+-----------+-----------+
    | name      | value     | color     |
    +===========+===========+===========+
    | blue      | 0         | 0x7289da  |
    +-----------+-----------+-----------+
    | gray      | 1         | 0x747f8d  |
    +-----------+-----------+-----------+
    | green     | 2         | 0x43b581  |
    +-----------+-----------+-----------+
    | orange    | 3         | 0xfaa61a  |
    +-----------+-----------+-----------+
    | red       | 4         | 0xf04747  |
    +-----------+-----------+-----------+
    
    Attributes
    ----------
    color : ``Color``
        The color of the default avatar.
    name : `str`
        The name of the default avatar's color.
    value : ``int`
        The index value of the default avatar.
        
    Class Attributes
    ----------------
    COUNT : `int` = 5
        The number of the default avatars defined.
    INSTANCES : `list` of ``DefaultAvatar`` objects
        The predefined default avatar instances stored for lookup.
    """
    
    # class related
    COUNT = 5
    INSTANCES = [NotImplemented] * COUNT
    
    @classmethod
    def for_(cls, user):
        """
        Returns the default avatar for the given user.
        
        Parameters
        ----------
        user : ``UserBase`` instance
            The user, who's default avatar will be looked up.

        Returns
        -------
        default_avatar : ``DefaultAvatar``
        """
        return cls.INSTANCES[user.discriminator%cls.COUNT]
    
    # object related
    __slots__ = ('color', 'name', 'value',)
    
    def __init__(self, value, name, color):
        """
        Creates a default avatar and puts it into the classe's `.INSTANCES`.
        
        Parameters
        ----------
        color : ``Color``
            The color of the default avatar.
        name : `str`
            The name of the default avatar's color.
        value : ``int`
            The index value of the default avatar.
        """
        self.value = value
        self.name = name
        self.color = color
        self.INSTANCES[value] = self
    
    def __str__(self):
        """Returns the default's avatar's name."""
        return self.name
    
    def __int__(self):
        """Returns the default's avatar's value."""
        return self.value
    
    def __repr__(self):
        """Returns the default's avatar's representation."""
        return f'<{self.__class__.__name__} name={self.name}, value={self.value}>'
    
    url = property(URLS.default_avatar_url)
    
    # predefined
    blue   = NotImplemented
    gray   = NotImplemented
    green  = NotImplemented
    orange = NotImplemented
    red    = NotImplemented

DefaultAvatar.blue   = DefaultAvatar(0 ,   'blue' , Color(0x7289da))
DefaultAvatar.gray   = DefaultAvatar(1 ,   'gray' , Color(0x747f8d))
DefaultAvatar.green  = DefaultAvatar(2 ,  'green' , Color(0x43b581))
DefaultAvatar.orange = DefaultAvatar(3 , 'orange' , Color(0xfaa61a))
DefaultAvatar.red    = DefaultAvatar(4 ,    'red' , Color(0xf04747))

del URLS
