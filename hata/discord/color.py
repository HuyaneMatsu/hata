# -*- coding: utf-8 -*-
__all__ = ('Color', )

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
        tuple_value : `tuple` (`int`, `int`, `int`)
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
