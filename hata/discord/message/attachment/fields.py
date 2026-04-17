__all__ = ()

from base64 import b64decode as base_64_decode, b64encode as base_64_encode

from ...application import Application
from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, flag_parser_factory, float_parser_factory,
    force_string_parser_factory, int_parser_factory, nullable_date_time_parser_factory,
    nullable_entity_array_parser_factory, nullable_functional_parser_factory, nullable_string_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_putter_factory, flag_optional_putter_factory, float_optional_putter_factory,
    force_string_putter_factory, int_putter_factory, nullable_date_time_optional_putter_factory,
    nullable_entity_array_optional_putter_factory, nullable_string_optional_putter_factory,
    nullable_string_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, flag_validator_factory, float_conditional_validator_factory,
    force_string_validator_factory, int_conditional_validator_factory, nullable_bytes_validator_factory,
    nullable_date_time_validator_factory, nullable_entity_array_validator_factory, nullable_entity_validator_factory,
    nullable_string_validator_factory, url_optional_validator_factory, url_required_validator_factory
)
from ...user import User

from .constants import DESCRIPTION_LENGTH_MAX, DURATION_DEFAULT
from .flags import AttachmentFlag


# application

parse_application = nullable_functional_parser_factory('application', Application.from_data_invite)


def put_application(application, data, defaults):
    """
    Serializes the attachment's application into the given data.
    
    Parameters
    ----------
    application : ``None | Application``
        The application to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (application is not None):
        if application is None:
            application_data = None
        else:
            application_data = application.to_data_invite(defaults = defaults, include_internals = True)
        
        data['application'] = application_data
    
    return data


validate_application = nullable_entity_validator_factory('application', Application)


# clip_created_at

parse_clip_created_at = nullable_date_time_parser_factory('clip_created_at')
put_clip_created_at = nullable_date_time_optional_putter_factory('clip_created_at')
validate_clip_created_at = nullable_date_time_validator_factory('clip_created_at')


# clip_users

parse_clip_users = nullable_entity_array_parser_factory('clip_participants', User)
put_clip_users = nullable_entity_array_optional_putter_factory(
    'clip_participants', User,force_include_internals = True
)
validate_clip_users = nullable_entity_array_validator_factory('clip_users', User)


# content_type

parse_content_type = nullable_string_parser_factory('content_type')
put_content_type = nullable_string_putter_factory('content_type')
validate_content_type = nullable_string_validator_factory('content_type', 0, 1024)

# description

parse_description = nullable_string_parser_factory('description')
put_description = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# duration

parse_duration = float_parser_factory('duration_secs', DURATION_DEFAULT)
put_duration = float_optional_putter_factory('duration_secs', DURATION_DEFAULT)
validate_duration = float_conditional_validator_factory(
    'duration',
    DURATION_DEFAULT,
    lambda duration : duration >= 0.0,
    '>= 0.0',
)

# flags

parse_flags = flag_parser_factory('flags', AttachmentFlag)
put_flags = flag_optional_putter_factory('flags', AttachmentFlag())
validate_flags = flag_validator_factory('flags', AttachmentFlag)

# height

parse_height = int_parser_factory('height', 0)
put_height = int_putter_factory('height')
validate_height = int_conditional_validator_factory(
    'height',
    0,
    lambda height : height >= 0,
    '>= 0',
)

# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('id')

# name

parse_name = force_string_parser_factory('filename')
put_name = force_string_putter_factory('filename')
validate_name = force_string_validator_factory('name', 0, 1024)

# proxy_url

parse_proxy_url = nullable_string_parser_factory('proxy_url')
put_proxy_url = url_optional_putter_factory('proxy_url')
validate_proxy_url = url_optional_validator_factory('proxy_url')

# size

parse_size = int_parser_factory('size', 0)
put_size = int_putter_factory('size')
validate_size = int_conditional_validator_factory(
    'size',
    0,
    lambda size : size >= 0,
    '>= 0',
)

# temporary

parse_temporary = bool_parser_factory('ephemeral', False)
put_temporary = bool_optional_putter_factory('ephemeral', False)
validate_temporary = bool_validator_factory('temporary', False)

# title

parse_title = nullable_string_parser_factory('title')
put_title = nullable_string_optional_putter_factory('title')
validate_title = nullable_string_validator_factory('title', 0, 1024)

# url

parse_url = force_string_parser_factory('url')
put_url = url_optional_putter_factory('url')
validate_url = url_required_validator_factory('url')


# waveform

def parse_waveform(data):
    """
    Parses the waveform out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    waveform : `None | bytes`
    """
    waveform = data.get('waveform')
    if (waveform is not None) and waveform:
        try:
            return base_64_decode(waveform)
        except ValueError:
            pass


def put_waveform(waveform, data, defaults):
    """
    Serializes the waveform into the given data.
    
    Parameters
    ----------
    waveform : `None | bytes`
        The waveform to serialize.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (waveform is not None) or defaults:
        if waveform is not None:
            waveform = base_64_encode(waveform).decode('ascii')
        
        data['waveform'] = waveform
    
    return data


validate_waveform = nullable_bytes_validator_factory('waveform', 0, 4096)


# width

parse_width = int_parser_factory('width', 0)
put_width = int_putter_factory('width')
validate_width = int_conditional_validator_factory(
    'width',
    0,
    lambda width : width >= 0,
    '>= 0',
)
