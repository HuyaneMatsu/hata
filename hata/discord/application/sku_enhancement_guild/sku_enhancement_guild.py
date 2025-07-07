__all__ = ('SKUEnhancementGuild',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_additional_emoji_slots, parse_additional_soundboard_sound_slots, parse_additional_sticker_slots,
    parse_features, put_additional_emoji_slots, put_additional_soundboard_sound_slots, put_additional_sticker_slots,
    put_features, validate_additional_emoji_slots, validate_additional_soundboard_sound_slots,
    validate_additional_sticker_slots, validate_features
)


class SKUEnhancementGuild(RichAttributeErrorBaseType):
    """
    Represents an applied enhancements to a guild of an SKU.
    
    Attributes
    ----------
    additional_emoji_slots : `int`
        Additional granted emoji slots by the enhancement.
    
    additional_soundboard_sound_slots : `int`
        Additionally granted soundboard sound slots by the enhancement.
    
    additional_sticker_slots : `int`
        Additionally granted sticker by the enhancement.
    
    features : ``None | tuple<GuildFeature>``
        The granted features by the enhancement.
    """
    __slots__ = ('additional_emoji_slots', 'additional_soundboard_sound_slots', 'additional_sticker_slots', 'features')
    
    def __new__(
        cls,
        *,
        additional_emoji_slots = ...,
        additional_soundboard_sound_slots = ...,
        additional_sticker_slots = ...,
        features = ...,
    ):
        """
        Creates a new user SKU enhancement guild instance from the given parameters.
        
        Attributes
        ----------
        additional_emoji_slots : `None | int`, Optional (Keyword only)
            Additional granted emoji slots by the enhancement.
        
        additional_soundboard_sound_slots : `None | int`, Optional (Keyword only)
            Additionally granted soundboard sound slots by the enhancement.
        
        additional_sticker_slots : `None | int`, Optional (Keyword only)
            Additionally granted sticker by the enhancement.
        
        features : ``None | str | GuildFeature| iterable<str> | iterable<GuildFeature>``, Optional (Keyword only)
            The granted features by the enhancement.
            
        """
        # additional_emoji_slots
        if additional_emoji_slots is ...:
            additional_emoji_slots = 0
        else:
            additional_emoji_slots = validate_additional_emoji_slots(additional_emoji_slots)
        
        # additional_soundboard_sound_slots
        if additional_soundboard_sound_slots is ...:
            additional_soundboard_sound_slots = 0
        else:
            additional_soundboard_sound_slots = validate_additional_soundboard_sound_slots(additional_soundboard_sound_slots)
        
        # additional_sticker_slots
        if additional_sticker_slots is ...:
            additional_sticker_slots = 0
        else:
            additional_sticker_slots = validate_additional_sticker_slots(additional_sticker_slots)
        
        # features
        if features is ...:
            features = None
        else:
            features = validate_features(features)
        
        # Construct
        self = object.__new__(cls)
        self.additional_emoji_slots = additional_emoji_slots
        self.additional_soundboard_sound_slots = additional_soundboard_sound_slots
        self.additional_sticker_slots = additional_sticker_slots
        self.features = features
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        # additional_emoji_slots
        additional_emoji_slots = self.additional_emoji_slots
        if additional_emoji_slots:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' additional_emoji_slots = ')
            repr_parts.append(repr(additional_emoji_slots))
        
        # additional_soundboard_sound_slots
        additional_soundboard_sound_slots = self.additional_soundboard_sound_slots
        if additional_soundboard_sound_slots:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' additional_soundboard_sound_slots = ')
            repr_parts.append(repr(additional_soundboard_sound_slots))
        
        # additional_sticker_slots
        additional_sticker_slots = self.additional_sticker_slots
        if additional_sticker_slots:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' additional_sticker_slots = ')
            repr_parts.append(repr(additional_sticker_slots))
        
        # features
        features = self.features
        if (features is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' features = ')
            repr(features)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # additional_emoji_slots
        hash_value ^= self.additional_emoji_slots
        
        # additional_soundboard_sound_slots
        hash_value ^= self.additional_soundboard_sound_slots << 8
        
        # additional_sticker_slots
        hash_value ^= self.additional_sticker_slots << 16
        
        # features
        features = self.features
        if (features is not None):
            hash_value ^= hash(features)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # additional_emoji_slots
        if self.additional_emoji_slots != other.additional_emoji_slots:
            return False
        
        # additional_soundboard_sound_slots
        if self.additional_soundboard_sound_slots != other.additional_soundboard_sound_slots:
            return False
        
        # additional_sticker_slots
        if self.additional_sticker_slots != other.additional_sticker_slots:
            return False
        
        # features
        if self.features != other.features:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a SKU enhancement guild from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received SKU enhancement guild data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.additional_emoji_slots = parse_additional_emoji_slots(data)
        self.additional_soundboard_sound_slots = parse_additional_soundboard_sound_slots(data)
        self.additional_sticker_slots = parse_additional_sticker_slots(data)
        self.features = parse_features(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serializes the SKU enhancement guild to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_additional_emoji_slots(self.additional_emoji_slots, data, defaults)
        put_additional_soundboard_sound_slots(self.additional_soundboard_sound_slots, data, defaults)
        put_additional_sticker_slots(self.additional_sticker_slots, data, defaults)
        put_features(self.features, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the SKU enhancement guild.
        
        Returns
        -------
        new : `instance<type<self>>
        """
        new = object.__new__(type(self))
        new.additional_emoji_slots = self.additional_emoji_slots
        new.additional_soundboard_sound_slots = self.additional_soundboard_sound_slots
        new.additional_sticker_slots = self.additional_sticker_slots
        new.features = self.features
        return new
    
    
    def copy_with(
        self, 
        *,
        additional_emoji_slots = ...,
        additional_soundboard_sound_slots = ...,
        additional_sticker_slots = ...,
        features = ...,
    ):
        """
        Copies the SKU enhancement guild with the given fields.
        
        Parameters
        ----------
        additional_emoji_slots : `None | int`, Optional (Keyword only)
            Additional granted emoji slots by the enhancement.
        
        additional_soundboard_sound_slots : `None | int`, Optional (Keyword only)
            Additionally granted soundboard sound slots by the enhancement.
        
        additional_sticker_slots : `None | int`, Optional (Keyword only)
            Additionally granted sticker by the enhancement.
        
        features : ``None | str | GuildFeature| iterable<str> | iterable<GuildFeature>``, Optional (Keyword only)
            The granted features by the enhancement.
        
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
        # additional_emoji_slots
        if additional_emoji_slots is ...:
            additional_emoji_slots = self.additional_emoji_slots
        else:
            additional_emoji_slots = validate_additional_emoji_slots(additional_emoji_slots)
        
        # additional_soundboard_sound_slots
        if additional_soundboard_sound_slots is ...:
            additional_soundboard_sound_slots = self.additional_soundboard_sound_slots
        else:
            additional_soundboard_sound_slots = validate_additional_soundboard_sound_slots(additional_soundboard_sound_slots)
        
        # additional_sticker_slots
        if additional_sticker_slots is ...:
            additional_sticker_slots = self.additional_sticker_slots
        else:
            additional_sticker_slots = validate_additional_sticker_slots(additional_sticker_slots)
        
        # features
        if features is ...:
            features = self.features
        else:
            features = validate_features(features)
        
        # Construct
        new = object.__new__(type(self))
        new.additional_emoji_slots = additional_emoji_slots
        new.additional_soundboard_sound_slots = additional_soundboard_sound_slots
        new.additional_sticker_slots = additional_sticker_slots
        new.features = features
        return new
    
    
    def iter_features(self):
        """
        Iterates over the features granted by the enhancement.
        
        This method is an iterable generator.
        
        Yields
        ------
        feature : ``GuildFeature``
        """
        features = self.features
        if (features is not None):
            yield from features
    
    
    def has_feature(self, feature):
        """
        Returns whether the enhancement grants the given feature.
        
        Parameters
        ----------
        feature : ``GuildFeature``
            The feature to look for.
        
        Returns
        -------
        has_feature : `bool`
        """
        features = self.features
        if features is None:
            return False
        
        return feature in features
    
    
