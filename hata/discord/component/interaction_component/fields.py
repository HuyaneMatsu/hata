__all__ = ()

from ...component import ComponentType
from ...field_putters import preinstanced_putter_factory
from ...field_validators import preinstanced_validator_factory


# type

def parse_type(data):
    """
    Parses component type out from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    component_type : ``ComponentType``
    """
    for key in ('type', 'component_type'):
        component_type_raw = data.get(key, None)
        if (component_type_raw is not None):
            return ComponentType(component_type_raw)
    
    return ComponentType.none


put_type = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', ComponentType)
