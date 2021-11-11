__all__ = ()

import reprlib
from json import JSONDecodeError

from ...backend.utils import from_json
from ...backend.formdata import Formdata

TYPE_NAME_UNEXPECTED = 'object'
TYPE_NAME_STRING = 'string'
TYPE_NAME_BINARY = 'binary'
TYPE_NAME_BOOLEAN = 'boolean'
TYPE_NAME_INTEGER = 'integer'
TYPE_NAME_FLOAT = 'float'
TYPE_NAME_LIST = 'list'
TYPE_NAME_HASH_MAP = 'dictionary'

MODIFIER_NAME_LENGTH = 'length'

VALUE_INDENT = '    '
VALUE_NONE = 'null'
VALUE_BOOLEAN_TRUE = 'true'
VALUE_BOOLEAN_FALSE = 'false'

def reconstruct_payload(payload):
    """
    Tries to reconstruct teh given payload.
    
    Parameters
    ----------
    payload : `Any`
        The payload to try to reconstruct.
    
    Returns
    -------
    reconstructed_value : `str`
    """
    if payload is None: # nothing to do
        return None
    
    if isinstance(payload, str):
        return reconstruct_json(payload)
    
    if isinstance(payload, Formdata):
        return reconstruct_formdata(payload)
    
    if isinstance(payload, bytes):
        return reconstruct_bytes(payload)
    
    return reconstruct_unexpected_value(payload)


def reconstruct_json(payload):
    """
    Tries to reconstruct json data.
    
    payload_json : `str`
        Payload data to reconstruct
    
    Returns
    -------
    reconstructed_value : `str`
    """
    try:
        json_data = from_json(payload)
    except JSONDecodeError:
        return f'{TYPE_NAME_STRING}({MODIFIER_NAME_LENGTH}={len(payload)}): {reprlib.repr(payload)}'
    
    reconstruct_into = []
    reconstruct_json_value_into(json_data, reconstruct_into, 0)
    return ''.join(reconstruct_into)


def reconstruct_json_value_into(value, into, indent):
    """
    Reconstructs a json value extending the given `into` list.
    
    Parameters
    ----------
    value : `str`, `None`, `list`, `dict`, `int`, `float`, `bool`
        The deserialized json value.
    into : `list` of `str`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    """
    for counter in indent:
        into.append(VALUE_INDENT)
    
    if value is None:
        reconstruct_null_into(into)
        return
    
    if isinstance(value, bool):
        reconstruct_boolean_into(value, into)
        return

    if isinstance(value, str):
        reconstruct_string_into(value, into)
        return
    
    if isinstance(value, int):
        reconstruct_integer_into(value, into)
        return
    
    if isinstance(value, float):
        reconstruct_float_into(value, into)
        return
    
    if isinstance(value, list):
        reconstruct_list_into(value, into, indent)
        return
    
    if isinstance(value, dict):
        reconstruct_dictionary_into(value, into, indent)
        return

    reconstruct_unexpected_into(value, into)


def reconstruct_null_into(into):
    """
    Reconstructs a null value to the given `into` list.
    
    Parameters
    ----------
    into : `list` of `str`
        A list to extend it's content.
    """
    into.append(VALUE_NONE)


def reconstruct_boolean_into(value, into):
    """
    Reconstructs a boolean value to the given `into` list.
    
    Parameters
    ----------
    value : `bool`
        The boolean value.
    into : `list` of `str`
        A list to extend it's content.
    """
    into.append(TYPE_NAME_BOOLEAN)
    into.append(': ')
    
    if value:
        value_representation = VALUE_BOOLEAN_TRUE
    else:
        value_representation = VALUE_BOOLEAN_FALSE
    
    into.append(value_representation)


def reconstruct_string_into(value, into):
    """
    Reconstructs a string value to the given `into` list.
    
    Parameters
    ----------
    value : `str`
        The string value.
    into : `list` of `str`
        A list to extend it's content.
    """
    into.append(TYPE_NAME_STRING)
    into.append('(')
    into.append('length=')
    into.append(str(len(value)))
    into.append(')')
    into.append(': ')
    into.append(repr(value))


def reconstruct_integer_into(value, into):
    """
    Reconstructs an integer value to the given `into` list.
    
    Parameters
    ----------
    value : `int`
        The integer value.
    into : `list` of `str`
        A list to extend it's content.
    """
    into.append(TYPE_NAME_INTEGER)
    into.append(': ')
    into.append(repr(value))


def reconstruct_float_into(value, into):
    """
    Reconstructs a float value to the given `into` list.
    
    Parameters
    ----------
    value : `float`
        The float value.
    into : `list` of `str`
        A list to extend it's content.
    """
    into.append(TYPE_NAME_FLOAT)
    into.append(': ')
    into.append(repr(value))


def reconstruct_list_into(value, into, indent):
    """
    Reconstructs a list value extending the given `into` list.
    
    Parameters
    ----------
    value : `list`
        The list value.
    into : `list` of `str`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    """
    length = len(value)
    
    into.append(TYPE_NAME_LIST)
    into.append('(')
    into.append(MODIFIER_NAME_LENGTH)
    into.append('=')
    into.append(str(length))
    into.append('): [')
    
    if length:
        for list_element in value:
            for counter in indent:
                into.append(VALUE_INDENT)
            
            reconstruct_json_value_into(list_element, into, indent+1)
            
            into.append(',\n')
    
    into.append(']')


def reconstruct_dictionary_into(value, into, indent):
    """
    Reconstructs a dictionary value extending the given `into` list.
    
    Parameters
    ----------
    value : `dict`
        The dictionary value.
    into : `list` of `str`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    """
    length = len(value)
    
    into.append(TYPE_NAME_HASH_MAP)
    into.append('(')
    into.append(MODIFIER_NAME_LENGTH)
    into.append('=')
    into.append(str(length))
    into.append('): {')
    
    if length:
        for item_key, item_value in value.items():
            for counter in indent:
                into.append(VALUE_INDENT)
            
            into.append(repr(item_key))
            into.append(': ')
            
            reconstruct_json_value_into(item_value, into, indent+1)
            
            into.append(',\n')
    
    into.append('}')


def reconstruct_unexpected_into(value, into):
    """
    Reconstructs a value with an unexpected type to the given `into` list.
    
    Parameters
    ----------
    value : `Any`
        Le value.
    into : `list` of `str`
        A list to extend it's content.
    """
    into.append(TYPE_NAME_UNEXPECTED)
    into.append(': ')
    into.append(reprlib.repr(value))



def reconstruct_unexpected_value(value):
    """
    Reconstructs a value with an unexpected type.
    
    Parameters
    ----------
    value : `Any`
        Le value.
    
    Returns
    -------
    reconstructed_value : `str`
    """
    reconstruct_into = []
    reconstruct_unexpected_into(value, reconstruct_into)
    return ''.join(reconstruct_into)
