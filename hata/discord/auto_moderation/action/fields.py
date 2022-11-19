__all__ = ()

from ...field_parsers import preinstanced_parser_factory
from ...field_putters import preinstanced_putter_factory
from ...field_validators import preinstanced_validator_factory

from ..action_metadata import AutoModerationActionMetadataBase

from .preinstanced import AutoModerationActionType

# type

parse_type = preinstanced_parser_factory('type', AutoModerationActionType, AutoModerationActionType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', AutoModerationActionType)

# metadata

def parse_metadata(data, action_type):
    """
    Parsers out an auto moderation action's metadata form the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Auto moderation action data.
    
    action_type : ``AutoModerationActionType``
        The action's type.
    
    Returns
    -------
    metadata : ``AutoModerationActionMetadataBase``
    """
    metadata_type = action_type.metadata_type
    metadata_data = data.get('metadata', None)
    
    if metadata_data is None:
        metadata = metadata_type()
    else:
        metadata = metadata_type.from_data(metadata_data)
    
    return metadata


def put_metadata_into(metadata, data, defaults):
    """
    Puts the given action metadata's data into the given `data` json serializable object.
    
    Parameters
    ----------
    metadata : ``AutoModerationActionMetadataBase``
        Action metadata.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (type(metadata) is not AutoModerationActionMetadataBase):
        data['metadata'] = metadata.to_data(defaults = defaults)
    
    return data
