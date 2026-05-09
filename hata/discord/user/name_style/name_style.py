__all__ = ('NameStyle',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_colors, parse_effect, parse_font, put_colors, put_effect, put_font, validate_colors, validate_effect,
    validate_font
)
from .preinstanced import NameStyleEffect, NameStyleFont


class NameStyle(RichAttributeErrorBaseType):
    """
    Represents a user's name's style.
    
    Attributes
    ----------
    colors : ``None | tuple<Color>``
        The used colors.
    
    effect : ``NameStyleEffect``
        When the name style expires.
    
    font : ``NameStyleFont``
        The dominant color of the name style.
    """
    __slots__ = ('colors', 'effect', 'font')
    
    def __new__(cls, *, colors = ..., effect = ..., font = ...):
        """
        Creates a new user  plate instance from the given parameters.
        
        Attributes
        ----------
        colors : ``None | iterable<int> | iterable<Color>``, Optional (Keyword only)
            The used colors.
        
        effect : ``None | int | NameStyleEffect``, Optional (Keyword only)
            When the name style expires.
        
        font : ``None | int | NameStyleFont``, Optional (Keyword only)
            The dominant color of the name style.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # colors
        if colors is ...:
            colors = None
        else:
            colors = validate_colors(colors)
        
        # effect
        if effect is ...:
            effect = NameStyleEffect.none
        else:
            effect = validate_effect(effect)
        
        # font
        if font is ...:
            font = NameStyleFont.default
        else:
            font = validate_font(font)
        
        # Construct
        self = object.__new__(cls)
        self.colors = colors
        self.effect = effect
        self.font = font
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # colors
        repr_parts.append(' colors = ')
        repr_parts.append(repr(self.colors))
        
        # effect
        effect = self.effect
        repr_parts.append(', effect = ')
        repr_parts.append(effect.name)
        repr_parts.append(' ~ ')
        repr_parts.append(str(effect.value))
        
        # font
        font = self.font
        repr_parts.append(', font = ')
        repr_parts.append(font.name)
        repr_parts.append(' ~ ')
        repr_parts.append(str(font.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # colors
        hash_value ^= hash(self.colors)
        
        # effect
        hash_value ^= hash(self.effect)
        
        # font
        hash_value ^= hash(self.font)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # colors
        if self.colors != other.colors:
            return False
        
        # effect
        if self.effect != other.effect:
            return False
        
        # font
        if self.font != other.font:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a name style from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received  plate data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.colors = parse_colors(data)
        self.effect = parse_effect(data)
        self.font = parse_font(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the name style to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_colors(self.colors, data, defaults)
        put_effect(self.effect, data, defaults)
        put_font(self.font, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the name style.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        colors = self.colors
        if (colors is not None):
            colors = (*colors,)
        new.colors = colors
        new.effect = self.effect
        new.font = self.font
        return new
    
    
    def copy_with(
        self, 
        *,
        colors = ...,
        effect = ...,
        font = ...,
    ):
        """
        Copies the name style with the given fields.
        
        Parameters
        ----------
        colors : ``None | iterable<int> | iterable<Color>``, Optional (Keyword only)
            The used colors.
        
        effect : ``None | int | NameStyleEffect``, Optional (Keyword only)
            When the name style expires.
        
        font : ``None | int | NameStyleFont``, Optional (Keyword only)
            The dominant color of the name style.
        
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
        # colors
        if colors is ...:
            colors = self.colors
            if (colors is not None):
                colors = (*colors,)
        else:
            colors = validate_colors(colors)
        
        # effect
        if effect is ...:
            effect = self.effect
        else:
            effect = validate_effect(effect)
        
        # font
        if font is ...:
            font = self.font
        else:
            font = validate_font(font)
        
        # Construct
        new = object.__new__(type(self))
        new.colors = colors
        new.effect = effect
        new.font = font
        return new
