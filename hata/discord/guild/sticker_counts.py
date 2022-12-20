__all__ = ()

import warnings

from scarletio import RichAttributeErrorBaseType

from ..sticker import StickerFormat


STICKER_FORMAT_STATIC = StickerFormat.png
STICKER_FORMAT_ANIMATED = StickerFormat.apng
STICKER_FORMAT_LOTTIE = StickerFormat.lottie


class StickerCounts(RichAttributeErrorBaseType):
    """
    Represents a guild's counted stickers by their type.
    
    Attributes
    ----------
    animated : `int`
        Animated sticker count.
    lottie : `int`
        Lottie sticker count.
    static : `int`
        Static sticker count.
    
    Notes
    -----
    Use ``Guild.sticker_limit`` to get it's sticker limit.
    """
    __slots__ = ('animated', 'lottie', 'static')
    
    def __new__(
        cls,
        *,
        animated = 0,
        lottie = 0,
        static = 0,
    ):
        """
        Creates a new sticker counts with the given fields.
        
        Parameters
        ----------
        animated : `int` = `0`, Optional (Keyword only)
            Animated sticker count.
        lottie : `int` = `0`, Optional (Keyword only)
            Lottie sticker count.
        static : `int` = `0`, Optional (Keyword only)
            Static sticker count.
        """
        self = object.__new__(cls)
        self.animated = animated
        self.lottie = lottie
        self.static = static
        return self
    
    
    @classmethod
    def from_stickers(cls, iterator):
        """
        Creates a new sticker counts instance from the iterable.
        
        Parameters
        ----------
        iterator : `iterable` of ``Sticker``
            Sticker iterator.
        
        Returns
        -------
        self : `instance<cls>`
        """
        animated = 0
        lottie = 0
        static = 0
        
        for sticker in iterator:
            sticker_format = sticker.format
            if sticker_format is STICKER_FORMAT_ANIMATED:
                animated += 1
                continue
            
            if sticker_format is STICKER_FORMAT_LOTTIE:
                lottie += 1
                continue
            
            if sticker_format is STICKER_FORMAT_STATIC:
                static += 1
                continue
        
        
        self = object.__new__(cls)
        self.animated = animated
        self.lottie = lottie
        self.static = static
        return self
    
    
    @property
    def normal_total(self):
        """
        Returns the total amount of normal stickers.
        
        Returns
        -------
        normal_total : `int`
        """
        return self.animated + self.static
    
    @property
    def total(self):
        """
        Returns the total count of stickers.
        
        Returns
        -------
        total : `int`
        """
        return self.lottie + self.static + self.animated
    
    
    def _iter_field_values(self):
        """
        Iterates over the fields of the sticker counts.
        
        This method is an iterable generator.
        
        Yields
        ------
        field_value : `int`
        """
        yield self.animated
        yield self.lottie
        yield self.static
    
    
    def __bool__(self):
        """Returns whether the sticker counts counted any stickers"""
        for field_value in self._iter_field_values():
            if field_value:
                return True
        
        return False
    
    
    def __repr__(self):
        """Returns the sticker counts' representation"""
        repr_parts = [self.__class__.__name__, '(']
        field_added = False
        
        for field_name, field_value in zip(self.__slots__, self._iter_field_values()):
            if field_value:
                if field_added:
                    repr_parts.append(', ')
                else:
                    field_added = True
                
                repr_parts.append(field_name)
                repr_parts.append(' = ')
                repr_parts.append(repr(field_value))
        
        repr_parts.append(')')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two sticker counts equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        for self_field, other_field in zip(self._iter_field_values(), other._iter_field_values()):
            if self_field != other_field:
                return False
        
        return True
    
    
    def __hash__(self):
        """Returns the sticker counts' hash value."""
        hash_value = 0
        
        shift = 0
        
        for field_value in self._iter_field_values():
            hash_value ^= field_value << shift
            shift += 4
        
        return hash_value
    
    
    def __iter__(self):
        """Deprecated and will be removed in 2023 April."""
        warnings.warn(
            (
                f'Unpacking `Guild.sticker_counts` is deprecated and will be removed in 2023 April.\n'
                f'Please do the following instead:\n'
                f'sticker_counts = guild.sticker_counts\n'
                f'animated = sticker_counts.animated\n'
                f'lottie = sticker_counts.lottie\n'
                f'static = sticker_counts.static'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        yield self.static
        yield self.animated
        yield self.lottie
