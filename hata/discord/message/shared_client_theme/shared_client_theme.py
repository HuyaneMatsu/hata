__all__ = ('SharedClientTheme',)

from scarletio import RichAttributeErrorBaseType

from .constants import GRADIENT_ANGLE_MIN, INTENSITY_MIN
from .fields import (
    parse_base_theme, parse_colors, parse_gradient_angle, parse_intensity, put_base_theme, put_colors,
    put_gradient_angle, put_intensity, validate_base_theme, validate_colors, validate_gradient_angle,
    validate_intensity
)
from .preinstanced import SharedClientThemeBaseTheme


class SharedClientTheme(RichAttributeErrorBaseType):
    """
    Represents a shared client theme through a message.
    
    Attributes
    ----------
    base_theme : ``SharedClientThemeBaseTheme``
        The base theme to build upon.
    
    colors : ``None | tuple<Color>``
        The colors of the theme.
    
    gradient_angle : `int`
        The angle of the theme's colors.
    
    intensity : `int`
        The intensity of the theme's colors.
    """
    __slots__ = ('base_theme', 'colors', 'gradient_angle', 'intensity')
    
    def __new__(cls, *, base_theme = ..., colors = ..., gradient_angle = ..., intensity = ...):
        """
        Creates a new shared client theme with the given parameters.
        
        Parameters
        ----------
        base_theme : ``None | int | SharedClientThemeBaseTheme``, Optional (Keyword only)
            The base theme to build upon.
        
        colors : ``None | iterable<Color>``, Optional (Keyword only)
            The colors of the theme.
        
        gradient_angle : `None | int`, Optional (Keyword only)
            The angle of the theme's colors.
        
        intensity : `None | int`, Optional (Keyword only)
            The intensity of the theme's colors.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # base_theme
        if base_theme is ...:
            base_theme = SharedClientThemeBaseTheme.none
        else:
            base_theme = validate_base_theme(base_theme)
        
        # colors
        if colors is ...:
            colors = None
        else:
            colors = validate_colors(colors)
        
        # gradient_angle
        if gradient_angle is ...:
            gradient_angle = GRADIENT_ANGLE_MIN
        else:
            gradient_angle = validate_gradient_angle(gradient_angle)
        
        # intensity
        if intensity is ...:
            intensity = INTENSITY_MIN
        else:
            intensity = validate_intensity(intensity)
        
        # Construct
        self = object.__new__(cls)
        self.base_theme = base_theme
        self.colors = colors
        self.gradient_angle = gradient_angle
        self.intensity = intensity
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a shared client theme from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Shared client theme data.
        """
        self = object.__new__(cls)
        self.base_theme = parse_base_theme(data)
        self.colors = parse_colors(data)
        self.gradient_angle = parse_gradient_angle(data)
        self.intensity = parse_intensity(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the shared client theme to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_base_theme(self.base_theme, data, defaults)
        put_colors(self.colors, data, defaults)
        put_gradient_angle(self.gradient_angle, data, defaults)
        put_intensity(self.intensity, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # base_theme
        base_theme = self.base_theme
        repr_parts.append(' base_theme = ')
        repr_parts.append(base_theme.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(base_theme.value))
        
        # colors
        repr_parts.append(', colors = ')
        repr_parts.append(repr(self.colors))
        
        # gradient_angle
        repr_parts.append(' gradient_angle = ')
        repr_parts.append(repr(self.gradient_angle))
        
        # intensity
        repr_parts.append(' intensity = ')
        repr_parts.append(repr(self.intensity))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # base_theme
        hash_value ^= self.base_theme.value
        
        # colors
        colors = self.colors
        if (colors is not None):
            hash_value ^= hash(colors)
        
        # gradient_angle
        hash_value ^= self.gradient_angle << 8
        
        # intensity
        hash_value ^= self.intensity << 16
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return False
        
        # base_theme
        if (self.base_theme is not other.base_theme):
            return False
        
        # colors
        if (self.colors != other.colors):
            return False
        
        # gradient_angle
        if (self.gradient_angle != other.gradient_angle):
            return False
        
        # intensity
        if (self.intensity != other.intensity):
            return False
        
        return True
    
    
    def copy(self):
        """
        Copies the shared client theme.
        
        Returns
        -------
        new : `instance<type<self>`
        """
        new = object.__new__(type(self))
        new.base_theme = self.base_theme
        
        colors = self.colors
        if (colors is not None):
            colors = (*colors,)
        new.colors = colors
        
        new.gradient_angle = self.gradient_angle
        new.intensity = self.intensity
        return new
    
    
    def copy_with(self, *, base_theme = ..., colors = ..., gradient_angle = ..., intensity = ...):
        """
        Copies the shared client theme with the the defined fields.
        
        Parameters
        ----------
        base_theme : ``None | int | SharedClientThemeBaseTheme``, Optional (Keyword only)
            The base theme to build upon.
        
        colors : ``None | iterable<Color>``, Optional (Keyword only)
        The colors of the theme.
        
        gradient_angle : `None | int`, Optional (Keyword only)
            The angle of the theme's colors.
        
        intensity : `None | int`, Optional (Keyword only)
            The intensity of the theme's colors.
        
        Returns
        -------
        new : `instance<type<self>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # base_theme
        if base_theme is ...:
            base_theme = self.base_theme
        else:
            base_theme = validate_base_theme(base_theme)
        
        # colors
        if colors is ...:
            colors = self.colors
            if (colors is not None):
                colors = (*colors),
        else:
            colors = validate_colors(colors)
        
        # gradient_angle
        if gradient_angle is ...:
            gradient_angle = self.gradient_angle
        else:
            gradient_angle = validate_gradient_angle(gradient_angle)
        
        # intensity
        if intensity is ...:
            intensity = self.intensity
        else:
            intensity = validate_intensity(intensity)
        
        # Construct
        new = object.__new__(type(self))
        new.base_theme = base_theme
        new.colors = colors
        new.gradient_angle = gradient_angle
        new.intensity = intensity
        return new
