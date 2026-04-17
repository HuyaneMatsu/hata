__all__ = ()

from ...application_command import ApplicationCommand, ApplicationCommandTargetType
from ...application_command.application_command.constants import (
    NAME_LENGTH_MAX as APPLICATION_COMMAND_NAME_LENGTH_MAX, NAME_LENGTH_MIN as APPLICATION_COMMAND_NAME_LENGTH_MIN
)
from ...bases import DiscordEntity
from ...component import InteractionComponent
from ...component.shared_fields import validate_custom_id
from ...field_validators import (
    entity_id_validator_factory, force_string_validator_factory, nullable_entity_validator_factory,
    nullable_object_array_validator_factory, preinstanced_validator_factory
)

from ..interaction_option import InteractionOption


# component

def parse_component(data):
    """
    Parses an inline component from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    component : ``None | InteractionComponent``
    """
    nested_data = data.get('data', None)
    if (nested_data is not None) and nested_data:
        return InteractionComponent.from_data(nested_data)


def put_component(component, data, defaults):
    """
    Serializes the given inline component.
    
    Parameters
    ----------
    component : ``None | InteractionComponent``
        Interaction component.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if (component is not None):
        nested_data = data.get('data', None)
        
        component_data = component.to_data(defaults = defaults)
        
        if nested_data is None:
            data['data'] = component_data
        else:
            nested_data.update(component_data)
    
    return data


validate_component = nullable_entity_validator_factory('component', InteractionComponent)


# components

def parse_components(data):
    """
    Parses the components out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    components : ``None | tuple<InteractionComponent>``
    """
    nested_data = data.get('data', None)
    if (nested_data is not None):
        object_data_array = nested_data.get('components', None)
        if (object_data_array is not None) and object_data_array:
            return (*(InteractionComponent.from_data(object_data) for object_data in object_data_array),)


def put_components(components, data, defaults):
    """
    Serializes the given inline components.
    
    Parameters
    ----------
    components : ``None | tuple<InteractionComponent>``
        Interaction components.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (components is not None):
        nested_data = data.get('data', None)
        if nested_data is None:
            data['data'] = nested_data = {}
        
        if components is None:
            entity_data_array = []
        else:
            entity_data_array = [entity.to_data(defaults = defaults) for entity in components]
        
        nested_data['components'] = entity_data_array
    
    return data


validate_components = nullable_object_array_validator_factory('components', InteractionComponent)


# custom_id


def parse_custom_id(data):
    """
    Parses out the custom identifier from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    custom_id : `int`
    """
    nested_data = data.get('data', None)
    if (nested_data is not None):
        custom_id = nested_data.get('custom_id', None)
        if (custom_id is not None):
            return custom_id
    
    return ''


def put_custom_id(custom_id, data, defaults):
    """
    Serializes the given custom identifier.
    
    Parameters
    ----------
    custom_id : `int`
        Custom identifier.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if custom_id or (custom_id is not None):
        nested_data = data.get('data', None)
        if (nested_data is None):
            data['data'] = nested_data = {}
        
        nested_data['custom_id'] = custom_id

    return data


# id

def parse_application_command_id(data):
    """
    Parses out the application command identifier from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    application_command_id : `int`
    """
    nested_data = data.get('data', None)
    if (nested_data is not None):
        entity_id = nested_data.get('id', None)
        if (entity_id is not None):
            return int(entity_id)
    
    return 0


def put_application_command_id(application_command_id, data, defaults):
    """
    Serializes the given application command id.

    Parameters
    ----------
    application_command_id : `int`
        Application command identifier.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    nested_data = data.get('data', None)
    if (nested_data is None):
        data['data'] = nested_data = {}
    
    if application_command_id:
        raw_application_command_id = str(application_command_id)
    else:
        raw_application_command_id = None
    
    nested_data['id'] = raw_application_command_id

    return data


validate_application_command_id = entity_id_validator_factory('id', ApplicationCommand)

# name

def parse_application_command_name(data):
    """
    Parses out the application command name from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    application_command_name : `int`
    """
    nested_data = data.get('data', None)
    if (nested_data is not None):
        application_command_name = nested_data.get('name', None)
        if (application_command_name is not None):
            return application_command_name
    
    return ''


def put_application_command_name(application_command_name, data, defaults):
    """
    Serializes the given application command name.
    
    Parameters
    ----------
    application_command_name : `int`
        Application command name.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    nested_data = data.get('data', None)
    if (nested_data is None):
        data['data'] = nested_data = {}
    
    nested_data['name'] = application_command_name

    return data


validate_application_command_name = force_string_validator_factory(
    'name', APPLICATION_COMMAND_NAME_LENGTH_MIN, APPLICATION_COMMAND_NAME_LENGTH_MAX
)


# options


def parse_options(data):
    """
    Parses the options out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    options : ``None | tuple<InteractionOption>``
    """
    nested_data = data.get('data', None)
    if (nested_data is not None):
        object_data_array = nested_data.get('options', None)
        if (object_data_array is not None) and object_data_array:
            return (*(InteractionOption.from_data(object_data) for object_data in object_data_array),)


def put_options(options, data, defaults):
    """
    Serializes the given inline options.
    
    Parameters
    ----------
    options : ``None | tuple<InteractionOption>``
        Interaction options.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if defaults or (options is not None):
        nested_data = data.get('data', None)
        if nested_data is None:
            data['data'] = nested_data = {}
        
        if options is None:
            entity_data_array = []
        else:
            entity_data_array = [entity.to_data(defaults = defaults) for entity in options]
        
        nested_data['options'] = entity_data_array
    
    return data


validate_options = nullable_object_array_validator_factory('options', InteractionOption)


# target_id

def parse_target_id(data):
    """
    Parses out the target identifier from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    target_id : `int`
    """
    nested_data = data.get('data', None)
    if (nested_data is not None):
        entity_id = nested_data.get('target_id', None)
        if (entity_id is not None):
            return int(entity_id)
    
    return 0


def put_target_id(target_id, data, defaults):
    """
    Serializes the given target id.
    
    Parameters
    ----------
    target_id : `int`
        Application command identifier.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if target_id or defaults:
        nested_data = data.get('data', None)
        if (nested_data is None):
            data['data'] = nested_data = {}
        
        if target_id:
            raw_target_id = str(target_id)
        else:
            raw_target_id = None
        
        nested_data['target_id'] = raw_target_id

    return data


validate_target_id = entity_id_validator_factory('target_id', DiscordEntity)


# target_type

def parse_target_type(data):
    """
    Parses out the target type from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    target_type : ``ApplicationCommandTargetType``
    """
    nested_data = data.get('data', None)
    if (nested_data is not None):
        target_type_value = nested_data.get('type', None)
        if (target_type_value is not None):
            return ApplicationCommandTargetType(target_type_value)
    
    return ApplicationCommandTargetType.none


def put_target_type(target_type, data, defaults):
    """
    Serializes the given target type.
    
    Parameters
    ----------
    target_type : ``ApplicationCommandTargetType``
        Application command target type.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    nested_data = data.get('data', None)
    if (nested_data is None):
        data['data'] = nested_data = {}
    
    nested_data['type'] = target_type.value

    return data

validate_target_type = preinstanced_validator_factory('target_type', ApplicationCommandTargetType)
