__all__ = ()

from ...field_putters import bool_optional_putter_factory, float_putter_factory, nullable_string_optional_putter_factory
from ...field_validators import bool_validator_factory, entity_id_validator_factory

from ..attachment.fields import (
    put_title, put_waveform, validate_description, validate_duration, validate_name, validate_title, validate_waveform
)


# attachment_id

def put_attachment_id(attachment_id, data, defaults):
    """
    Puts the attachment identifier into the given data.
    
    Parameters
    ----------
    attachment_id : `int`
        Attachment identifier to serialise.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data['id'] = str(attachment_id)
    return data

validate_attachment_id = entity_id_validator_factory('attachment_id')


# description

put_description = nullable_string_optional_putter_factory('description')


# duration

put_duration = float_putter_factory('duration_secs')


# spoiler

put_spoiler = bool_optional_putter_factory('is_spoiler', False)
validate_spoiler = bool_validator_factory('spoiler', False)
