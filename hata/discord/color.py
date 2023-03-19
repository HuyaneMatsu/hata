__all__ = ('COLORS', 'Color', 'parse_color',)

import re
from colorsys import rgb_to_hls
from math import floor
from random import Random

from scarletio import modulize


class Color(int):
    """
    A Color object represents a RGB color. Using int instead of Color is completely fine.
    
    Class Attributes
    ----------------
    _random : `random.Random`
        Used for random seeding, so it has it's own `random.Random` to do it.
        
        To get a random color, use ``.random` and to set seed use ``.set_seed``
    
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
    <Color #FF0000>
    
    >>> # Converting color back to html color code
    <Color #FF0000>
    >>> color.as_html
    '#FF0000'
    
    >>> # str(color) is same as color.as_html
    >>> str(color)
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
    
    
    def __str__(self):
        """Returns the color as a string. Same as ``.as_html``."""
        return f'#{self:06X}'
    
    
    @classmethod
    def from_html(cls, value):
        """
        Converts a HTML color code to a color object.
        
        Parameters
        ----------
        value : `str`
            HTML color code.
        
        Returns
        -------
        color : `instance<cls>`
        
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
                    color = cls(value, base = 16)
                except ValueError:
                    pass
                else:
                    return color
            
            elif value_length == 3:
                try:
                    color_value = int(value, base = 16)
                except ValueError:
                    pass
                else:
                    red = (color_value >> 8) * 17
                    green = ((color_value >> 4) & 0xf) * 17
                    blue = (color_value & 0xf) * 17
                    return cls((red << 16) | (green << 8) | blue)
        
        raise ValueError(
            f'The given value has invalid length or is not hexadecimal, got {value!r}.'
        )
    
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
        Converts the given red-green-blue tuple to a color object.
        
        Parameters
        ----------
        rgb_tuple : `tuple` (`int`, `int`, `int`)
            A tuple of `3` integers which are in range [0, 255].
        
        Returns
        -------
        color : `instance<cls>`
        
        Raises
        ------
        ValueError
            - If `rgb_tuple`'s length is not `3`.
            - If a channel value out of expected range.
        """
        if len(rgb_tuple) != 3:
            raise ValueError(
                f'Rgb tuple should have length `3`, got {len(rgb_tuple)!r}; {rgb_tuple!r}.'
            )
        
        return cls.from_rgb(*rgb_tuple)
    
    from_tuple = from_rgb_tuple
    
    @property
    def as_rgb_tuple(self):
        """
        Returns the color in red-green-blue tuple format.
        
        Returns
        -------
        rgb_tuple : `tuple` (`int`, `int`, `int`)
        """
        return (self >> 16, (self >> 8) & 0x00ff, self & 0x0000ff)
    
    as_tuple = as_rgb_tuple
    as_rgb = as_rgb_tuple
    
    @classmethod
    def from_rgb_float_tuple(cls, rgb_tuple):
        """
        Converts the given red-green-blue float tuple to a color object.
        
        Parameters
        ----------
        rgb_tuple : `tuple` (`float`, `float`, `float`)
            A tuple of `3` floats which are in range [0.0, 1.0].
        
        Returns
        -------
        color : `instance<cls>`
        
        Raises
        ------
        ValueError
            - `rgb_tuple` has no length of `3`.
        """
        if len(rgb_tuple) != 3:
            raise ValueError(
                f'Rgb tuple should have length `3`, got {len(rgb_tuple)!r}; {rgb_tuple!r}.'
            )
        
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
        return ((self >> 16) * (1.0 / 255.0), ((self >> 8) & 0x00ff) * (1.0 / 255.0), (self & 0x0000ff) * (1.0 / 255.0))
    
    as_float_tuple = as_rgb_float_tuple
    as_rgb_float = as_rgb_float_tuple
    
    @classmethod
    def from_rgb(cls, red, green, blue):
        """
        Converts red, green and blue channels to a color object.
        
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
        color : `instance<cls>`
        """
        if red > 255:
            red = 255
        elif red < 0:
            red = 0
        
        if green > 255:
            green = 255
        elif green < 0:
            green = 0
        
        if blue > 255:
            blue = 255
        elif blue < 0:
            blue = 0
        
        return cls((red << 16) | (green << 8) | blue)
    
    
    @classmethod
    def from_rgb_float(cls, red, green, blue):
        """
        Converts red, green and blue float channels to a color object.
        
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
        color : `instance<cls>`
        """
        return cls.from_rgb(floor(red * 255.0), floor(green * 255.0), floor(blue * 255.0))
    
    # hsl
    
    @classmethod
    def from_hsl_tuple(cls, hsl_tuple):
        """
        Converts the given hue-saturation-lightness tuple to a color object.
        
        Parameters
        ----------
        hsl_tuple : `tuple` (`int`, `int`, `int`)
            A tuple of `3` integers ([0, 360], [0, 100], [0, 100]).
        
        Returns
        -------
        color : `instance<cls>`
        
        Raises
        ------
        ValueError
            - If `hsl_tuple`'s length is not `3`.
        """
        if len(hsl_tuple) != 3:
            raise ValueError(
                f'Hsl tuple should have length `3`, got {len(hsl_tuple)!r}; {hsl_tuple!r}.'
            )
        
        return cls.from_hsl(*hsl_tuple)
    
    
    @property
    def as_hsl_tuple(self):
        """
        Returns the color in hue-saturation-lightness tuple format.
        
        Returns
        -------
        hsl_tuple : `tuple` (`int`, `int`, `int`)
        """
        hue, saturation, lightness = self.as_hsl_float_tuple
        return round(hue * 360), round(saturation * 100), round(lightness * 100)
    
    
    @classmethod
    def from_hsl_float_tuple(cls, hsl_tuple):
        """
        Converts a hue-saturation-lightness float tuple to a color object.
        
        Parameters
        ----------
        hsl_tuple : `tuple` (`float`, `float`, `float`)
            A tuple of `3` floats which are in range [0.0, 1.0].
        
        Returns
        -------
        color : `instance<cls>`
        
        Raises
        ------
        ValueError
            - `hsl_tuple` has no length of `3`.
            - Channel value out of expected range.
        """
        if len(hsl_tuple) != 3:
            raise ValueError(
                f'Rgb tuple should have length `3`, got {len(hsl_tuple)!r}; {hsl_tuple!r}.'
            )
        
        return cls.from_hsl_float(*hsl_tuple)
    
    
    @property
    def as_hsl_float_tuple(self):
        """
        Returns the color in hue-saturation-lightness float tuple format.
        
        Returns
        -------
        hsl_float_tuple : `tuple` (`float`, `float`, `float`)
        """
        red = ((self >> 16) & 0xff) * (1.0 / 255.0)
        green = ((self >> 8) & 0xff) * (1.0 / 255.0)
        blue = (self & 0xff) * (1.0 / 255.0)
        
        max_value = max(red, green, blue)
        min_value = min(red, green, blue)
        diversity = max_value - min_value
        
        if diversity == 0.0:
            hue = 0.0
        elif max_value == red:
            hue = ((green - blue) / diversity) % 6.0
        elif max_value == green:
            hue = (blue - red) / diversity + 2.0
        else:
            hue = (red - green) / diversity + 4.0
        
        hue *= (1.0 / 6.0)
        if hue < 0.0:
            hue += 1.0
        
        lightness = (max_value + min_value) * 0.5
        
        if diversity == 0.0:
            saturation = 0.0
        else:
            saturation = diversity / (1.0 - abs(2.0 * lightness - 1.0))
        
        return hue, saturation, lightness
    
    
    @classmethod
    def from_hsl(cls, hue, saturation, lightness):
        """
        Converts hue, saturation and lightness channels to a color object.
        
        Parameters
        ----------
        hue : `int`
            Hue channel.
        saturation : `int`
            Saturation channel.
        lightness : `int`
            Lightness channel.
        
        Returns
        -------
        color : `instance<cls>`
        """
        return cls.from_hsl_float(hue * (1.0 / 360.0), saturation * (1.0 / 100.0), lightness * (1.0 / 100.0))
    
    
    @classmethod
    def from_hsl_float(cls, hue, saturation, lightness):
        """
        Converts hue, saturation and lightness float channels to a color object.
        
        Parameters
        ----------
        hue : `float`
            Hue channel.
        saturation : `float`
            Saturation channel.
        lightness : `float`
            Lightness channel.
        
        Returns
        -------
        color : `instance<cls>`
        
        Raises
        ------
        ValueError
            Channel value out of expected range.
        """
        hue %= 1.0
        
        if saturation > 1.0:
            saturation = 1.0
        elif saturation < 0.0:
            saturation = 0.0
        
        if lightness > 1.0:
            lightness = 1.0
        elif lightness < 0.0:
            lightness = 0.0
        
        primary_channel_value = (1 - abs(2 * lightness - 1)) * saturation
        secondary_channel_value = primary_channel_value * (1.0 - abs((hue * 6.0) % 2.0 - 1.0))
        lightness_base = lightness - primary_channel_value * 0.5
        
        if hue < (2.0 / 6.0):
            if hue < (1.0 / 6.0):
                red = primary_channel_value
                green = secondary_channel_value
                blue = 0.0
            
            else:
                red = secondary_channel_value
                green = primary_channel_value
                blue = 0.0
        
        elif hue < (4.0 / 6.0):
            if hue < (3.0 / 6.0):
                red = 0.0
                green = primary_channel_value
                blue = secondary_channel_value
            
            else:
                red = 0.0
                green = secondary_channel_value
                blue = primary_channel_value
        
        else:
            if hue < (5.0 / 6.0):
                red = secondary_channel_value
                green = 0.0
                blue = primary_channel_value
            
            else:
                red = primary_channel_value
                green = 0.0
                blue = secondary_channel_value
        
        red += lightness_base
        green += lightness_base
        blue += lightness_base
        
        return cls((round(red * 255.0) << 16) | (round(green * 255.0) << 8) | round(blue * 255.0))
    
    
    # Read only stuff
    
    @property
    def red(self):
        """
        Returns the color's red channel's value.
        
        Returns
        -------
        red_value : `int`
        """
        return self >> 16
    
    r = red
    
    @property
    def green(self):
        """
        Returns the color's green channel's value.
        
        Returns
        -------
        green_value : `int`
        """
        return (self >> 8) & 0x0000ff
    
    g = green
    
    @property
    def blue(self):
        """
        Returns the color's blue channel's value.
        
        Returns
        -------
        blue_value : `int`
        """
        return self & 0x0000ff
    
    b = blue
    
    _random = Random()
    
    @classmethod
    def random(cls):
        """
        Returns a random color.
        
        Returns
        -------
        color : `instance<cls>`
        """
        return cls(cls._random.random() * 0xffffff)
    
    
    @classmethod
    def set_seed(cls, seed = None, version = 2):
        """
        Initialize the random number generator for the color type.
        
        Parameters
        ----------
        seed : `object` = `None`, Optional
            If `seed` is given as `None`, the current system time is used. If randomness sources are provided by the
            operating system, they are used instead of the system time.
            
            If `seed` is an `int`, it is used directly.
            
            > Since Python 3.9 the seed must be one of the following types: `NoneType`, `int`, `float`, `str`, `bytes`,
            > or `bytearray`.
            
        version : `int` = `2`, Optional
            Can be given either as `1`, `2`.
            
            If given as `2` (so by default), a `str`, `bytes`, `bytearray` object gets converted to an `int` and all
            of its bits are used.
            
            If given as `1` (provided for reproducing random sequences from older versions of Python), the algorithm
            for `str` and `bytes` generates a narrower range of seeds.
        """
        cls._random.seed(seed, version)


COLOR_RGB_INT_RP = re.compile(
    '(25[0-5]|2[0-4][0-9]|1[0-9]{2}|0?[0-9]{0,2})[\s\,]+'
    '(25[0-5]|2[0-4][0-9]|1[0-9]{2}|0?[0-9]{0,2})[\s\,]+'
    '(25[0-5]|2[0-4][0-9]|1[0-9]{2}|0?[0-9]{0,2})'
)

COLOR_RGB_FLOAT_RP = re.compile(
    '([01]|0?\.[0-9]{1,32})[\s\,]+'
    '([01]|0?\.[0-9]{1,32})[\s\,]+'
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

@modulize
class COLORS:
    """
    Contains the web colors as attributes.
    """
    alice_blue = Color(0xF0F8FF)
    antique_white = Color(0xFAEBD7)
    aquamarine = Color(0x7FFFD4)
    azure = Color(0xF0FFFF)
    beige = Color(0xF5F5DC)
    bisque = Color(0xFFE4C4)
    black = Color(0x0)
    blanched_almond = Color(0xFFEBCD)
    blue = Color(0xFF)
    blue_violet = Color(0x8A2BE2)
    brown = Color(0xA52A2A)
    burlywood = Color(0xDEB887)
    cadet_blue = Color(0x5F9EA0)
    chartreuse = Color(0x7FFF00)
    chocolate = Color(0xD2691E)
    coral = Color(0xFF7F50)
    cornflower_blue = Color(0x6495ED)
    cornsilk = Color(0xFFF8DC)
    crimson = Color(0xDC143C)
    cyan = Color(0xFFFF)
    dark_blue = Color(0x8B)
    dark_cyan = Color(0x8B8B)
    dark_goldenrod = Color(0xB8860B)
    dark_gray = Color(0xA9A9A9)
    dark_green = Color(0x6400)
    dark_khaki = Color(0xBDB76B)
    dark_magenta = Color(0x8B008B)
    dark_olive_green = Color(0x556B2F)
    dark_orange = Color(0xFF8C00)
    dark_orchid = Color(0x9932CC)
    dark_red = Color(0x8B0000)
    dark_salmon = Color(0xE9967A)
    dark_sea_green = Color(0x8FBC8F)
    dark_slate_blue = Color(0x483D8B)
    dark_slate_gray = Color(0x2F4F4F)
    dark_turquoise = Color(0xCED1)
    dark_violet = Color(0x9400D3)
    deep_pink = Color(0xFF1493)
    deep_sky_blue = Color(0xBFFF)
    dim_gray = Color(0x696969)
    dodger_blue = Color(0x1E90FF)
    firebrick = Color(0xB22222)
    floral_white = Color(0xFFFAF0)
    forest_green = Color(0x228B22)
    gainsboro = Color(0xDCDCDC)
    ghost_white = Color(0xF8F8FF)
    gold = Color(0xFFD700)
    goldenrod = Color(0xDAA520)
    gray = Color(0x808080)
    green = Color(0x8000)
    green_yellow = Color(0xADFF2F)
    honeydew = Color(0xF0FFF0)
    hot_pink = Color(0xFF69B4)
    indian_red = Color(0xCD5C5C)
    indigo = Color(0x4B0082)
    ivory = Color(0xFFFFF0)
    khaki = Color(0xF0E68C)
    koishi_mint = Color(0x7FE3B5)
    koishi_pine = Color(0x6EC8A9)
    koishi_shiny = Color(0xB3FCFF)
    koishi_turquoise = Color(0x498B7E)
    lavender = Color(0xE6E6FA)
    lavender_blush = Color(0xFFF0F5)
    lawn_green = Color(0x7CFC00)
    lemon_chiffon = Color(0xFFFACD)
    light_blue = Color(0xADD8E6)
    light_coral = Color(0xF08080)
    light_cyan = Color(0xE0FFFF)
    light_goldenrod_yellow = Color(0xFAFAD2)
    light_gray = Color(0xD3D3D3)
    light_green = Color(0x90EE90)
    light_pink = Color(0xFFB6C1)
    light_salmon = Color(0xFFA07A)
    light_sea_green = Color(0x20B2AA)
    light_sky_blue = Color(0x87CEFA)
    light_slate_gray = Color(0x778899)
    light_steel_blue = Color(0xB0C4DE)
    light_yellow = Color(0xFFFFE0)
    lime = Color(0xFF00)
    lime_green = Color(0x32CD32)
    linen = Color(0xFAF0E6)
    magenta = Color(0xFF00FF)
    maroon = Color(0x800000)
    medium_aquamarine = Color(0x66CDAA)
    medium_blue = Color(0xCD)
    medium_orchid = Color(0xBA55D3)
    medium_purple = Color(0x9370DB)
    medium_sea_green = Color(0x3CB371)
    medium_slate_blue = Color(0x7B68EE)
    medium_spring_green = Color(0xFA9A)
    medium_turquoise = Color(0x48D1CC)
    medium_violet_red = Color(0xC71585)
    midnight_blue = Color(0x191970)
    mint_cream = Color(0xF5FFFA)
    misty_rose = Color(0xFFE4E1)
    moccasin = Color(0xFFE4B5)
    navajo_white = Color(0xFFDEAD)
    navy = Color(0x80)
    old_lace = Color(0xFDF5E6)
    olive = Color(0x808000)
    olive_drab = Color(0x6B8E23)
    orange = Color(0xFFA500)
    orange_red = Color(0xFF4500)
    orchid = Color(0xDA70D6)
    pale_goldenrod = Color(0xEEE8AA)
    pale_green = Color(0x98FB98)
    pale_turquoise = Color(0xAFEEEE)
    pale_violet_red = Color(0xDB7093)
    papaya_whip = Color(0xFFEFD5)
    peach_puff = Color(0xFFDAB9)
    peru = Color(0xCD853F)
    pink = Color(0xFFC0CB)
    plum = Color(0xDDA0DD)
    powder_blue = Color(0xB0E0E6)
    purple = Color(0x800080)
    red = Color(0xFF0000)
    rosy_brown = Color(0xBC8F8F)
    royal_blue = Color(0x4169E1)
    saddle_brown = Color(0x8B4513)
    salmon = Color(0xFA8072)
    sandy_brown = Color(0xF4A460)
    sea_green = Color(0x2E8B57)
    seashell = Color(0xFFF5EE)
    sienna = Color(0xA0522D)
    silver = Color(0xC0C0C0)
    sky_blue = Color(0x87CEEB)
    slate_blue = Color(0x6A5ACD)
    slate_gray = Color(0x708090)
    snow = Color(0xFFFAFA)
    spring_green = Color(0xFF7F)
    steel_blue = Color(0x4682B4)
    tan = Color(0xD2B48C)
    teal = Color(0x8080)
    thistle = Color(0xD8BFD8)
    tomato = Color(0xFF6347)
    turquoise = Color(0x40E0D0)
    violet = Color(0xEE82EE)
    wheat = Color(0xF5DEB3)
    white = Color(0xFFFFFF)
    white_smoke = Color(0xF5F5F5)
    yellow = Color(0xFFFF00)
    yellow_green = Color(0x9ACD32)


for attribute_name, attribute_value in COLORS.__dict__.items():
    if isinstance(attribute_value, Color):
        COLOR_BY_NAME[attribute_name.replace('_', '')] = attribute_value
        COLOR_BY_NAME[attribute_name.replace(' ', '')] = attribute_value

del attribute_name, attribute_value


def parse_color(text):
    """
    Tries to parse out a color from the inputted text.
    
    Returns
    -------
    color : `None`, ``Color``
    """
    text = text.lower()
    
    parsed = COLOR_HTML_6_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1), base = 16)
    
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
        return Color((red << 16) | (green << 8) | blue)
    
    parsed = COLOR_HEX_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1), base = 16)
    
    parsed = COLOR_OCT_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1), base = 8)
    
    parsed = COLOR_BIN_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1), base = 2)
    
    parsed = COLOR_RGB_FLOAT_RP.fullmatch(text)
    if (parsed is not None):
        red, green, blue = parsed.groups()
        red = floor(float(red) * 255.0)
        green = floor(float(green) * 255.0)
        blue = floor(float(blue) * 255.0)
        return Color((red << 16) | (green << 8) | blue)
    
    parsed = COLOR_HTML_3_RP.fullmatch(text)
    if (parsed is not None):
        raw_value = int(parsed.group(1), base=16)
        red = (raw_value >> 8) * 17
        green = ((raw_value >> 4) & 0xf) * 17
        blue = (raw_value & 0xf) * 17
        return Color((red << 16) | (green << 8) | blue)
    
    parsed = COLOR_DEC_RP.fullmatch(text)
    if (parsed is not None):
        return Color(parsed.group(1))
    
    return None
