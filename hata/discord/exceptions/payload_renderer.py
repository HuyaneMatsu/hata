__all__ = ()

import reprlib
from json import JSONDecodeError

from scarletio import from_json
from scarletio.web_common import Formdata


TYPE_NAME_UNEXPECTED = 'object'
TYPE_NAME_STRING = 'string'
TYPE_NAME_BINARY = 'binary'
TYPE_NAME_BOOLEAN = 'boolean'
TYPE_NAME_INTEGER = 'integer'
TYPE_NAME_FLOAT = 'float'
TYPE_NAME_LIST = 'list'
TYPE_NAME_HASH_MAP = 'object'
TYPE_NAME_FORMDATA = 'formdata'

MODIFIER_LENGTH = 'length'

VALUE_INDENT = '    '
VALUE_NONE = 'null'
VALUE_BOOLEAN_TRUE = 'true'
VALUE_BOOLEAN_FALSE = 'false'

STRING_MIN_LINE_LENGTH = 60
STRING_MAX_LINE_LENGTH = 120
STRING_BREAK_TO_MULTI_LINE_OVER = 60
STRING_MAX_RENDER_LENGTH = 12000


def reconstruct_payload(payload):
    """
    Tries to reconstruct the given payload.
    
    Parameters
    ----------
    payload : `object`
        The payload to try to reconstruct.
    
    Returns
    -------
    reconstructed_value : `str`
    """
    if payload is None: # nothing to do
        return None
    
    into = ['payload = ']
    if isinstance(payload, str):
        reconstruct_json_into(payload, into, 0)
    
    elif isinstance(payload, Formdata):
        reconstruct_formdata_into(payload, into)
    
    elif isinstance(payload, bytes):
        reconstruct_binary_into(payload, into)
    
    else:
        reconstruct_unexpected_into(payload, into)
    
    return ''.join(into)


def reconstruct_json_into(value, into, indent):
    """
    Reconstructs a json payload extending the given `into` list.
    
    Parameters
    ----------
    value : `str`
        Json payload data to reconstruct.
    into : `list` of `str`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    """
    try:
        json_data = from_json(value)
    except JSONDecodeError:
        into.append(TYPE_NAME_STRING)
        into.append('(')
        into.append(MODIFIER_LENGTH)
        into.append('=')
        into.append(str(len(value)))
        into.append('): ')
        into.append(reprlib.repr(value))
    else:
        reconstruct_value_into(json_data, into, indent, False)


def reconstruct_value_into(value, into, indent, is_file):
    """
    Reconstructs a value extending the given `into` list.
    
    Parameters
    ----------
    value : `None`, `str`, `list`, `dict`, `int`, `float`, `bool`
        The deserialized json value.
    into : `list` of `str`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    is_file : `bool`
        Whether the value is a file and should not shown.
    """
    if value is None:
        reconstruct_null_into(into)
        return
    
    if isinstance(value, bool):
        reconstruct_boolean_into(value, into)
        return

    if isinstance(value, str):
        reconstruct_string_into(value, into, indent, is_file)
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
        reconstruct_hash_map_into(value, into, indent)
        return
    
    # Used at form data
    if isinstance(value, bytes):
        reconstruct_binary_into(value, into)
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
    if value:
        value_representation = VALUE_BOOLEAN_TRUE
    else:
        value_representation = VALUE_BOOLEAN_FALSE
    
    into.append(value_representation)


def reconstruct_string_into(value, into, indent, is_file):
    """
    Reconstructs a string value to the given `into` list.
    
    Parameters
    ----------
    value : `str`
        The string value.
    into : `list` of `str`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    is_file : `bool`
        Whether the value is a file and should not be shown.
    """
    length = len(value)
    
    if is_file or (length > STRING_MAX_RENDER_LENGTH):
        into.append(TYPE_NAME_STRING)
        into.append('(')
        into.append(MODIFIER_LENGTH)
        into.append('=')
        into.append(str(length))
        into.append(')')
    
    else:
        if length > STRING_BREAK_TO_MULTI_LINE_OVER:
            into.append('(\n')
            
            string_indent = indent + 1
            
            chunk_size = STRING_MAX_LINE_LENGTH - string_indent * len(VALUE_INDENT)
            if chunk_size < STRING_MIN_LINE_LENGTH:
                chunk_size = STRING_MIN_LINE_LENGTH
            
            start_index = 0
            while True:
                end_index = start_index + chunk_size
                if end_index >= length:
                    end_index = length
                    should_break = True
                else:
                    should_break = False
                
                for counter in range(string_indent):
                    into.append(VALUE_INDENT)
                
                into.append(repr(value[start_index:end_index]))
                into.append('\n')
                
                if should_break:
                    break
                
                start_index = end_index
                continue
            
            for counter in range(indent):
                into.append(VALUE_INDENT)
            
            into.append(')')
        
        else:
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
    
    into.append('[')
    
    if length:
        into.append('\n')
        
        element_indent = indent + 1
        
        for index, list_element in enumerate(value):
            for counter in range(element_indent):
                into.append(VALUE_INDENT)
            into.append(str(index))
            into.append(': ')
            
            reconstruct_value_into(list_element, into, element_indent, False)
            
            into.append(',\n')
        
        for counter in range(indent):
            into.append(VALUE_INDENT)
    
    into.append(']')


def reconstruct_hash_map_into(value, into, indent):
    """
    Reconstructs a hash map value extending the given `into` list.
    
    Parameters
    ----------
    value : `dict`
        The hash map value.
    into : `list` of `str`
        A list to extend it's content.
    indent : `int`
        The amount of indents to add.
    """
    length = len(value)
    
    into.append('{')
    
    if length:
        into.append('\n')
        item_indent = indent + 1
        
        for item_key, item_value in sorted(value.items(), key = hash_map_key_sort_key):
            for counter in range(item_indent):
                into.append(VALUE_INDENT)
            
            into.append(repr(item_key))
            into.append(': ')
            
            reconstruct_value_into(item_value, into, item_indent, False)
            
            into.append(',\n')
        
        for counter in range(indent):
            into.append(VALUE_INDENT)
    
    into.append('}')


def reconstruct_unexpected_into(value, into):
    """
    Reconstructs a value with an unexpected type to the given `into` list.
    
    Parameters
    ----------
    value : `object`
        Le value.
    into : `list` of `str`
        A list to extend it's content.
    """
    into.append(TYPE_NAME_UNEXPECTED)
    into.append(': ')
    into.append(reprlib.repr(value))


def reconstruct_binary_into(value, into):
    """
    Reconstructs a binary value to the given `into` list.
    
    Parameters
    ----------
    value : `binary`
        The binary value.
    into : `list` of `str`
        A list to extend it's content.
    """
    into.append(TYPE_NAME_BINARY)
    into.append('(')
    into.append(MODIFIER_LENGTH)
    into.append('=')
    into.append(str(len(value)))
    into.append(')')


def reconstruct_formdata_into(value, into):
    """
    Tries to reconstruct formdata into the given `into` list.
    
    Parameters
    ----------
    value : ``Formdata``
        The formdata to reconstruct.
    into : `list` of `str`
        A list to extend it's content.
    
    Returns
    -------
    reconstructed_value : `str`
    """
    into.append(TYPE_NAME_FORMDATA)
    
    fields = value.fields
    
    into.append('({\n')
    
    for index, (field_type_options, field_headers, field_value) in enumerate(fields):
        field_name = field_type_options['name']
        filename = field_type_options.get('filename', None)
        
        into.append(VALUE_INDENT)
        into.append(str(index))
        into.append(': ')
        into.append(repr(field_name))
        if (filename is not None) and (filename != field_name):
            into.append(' | ')
            into.append(repr(filename))
        
        into.append(': ')
        if (filename is None) and (field_name == 'payload_json'):
            reconstruct_json_into(field_value, into, 1)
        else:
            reconstruct_value_into(field_value, into, 1, True)
        into.append('\n')
    
    into.append('})')


def hash_map_key_sort_key(item):
    """
    Used to sort hash maps based on their key.
    
    Parameters
    ----------
    item : `tuple` (`str`, `object`)
        An item of a hash map.
    
    Returns
    -------
    key : `str`
    """
    return item[0]
