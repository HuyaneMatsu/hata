__all__ = ()

VARIATION_SELECTOR_16_POSTFIX = '_vr16'


class Unicode:
    """
    Represents a raw unicode emoji. These objects are further processed on the line.
    
    Attributes
    ----------
    aliases : `None`, `tuple` of `str`
        Alternative names of the emoji.
    emoticons : `None`, `tuple` of `str`
        Emoticons which the emoji represents.
    name : `str`
        The unicode's name.
    value : `str`
        Unicode value.
    variation_selector_16 : `bool`
        Whether the emoji is a variation selector 16 emoji.
    """
    __slots__ = ('aliases', 'emoticons', 'name', 'value', 'variation_selector_16')
    
    def __new__(cls, name, raw_value, variation_selector_16, aliases, emoticons):
        """
        Creates a new unicode.
        
        Parameters
        ----------
        name : `str`
            The unicode's name.
        raw_value : `bytes`
            Binary unicode value.
        variation_selector_16 : `bool`
            Whether the emoji is a variation selector 16 emoji.
        aliases : `None`, `tuple` of `str`
            Alternative names of the emoji.
        emoticons : `None`, `tuple` of `str`
            Emoticons which the emoji represents.
        """
        value = raw_value.decode('utf8')
        
        self = object.__new__(cls)
        
        self.aliases = aliases
        self.emoticons = emoticons
        self.name = name
        self.value = value
        self.variation_selector_16 = variation_selector_16
        
        return self
    
    
    def __repr__(self):
        """Returns the unicode's representation."""
        return f'<{self.__class__.__name__} name={self.name!r}>'
    
    
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
