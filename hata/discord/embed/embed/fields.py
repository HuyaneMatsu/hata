__all__ = ()

from ...color import Color
from ...field_parsers import (
    nullable_date_time_parser_factory, nullable_entity_parser_factory, nullable_flag_parser_factory,
    nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    nullable_date_time_optional_putter_factory, nullable_entity_optional_putter_factory,
    nullable_flag_optional_putter_factory, nullable_string_optional_putter_factory, preinstanced_putter_factory,
    url_optional_putter_factory
)
from ...field_validators import (
    nullable_date_time_validator_factory, nullable_entity_validator_factory, nullable_flag_validator_factory,
    preinstanced_validator_factory, url_optional_validator_factory
)

from ..embed_author import EmbedAuthor
from ..embed_field import EmbedField
from ..embed_footer import EmbedFooter
from ..embed_image import EmbedImage
from ..embed_provider import EmbedProvider
from ..embed_thumbnail import EmbedThumbnail
from ..embed_video import EmbedVideo

from .constants import EMBED_DESCRIPTION_LENGTH_MAX, EMBED_TITLE_LENGTH_MAX
from .preinstanced import EmbedType

# author

parse_author = nullable_entity_parser_factory('author', EmbedAuthor)
put_author_into = nullable_entity_optional_putter_factory('author', EmbedAuthor)
validate_author = nullable_entity_validator_factory('author', EmbedAuthor)

# color

parse_color = nullable_flag_parser_factory('color', Color)
put_color_into = nullable_flag_optional_putter_factory('color')
validate_color = nullable_flag_validator_factory('color', Color)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_optional_putter_factory('description')


def validate_description(description):
    """
    Validates the given embed description.
    
    Parameters
    ----------
    description : `None`, `str`, `object`
        Embed author description.
    
    Returns
    -------
    description : `None`, `str`
    
    Raises
    ------
    TypeError
        - If `description`'s type is incorrect.
    ValueError
        - If `description`'s length is out of the expected range.
    """
    if description is None:
        return None
    
    if not isinstance(description, str):
        description = str(description)
    
    description_length = len(description)
    if description_length == 0:
        return None
    
    if description_length > EMBED_DESCRIPTION_LENGTH_MAX:
        raise ValueError(
            f'`description` length` must be <= {EMBED_DESCRIPTION_LENGTH_MAX}, '
            f'got {description_length}; description = {description!r}.'
        )
    
    return description


# fields

def parse_fields(data):
    """
    Parses the fields out from the given embed data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        User presence data.
    
    Returns
    -------
    fields : `None`, `list` of ``EmbedField``
    """
    field_datas = data.get('fields', None)
    if (field_datas is None) or (not field_datas):
        return None
    
    return [EmbedField.from_data(field_data) for field_data in field_datas]


def put_fields_into(fields, data, defaults):
    """
    Puts the given fields into the given data.
    
    Parameters
    ----------
    fields : `None`, `list` of ``EmbedField``
        Activities.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if defaults or (fields is not None):
        if fields is None:
            field_datas = []
        else:
            field_datas = [field.to_data(defaults = defaults) for field in fields]
        
        data['fields'] = field_datas
    
    return data


def validate_fields(fields):
    """
    Validates the given fields.
    
    Parameters
    ----------
    fields : `None`, `iterable` of ``EmbedField``
        The fields to validate.
    
    Returns
    -------
    fields : `None`, `list` of ``EmbedField``
    
    Raises
    ------
    TypeError
        - If `fields` type is incorrect.
    """
    if fields is None:
        return None
    
    if getattr(fields, '__iter__', None) is None:
        raise TypeError(
            f'`fields` can be `None`, `iterable` of `{EmbedField.__name__}`, got '
            f'{fields.__class__.__name__}; {fields!r}.'
        )
    
    fields_validated = None
    
    for field in fields:
        if not isinstance(field, EmbedField):
            raise TypeError(
                f'`fields` elements can be `{EmbedField.__name__}`, got '
                f'{field.__class__.__name__}; {field!r}; fields = {fields!r}'
            )
        
        if fields_validated is None:
            fields_validated = []
        
        fields_validated.append(field)
    
    return fields_validated


# footer

parse_footer = nullable_entity_parser_factory('footer', EmbedFooter)
put_footer_into = nullable_entity_optional_putter_factory('footer', EmbedFooter)
validate_footer = nullable_entity_validator_factory('footer', EmbedFooter)

# image

parse_image = nullable_entity_parser_factory('image', EmbedImage)
put_image_into = nullable_entity_optional_putter_factory('image', EmbedImage)
validate_image = nullable_entity_validator_factory('image', EmbedImage)

# provider

parse_provider = nullable_entity_parser_factory('provider', EmbedProvider)
put_provider_into = nullable_entity_optional_putter_factory('provider', EmbedProvider)
validate_provider = nullable_entity_validator_factory('provider', EmbedProvider)

# thumbnail

parse_thumbnail = nullable_entity_parser_factory('thumbnail', EmbedThumbnail)
put_thumbnail_into = nullable_entity_optional_putter_factory('thumbnail', EmbedThumbnail)
validate_thumbnail = nullable_entity_validator_factory('thumbnail', EmbedThumbnail)

# timestamp

parse_timestamp = nullable_date_time_parser_factory('timestamp')
put_timestamp_into = nullable_date_time_optional_putter_factory('timestamp')
validate_timestamp = nullable_date_time_validator_factory('timestamp')

# title

parse_title = nullable_string_parser_factory('title')
put_title_into = nullable_string_optional_putter_factory('title')


def validate_title(title):
    """
    Validates the given embed title.
    
    Parameters
    ----------
    title : `None`, `str`, `object`
        Embed author title.
    
    Returns
    -------
    title : `None`, `str`
    
    Raises
    ------
    TypeError
        - If `title`'s type is incorrect.
    ValueError
        - If `title`'s length is out of the expected range.
    """
    if title is None:
        return None
    
    if not isinstance(title, str):
        title = str(title)
    
    title_length = len(title)
    if title_length == 0:
        return None
    
    if title_length > EMBED_TITLE_LENGTH_MAX:
        raise ValueError(
            f'`title` length` must be <= {EMBED_TITLE_LENGTH_MAX}, '
            f'got {title_length}; title = {title!r}.'
        )
    
    return title

# type

parse_type = preinstanced_parser_factory('type', EmbedType, EmbedType.rich)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('embed_type', EmbedType)

# url

parse_url = nullable_string_parser_factory('url')
put_url_into = url_optional_putter_factory('url')
validate_url = url_optional_validator_factory('url')

# video

parse_video = nullable_entity_parser_factory('video', EmbedVideo)
put_video_into = nullable_entity_optional_putter_factory('video', EmbedVideo)
validate_video = nullable_entity_validator_factory('video', EmbedVideo)
