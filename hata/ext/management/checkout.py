__all__ = ()

ELEMENT_TYPE_IDENTIFIER_NONE = 0
ELEMENT_TYPE_IDENTIFIER_STRING = 1
ELEMENT_TYPE_IDENTIFIER_INTEGER = 2
ELEMENT_TYPE_IDENTIFIER_FLOAT = 3

ELEMENT_TYPE_IDENTIFIER_TO_NAME = {
    ELEMENT_TYPE_IDENTIFIER_NONE: 'none',
    ELEMENT_TYPE_IDENTIFIER_STRING: 'string',
    ELEMENT_TYPE_IDENTIFIER_INTEGER: 'integer',
    ELEMENT_TYPE_IDENTIFIER_FLOAT: 'float',
}

def element_validator_none(container_name, element, empty_elements_allowed):
    """
    Dummy validator not allowing anything to pass.
    
    Parameters
    ----------
    container_name : `str`
        The respective container's name.
    element : `Any`
        An element of the container.
    empty_elements_allowed : `bool`
        Whether empty elements are allowed.
    
    Raises
    ------
    RuntimeError
        The container has any elements.
    """
    raise RuntimeError(f'{container_name} excepts no elements.')


def element_validator_string(container_name, element, empty_elements_allowed):
    """
    String element validator.
    
    Parameters
    ----------
    container_name : `str`
        The respective container's name.
    element : `Any`
        An element of the container.
    empty_elements_allowed : `bool`
        Whether empty elements are allowed.
    
    Raises
    ------
    RuntimeError
        - `element` is not `str` instance.
        - `empty_elements_allowed` is `False`, but `element` is an empty string.
    """
    if not isinstance(element, str):
        raise RuntimeError(f'{container_name} excepts only string elements, got: {element!r}.')
    
    if (not empty_elements_allowed) and (not element):
        raise RuntimeError(f'{container_name} contains empty string meanwhile it should not.')


def element_validator_integer(container_name, element, empty_elements_allowed):
    """
    Integer element validator.
    
    Parameters
    ----------
    container_name : `str`
        The respective container's name.
    element : `Any`
        An element of the container.
    empty_elements_allowed : `bool`
        Whether empty elements are allowed.
    
    Raises
    ------
    RuntimeError
        `element` is not `int` instance.
    """
    if not isinstance(element, int):
        raise RuntimeError(f'{container_name} excepts only integer elements, got: {element!r}.')
    
def element_validator_float(container_name, element, empty_elements_allowed):
    """
    Float element validator.
    
    Parameters
    ----------
    container_name : `str`
        The respective container's name.
    element : `Any`
        An element of the container.
    empty_elements_allowed : `bool`
        Whether empty elements are allowed.
    
    Raises
    ------
    RuntimeError
        `element` is not `float` instance.
    """
    if not isinstance(element, float):
        raise RuntimeError(f'{container_name} excepts only float elements, got: {element!r}.')


ELEMENT_TYPE_IDENTIFIER_TO_VALIDATOR = {
    ELEMENT_TYPE_IDENTIFIER_NONE: element_validator_none,
    ELEMENT_TYPE_IDENTIFIER_STRING: element_validator_string,
    ELEMENT_TYPE_IDENTIFIER_INTEGER: element_validator_integer,
    ELEMENT_TYPE_IDENTIFIER_FLOAT: element_validator_float,
}

def checkout_list_structure(root, name, nullable, element_type_identifier, empty_elements_allowed):
    """
    Checks a list's structure.
    
    Parameters
    ----------
    root : `Any`
        The expected list instance.
    name : `str`
        The list's name.
    nullable : `bool`
        Whether the list can be `None`.
    element_type_identifier : `int`
        Identifier for element type.
    
    Returns
    -------
    root : `None` or `list`
    
    Raises
    ------
    TypeError
        - `root` is not `list` instance, or neither `None` if nullable.
        - `root` element type incorrect.
    """
    if nullable:
        if (root is not None) and (not isinstance(root, list)):
           raise RuntimeError(f'{name} can be list instance (nullable), got {root.__class__.__name__}.')
    else:
        if (not isinstance(root, list)):
           raise RuntimeError(f'{name} can be list instance, got {root.__class__.__name__}.')
    
    try:
        element_validator = ELEMENT_TYPE_IDENTIFIER_TO_VALIDATOR[element_type_identifier]
    except KeyError:
        raise RuntimeError(f'Unknown element validator identifier: {element_type_identifier!r}.') from None
    
    if (root is not None):
        if root:
            for element in root:
                element_validator(name, element, empty_elements_allowed)
        
        else:
            if nullable and (not root):
                root = None
    
    return root
