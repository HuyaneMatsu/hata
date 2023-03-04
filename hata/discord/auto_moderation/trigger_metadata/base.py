__all__ = ('AutoModerationRuleTriggerMetadataBase', )

from scarletio import RichAttributeErrorBaseType

from ...bases import PlaceHolder


class AutoModerationRuleTriggerMetadataBase(RichAttributeErrorBaseType):
    """
    Base class for ``AutoModerationRule``'s trigger metadata.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new trigger metadata instance.
        """
        return object.__new__(cls)
        
    def __repr__(self):
        """Returns the trigger metadata's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new auto moderation rule trigger metadata instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Auto moderation rule trigger metadata payload.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return object.__new__(cls)
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the trigger metadata to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        return {}
    
    
    def __eq__(self, other):
        """Returns whether the two trigger metadatas are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the trigger metadata's hash value."""
        return 0
    
    
    def copy(self):
        """
        Copies the trigger metadata.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return object.__new__(type(self))
    
    
    def copy_with(self):
        """
        Copies the trigger metadata with altering it's attributes based on the given fields.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return self.copy()
    
    
    # ---- Place holders ----
    
    excluded_keywords = PlaceHolder(
        None,
        """
        Excluded keywords from under the rule.
        
        Returns
        -------
        excluded_keywords : `None`, `tuple` of `str`
        """
    )
    
    
    keyword_presets = PlaceHolder(
        None,
        """
        Keyword preset defined by Discord which will be searched for in content.
        
        Returns
        -------
        keyword_presets : `None`, `tuple` of ``AutoModerationKeywordPresetType``
        """
    )
    
    
    keywords = PlaceHolder(
        None,
        """
        Substrings which will be searched for in content.
        
        Returns
        -------
        keywords : `None`, `tuple` of `str`
        """
    )
    mention_limit = PlaceHolder(
        0,
        """
        The amount of mentions in a message after the rule is triggered.
        
        Returns
        -------
        mention_limit : `int`
        """
    )
    
    raid_protection = PlaceHolder(
        False,
        """
        Whether mention raid protection is enabled.
        
        Returns
        -------
        raid_protection : `bool`
        """
    )
    
    
    regex_patterns = PlaceHolder(
        None,
        """
        Regular expression patterns which are matched against content.
        
        Returns
        -------
        regex_patterns : `None`, `tuple` of `str`
        """
    )
    
    
    
    # ---- Extra utility ----
    
    def iter_excluded_keywords(self):
        """
        Iterates over the excluded keyword of the keyword trigger metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        excluded_keyword : `str`
        """
        excluded_keywords = self.excluded_keywords
        if (excluded_keywords is not None):
            yield from excluded_keywords
    
    
    def iter_keyword_presets(self):
        """
        Iterates over the keyword presets of the keyword trigger metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        keyword_preset : `AutoModerationKeywordPresetType`
        """
        keyword_presets = self.keyword_presets
        if (keyword_presets is not None):
            yield from keyword_presets

    
    def iter_keywords(self):
        """
        Iterates over the keywords of the keyword trigger metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        keyword : `str`
        """
        keywords = self.keywords
        if (keywords is not None):
            yield from keywords
    
    
    def iter_regex_patterns(self):
        """
        Iterates over the regex patterns of the keyword trigger metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        regex_patterns : `str`
        """
        regex_patterns = self.regex_patterns
        if (regex_patterns is not None):
            yield from regex_patterns
