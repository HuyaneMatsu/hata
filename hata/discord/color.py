# -*- coding: utf-8 -*-
__all__ = ('Color', )

from math import floor

class Color(int):
    """
    A Color object represents a RGB color. Using int instead of Color is completely fine.
    
    Examples
    --------
    ```py
    >>> # Colors are just int instances, so they can be freely converted between each other.
    >>> color = Color(0x022587)
    >>> color
    <Color #022587>
    
    >>> # Creating a color from rgb
    >>> color = Color.from_rgb(120, 255, 0)
    >>> color
    <Color #78FF00>
    
    >>> # Or creating a color from a tuple
    >>> color = Color.from_rgb_tuple((100, 20, 255))
    >>> color
    <Color #6414FF>
    
    >>> # Converting back to rgb
    >>> color.as_rgb
    (100, 20, 255)
    
    >>> # Creating color from float color channels
    >>> color = Color.from_rgb_float(1.0, 0.125, 0.862)
    >>> color
    <Color #FF1FDB>
    
    >>> # Converting color back to float color channels
    >>> color.as_rgb_float
    (1.0, 0.12156862745098039, 0.8588235294117647)
    
    >>> # Creating color from html color code
    >>> color = Color.from_html('#ff0000')
    >>> color
    
    >>> # Converting color back to html color code
    <Color #FF0000>
    >>> color.as_html
    '#FF0000'
    
    >>> # html color codes with length of 3 are working as well
    >>> color = Color.from_html('#f00')
    >>> color
    <Color #FF0000>
    ```
    """
    __slots__ = ()
    
    def __repr__(self):
        """Returns the color's representation."""
        return f'<{self.__class__.__name__} #{self:06X}>'
    
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
            The given value has invalid length or is not hexadecimal.
        """
        value_length = len(value)
        if value_length in (7, 6, 4, 3):
            if value[0] == '#':
                value = value[1:]
                value_length -= 1
            
            if value_length == 6:
                try:
                    color = cls(value, base=16)
                except ValueError:
                    pass
                else:
                    return color
            
            elif value_length == 3:
                try:
                    color_value = int(value, base=16)
                except ValueError:
                    pass
                else:
                    red = (color_value>>8)*17
                    green = ((color_value>>4)&0xf)*17
                    blue = (color_value&0xf)*17
                    return Color((red<<16)|(green<<8)|blue)
        
        raise ValueError('The given value has invalid length or is not hexadecimal.')
    
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
    def from_rgb_tuple(cls, rgb_tuple):
        """
        Converts a tuple of ints to a ``Color`` object.
        
        Parameters
        ----------
        rgb_tuple : `tuple` (`int`, `int`, `int`)
            A tuple of `3` ints which are in range [0, 255].

        Returns
        -------
        color : ``Color``
        
        Raises
        ------
        ValueError
            - `rgb_tuple` has no length of `3`.
            - Channel value out of expected range.
        """
        if len(rgb_tuple) != 3:
            raise ValueError(f'Rgb tuple should have length `3`, got: {rgb_tuple!r}.')
        
        return cls.from_rgb(*rgb_tuple)
    
    from_tuple = from_rgb_tuple
    
    @property
    def as_rgb_tuple(self):
        """
        Returns the color's red, green and blue channel's value in a tuple of integers.
        
        Returns
        -------
        rgb_tuple : `tuple` (`int`, `int`, `int`)
        """
        return (self>>16, (self>>8)&0x00ff, self&0x0000ff)
    
    as_tuple = as_rgb_tuple
    as_rgb = as_rgb_tuple
    
    @classmethod
    def from_rgb_float_tuple(cls, rgb_tuple):
        """
        Converts a tuple of floats to a ``Color`` object.
        
        Parameters
        ----------
        rgb_tuple : `tuple` (`float`, `float`, `float`)
            A tuple of `3` floats which are in range [0.0, 1.0].
        
        Returns
        -------
        color : ``Color``
        
        Raises
        ------
        ValueError
            - `rgb_tuple` has no length of `3`.
            - Channel value out of expected range.
        """
        if len(rgb_tuple) != 3:
            raise ValueError(f'Rgb tuple should have length `3`, got: {rgb_tuple!r}.')
        
        return cls.from_rgb_float(*rgb_tuple)
    
    from_float_tuple = from_rgb_float_tuple
    
    @property
    def as_rgb_float_tuple(self):
        """
        Returns the color's red, green and blue channel's value as a tuple of floats.
        
        Returns
        -------
        rgb_tuple : `tuple` (`float`, `float`, `float`)
        """
        return ((self>>16)*(1.0/255.0), ((self>>8)&0x00ff)*(1.0/255.0), (self&0x0000ff)*(1.0/255.0))
    
    as_float_tuple = as_rgb_float_tuple
    as_rgb_float = as_rgb_float_tuple
    
    @classmethod
    def from_rgb(cls, red, green, blue):
        """
        Converts red, green and blue channels to a `Color` object.
        
        Does not checks if each element of the tuple is in 0-255, so inputting bad values can yield any error.

        Parameters
        ----------
        red : `int`
            Red channel.
        green : `int`
            Green channel.
        blue : `int`
            Blue channel.

        Returns
        -------
        color : ``Color``
        
        Raises
        ------
            Channel value out of expected range.
        """
        if red > 255 or red < 0:
            raise ValueError(f'Red channel value out of [0, 255] expected range, got {red!r}.')
        if green > 255 or green < 0:
            raise ValueError(f'Green channel value out of [0, 255] expected range, got {green!r}.')
        if blue > 255 or blue < 0:
            raise ValueError(f'Blue channel value out of [0, 255] expected range, got {blue!r}.')
        
        return cls((red<<16)|(green<<8)|blue)
    
    @classmethod
    def from_rgb_float(cls, red, green, blue):
        """
        Converts red, green and blue to a `Color` object.
        
        Does not checks if each element of the tuple is in 0-255, so inputting bad values can yield any error.

        Parameters
        ----------
        red : `float`
            Red channel.
        green : `float`
            Green channel.
        blue : `float`
            Blue channel.

        Returns
        -------
        color : ``Color``
        
        Raises
        ------
        ValueError
            Channel value out of expected range.
        """
        if red > 1.0 or red < 0.0:
            raise ValueError(f'Red channel value out of [0.0, 1.0] expected range, got {red!r}.')
        if green > 1.0 or green < 0.0:
            raise ValueError(f'Green channel value out of [0.0, 1.0] expected range, got {green!r}.')
        if blue > 1.0 or blue < 0.0:
            raise ValueError(f'Blue channel value out of [0.0, 1.0] expected range, got {blue!r}.')
        
        # Convert float values to 8 bit ints.
        red = floor(red*255.0)
        green = floor(green*255.0)
        blue = floor(blue*255.0)
        # Build color.
        return Color((red<<16)|(green<<8)|blue)
    
    @property
    def red(self):
        """
        Returns the color's red channel's value.
        
        Returns
        -------
        red_value : `int`
        """
        return self>>16
    
    r = red
    
    @property
    def green(self):
        """
        Returns the color's green channel's value.
        
        Returns
        -------
        green_value : `int`
        """
        return (self>>8)&0x0000ff
    
    g = green
    
    @property
    def blue(self):
        """
        Returns the color's blue channel's value.
        
        Returns
        -------
        blue_value : `int`
        """
        return self&0x0000ff
    
    b = blue
