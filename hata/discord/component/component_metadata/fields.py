__all__ = ()

from scarletio import include

from ...application import SKU
from ...channel import Channel, ChannelType
from ...color import Color
from ...field_parsers import (
    bool_parser_factory, default_entity_parser_factory, entity_id_parser_factory, int_parser_factory,
    negated_bool_parser_factory, nullable_entity_parser_factory, nullable_flag_parser_factory,
    nullable_object_array_parser_factory, nullable_string_parser_factory, preinstanced_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_putter_factory, int_optional_putter_factory,
    negated_bool_optional_putter_factory, nullable_entity_array_putter_factory, nullable_entity_optional_putter_factory,
    nullable_flag_optional_putter_factory, nullable_string_optional_putter_factory, nullable_string_putter_factory,
    preinstanced_array_putter_factory, preinstanced_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, int_conditional_validator_factory,
    nullable_flag_validator_factory, nullable_object_array_validator_factory, nullable_string_validator_factory,
    preinstanced_array_validator_factory, preinstanced_validator_factory, url_optional_validator_factory
)
from ...role import Role
from ...user import ClientUserBase

from ..entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType
from ..media_info import MediaInfo
from ..media_item import MediaItem
from ..shared_fields import (
    parse_components, parse_custom_id, parse_emoji, put_components, put_custom_id, put_emoji,
    validate_components_factory, validate_custom_id, validate_emoji
)
from ..string_select_option import StringSelectOption

from .constants import (
    BUTTON_STYLE_DEFAULT, CONTENT_LENGTH_MAX, CONTENT_LENGTH_MIN, DESCRIPTION_LENGTH_MAX, DESCRIPTION_LENGTH_MIN,
    LABEL_LENGTH_MAX, MAX_LENGTH_DEFAULT, MAX_LENGTH_MAX, MAX_LENGTH_MIN, MAX_VALUES_DEFAULT, MAX_VALUES_MAX,
    MAX_VALUES_MIN, MIN_LENGTH_DEFAULT, MIN_LENGTH_MAX, MIN_LENGTH_MIN, MIN_VALUES_DEFAULT, MIN_VALUES_MAX,
    MIN_VALUES_MIN, PLACEHOLDER_LENGTH_MAX, SEPARATOR_SPACING_SIZE_DEFAULT, TEXT_INPUT_STYLE_DEFAULT, URL_LENGTH_MAX,
    VALUE_LENGTH_MAX
)
from .preinstanced import ButtonStyle, SeparatorSpacingSize, TextInputStyle


Component = include('Component')


# button_style

parse_button_style = preinstanced_parser_factory('style', ButtonStyle, BUTTON_STYLE_DEFAULT)
put_button_style = preinstanced_putter_factory('style')
validate_button_style = preinstanced_validator_factory('button_style', ButtonStyle)


# channel_types

parse_channel_types = preinstanced_array_parser_factory('channel_types', ChannelType)
put_channel_types = preinstanced_array_putter_factory('channel_types')
validate_channel_types = preinstanced_array_validator_factory('channel_types', ChannelType)


# color

parse_color = nullable_flag_parser_factory('accent_color', Color)
put_color = nullable_flag_optional_putter_factory('accent_color')
validate_color = nullable_flag_validator_factory('color', Color)


# components

validate_components__row = validate_components_factory(
    'row',
    'message / form',
    (
        'allowed_in_message',
        'allowed_in_form',
    ),
    (
        'nestable_into_row',
    ),
)

validate_components__container = validate_components_factory(
    'container',
    'message',
    (
        'allowed_in_message',
    ),
    (
        'nestable_into_container',
    ),
)

validate_components__section = validate_components_factory(
    'section',
    'message',
    (
        'allowed_in_message',
    ),
    (
        'nestable_into_section',
    ),
)


# content

parse_content = nullable_string_parser_factory('content')
put_content = nullable_string_putter_factory('content')
validate_content = nullable_string_validator_factory('content', CONTENT_LENGTH_MIN, CONTENT_LENGTH_MAX)


# default_values

parse_default_values = nullable_object_array_parser_factory('default_values', EntitySelectDefaultValue)
put_default_values = nullable_entity_array_putter_factory('default_values', EntitySelectDefaultValue)


def _validate_default_value_channel(channel):
    """
    Creates a default option from a channel.
    
    Parameters
    ----------
    channel : ``Channel``
        Channel to create default option from.
    
    Returns
    -------
    default_value : ``EntitySelectDefaultValue``
    """
    return EntitySelectDefaultValue.from_fields(EntitySelectDefaultValueType.channel, channel.id)


def _validate_default_value_role(role):
    """
    Creates a default option from a role.
    
    Parameters
    ----------
    role : ``Role``
        Role to create default option from.
    
    Returns
    -------
    default_value : ``EntitySelectDefaultValue``
    """
    return EntitySelectDefaultValue.from_fields(EntitySelectDefaultValueType.role, role.id)


def _validate_default_value_user(user):
    """
    Creates a default option from a user.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        User to create default option from.
    
    Returns
    -------
    default_value : ``EntitySelectDefaultValue``
    """
    return EntitySelectDefaultValue.from_fields(EntitySelectDefaultValueType.user, user.id)


def _validate_default_value_option(default_value):
    """
    Creates a default option from a default option
    
    Parameters
    ----------
    default_value : ``EntitySelectDefaultValue``
        Just returns it.
    
    Returns
    -------
    default_value : ``EntitySelectDefaultValue``
    """
    return default_value


def _validate_default_value_tuple(default_value_tuple):
    """
    Creates a default option from a tuple.
    
    Parameters
    ----------
    default_value_tuple : `tuple`
        Tuple to create default option from.
    
    Returns
    -------
    default_value : ``EntitySelectDefaultValue``
    
    Raises
    ------
    ValueError
        - If tuple length is not `2`.
    """
    default_value_tuple_length = len(default_value_tuple)
    if default_value_tuple_length != 2:
        raise ValueError(
            f'When a default option is given as a `tuple` its length can be `2`, got {default_value_tuple_length!r}; '
            f'default_value = {default_value_tuple!r}.'
        )
    
    return EntitySelectDefaultValue(*default_value_tuple)


DEFAULT_OPTION_VALIDATORS_BY_TYPE = {
    Channel: _validate_default_value_channel,
    Role: _validate_default_value_role,
    ClientUserBase: _validate_default_value_user,
    EntitySelectDefaultValue: _validate_default_value_option,
    tuple: _validate_default_value_tuple,
}


def _validate_default_value_single(default_value):
    """
    Validates a single option.
    
    Parameters
    ----------
    default_value : `Channel | Role | ClientUserBase | EntitySelectDefaultValue | tuple`
        Default option to validate.
    
    Returns
    -------
    default_value : ``EntitySelectDefaultValue``
    
    Raises
    ------
    TypeError
        If a parameter has invalid type.
    ValueError
        If a parameter has invalid value.
    """
    default_value_type = type(default_value)
    
    try:
        validator = DEFAULT_OPTION_VALIDATORS_BY_TYPE[default_value_type]
    except KeyError:
        for validated_type, validator in DEFAULT_OPTION_VALIDATORS_BY_TYPE.items():
            if issubclass(default_value_type, validated_type):
                break
        
        else:
            raise TypeError(
                f'Default option can be `{Channel.__name__}`, `{Role.__name__}`, `{ClientUserBase.__name__}`,'
                f'`{EntitySelectDefaultValue.__name__}`, `tuple`, '
                f'got {default_value_type.__name__}; {default_value!r}.'
            ) from None
        
        
        DEFAULT_OPTION_VALIDATORS_BY_TYPE[default_value_type] = validator
    
    return validator(default_value)


def validate_default_values(default_values):
    """
    Validates the given default options.
    
    Parameters
    ----------
    default_values : ``None | iterable<Channel> | iterable<Role> | iterable<ClientUserBase> | iterable<EntitySelectDefaultValue> | iterable<(str | EntitySelectDefaultValueTyp, int | str)>>``
        Default options to validate.
    
    Returns
    -------
    default_values : `None | tuple<EntitySelectDefaultValue>`
    
    Raises
    ------
    TypeError
        If a parameter has invalid type.
    ValueError
        If a parameter has invalid value.
    """
    default_values_validated = None
    
    if default_values is None:
        return default_values_validated
    
    if getattr(type(default_values), '__iter__', None) is not None:
        for default_value in default_values:
            try:
                default_value = _validate_default_value_single(default_value)
            except (ValueError, TypeError) as err:
                err.args = (*err.args, f'default_values = {default_values!r}')
                raise
            
            if default_values_validated is None:
                default_values_validated = []
            default_values_validated.append(default_value)
        
        if (default_values_validated is not None):
            default_values_validated = (*default_values_validated,)
        
        return default_values_validated
        
    raise TypeError(
        f'`default_values` can be `None` or `iterable` of any of the following: `{Channel.__name__}`, '
        f'`{Role.__name__}`, `{ClientUserBase.__name__}`, `{EntitySelectDefaultValue.__name__}`; '
        f'got {type(default_values).__name__}; {default_values!r}.'
    )


# description

parse_description = nullable_string_parser_factory('description')
put_description = nullable_string_optional_putter_factory('description')
validate_description = nullable_string_validator_factory(
    'description', DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX
)


# divider

parse_divider = bool_parser_factory('divider', True)
put_divider = bool_optional_putter_factory('divider', True)
validate_divider = bool_validator_factory('divider', True)


# enabled

parse_enabled = negated_bool_parser_factory('disabled', True)
put_enabled = negated_bool_optional_putter_factory('disabled', True)
validate_enabled = bool_validator_factory('enabled', True)


# items

parse_items = nullable_object_array_parser_factory('items', MediaItem)
put_items = nullable_entity_array_putter_factory('items', MediaItem)


def validate_items(items):
    """
    Validates whether the given items are is correct type.
    
    Parameters
    ----------
    items : ``None | iterable<str> | iterable<MediaInfo>``
        The items to validate.
    
    Returns
    -------
    items : ``None | tuple<MediaInfo>``
    
    Raises
    ------
    TypeError
        - If `items`'s type is incorrect.
    """
    if items is None:
        return None
    
    if (getattr(items, '__iter__', None) is None):
        raise TypeError(
            f'`items` can be `None | iterable<str> | iterable<{MediaItem.__name__}>`, got '
            f'{type(items).__name__}; {items!r}.'
        )
    
    items_processed = None
    
    for item in items:
        if isinstance(item, str):
            item = MediaItem(MediaInfo(item))
        
        elif isinstance(item, MediaItem):
            pass
        
        else:
            raise TypeError(
                f'`items` can contain `str | {MediaItem.__name__}` elements, got '
                f'{type(item).__name__}; {item!r}; items = {items!r}.'
            )
        
        if (items_processed is None):
            items_processed = []
        
        items_processed.append(item)
    
    if (items_processed is not None):
        items_processed = tuple(items_processed)
    
    return items_processed


# label

parse_label = nullable_string_parser_factory('label')
put_label = nullable_string_optional_putter_factory('label')
validate_label = nullable_string_validator_factory('label', 0, LABEL_LENGTH_MAX)


# max_length

parse_max_length = int_parser_factory('max_length', MAX_LENGTH_DEFAULT)
put_max_length = int_optional_putter_factory('max_length', MAX_LENGTH_DEFAULT)
validate_max_length = int_conditional_validator_factory(
    'max_length',
    MAX_LENGTH_MIN,
    (lambda user_limit: user_limit >= MAX_LENGTH_MIN and user_limit <= MAX_LENGTH_MAX),
    f'>= {MAX_LENGTH_MIN} and <= {MAX_LENGTH_MAX},'
)


# max_values

parse_max_values = int_parser_factory('max_values', MAX_VALUES_DEFAULT)
put_max_values = int_optional_putter_factory('max_values', MAX_VALUES_DEFAULT)
validate_max_values = int_conditional_validator_factory(
    'max_values',
    MAX_VALUES_MIN,
    (lambda user_limit: user_limit >= MAX_VALUES_MIN and user_limit <= MAX_VALUES_MAX),
    f'>= {MAX_VALUES_MIN} and <= {MAX_VALUES_MAX},'
)


# media

parse_media__attachment_only = default_entity_parser_factory('file', MediaInfo, default_factory = MediaInfo._create_empty)
put_media__attachment_only = entity_putter_factory('file', MediaInfo)

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

# min_length

parse_min_length = int_parser_factory('min_length', MIN_LENGTH_DEFAULT)
put_min_length = int_optional_putter_factory('min_length', MIN_LENGTH_DEFAULT)
validate_min_length = int_conditional_validator_factory(
    'min_length',
    MIN_LENGTH_MIN,
    (lambda user_limit: user_limit >= MIN_LENGTH_MIN and user_limit <= MIN_LENGTH_MAX),
    f'>= {MIN_LENGTH_MIN} and <= {MIN_LENGTH_MAX},'
)

# min_values

parse_min_values = int_parser_factory('min_values', MIN_VALUES_DEFAULT)
put_min_values = int_optional_putter_factory('min_values', MIN_VALUES_DEFAULT)
validate_min_values = int_conditional_validator_factory(
    'min_values',
    MIN_VALUES_MIN,
    (lambda user_limit: user_limit >= MIN_VALUES_MIN and user_limit <= MIN_VALUES_MAX),
    f'>= {MIN_VALUES_MIN} and <= {MIN_VALUES_MAX},'
)

# options

parse_options = nullable_object_array_parser_factory('options', StringSelectOption)
put_options = nullable_entity_array_putter_factory('options', StringSelectOption)
validate_options = nullable_object_array_validator_factory('options', StringSelectOption)

# placeholder

parse_placeholder = nullable_string_parser_factory('placeholder')
put_placeholder = nullable_string_optional_putter_factory('placeholder')
validate_placeholder = nullable_string_validator_factory('placeholder', 0, PLACEHOLDER_LENGTH_MAX)

# required

parse_required = bool_parser_factory('required', True)
put_required = bool_optional_putter_factory('required', True)
validate_required = bool_validator_factory('required', True)

# sku_id

parse_sku_id = entity_id_parser_factory('sku_id')
put_sku_id = entity_id_optional_putter_factory('sku_id')
validate_sku_id = entity_id_validator_factory('sku_id', SKU)


# spacing_size

parse_spacing_size = preinstanced_parser_factory('spacing', SeparatorSpacingSize, SEPARATOR_SPACING_SIZE_DEFAULT)
put_spacing_size = preinstanced_putter_factory('spacing')
validate_spacing_size = preinstanced_validator_factory('spacing_size', SeparatorSpacingSize)


# spoiler

parse_spoiler = bool_parser_factory('spoiler', False)
put_spoiler = bool_optional_putter_factory('spoiler', False)
validate_spoiler = bool_validator_factory('spoiler', False)


# text_input_style

parse_text_input_style = preinstanced_parser_factory('style', TextInputStyle, TEXT_INPUT_STYLE_DEFAULT)
put_text_input_style = preinstanced_putter_factory('style')
validate_text_input_style = preinstanced_validator_factory('text_input_style', TextInputStyle)


# thumbnail

parse_thumbnail = nullable_entity_parser_factory('accessory', NotImplemented, include = 'Component')
put_thumbnail = nullable_entity_optional_putter_factory('accessory', NotImplemented, can_include_internals = True)

def validate_thumbnail(thumbnail):
    """
    Validates whether the given thumbnail is correct type.
    
    Parameters
    ----------
    thumbnail : ``None | Component``
        The thumbnail to validate.
    
    Returns
    -------
    thumbnail : ``Component``
    
    Raises
    ------
    TypeError
        - If `thumbnail` is given as an invalid type.
    """
    if thumbnail is None:
        return None
    
    if isinstance(thumbnail, Component):
        if thumbnail.type.layout_flags.section_thumbnail:
            return thumbnail
        
        raise ValueError(
            f'Component of type: {thumbnail.type.name} cannot be used as a section thumbnail, got {thumbnail!r}.'
        )
    
    raise TypeError(
        f'`thumbnail` can be `{Component.__name__}`, got {type(thumbnail).__name__}, {thumbnail!r}.'
    )


# url

parse_url = nullable_string_parser_factory('url')
put_url = url_optional_putter_factory('url')
validate_url = url_optional_validator_factory('url', length_max = URL_LENGTH_MAX)


# value

parse_value = nullable_string_parser_factory('value')
put_value = nullable_string_optional_putter_factory('value')
validate_value = nullable_string_validator_factory('value', 0, VALUE_LENGTH_MAX)
