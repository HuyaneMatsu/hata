__all__ = ()

from ...field_parsers import bool_parser_factory, default_entity_parser_factory, nullable_string_parser_factory
from ...field_putters import (
    bool_optional_putter_factory, entity_putter_factory, nullable_string_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_validator_factory, nullable_string_validator_factory
)

from ..media_info import MediaInfo

from .constants import DESCRIPTION_LENGTH_MAX, DESCRIPTION_LENGTH_MIN


# description

parse_description = nullable_string_parser_factory('description')
put_description = nullable_string_optional_putter_factory('description')
validate_description = nullable_string_validator_factory(
    'description', DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX
)


# media

parse_media = default_entity_parser_factory('media', MediaInfo, default_factory = MediaInfo._create_empty)
put_media = entity_putter_factory('media', MediaInfo)


def validate_media(media):
    """
    Validates whether the given media is correct type.
    
    Parameters
    ----------
    media : ``str | MediaInfo``
        The media to validate.
    
    Returns
    -------
    media : ``MediaInfo``
    
    Raises
    ------
    TypeError
        - If `media` is given as an invalid type.
    """
    if isinstance(media, str):
        return MediaInfo(media)
    
    if isinstance(media, MediaInfo):
        return media
    
    raise TypeError(
        f'`media` can be `str | {MediaInfo.__name__}`, got {type(media).__name__}, {media!r}.'
    )


# spoiler

parse_spoiler = bool_parser_factory('spoiler', False)
put_spoiler = bool_optional_putter_factory('spoiler', False)
validate_spoiler = bool_validator_factory('spoiler', False)
