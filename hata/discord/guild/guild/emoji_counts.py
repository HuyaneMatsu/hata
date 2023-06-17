__all__ = ()

import warnings

from scarletio import RichAttributeErrorBaseType


class EmojiCounts(RichAttributeErrorBaseType):
    """
    Represents a guild's counted emojis by their type.
    
    Attributes
    ----------
    managed_animated : `int`
        Animated managed (by an outer integration) emoji count.
    managed_static : `int`
        Static managed (by an outer integration)  emoji count.
    normal_animated : `int`
        Animated emoji count of the guild (excludes managed and premium emojis).
    normal_static : `int`
        Static emoji count of the guild (excludes managed and premium emojis).
    premium_animated : `int`
        Animated premium emoji counts.
    premium_static : `int`
        Static premium emoji counts.
    
    Notes
    -----
    Use ``Guild.emoji_limit`` to get it's emoji limit. That emoji limit is applicable for normal emojis only.
    Premium emojis have their own limit of `25`.
    """
    __slots__ = (
        'managed_animated', 'managed_static', 'normal_animated', 'normal_static', 'premium_animated', 'premium_static'
    )
    
    def __new__(
        cls,
        *,
        managed_animated = 0,
        managed_static = 0,
        normal_animated = 0,
        normal_static = 0,
        premium_animated = 0,
        premium_static = 0,
    ):
        """
        Creates a new emoji counts with the given fields.
        
        Parameters
        ----------
        managed_animated : `int` = `0`, Optional (Keyword only)
            Animated managed (by an outer integration) emoji count.
        managed_static : `int` = `0`, Optional (Keyword only)
            Static managed (by an outer integration)  emoji count.
        normal_animated : `int` = `0`, Optional (Keyword only)
            Animated emoji count of the guild (excludes managed and premium emojis).
        normal_static : `int` = `0`, Optional (Keyword only)
            Static emoji count of the guild (excludes managed and premium emojis).
        premium_animated : `int` = `0`, Optional (Keyword only)
            Animated premium emoji counts.
        premium_static : `int` = `0`, Optional (Keyword only)
            Static premium emoji counts.
        """
        self = object.__new__(cls)
        self.managed_animated = managed_animated
        self.managed_static = managed_static
        self.normal_animated = normal_animated
        self.normal_static = normal_static
        self.premium_animated = premium_animated
        self.premium_static = premium_static
        return self
    
    
    @classmethod
    def from_emojis(cls, iterator):
        """
        Creates a new emoji counts instance from the iterable.
        
        Parameters
        ----------
        iterator : `iterable` of ``Emoji``
            Emoji iterator.
        
        Returns
        -------
        self : `instance<cls>`
        """
        normal_animated = 0
        normal_static = 0
        managed_animated = 0
        managed_static = 0
        premium_static = 0
        premium_animated = 0
        
        for emoji in iterator:
            if emoji.is_premium():
                if emoji.animated:
                    premium_animated += 1
                else:
                    premium_static += 1
                continue
            
            if emoji.managed:
                if emoji.animated:
                    managed_animated += 1
                else:
                    managed_static += 1
                continue
            
            if emoji.animated:
                normal_animated += 1
            else:
                normal_static += 1
            continue
        
        
        self = object.__new__(cls)
        self.managed_animated = managed_animated
        self.managed_static = managed_static
        self.normal_animated = normal_animated
        self.normal_static = normal_static
        self.premium_animated = premium_animated
        self.premium_static = premium_static
        return self
    
    
    @property
    def managed_total(self):
        """
        Returns the total amount of managed emojis.
        
        Returns
        -------
        managed_total : `int`
        """
        return self.managed_animated + self.managed_static
    
    
    @property
    def normal_total(self):
        """
        Returns the total amount of normal emojis.
        
        Returns
        -------
        normal_total : `int`
        """
        return self.normal_animated + self.normal_static
    
    
    @property
    def premium_total(self):
        """
        Returns the total amount of premium emojis.
        
        Returns
        -------
        premium_total : `int`
        """
        return self.premium_animated + self.premium_static
    
    
    @property
    def animated_total(self):
        """
        Returns the total amount of animated emojis.
        
        Returns
        -------
        animated_total : `int`
        """
        return self.managed_animated + self.normal_animated + self.premium_animated
    
    
    @property
    def static_total(self):
        """
        Returns the total amount static emojis.
        
        Returns
        -------
        static_total : `int`
        """
        return self.managed_static + self.normal_static + self.premium_static
    
    
    @property
    def total(self):
        """
        Returns the total count of emojis.
        
        Returns
        -------
        total : `int`
        """
        return (
            self.managed_animated +
            self.managed_static +
            self.normal_animated +
            self.normal_static +
            self.premium_animated +
            self.premium_static
        )
    
    
    def _iter_field_values(self):
        """
        Iterates over the fields of the emoji counts.
        
        This method is an iterable generator.
        
        Yields
        ------
        field_value : `int`
        """
        yield self.managed_animated
        yield self.managed_static
        yield self.normal_animated
        yield self.normal_static
        yield self.premium_animated
        yield self.premium_static
    
    
    def __bool__(self):
        """Returns whether the emoji counts counted any emojis"""
        for field_value in self._iter_field_values():
            if field_value:
                return True
        
        return False
    
    
    def __repr__(self):
        """Returns the emoji counts' representation"""
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
        """Returns whether the two emoji counts equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        for self_field, other_field in zip(self._iter_field_values(), other._iter_field_values()):
            if self_field != other_field:
                return False
        
        return True
    
    
    def __hash__(self):
        """Returns the emoji counts' hash value."""
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
                f'Unpacking `Guild.emoji_counts` is deprecated and will be removed in 2023 April.\n'
                f'Please do the following instead:\n'
                f'emoji_counts = guild.emoji_counts\n'
                f'normal_static = emoji_counts.normal_static\n'
                f'normal_animated = emoji_counts.normal_animated\n'
                f'managed_static = emoji_counts.managed_static\n'
                f'managed_animated = emoji_counts.managed_animated'
            ),
            FutureWarning,
            stacklevel = 2,
        )

        yield self.normal_static
        yield self.normal_animated
        yield self.managed_static
        yield self.managed_animated
