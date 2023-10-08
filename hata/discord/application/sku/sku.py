__all__ = ('SKU',)

from scarletio import export

from ...bases import DiscordEntity
from ...core import SKUS
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_access_type, parse_application_id, parse_features, parse_flags, parse_id, parse_name, parse_premium,
    parse_release_at, parse_slug, parse_type, put_access_type_into, put_application_id_into, put_features_into,
    put_flags_into, put_id_into, put_name_into, put_premium_into, put_release_at_into, put_slug_into, put_type_into,
    validate_access_type, validate_application_id, validate_features, validate_flags, validate_id, validate_name,
    validate_premium, validate_release_at, validate_slug, validate_type
)
from .flags import SKUFlag
from .preinstanced import SKUAccessType, SKUType


PRECREATE_FIELDS = {
    'access_type': ('access_type', validate_access_type),
    'application': ('application_id', validate_application_id),
    'application_id': ('application_id', validate_application_id),
    'features': ('features', validate_features),
    'flags': ('flags', validate_flags),
    'name': ('name', validate_name),
    'premium': ('premium', validate_premium),
    'release_at': ('release_at', validate_release_at),
    'slug': ('slug', validate_slug),
    'sku_type': ('type', validate_type),
}


@export
class SKU(DiscordEntity):
    """
    A stock keeping unit.
    
    Attributes
    ----------
    access_type : ``SKUAccessType``
        What kind of access the stock keeping unit provides for its content.
    
    application_id : `int`
        The stock keeping unit's owner application identifier.
    
    features : `None, tuple<SKUFeature>`
        The features of the stock keeping unit.
    
    flags : ``SKUFlag``
        The flags of the stock keeping unit.
    
    id : `int`
        The unique identifier number of the stock keeping unit.
    
    name : `str`
        The name of the stock keeping unit.
    
    premium : `bool`
        Whether the stock keeping unit is a premium one.
    
    release_at : `None`, `DateTime`
        When the stock keeping unit has its release.
        Can be both in the past and in the future as well.
    
    slug : `None`, `str`
        System generated url to the stock keeping unit generated based on its name.
    
    type : ``SKUType``
        The stock keeping unit's type.
    
    Notes
    -----
    Stock keeping unit instances are weakreferable.
    """
    __slots__ = (
        '__weakref__', 'access_type', 'application_id', 'features', 'flags', 'name', 'premium', 'release_at', 'slug',
        'type'
    )
    
    def __new__(
        cls,
        *,
        access_type = ...,
        features = ...,
        flags = ...,
        name = ...,
        premium = ...,
        release_at = ...,
        sku_type = ...,
    ):
        """
        Creates a new partial stock keeping unit.
        
        Parameters
        ----------
        access_type : ``SKUAccessType``, `int`, Optional (Keyword only)
            What kind of access the stock keeping unit provides for its content.
        
        features : `None`, `iterable<SKUFeature | int>`, `SKUFeature`, `int`, Optional (Keyword only)
            The features of the stock keeping unit.
        
        flags : ``SKUFlag``, `int`, Optional (Keyword only)
            The flags of the stock keeping unit.
        
        name : `str`, Optional (Keyword only)
            The name of the stock keeping unit.
        
        premium : `bool`, Optional (Keyword only)
            Whether the stock keeping unit is a premium one.
            
        release_at : `None`, `DateTime`, Optional (Keyword only)
            When the stock keeping unit has its release.
        
        sku_type : ``SKUType``, `int`, Optional (Keyword only)
            The stock keeping unit's type.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # access_type
        if access_type is ...:
            access_type = SKUAccessType.none
        else:
            access_type = validate_access_type(access_type)
        
        # features
        if features is ...:
            features = None
        else:
            features = validate_features(features)
        
        # flags
        if flags is ...:
            flags = SKUFlag()
        else:
            flags = validate_flags(flags)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # premium
        if premium is ...:
            premium = False
        else:
            premium = validate_premium(premium)
        
        # release_at
        if release_at is ...:
            release_at = None
        else:
            release_at = validate_release_at(release_at)
        
        # sku_type
        if sku_type is ...:
            sku_type = SKUType.none
        else:
            sku_type = validate_type(sku_type)
        
        # Construct
        self = object.__new__(cls)
        self.access_type = access_type
        self.application_id = 0
        self.features = features
        self.flags = flags
        self.id = 0
        self.name = name
        self.premium = premium
        self.release_at = release_at
        self.slug = None
        self.type = sku_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new stock keeping unit.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Stock keeping unit data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        sku_id = parse_id(data)
        try:
            self = SKUS[sku_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = sku_id
            self._set_attributes(data)
            SKUS[sku_id] = self
        else:
            self._set_attributes(data)
        
        return self
    
    def _set_attributes(self, data):
        """
        Sets the stock keeping unit's attributes. (Except `.id`.)
        
        Parameters
        ----------
        data : `dict<str, object>`
            Stock keeping unit data.
        """
        self.access_type = parse_access_type(data)
        self.application_id = parse_application_id(data)
        self.features = parse_features(data)
        self.flags = parse_flags(data)
        self.name = parse_name(data)
        self.premium = parse_premium(data)
        self.release_at = parse_release_at(data)
        self.slug = parse_slug(data)
        self.type = parse_type(data)
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the stock keeping unit into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        put_access_type_into(self.access_type, data, defaults)
        put_features_into(self.features, data, defaults)
        put_flags_into(self.flags, data, defaults)
        put_name_into(self.name, data, defaults)
        put_premium_into(self.premium, data, defaults)
        put_release_at_into(self.release_at, data, defaults)
        put_type_into(self.type, data, defaults)
        
        if include_internals:
            put_application_id_into(self.application_id, data, defaults)
            put_id_into(self.id, data, defaults)
            put_slug_into(self.slug, data, defaults)
        
        return data
    
    
    @classmethod
    def _create_empty(cls, sku_id):
        """
        Creates a new stock keeping unit instance with it's attribute set to their default values.
        
        Parameters
        ----------
        sku_id : `int`
            The stock keeping unit's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.access_type = SKUAccessType.none
        self.application_id = 0
        self.features = None
        self.flags = SKUFlag()
        self.id = sku_id
        self.name = ''
        self.premium = False
        self.release_at = None
        self.slug = None
        self.type = SKUType.none
        return self
    

    @classmethod
    def precreate(cls, sku_id, **keyword_parameters):
        """
        Creates an stock keeping unit instance.
        
        Parameters
        ----------
        sku_id : `int`
            The stock keeping unit's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        access_type : ``SKUAccessType``, `int`, Optional (Keyword only)
            What kind of access the stock keeping unit provides for its content.
        
        application : `int`, ``Application``, Optional (Keyword only)
            Alternative for `application_id`.
        
        application_id : `int`, ``Application``, Optional (Keyword only)
            The stock keeping unit's owner application identifier.
        
        features : `None`, `iterable<SKUFeature | int>`, `SKUFeature`, `int`, Optional (Keyword only)
            The features of the stock keeping unit.
        
        flags : ``SKUFlag``, `int`, Optional (Keyword only)
            The flags of the stock keeping unit.
        
        name : `str`, Optional (Keyword only)
            The stock keeping unit's name.
        
        premium : `bool`, Optional (Keyword only)
            Whether the stock keeping unit is a premium one.
            
        release_at : `None`, `DateTime`, Optional (Keyword only)
            When the stock keeping unit has its release.
        
        slug : `None`, `str`, Optional (Keyword only)
             System generated url to the stock keeping unit generated based on its name.
        
        sku_type : ``SKUType``, `int`, Optional (Keyword only)
            The stock keeping unit's type.
         
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
        sku_id = validate_id(sku_id)

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = SKUS[sku_id]
        except KeyError:
            self = cls._create_empty(sku_id)
            SKUS[sku_id] = self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def __repr__(self):
        """Returns the stock keeping unit's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        sku_id = self.id
        if sku_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two stock keeping units are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two stock keeping units are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self.id != other.id:
                return False
        
        # access_type
        if self.access_type is not other.access_type:
            return False
        
        # application_id -> ignore, internal
        
        # features
        if self.features != other.features:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # premium
        if self.premium != other.premium:
            return False
        
        # release_at
        if self.release_at != other.release_at:
            return False
        
        # slug -> ignore, internal
        
        # type
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the stock keeping unit."""
        sku_id = self.id
        if sku_id:
            return sku_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Calculates the stock keeping unit's hash based on their fields.
        
        This method is called by ``.__hash__`` if the channel has no ``.id`` set.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # access_type
        hash_value ^= self.access_type.value
        
        # application_id -> ignore, internal
        
        # features
        features = self.features
        if (features is not None):
            hash_value ^= hash(features)
        
        # flags
        hash_value ^= self.flags << 4
        
        # id -> ignore internal
        
        # name
        hash_value ^= hash(self.name)
        
        # premium
        hash_value ^= self.premium << 8
        
        # release_at
        release_at = self.release_at
        if (release_at is not None):
            hash_value ^= hash(release_at)
        
        # slug -> ignore, internal
        
        # type
        hash_value ^= self.type.value << 12
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the stock keeping unit.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.access_type = self.access_type
        new.application_id = 0
        features = self.features
        if (features is not None):
            features = (*features,)
        new.features = features
        new.flags = self.flags
        new.id = 0
        new.name = self.name
        new.premium = self.premium
        new.release_at = self.release_at
        new.slug = None
        new.type = self.type
        return new
    
    
    def copy_with(
        self,
        *,
        access_type = ...,
        features = ...,
        flags = ...,
        name = ...,
        premium = ...,
        release_at = ...,
        sku_type = ...,
    ):
        """
        Copies the stock keeping unit with the given fields.
        
        Parameters
        ----------
        access_type : ``SKUAccessType``, `int`, Optional (Keyword only)
            What kind of access the stock keeping unit provides for its content.
        
        features : `None`, `iterable<SKUFeature | int>`, `SKUFeature`, `int`, Optional (Keyword only)
            The features of the stock keeping unit.
        
        flags : ``SKUFlag``, `int`, Optional (Keyword only)
            The flags of the stock keeping unit.
        
        name : `str`, Optional (Keyword only)
            The stock keeping unit's name.
        
        premium : `bool`, Optional (Keyword only)
            Whether the stock keeping unit is a premium one.
            
        release_at : `None`, `DateTime`, Optional (Keyword only)
            When the stock keeping unit has its release.
        
        sku_type : ``SKUType``, `int`, Optional (Keyword only)
            The stock keeping unit's type.
        
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
        # access_type
        if access_type is ...:
            access_type = self.access_type
        else:
            access_type = validate_access_type(access_type)
        
        # features
        if features is ...:
            features = self.features
            if (features is not None):
                features = (*features,)
        else:
            features = validate_features(features)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # premium
        if premium is ...:
            premium = self.premium
        else:
            premium = validate_premium(premium)
        
        # release_at
        if release_at is ...:
            release_at = self.release_at
        else:
            release_at = validate_release_at(release_at)
        
        # sku_type
        if sku_type is ...:
            sku_type = self.type
        else:
            sku_type = validate_type(sku_type)
        
        # Construct
        new = object.__new__(type(self))
        new.access_type = access_type
        new.application_id = 0
        new.features = features
        new.flags = flags
        new.id = 0
        new.name = name
        new.premium = premium
        new.release_at = release_at
        new.slug = None
        new.type = sku_type
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether the stock keeping unit is partial.
        
        Returns
        -------
        partial : `bool
        """
        return (self.id == 0)
    
    
    def has_feature(self, feature):
        """
        Returns whether the stock keeping unit has the give feature.
        
        Parameters
        ----------
        feature : ``SKUFeature``
            The feature to look for.
        
        Returns
        -------
        has_feature : `bool`
        """
        features = self.features
        if features is None:
            return False
        
        return feature in features
    
    
    def iter_features(self):
        """
        Iterates over the features of the stock keeping unit.
        
        This method is an iterable generator.
        
        Yields
        ------
        feature : ``SKUFeature``
        """
        features = self.features
        if (features is not None):
            yield from features
