__all__ = ()

from scarletio import RichAttributeErrorBaseType, export


VARIATION_SELECTOR_16_POSTFIX = '_vr16'


@export
class Unicode(RichAttributeErrorBaseType):
    """
    Represents a raw unicode emoji. These objects are further processed on the line.
    
    Attributes
    ----------
    aliases : `None | tuple<str>`
        Alternative names of the emoji.
    emoticons : `None | tuple<str>`
        Emoticons which the emoji represents.
    name : `str`
        The unicode's name.
    value : `str`
        Unicode value.
    variation_selector_16 : `bool`
        Whether the emoji is a variation selector 16 emoji.
    unicode_aliases : `None | tuple<str>`
        Alternative unicode strings representing the same unicode.
        These are required because some shitty systems store 32 bit characters as 2 16 bit code point parses.
    """
    __slots__ = ('aliases', 'emoticons', 'name', 'value', 'variation_selector_16', 'unicode_aliases')
    
    def __new__(cls, name, value, variation_selector_16, aliases, emoticons, unicode_aliases):
        """
        Creates a new unicode.
        
        Parameters
        ----------
        name : `str`
            The unicode's name.
        value : `str`
            Unicode value.
        variation_selector_16 : `bool`
            Whether the emoji is a variation selector 16 emoji.
        aliases : `None | tuple<str>`
            Alternative names of the emoji.
        emoticons : `None | tuple<str>`
            Emoticons which the emoji represents.
        unicode_aliases : `None | tuple<str>`
            Alternative unicode strings representing the same unicode.
        """
        self = object.__new__(cls)
        
        self.aliases = aliases
        self.emoticons = emoticons
        self.name = name
        self.value = value
        self.variation_selector_16 = variation_selector_16
        self.unicode_aliases = unicode_aliases
        
        return self
    
    
    def __repr__(self):
        """Returns the unicode's representation."""
        return f'<{self.__class__.__name__} name = {self.name!r}>'
    
    
    def get_system_name(self):
        """
        Returns the unicode's system name.
        
        Returns
        -------
        system_name : `str`
        """
        system_name = self.name
        
        if self.variation_selector_16:
            system_name += VARIATION_SELECTOR_16_POSTFIX
        
        return system_name
    
    
    def iter_emoticons(self):
        """
        Iterates over the unicode's emoticons.
        
        This method is an iterable generator.
        
        Yields
        ------
        emoticon : `str`
        """
        emoticons = self.emoticons
        if (emoticons is not None):
            yield from emoticons
    
    
    def iter_aliases(self):
        """
        Iterates over the unicode's aliases.
        
        This method is an iterable generator.
        
        Yields
        ------
        alias : `str`
        """
        aliases = self.aliases
        if (aliases is not None):
            yield from aliases
        
    
    def iter_alternative_names(self):
        """
        Iterates over the unicode's alternative names. Includes emoticons and aliases.
        
        This method is an iterable generator
        
        Yields
        ------
        alternative_name : `str`
        """
        yield from self.iter_emoticons()
        yield from self.iter_aliases()
    
    
    def iter_unicode_aliases(self):
        """
        Iterates over the unicode's unicode aliases.
        
        This method is an iterable generator.
        
        Yields
        ------
        unicode_alias : `str`
        """
        unicode_aliases = self.unicode_aliases
        if (unicode_aliases is not None):
            yield from unicode_aliases
