__all__ = ()

from datetime import datetime as DateTime

from ...channel import Channel
from ...embed import EmbedType
from ...field_parsers import (
    bool_parser_factory, entity_id_array_parser_factory, int_parser_factory, nullable_array_parser_factory,
    nullable_string_parser_factory, preinstanced_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, int_optional_putter_factory, nullable_string_array_optional_putter_factory,
    nullable_string_optional_putter_factory, optional_entity_id_array_optional_putter_factory,
    preinstanced_array_optional_putter_factory, preinstanced_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_array_validator_factory, int_conditional_validator_factory,
    nullable_string_array_validator_factory, nullable_string_validator_factory, preinstanced_array_validator_factory,
    preinstanced_validator_factory
)
from ...user import ClientUserBase, UserBase
from ...utils import DISCORD_EPOCH_START, datetime_to_id, id_to_datetime

from .constants import (
    CONTENT_LENGTH_MAX, LIMIT_DEFAULT, LIMIT_MAX, LIMIT_MIN, OFFSET_DEFAULT, OFFSET_MAX, OFFSET_MIN, SLOP_DEFAULT,
    SLOP_MAX, SLOP_MIN
)
from .preinstanced import (
    MessageSearchAuthorType, MessageSearchHasType, MessageSearchSortByType, MessageSearchSortOrderType
)


# after

def parse_after(data):
    """
    Parses the after from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    after : `None | DateTime`
    """
    value = data.get('min_id', None)
    if (value is not None) and value:
        return id_to_datetime(value)


def put_after(after, data, defaults):
    """
    Puts the activity timestamps after into the given data.
    
    Parameters
    ----------
    after : `None | DateTime`
        Value to serialise.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (after is not None):
        if (after is None):
            after = 0
        else:
            after = datetime_to_id(after)
        
        data['min_id'] = after
    
    return data


def validate_after(after):
    """
    Validates the given after value.
    
    Parameters
    ----------
    after : `None | DateTime`
        The value to validate.
    
    Returns
    -------
    after : `None | DateTime`
    """
    if (after is None):
        return None
    
    if isinstance(after, DateTime):
        if after <= DISCORD_EPOCH_START:
            return None
        
        return after
    
    raise TypeError(
        f'`after` can be `None | DateTime`, got {type(after).__name__}; {after!r}.'
    )


# attachment_extensions

parse_attachment_extensions = nullable_array_parser_factory('attachment_extension')
put_attachment_extensions = nullable_string_array_optional_putter_factory('attachment_extension')
validate_attachment_extensions = nullable_string_array_validator_factory('attachment_extensions')


# attachment_names

parse_attachment_names = nullable_array_parser_factory('attachment_filename')
put_attachment_names = nullable_string_array_optional_putter_factory('attachment_filename')
validate_attachment_names = nullable_string_array_validator_factory('attachment_names')


# author_ids

parse_author_ids = entity_id_array_parser_factory('author_id')
put_author_ids = optional_entity_id_array_optional_putter_factory('author_id')
validate_author_ids = entity_id_array_validator_factory('author_ids', UserBase)


# author_types

parse_author_types = preinstanced_array_parser_factory('author_type', MessageSearchAuthorType)
put_author_types = preinstanced_array_optional_putter_factory('author_type')
validate_author_types = preinstanced_array_validator_factory('author_types', MessageSearchAuthorType)


# before

def parse_before(data):
    """
    Parses the before from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    before : `None | DateTime`
    """
    value = data.get('max_id', None)
    if (value is not None):
        return id_to_datetime(value)


def put_before(before, data, defaults):
    """
    Puts the activity timestamps before into the given data.
    
    Parameters
    ----------
    before : `None | DateTime`
        Value to serialise.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (before is not None):
        if (before is None):
            before = 0
        else:
            before = datetime_to_id(before)
        
        data['max_id'] = before
    
    return data


def validate_before(before):
    """
    Validates the given before value.
    
    Parameters
    ----------
    before : `None | DateTime`
        The value to validate.
    
    Returns
    -------
    before : `None | DateTime`
    """
    if (before is None):
        return None
    
    if isinstance(before, DateTime):
        if before < DISCORD_EPOCH_START:
            return DISCORD_EPOCH_START
        
        return before
    
    raise TypeError(
        f'`before` can be `None | DateTime`, got {type(before).__name__}; {before!r}.'
    )


# channel_ids

parse_channel_ids = entity_id_array_parser_factory('channel_id')
put_channel_ids = optional_entity_id_array_optional_putter_factory('channel_id')
validate_channel_ids = entity_id_array_validator_factory('channel_ids', Channel)


# content

parse_content = nullable_string_parser_factory('content')
put_content = nullable_string_optional_putter_factory('content')
validate_content = nullable_string_validator_factory('content', 0, CONTENT_LENGTH_MAX)


# embed_providers

parse_embed_providers = nullable_array_parser_factory('embed_provider')
put_embed_providers = nullable_string_array_optional_putter_factory('embed_provider')
validate_embed_providers = nullable_string_array_validator_factory('embed_providers')


# embed_types

parse_embed_types = preinstanced_array_parser_factory('embed_type', EmbedType)
put_embed_types = preinstanced_array_optional_putter_factory('embed_type')
validate_embed_types = preinstanced_array_validator_factory('embed_types', EmbedType)


# has_types

parse_has_types = preinstanced_array_parser_factory('has', MessageSearchHasType)
put_has_types = preinstanced_array_optional_putter_factory('has')
validate_has_types = preinstanced_array_validator_factory('has_types', MessageSearchHasType)


# include_nsfw_channels

parse_include_nsfw_channels = bool_parser_factory('include_nsfw', False)
put_include_nsfw_channels = bool_optional_putter_factory('include_nsfw', False)
validate_include_nsfw_channels = bool_validator_factory('include_nsfw_channels', False)


# limit

parse_limit = int_parser_factory('limit', LIMIT_DEFAULT)
put_limit = int_optional_putter_factory('limit', LIMIT_DEFAULT)
validate_limit = int_conditional_validator_factory(
    'limit',
    LIMIT_DEFAULT,
    (lambda limit : (limit >= LIMIT_MIN) and (limit <= LIMIT_MAX)),
    f'>= {LIMIT_MIN!s} and <= {LIMIT_MAX!s}',
)


# mentioned_everyone

parse_mentioned_everyone = bool_parser_factory('mention_everyone', False)
put_mentioned_everyone = bool_optional_putter_factory('mention_everyone', False)
validate_mentioned_everyone = bool_validator_factory('mention_everyone', False)


# mentioned_user_ids

parse_mentioned_user_ids = entity_id_array_parser_factory('mentions')
put_mentioned_user_ids = optional_entity_id_array_optional_putter_factory('mentions')
validate_mentioned_user_ids = entity_id_array_validator_factory('mentioned_user_ids', ClientUserBase)


# offset

parse_offset = int_parser_factory('offset', OFFSET_DEFAULT)
put_offset = int_optional_putter_factory('offset', OFFSET_DEFAULT)
validate_offset = int_conditional_validator_factory(
    'offset',
    OFFSET_DEFAULT,
    (lambda offset : (offset >= OFFSET_MIN) and (offset <= OFFSET_MAX)),
    f'>= {OFFSET_MIN!s} and <= {OFFSET_MAX!s}',
)


# pinned

parse_pinned = bool_parser_factory('pinned', False)
put_pinned = bool_optional_putter_factory('pinned', False)
validate_pinned = bool_validator_factory('pinned', False)


# slop

parse_slop = int_parser_factory('slop', SLOP_DEFAULT)
put_slop = int_optional_putter_factory('slop', SLOP_DEFAULT)
validate_slop = int_conditional_validator_factory(
    'slop',
    SLOP_DEFAULT,
    (lambda slop : (slop >= SLOP_MIN) and (slop <= SLOP_MAX)),
    f'>= {SLOP_MIN!s} and <= {SLOP_MAX!s}',
)


# sort_by

parse_sort_by = preinstanced_parser_factory('sort_by', MessageSearchSortByType, MessageSearchSortByType.creation)
put_sort_by = preinstanced_optional_putter_factory('sort_by', MessageSearchSortByType.creation)
validate_sort_by = preinstanced_validator_factory('sort_by', MessageSearchSortByType)


# sort_order

parse_sort_order = preinstanced_parser_factory(
    'sort_order', MessageSearchSortOrderType, MessageSearchSortOrderType.descending
)
put_sort_order = preinstanced_optional_putter_factory('sort_order', MessageSearchSortOrderType.descending)
validate_sort_order = preinstanced_validator_factory('sort_order', MessageSearchSortOrderType)


# url_host_names

parse_url_host_names = nullable_array_parser_factory('link_hostname')
put_url_host_names = nullable_string_array_optional_putter_factory('link_hostname')
validate_url_host_names = nullable_string_array_validator_factory('url_host_names')
