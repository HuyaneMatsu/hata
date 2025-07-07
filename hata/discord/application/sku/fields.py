__all__ = ()

from functools import partial as partial_func

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, flag_parser_factory, nullable_date_time_parser_factory,
    nullable_entity_parser_factory, nullable_string_parser_factory, preinstanced_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_putter_factory, flag_optional_putter_factory,
    nullable_date_time_optional_putter_factory, nullable_entity_optional_putter_factory,
    preinstanced_array_putter_factory, preinstanced_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, flag_validator_factory, force_string_validator_factory,
    nullable_date_time_validator_factory, nullable_entity_validator_factory, preinstanced_array_validator_factory,
    preinstanced_validator_factory, url_optional_validator_factory
)
from ...localization.helpers import localized_dictionary_builder
from ...localization.utils import build_locale_dictionary, destroy_locale_dictionary

from ..application import Application
from ..sku_enhancement import SKUEnhancement

from .constants import NAME_LENGTH_MAX, NAME_LENGTH_MIN
from .flags import SKUFlag
from .preinstanced import SKUAccessType, SKUFeature, SKUProductFamily, SKUType


# access_type

parse_access_type = preinstanced_parser_factory('access_type', SKUAccessType, SKUAccessType.none)
put_access_type = preinstanced_putter_factory('access_type')
validate_access_type = preinstanced_validator_factory('access_type', SKUAccessType)

# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id = entity_id_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', Application)

# dependent_sku_id

parse_dependent_sku_id = entity_id_parser_factory('dependent_sku_id')
put_dependent_sku_id = entity_id_putter_factory('dependent_sku_id')
validate_dependent_sku_id = entity_id_validator_factory('dependent_sku_id', NotImplemented, include = 'SKU')


# enhancement

parse_enhancement = nullable_entity_parser_factory('powerup_metadata', SKUEnhancement)
put_enhancement = nullable_entity_optional_putter_factory('powerup_metadata', SKUEnhancement)
validate_enhancement = nullable_entity_validator_factory('enhancement', SKUEnhancement)


# features

parse_features = preinstanced_array_parser_factory('features', SKUFeature)
put_features = preinstanced_array_putter_factory('features')
validate_features = preinstanced_array_validator_factory('features', SKUFeature)

# flags

parse_flags = flag_parser_factory('flags', SKUFlag)
put_flags = flag_optional_putter_factory('flags', SKUFlag())
validate_flags = flag_validator_factory('flags', SKUFlag)

# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('sku_id')


# name

def parse_name(data):
    """
    Parses a name out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    name : `str`
    """
    name_data = data.get('name', None)
    if name_data is None:
        return ''
    
    if isinstance(name_data, dict):
        default = name_data.get('default', None)
        if default is None:
            return ''
        
        return default
    
    if isinstance(name_data, str):
        return name_data
    
    return ''


def put_name(name, data, defaults):
    """
    Serializes the name value into the given data.
    
    Parameters
    ----------
    name : `str`
        The value to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    try:
        name_data = data['name']
    except KeyError:
        name_data = data['name'] = {}
    
    name_data['default'] = name
    return data


validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)


# name_localizations


def parse_name_localizations(data):
    """
    Parses name localizations out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    name_localizations : ``None | dict<<Locale, str>``
    """
    name_data = data.get('name', None)
    if name_data is None:
        return None
    
    if isinstance(name_data, dict):
        return build_locale_dictionary(name_data.get('localizations', None))
    
    return None


def put_name_localizations(name_localizations, data, defaults):
    """
    Serializes the name localizations value into the given data.
    
    Parameters
    ----------
    name_localizations : ``None | dict<Locale, str>``
        The value to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (name_localizations is not None):
        try:
            name_localizations_data = data['name']
        except KeyError:
            name_localizations_data = data['name'] = {}
        
        name_localizations_data['localizations'] = destroy_locale_dictionary(name_localizations)
    
    return data


validate_name_localizations = partial_func(
    localized_dictionary_builder, parameter_name = 'name_localizations'
)


# premium

parse_premium = bool_parser_factory('premium', False)
put_premium = bool_optional_putter_factory('premium', False)
validate_premium = bool_validator_factory('premium', False)


# product_family

parse_product_family = preinstanced_parser_factory('product_line', SKUProductFamily, SKUProductFamily.none)
put_product_family = preinstanced_putter_factory('product_line')
validate_product_family = preinstanced_validator_factory('product_family', SKUProductFamily)


# release_at

parse_release_at = nullable_date_time_parser_factory('release_date')
put_release_at = nullable_date_time_optional_putter_factory('release_date')
validate_release_at = nullable_date_time_validator_factory('release_at')

# slug

parse_slug = nullable_string_parser_factory('slug')
put_slug = url_optional_putter_factory('slug')
validate_slug = url_optional_validator_factory('slug')

# type

parse_type = preinstanced_parser_factory('type', SKUType, SKUType.none)
put_type = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('sku_type', SKUType)
