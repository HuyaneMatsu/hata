# -*- coding: utf-8 -*-
__all__ = ('Color', 'parse_color', )

import re
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


COLOR_RGB_INT_RP = re.compile(
    '(25[0-5]|2[0-4][0-9]|1[0-9]{2}|0?[0-9]{0,2})[ \t\n]+'
    '(25[0-5]|2[0-4][0-9]|1[0-9]{2}|0?[0-9]{0,2})[ \t\n]+'
    '(25[0-5]|2[0-4][0-9]|1[0-9]{2}|0?[0-9]{0,2})'
        )

COLOR_RGB_FLOAT_RP = re.compile(
    '([01]|0?\.[0-9]{1,32})[ \t\n]+'
    '([01]|0?\.[0-9]{1,32})[ \t\n]+'
    '([01]|0?\.[0-9]{1,32})'
        )

COLOR_HTML_6_RP = re.compile('#?([0-9a-f]{6})')
COLOR_HTML_3_RP = re.compile('#?([0-9a-f]{3})')


COLOR_HEX_RP = re.compile('0x([0-9a-f]{1,6})')

COLOR_OCT_RP = re.compile('0o([0-7]{1,8})')

COLOR_BIN_RP = re.compile('0b([01]{1,24})')

COLOR_DEC_RP = re.compile(
    '(1677721[0-5]|1677720[0-9]|16777[0-1][0-9]{2}|1677[0-6][0-9]{3}|'
    '167[0-6][0-9]{4}|16[0-6][0-9]{5}|1[0-5][0-9]{6}|0?[0-9]{1,7}|)'
        )

COLOR_BY_NAME = {}

for color, *color_names in (
        (Color(0x000000), 'black'                  ,                            ),
        (Color(0x000080), 'navy'                   ,                            ),
        (Color(0x00008B), 'darkblue'               , 'dark blue'              , ),
        (Color(0x0000CD), 'mediumblue'             , 'medium blue'            , ),
        (Color(0x0000FF), 'blue'                   ,                            ),
        (Color(0x006400), 'darkgreen'              , 'dark green'             , ),
        (Color(0x008000), 'green'                  ,                            ),
        (Color(0x008080), 'teal'                   ,                            ),
        (Color(0x008B8B), 'darkcyan'               , 'dark cyan'              , ),
        (Color(0x00BFFF), 'deepskyblue'            , 'deep sky blue'          , ),
        (Color(0x00CED1), 'darkturquoise'          , 'dark turquoise'         , ),
        (Color(0x00FA9A), 'mediumspringgreen'      , 'medium spring green'    , ),
        (Color(0x00FF00), 'lime'                   ,                            ),
        (Color(0x00FF7F), 'springgreen'            , 'spring green'           , ),
        (Color(0x00FFFF), 'aqua'                   , 'cyan'                   , ),
        (Color(0x191970), 'midnightblue'           , 'midnight blue'          , ),
        (Color(0x1E90FF), 'dodgerblue'             , 'dodger blue'            , ),
        (Color(0x20B2AA), 'lightseagreen'          , 'light sea green'        , ),
        (Color(0x228B22), 'forestgreen'            , 'forest green'           , ),
        (Color(0x2E8B57), 'seagreen'               , 'sea green'              , ),
        (Color(0x2F4F4F), 'darkslategray'          , 'dark slate gray'        , ),
        (Color(0x32CD32), 'limegreen'              , 'lime green'             , ),
        (Color(0x3CB371), 'mediumseagreen'         , 'medium sea green'       , ),
        (Color(0x40E0D0), 'turquoise'              ,                            ),
        (Color(0x4169E1), 'royalblue'              , 'royal blue'             , ),
        (Color(0x4682B4), 'steelblue'              , 'steel blue'             , ),
        (Color(0x483D8B), 'darkslateblue'          , 'dark slate blue'        , ),
        (Color(0x48D1CC), 'mediumturquoise'        , 'medium turquoise'       , ),
        (Color(0x4B0082), 'indigo'                 ,                            ),
        (Color(0x556B2F), 'darkolivegreen'         , 'dark olive green'       , ),
        (Color(0x5F9EA0), 'cadetblue'              , 'cadet blue'             , ),
        (Color(0x6495ED), 'cornflowerblue'         , 'cornflower blue'        , ),
        (Color(0x66CDAA), 'mediumaquamarine'       , 'medium aquamarine'      , ),
        (Color(0x696969), 'dimgray'                , 'dim gray'               , ),
        (Color(0x6A5ACD), 'slateblue'              , 'slate blue'             , ),
        (Color(0x6B8E23), 'olivedrab'              , 'olive drab'             , ),
        (Color(0x708090), 'slategray'              , 'slate gray'             , ),
        (Color(0x778899), 'lightslategray'         , 'light slate gray'       , ),
        (Color(0x7B68EE), 'mediumslateblue'        , 'medium slate blue'      , ),
        (Color(0x7CFC00), 'lawngreen'              , 'lawn green'             , ),
        (Color(0x7FFF00), 'chartreuse'             ,                            ),
        (Color(0x7FFFD4), 'aquamarine'             ,                            ),
        (Color(0x800000), 'maroon'                 ,                            ),
        (Color(0x800080), 'purple'                 ,                            ),
        (Color(0x808000), 'olive'                  ,                            ),
        (Color(0x808080), 'gray'                   ,                            ),
        (Color(0x87CEEB), 'skyblue'                , 'sky blue'               , ),
        (Color(0x87CEFA), 'lightskyblue'           , 'light sky blue'         , ),
        (Color(0x8A2BE2), 'blueviolet'             , 'blue violet'            , ),
        (Color(0x8B0000), 'darkred'                , 'dark red'               , ),
        (Color(0x8B008B), 'darkmagenta'            , 'dark magenta'           , ),
        (Color(0x8B4513), 'saddlebrown'            , 'saddle brown'           , ),
        (Color(0x8FBC8F), 'darkseagreen'           , 'dark sea green'         , ),
        (Color(0x90EE90), 'lightgreen'             , 'light green'            , ),
        (Color(0x9370DB), 'mediumpurple'           , 'medium purple'          , ),
        (Color(0x9400D3), 'darkviolet'             , 'dark violet'            , ),
        (Color(0x98FB98), 'palegreen'              , 'pale green'             , ),
        (Color(0x9932CC), 'darkorchid'             , 'dark orchid'            , ),
        (Color(0x9ACD32), 'yellowgreen'            , 'yellow green'           , ),
        (Color(0xA0522D), 'sienna'                 ,                            ),
        (Color(0xA52A2A), 'brown'                  ,                            ),
        (Color(0xA9A9A9), 'darkgray'               , 'dark gray'              , ),
        (Color(0xADD8E6), 'lightblue'              , 'light blue'             , ),
        (Color(0xADFF2F), 'greenyellow'            , 'green yellow'           , ),
        (Color(0xAFEEEE), 'paleturquoise'          , 'pale turquoise'         , ),
        (Color(0xB0C4DE), 'lightsteelblue'         , 'light steel blue'       , ),
        (Color(0xB0E0E6), 'powderblue'             , 'powder blue'            , ),
        (Color(0xB22222), 'firebrick'              ,                            ),
        (Color(0xB8860B), 'darkgoldenrod'          , 'dark goldenrod'         , ),
        (Color(0xBA55D3), 'mediumorchid'           , 'medium orchid'          , ),
        (Color(0xBC8F8F), 'rosybrown'              , 'rosy brown'             , ),
        (Color(0xBDB76B), 'darkkhaki'              , 'dark khaki'             , ),
        (Color(0xC0C0C0), 'silver'                 ,                            ),
        (Color(0xC71585), 'mediumvioletred'        , 'medium violet red'      , ),
        (Color(0xCD5C5C), 'indianred'              , 'indian red'             , ),
        (Color(0xCD853F), 'peru'                   ,                            ),
        (Color(0xD2691E), 'chocolate'              ,                            ),
        (Color(0xD2B48C), 'tan'                    ,                            ),
        (Color(0xD3D3D3), 'lightgray'              , 'light gray'             , ),
        (Color(0xD8BFD8), 'thistle'                ,                            ),
        (Color(0xDA70D6), 'orchid'                 ,                            ),
        (Color(0xDAA520), 'goldenrod'              ,                            ),
        (Color(0xDB7093), 'palevioletred'          , 'pale violet red'        , ),
        (Color(0xDC143C), 'crimson'                ,                            ),
        (Color(0xDCDCDC), 'gainsboro'              ,                            ),
        (Color(0xDDA0DD), 'plum'                   ,                            ),
        (Color(0xDEB887), 'burlywood'              ,                            ),
        (Color(0xE0FFFF), 'lightcyan'              , 'light cyan'             , ),
        (Color(0xE6E6FA), 'lavender'               ,                            ),
        (Color(0xE9967A), 'darksalmon'             , 'dark salmon'            , ),
        (Color(0xEE82EE), 'violet'                 ,                            ),
        (Color(0xEEE8AA), 'palegoldenrod'          , 'pale goldenrod'         , ),
        (Color(0xF08080), 'lightcoral'             , 'light coral'            , ),
        (Color(0xF0E68C), 'khaki'                  ,                            ),
        (Color(0xF0F8FF), 'aliceblue'              , 'alice blue'             , ),
        (Color(0xF0FFF0), 'honeydew'               ,                            ),
        (Color(0xF0FFFF), 'azure'                  ,                            ),
        (Color(0xF4A460), 'sandybrown'             , 'sandy brown'            , ),
        (Color(0xF5DEB3), 'wheat'                  ,                            ),
        (Color(0xF5F5DC), 'beige'                  ,                            ),
        (Color(0xF5F5F5), 'whitesmoke'             , 'white smoke'            , ),
        (Color(0xF5FFFA), 'mintcream'              , 'mint cream'             , ),
        (Color(0xF8F8FF), 'ghostwhite'             , 'ghost white'            , ),
        (Color(0xFA8072), 'salmon'                 ,                            ),
        (Color(0xFAEBD7), 'antiquewhite'           , 'antique white'          , ),
        (Color(0xFAF0E6), 'linen'                  ,                            ),
        (Color(0xFAFAD2), 'lightgoldenrodyellow'   , 'light goldenrod yellow' , ),
        (Color(0xFDF5E6), 'oldlace'                , 'old lace'               , ),
        (Color(0xFF0000), 'red'                    ,                            ),
        (Color(0xFF00FF), 'fuchsia'                , 'magenta'                , ),
        (Color(0xFF1493), 'deeppink'               , 'deep pink'              , ),
        (Color(0xFF4500), 'orangered'              , 'orange red'             , ),
        (Color(0xFF6347), 'tomato'                 ,                            ),
        (Color(0xFF69B4), 'hotpink'                , 'hot pink'               , ),
        (Color(0xFF7F50), 'coral'                  ,                            ),
        (Color(0xFF8C00), 'darkorange'             , 'dark orange'            , ),
        (Color(0xFFA07A), 'lightsalmon'            , 'light salmon'           , ),
        (Color(0xFFA500), 'orange'                 ,                            ),
        (Color(0xFFB6C1), 'lightpink'              , 'light pink'             , ),
        (Color(0xFFC0CB), 'pink'                   ,                            ),
        (Color(0xFFD700), 'gold'                   ,                            ),
        (Color(0xFFDAB9), 'peachpuff'              , 'peach puff'             , ),
        (Color(0xFFDEAD), 'navajowhite'            , 'navajo white'           , ),
        (Color(0xFFE4B5), 'moccasin'               ,                            ),
        (Color(0xFFE4C4), 'bisque'                 ,                            ),
        (Color(0xFFE4E1), 'mistyrose'              , 'misty rose'             , ),
        (Color(0xFFEBCD), 'blanchedalmond'         , 'blanched almond'        , ),
        (Color(0xFFEFD5), 'papayawhip'             , 'papaya whip'            , ),
        (Color(0xFFF0F5), 'lavenderblush'          , 'lavender blush'         , ),
        (Color(0xFFF5EE), 'seashell'               ,                            ),
        (Color(0xFFF8DC), 'cornsilk'               ,                            ),
        (Color(0xFFFACD), 'lemonchiffon'           , 'lemon chiffon'          , ),
        (Color(0xFFFAF0), 'floralwhite'            , 'floral white'           , ),
        (Color(0xFFFAFA), 'snow'                   ,                            ),
        (Color(0xFFFF00), 'yellow'                 ,                            ),
        (Color(0xFFFFE0), 'lightyellow'            , 'light yellow'           , ),
        (Color(0xFFFFF0), 'ivory'                  ,                            ),
        (Color(0xFFFFFF), 'white'                  ,                            ),
            ):
    
    for color_name in color_names:
        COLOR_BY_NAME[color_name] = color

del color, color_names, color_name

def parse_color(text):
    """
    Tries to parse out a ``Color`` from the inputted text.
    
    Returns
    -------
    color : `None` or ``Color``
    """
    text = text.lower()
    
    parsed = COLOR_HTML_6_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1), base=16)
    
    try:
        return COLOR_BY_NAME[text]
    except KeyError:
        pass
    
    parsed = COLOR_RGB_INT_RP.fullmatch(text)
    if (parsed is not None):
        red, green, blue = parsed.groups()
        red = int(red)
        green = int(green)
        blue = int(blue)
        return Color((red<<16)|(green<<8)|blue)
    
    parsed = COLOR_HEX_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1), base=16)
    
    parsed = COLOR_OCT_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1), base=8)
    
    parsed = COLOR_BIN_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1), base=2)
    
    parsed = COLOR_RGB_FLOAT_RP.fullmatch(text)
    if (parsed is not None):
        red, green, blue = parsed.groups()
        red = floor(float(red)*255.0)
        green = floor(float(green)*255.0)
        blue = floor(float(blue)*255.0)
        return Color((red<<16)|(green<<8)|blue)
    
    parsed = COLOR_HTML_3_RP.fullmatch(text)
    if (parsed is not None):
        raw_value = int(parsed.group(1), base=16)
        red = (raw_value>>8)*17
        green = ((raw_value>>4)&0xf)*17
        blue = (raw_value&0xf)*17
        return Color((red<<16)|(green<<8)|blue)
    
    parsed = COLOR_DEC_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1))
    
    return None

del re
